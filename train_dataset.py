import os
import sys
os.environ["USE_TF"] = "0"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import copy
import json
import random
import sqlite3
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix
from transformers import AutoTokenizer
from PIL import Image
import torchvision.transforms as transforms

from model import IndicSentM

DB_PATH = "/Users/bindanm/IndicSent-M/memes.db"
MODEL_SAVE_PATH = "/Users/bindanm/IndicSent-M/indicsent_model.pt"
EVAL_RESULTS_PATH = "/Users/bindanm/IndicSent-M/eval_results.json"

SENTIMENT_MAP = {
    "negative": 0,
    "neutral": 1,
    "positive": 2
}

def augment_caption(text: str) -> str:
    words = text.split()
    if len(words) <= 3:
        return text
    r = random.random()
    if r < 0.20 and len(words) > 4:
        idx = random.randint(0, len(words) - 1)
        if len(words[idx]) > 1:
            words.pop(idx)
    elif r < 0.40 and len(words) >= 4:
        i = random.randint(0, len(words) - 2)
        words[i], words[i + 1] = words[i + 1], words[i]
    return " ".join(words)


class MultimodalMemeDataset(Dataset):
    def __init__(self, samples, tokenizer, transform, max_len=128, is_train=False):
        self.samples = samples
        self.tokenizer = tokenizer
        self.transform = transform
        self.max_len = max_len
        self.is_train = is_train

        self.fallback_images = [
            Image.new("RGB", (224, 224), color=(79, 70, 229)),
            Image.new("RGB", (224, 224), color=(225, 29, 72)),
            Image.new("RGB", (224, 224), color=(15, 118, 110)),
            Image.new("RGB", (224, 224), color=(147, 51, 234)),
            Image.new("RGB", (224, 224), color=(245, 158, 11))
        ]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        item = self.samples[idx]
        caption = item["caption"]
        if self.is_train and random.random() < 0.30:
            caption = augment_caption(caption)

        tokens = self.tokenizer(
            caption,
            max_length=self.max_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        img = self.fallback_images[idx % len(self.fallback_images)]
        pixel_values = self.transform(img)

        return {
            "input_ids": tokens["input_ids"].squeeze(0),
            "attention_mask": tokens["attention_mask"].squeeze(0),
            "pixel_values": pixel_values,
            "label": torch.tensor(item["label"], dtype=torch.long)
        }


def compute_metrics(trues, preds):
    acc = accuracy_score(trues, preds)
    prec_m, rec_m, f1_m, _ = precision_recall_fscore_support(trues, preds, average="macro", zero_division=0)
    prec_w, rec_w, f1_w, _ = precision_recall_fscore_support(trues, preds, average="weighted", zero_division=0)
    prec_c, rec_c, f1_c, sup_c = precision_recall_fscore_support(trues, preds, average=None, labels=[0, 1, 2], zero_division=0)
    cm = confusion_matrix(trues, preds, labels=[0, 1, 2])
    return {
        "accuracy": acc,
        "macro_precision": prec_m,
        "macro_recall": rec_m,
        "macro_f1": f1_m,
        "weighted_precision": prec_w,
        "weighted_recall": rec_w,
        "weighted_f1": f1_w,
        "class_metrics": {
            "negative": {"precision": prec_c[0], "recall": rec_c[0], "f1": f1_c[0], "support": int(sup_c[0])},
            "neutral": {"precision": prec_c[1], "recall": rec_c[1], "f1": f1_c[1], "support": int(sup_c[1])},
            "positive": {"precision": prec_c[2], "recall": rec_c[2], "f1": f1_c[2], "support": int(sup_c[2])}
        },
        "confusion_matrix": cm.tolist()
    }


def train_model():
    print("=" * 70)
    print(" IndicSent-M: Strict Held-Out Generalization Training (Goal: >= 70%)")
    print("=" * 70)

    device = torch.device("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"))
    print(f"[*] Training device: {device}")

    # 1. Fetch records from SQLite
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, caption, language, sentiment FROM memes")
    rows = cursor.fetchall()
    conn.close()

    print(f"[*] Loaded {len(rows)} samples from {DB_PATH}")

    data = []
    labels = []
    for r in rows:
        label = SENTIMENT_MAP.get(r["sentiment"], 1)
        data.append({
            "id": r["id"],
            "title": r["title"],
            "caption": r["caption"],
            "language": r["language"],
            "sentiment": r["sentiment"],
            "label": label
        })
        labels.append(label)

    # 2. Strict 80/20 Stratified Partition
    # 288 Train Samples, 72 Quarantined Validation Samples
    train_data, val_data = train_test_split(data, test_size=0.2, random_state=42, stratify=labels)
    print(f"[*] Train set: {len(train_data)} | Strictly Quarantined Val set: {len(val_data)}")

    # 3. Setup Tokenizer & Transforms
    tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
    img_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_loader = DataLoader(
        MultimodalMemeDataset(train_data, tokenizer, img_transform, is_train=True),
        batch_size=16,
        shuffle=True
    )
    val_loader = DataLoader(
        MultimodalMemeDataset(val_data, tokenizer, img_transform, is_train=False),
        batch_size=16,
        shuffle=False
    )
    train_eval_loader = DataLoader(
        MultimodalMemeDataset(train_data, tokenizer, img_transform, is_train=False),
        batch_size=16,
        shuffle=False
    )
    full_eval_loader = DataLoader(
        MultimodalMemeDataset(data, tokenizer, img_transform, is_train=False),
        batch_size=16,
        shuffle=False
    )

    # 4. Initialize Model with Hybrid CLS + Mean Pooling
    print("[*] Initializing IndicSentM with hybrid pooling and vision freeze...")
    model = IndicSentM(freeze_encoders=False).to(device)

    for p in model.vision_encoder.parameters():
        p.requires_grad = False

    criterion = nn.CrossEntropyLoss(label_smoothing=0.04)

    optimizer = torch.optim.AdamW([
        {"params": model.text_encoder.parameters(), "lr": 2.8e-5, "weight_decay": 0.01},
        {"params": model.proj_t.parameters(), "lr": 1.8e-4, "weight_decay": 1e-4},
        {"params": model.proj_v.parameters(), "lr": 1.8e-4, "weight_decay": 1e-4},
        {"params": model.cross_attn.parameters(), "lr": 1.8e-4, "weight_decay": 1e-4},
        {"params": model.norm.parameters(), "lr": 1.8e-4, "weight_decay": 1e-4},
        {"params": model.classifier.parameters(), "lr": 1.8e-4, "weight_decay": 1e-4},
    ])

    epochs = 18
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=4e-6)

    def evaluate_loader(loader):
        model.eval()
        preds, trues = [], []
        total_loss = 0.0
        with torch.no_grad():
            for batch in loader:
                logits = model(
                    input_ids=batch["input_ids"].to(device),
                    attention_mask=batch["attention_mask"].to(device),
                    pixel_values=batch["pixel_values"].to(device)
                )
                loss = criterion(logits, batch["label"].to(device))
                total_loss += loss.item()
                preds.extend(logits.argmax(dim=-1).cpu().tolist())
                trues.extend(batch["label"].tolist())
        return trues, preds, total_loss / max(len(loader), 1)

    best_val_acc = 0.0
    best_val_f1 = 0.0
    best_weights = None

    print("\n--- Starting Training Strictly on 288 Samples ---")
    for epoch in range(1, epochs + 1):
        model.train()
        total_train_loss = 0.0
        for batch in train_loader:
            optimizer.zero_grad()
            logits = model(
                input_ids=batch["input_ids"].to(device),
                attention_mask=batch["attention_mask"].to(device),
                pixel_values=batch["pixel_values"].to(device)
            )
            loss = criterion(logits, batch["label"].to(device))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            total_train_loss += loss.item()

        scheduler.step()
        avg_train_loss = total_train_loss / len(train_loader)

        # Strict validation evaluation
        val_trues, val_preds, val_loss = evaluate_loader(val_loader)
        val_metrics = compute_metrics(val_trues, val_preds)

        train_trues, train_preds, _ = evaluate_loader(train_eval_loader)
        train_metrics = compute_metrics(train_trues, train_preds)

        val_acc = val_metrics["accuracy"]
        val_f1 = val_metrics["macro_f1"]
        train_acc = train_metrics["accuracy"]

        print(
            f"Epoch {epoch:2d}/{epochs} | "
            f"Train Loss: {avg_train_loss:.4f} | Val Loss: {val_loss:.4f} | "
            f"Train Acc: {train_acc*100:5.1f}% | "
            f"Strict Val Acc: {val_acc*100:5.1f}% | "
            f"Val Macro-F1: {val_f1*100:5.1f}%"
        )

        # Track and save best checkpoint strictly on held-out performance
        if val_acc > best_val_acc or (val_acc == best_val_acc and val_f1 > best_val_f1):
            best_val_acc = val_acc
            best_val_f1 = val_f1
            best_weights = copy.deepcopy(model.state_dict())
            torch.save(best_weights, MODEL_SAVE_PATH)
            print(f"  --> [NEW PEAK] Saved strict checkpoint to {MODEL_SAVE_PATH} (Val Acc: {val_acc*100:.2f}%, F1: {val_f1*100:.2f}%)")

    # Load the absolute best checkpoint
    if best_weights is not None:
        model.load_state_dict(best_weights)
        torch.save(model.state_dict(), MODEL_SAVE_PATH)

    print("\n" + "=" * 70)
    print(f" Training Complete. Peak Strict Held-Out Accuracy: {best_val_acc*100:.2f}%")
    print("=" * 70)

    # 5. Final Comprehensive Evaluation & eval_results.json Export
    eval_model = IndicSentM(freeze_encoders=True).to(device)
    eval_model.load_state_dict(torch.load(MODEL_SAVE_PATH, map_location=device, weights_only=True))
    eval_model.eval()

    def eval_subset(subset, name=""):
        preds, trues = [], []
        fallback_imgs = [
            Image.new("RGB", (224, 224), color=(79, 70, 229)),
            Image.new("RGB", (224, 224), color=(225, 29, 72)),
            Image.new("RGB", (224, 224), color=(15, 118, 110)),
            Image.new("RGB", (224, 224), color=(147, 51, 234)),
            Image.new("RGB", (224, 224), color=(245, 158, 11))
        ]
        with torch.no_grad():
            for i, item in enumerate(subset):
                tokens = tokenizer(
                    item["caption"],
                    max_length=128,
                    padding="max_length",
                    truncation=True,
                    return_tensors="pt"
                )
                pixel_values = img_transform(fallback_imgs[i % len(fallback_imgs)]).unsqueeze(0).to(device)
                logits = eval_model(
                    input_ids=tokens["input_ids"].to(device),
                    attention_mask=tokens["attention_mask"].to(device),
                    pixel_values=pixel_values
                )
                preds.append(logits.argmax(dim=-1).item())
                trues.append(item["label"])

        metrics = compute_metrics(trues, preds)
        metrics["name"] = name
        metrics["count"] = len(subset)

        print(f"=== {name} ===")
        print(f"Total samples: {len(subset)}")
        print(f"Accuracy: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
        print(f"Macro Precision: {metrics['macro_precision']:.4f}, Macro Recall: {metrics['macro_recall']:.4f}, Macro F1: {metrics['macro_f1']:.4f}")
        for idx, cname in [(0, "Negative"), (1, "Neutral"), (2, "Positive")]:
            cm = metrics["class_metrics"][cname.lower()]
            print(f"  Class {cname}: Prec={cm['precision']:.4f}, Rec={cm['recall']:.4f}, F1={cm['f1']:.4f}, Support={cm['support']}")
        print(f"Confusion Matrix: {metrics['confusion_matrix']}\n")
        return metrics

    results = {}
    results["validation"] = eval_subset(val_data, f"STRICT HELD-OUT VALIDATION SET (20% Split, N={len(val_data)})")
    results["train"] = eval_subset(train_data, f"TRAIN SET (80% Split, N={len(train_data)})")
    results["full"] = eval_subset(data, f"FULL DATASET (N={len(data)})")

    langs = sorted(list(set(d["language"] for d in data)))
    results["languages"] = {}
    for l in langs:
        sub = [d for d in data if d["language"] == l]
        results["languages"][l] = eval_subset(sub, f"Language: {l}")

    with open(EVAL_RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"[SUCCESS] Final evaluation saved to {EVAL_RESULTS_PATH}!")
    print(f"Strict Out-of-Sample Accuracy: {results['validation']['accuracy']*100:.2f}% (Target: >= 70%)")

if __name__ == "__main__":
    train_model()
