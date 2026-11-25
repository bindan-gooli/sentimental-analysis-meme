import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
from torchvision import transforms
from PIL import Image
from transformers import AutoTokenizer
from model import IndicSentM

class MemeDataset(Dataset):
    """
    Dataset wrapper for multimodal meme pairs (Text + Image).
    """
    def __init__(self, samples, tokenizer, transform, max_len=128):
        self.samples = samples
        self.tokenizer = tokenizer
        self.transform = transform
        self.max_len = max_len

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        item = self.samples[idx]
        tokens = self.tokenizer(
            item["text"],
            max_length=self.max_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        # Load and transform image
        if isinstance(item["image"], str):
            image = Image.open(item["image"]).convert("RGB")
        else:
            image = item["image"].convert("RGB")
            
        pixel_values = self.transform(image)
        return {
            "input_ids": tokens["input_ids"].squeeze(0),
            "attention_mask": tokens["attention_mask"].squeeze(0),
            "pixel_values": pixel_values,
            "label": torch.tensor(item["label"], dtype=torch.long)
        }

def train_epoch(model, dataloader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0
    for batch in dataloader:
        optimizer.zero_grad()
        logits = model(
            input_ids=batch["input_ids"].to(device),
            attention_mask=batch["attention_mask"].to(device),
            pixel_values=batch["pixel_values"].to(device)
        )
        loss = criterion(logits, batch["label"].to(device))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / max(len(dataloader), 1)

@torch.no_grad()
def evaluate(model, dataloader, device):
    model.eval()
    all_preds, all_labels = [], []
    for batch in dataloader:
        logits = model(
            input_ids=batch["input_ids"].to(device),
            attention_mask=batch["attention_mask"].to(device),
            pixel_values=batch["pixel_values"].to(device)
        )
        preds = logits.argmax(dim=-1).cpu().tolist()
        all_preds.extend(preds)
        all_labels.extend(batch["label"].tolist())

    acc = accuracy_score(all_labels, all_preds)
    macro_f1 = f1_score(all_labels, all_preds, average="macro", zero_division=0)
    cm = confusion_matrix(all_labels, all_preds, labels=[0, 1, 2])
    report = classification_report(
        all_labels,
        all_preds,
        labels=[0, 1, 2],
        target_names=["Negative", "Neutral", "Positive"],
        zero_division=0
    )
    return {"accuracy": acc, "macro_f1": macro_f1, "confusion_matrix": cm, "report": report}

def save_safe_checkpoint(model, filepath="indicsent_model.pt"):
    # Security: state_dict only to prevent arbitrary code execution
    torch.save(model.state_dict(), filepath)
    print(f"Secure checkpoint saved: {filepath}")

