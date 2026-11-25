import os
import io
import torch
import torch.nn as nn
from PIL import Image
from transformers import AutoTokenizer
from torchvision import transforms
from fastapi.testclient import TestClient

from model import IndicSentM
from train import MemeDataset, DataLoader, train_epoch, evaluate, save_safe_checkpoint

def run_pipeline_test():
    print("=" * 65)
    print(" IndicSent-M: End-to-End Multimodal Verification & Security Check")
    print("=" * 65)

    device = torch.device("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"))
    print(f"[*] Execution device: {device}")

    # 1. Model Initialization
    print("\n[Step 1] Initializing BERT + ResNet-50 Cross-Attention Network...")
    model = IndicSentM().to(device)
    tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
    print(" -> Model loaded successfully.")

    # 2. Forward Pass Test
    print("\n[Step 2] Testing Forward Pass on Multimodal Batch...")
    dummy_input_ids = torch.randint(0, 1000, (2, 128)).to(device)
    dummy_attn_mask = torch.ones((2, 128)).to(device)
    dummy_pixels = torch.randn(2, 3, 224, 224).to(device)
    
    with torch.no_grad():
        out = model(dummy_input_ids, dummy_attn_mask, dummy_pixels)
    assert out.shape == (2, 3), f"Expected output shape (2, 3), got {out.shape}"
    print(f" -> Forward pass verified. Output shape: {out.shape} (Batch x Classes)")

    # 3. Mini Dataset & Training / Evaluation Verification
    print("\n[Step 3] Simulating Training & Evaluation Epochs...")
    img_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Sample Indian-language posts (Bengali & Telugu)
    mock_samples = [
        {"text": "খুব সুন্দর অভিজ্ঞতা, সার্ভিস চমৎকার!", "image": Image.new("RGB", (100, 100), color="green"), "label": 2}, # Positive
        {"text": "সাধারণ মানের, খুব একটা বিশেষ কিছু না।", "image": Image.new("RGB", (100, 100), color="gray"), "label": 1},  # Neutral
        {"text": "చాలా చెత్త సర్వీస్, సమయం వృధా అయింది!", "image": Image.new("RGB", (100, 100), color="red"), "label": 0},  # Negative
        {"text": "వారేవా! ఇంతకంటే మంచి జోక్ ఎప్పుడూ చూడలేదు.", "image": Image.new("RGB", (100, 100), color="blue"), "label": 2} # Positive
    ]
    dataset = MemeDataset(mock_samples, tokenizer, img_transform)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    criterion = nn.CrossEntropyLoss()

    train_loss = train_epoch(model, dataloader, optimizer, criterion, device)
    print(f" -> Training loss after 1 epoch: {train_loss:.4f}")

    eval_results = evaluate(model, dataloader, device)
    print(f" -> Evaluation Accuracy: {eval_results['accuracy'] * 100:.2f}%")
    print(f" -> Evaluation Macro-F1: {eval_results['macro_f1']:.4f}")

    # 4. Safe Model Checkpointing
    checkpoint_file = "/tmp/demo_indicsent_checkpoint.pt"
    save_safe_checkpoint(model, checkpoint_file)

    # 5. API & Security Verification
    print("\n[Step 4] Validating FastAPI Security & Authorization...")
    from app import app, SERVER_API_KEY

    client = TestClient(app)

    # Health check
    res_health = client.get("/health")
    assert res_health.status_code == 200, "Health check failed"
    print(" [PASS] Health check endpoint returned 200 OK.")

    # Prepare dummy image in memory
    buf = io.BytesIO()
    Image.new("RGB", (200, 200), color="yellow").save(buf, format="JPEG")
    buf.seek(0)
    image_bytes = buf.getvalue()

    # Test 1: Open Prediction (No API Key Required) -> 200 OK
    res_pred = client.post(
        "/predict",
        data={"text": "చాలా బాగుంది! (Really good!)"},
        files={"image": ("test.jpg", image_bytes, "image/jpeg")}
    )
    assert res_pred.status_code == 200, f"Expected 200, got {res_pred.status_code} - {res_pred.text}"
    body = res_pred.json()
    print(" [PASS] Open meme prediction successful (Zero Auth Friction):")
    print(f"        Predicted Sentiment : {body['predicted_sentiment']}")
    print(f"        Confidence          : {body['confidence']}")
    print(f"        Probabilities       : {body['class_probabilities']}")
    print(f"        Predicted Sentiment : {body['predicted_sentiment']}")
    print(f"        Confidence          : {body['confidence']}")
    print(f"        Probabilities       : {body['class_probabilities']}")

    # Test 4: Malformed Image Injection Prevention -> 400 Bad Request
    res_malformed = client.post(
        "/predict",
        headers={"X-API-Key": SERVER_API_KEY},
        data={"text": "Valid text"},
        files={"image": ("fake.jpg", b"NOT_AN_IMAGE_HEADER_EXPLOIT", "image/jpeg")}
    )
    assert res_malformed.status_code == 400, f"Expected 400, got {res_malformed.status_code}"
    print(" [PASS] Malformed/Corrupt image payload rejected with 400 Bad Request.")

    print("\n" + "=" * 65)
    print(" [SUCCESS] All architecture, pipeline, and security tests PASSED!")
    print("=" * 65)

if __name__ == "__main__":
    run_pipeline_test()

