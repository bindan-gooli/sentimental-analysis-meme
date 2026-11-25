import io
import os
import secrets
import sqlite3
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Security, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from PIL import Image
import torch
from torchvision import transforms
from transformers import AutoTokenizer
from model import IndicSentM

# --- Security Mitigations ---
# 1. Prevent Image Decompression Bomb attacks (CVE-mitigated DoS)
Image.MAX_IMAGE_PIXELS = 10_000_000
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB maximum image size

# 2. Authentication & Authorization Config
API_KEY_HEADER_NAME = "X-API-Key"
DEFAULT_KEY = "indicsent-secret-key-change-me"
SERVER_API_KEY = os.getenv("API_KEY", DEFAULT_KEY)

api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)
app = FastAPI(
    title="IndicSent-M Multimodal Sentiment Service",
    description="Secure inference API for Indian-language meme and post sentiment classification.",
    version="1.0.0"
)

# Enable CORS for local front-end development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Device and Model Initialization
device = torch.device("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"))
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
model = IndicSentM().to(device)

MODEL_CHECKPOINT = "indicsent_model.pt"
if os.path.exists(MODEL_CHECKPOINT):
    # Safe weight loading strictly avoiding arbitrary code execution (unpickling exploit)
    model.load_state_dict(torch.load(MODEL_CHECKPOINT, map_location=device, weights_only=True))
model.eval()

img_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

CLASS_LABELS = {0: "negative", 1: "neutral", 2: "positive"}

def verify_authorization(api_key: str = Security(api_key_header)):
    """
    Constant-time comparison to prevent timing attacks during key verification.
    """
    if not api_key or not secrets.compare_digest(api_key, SERVER_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Missing or invalid API Key"
        )

@app.get("/health")
def health_check():
    return {"status": "healthy", "model": "IndicSent-M", "device": str(device)}

DB_PATH = os.path.join(os.path.dirname(__file__), "memes.db")

@app.get("/api/memes")
def get_memes(
    query: str = "",
    language: str = "All",
    page: int = 1,
    limit: int = 24
):
    try:
        page = max(1, int(page))
        limit = max(1, min(100, int(limit)))
    except (ValueError, TypeError):
        page = 1
        limit = 24
    offset = (page - 1) * limit
    if not os.path.exists(DB_PATH):
        return {"total": 0, "page": page, "limit": limit, "total_pages": 0, "memes": []}

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    conditions = []
    params = []

    if language and language != "All":
        conditions.append("language = ?")
        params.append(language)

    if query and query.strip():
        q_term = f"%{query.strip().lower()}%"
        conditions.append("(LOWER(title) LIKE ? OR LOWER(caption) LIKE ? OR LOWER(keywords) LIKE ? OR LOWER(tag) LIKE ?)")
        params.extend([q_term, q_term, q_term, q_term])

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    # Total matching records
    cursor.execute(f"SELECT COUNT(*) FROM memes {where_clause}", params)
    total = cursor.fetchone()[0]

    # Fetch page
    sql = f"""
    SELECT meme_id as id, title, language, tag, caption, image_url as imageUrl,
           fallback_bg_start, fallback_bg_end, emoji, sentiment
    FROM memes {where_clause}
    ORDER BY id ASC
    LIMIT ? OFFSET ?
    """
    cursor.execute(sql, params + [limit, offset])
    rows = cursor.fetchall()

    memes = []
    for r in rows:
        memes.append({
            "id": r["id"],
            "title": r["title"],
            "language": r["language"],
            "tag": r["tag"],
            "caption": r["caption"],
            "imageUrl": r["imageUrl"],
            "fallbackBg": [r["fallback_bg_start"], r["fallback_bg_end"]],
            "emoji": r["emoji"],
            "sentiment": r["sentiment"]
        })
    conn.close()

    total_pages = (total + limit - 1) // limit if total > 0 else 1

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "memes": memes
    }

@app.post("/predict")
async def predict_sentiment(
    text: str = Form(..., description="Indian-language caption or extracted meme text"),
    image: UploadFile = File(..., description="Meme image file (JPEG/PNG, max 5MB)")
):
    # 1. Text input sanitization and boundary check
    clean_text = text.strip()
    if not clean_text or len(clean_text) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text field must be between 1 and 1000 characters."
        )

    # 2. Upload size enforcement
    file_bytes = await image.read()
    if len(file_bytes) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Uploaded file exceeds limit of {MAX_UPLOAD_SIZE // (1024*1024)} MB."
        )

    # 3. Safe image parsing (in-memory buffer, validated format)
    try:
        pil_img = Image.open(io.BytesIO(file_bytes))
        pil_img.verify()  # Validate image headers
        pil_img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image payload. File must be a valid image."
        )

    # 4. Feature preprocessing
    tokens = tokenizer(
        clean_text,
        max_length=128,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )
    pixel_values = img_transforms(pil_img).unsqueeze(0)

    # 5. Model Inference
    with torch.no_grad():
        logits = model(
            input_ids=tokens["input_ids"].to(device),
            attention_mask=tokens["attention_mask"].to(device),
            pixel_values=pixel_values.to(device)
        )
        probs = torch.softmax(logits, dim=-1).squeeze(0)
        pred_idx = torch.argmax(probs).item()

    return {
        "predicted_sentiment": CLASS_LABELS[pred_idx],
        "confidence": round(probs[pred_idx].item(), 4),
        "class_probabilities": {CLASS_LABELS[i]: round(probs[i].item(), 4) for i in range(3)}
    }

# Mount React UI production bundle
dist_dir = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.exists(dist_dir):
    app.mount("/", StaticFiles(directory=dist_dir, html=True), name="frontend")


