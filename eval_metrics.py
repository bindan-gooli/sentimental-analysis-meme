import os
import sys
os.environ["USE_TF"] = "0"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import sqlite3
import torch
from transformers import AutoTokenizer
import torchvision.transforms as transforms
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix
import json

from model import IndicSentM

DB_PATH = '/Users/bindanm/IndicSent-M/memes.db'
MODEL_PATH = '/Users/bindanm/IndicSent-M/indicsent_model.pt'
SENTIMENT_MAP = {'negative': 0, 'neutral': 1, 'positive': 2}
INV_SENTIMENT = {0: 'negative', 1: 'neutral', 2: 'positive'}

device = torch.device('cpu')
print(f"Loading tokenizer & model on {device}...")
tokenizer = AutoTokenizer.from_pretrained('bert-base-multilingual-cased')
model = IndicSentM(freeze_encoders=True).to(device)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
model.eval()

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT id, title, caption, language, sentiment FROM memes')
rows = cursor.fetchall()
conn.close()

data = []
labels = []
for r in rows:
    label = SENTIMENT_MAP.get(r['sentiment'], 1)
    data.append({
        'id': r['id'],
        'title': r['title'],
        'caption': r['caption'],
        'language': r['language'],
        'sentiment': r['sentiment'],
        'label': label
    })
    labels.append(label)

train_data, val_data = train_test_split(data, test_size=0.2, random_state=42, stratify=labels)

img_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

fallback_images = [
    Image.new('RGB', (224, 224), color=(79, 70, 229)),
    Image.new('RGB', (224, 224), color=(225, 29, 72)),
    Image.new('RGB', (224, 224), color=(15, 118, 110)),
    Image.new('RGB', (224, 224), color=(147, 51, 234)),
    Image.new('RGB', (224, 224), color=(245, 158, 11))
]

def eval_subset(subset, name=''):
    preds, trues = [], []
    with torch.no_grad():
        for i, item in enumerate(subset):
            tokens = tokenizer(item['caption'], max_length=128, padding='max_length', truncation=True, return_tensors='pt')
            img = fallback_images[i % len(fallback_images)]
            pixel_values = img_transform(img).unsqueeze(0)
            logits = model(
                input_ids=tokens['input_ids'].to(device),
                attention_mask=tokens['attention_mask'].to(device),
                pixel_values=pixel_values.to(device)
            )
            p = logits.argmax(dim=-1).item()
            preds.append(p)
            trues.append(item['label'])
    
    acc = accuracy_score(trues, preds)
    prec_m, rec_m, f1_m, _ = precision_recall_fscore_support(trues, preds, average='macro', zero_division=0)
    prec_w, rec_w, f1_w, _ = precision_recall_fscore_support(trues, preds, average='weighted', zero_division=0)
    prec_c, rec_c, f1_c, sup_c = precision_recall_fscore_support(trues, preds, average=None, labels=[0, 1, 2], zero_division=0)
    cm = confusion_matrix(trues, preds, labels=[0, 1, 2])
    print(f'=== {name} ===')
    print(f'Total samples: {len(subset)}')
    print(f'Accuracy: {acc:.4f} ({acc*100:.2f}%)')
    print(f'Macro Precision: {prec_m:.4f}, Macro Recall: {rec_m:.4f}, Macro F1: {f1_m:.4f}')
    print(f'Weighted Precision: {prec_w:.4f}, Weighted Recall: {rec_w:.4f}, Weighted F1: {f1_w:.4f}')
    for idx, cname in [(0, 'Negative'), (1, 'Neutral'), (2, 'Positive')]:
        print(f'  Class {cname}: Prec={prec_c[idx]:.4f}, Rec={rec_c[idx]:.4f}, F1={f1_c[idx]:.4f}, Support={sup_c[idx]}')
    print('Confusion Matrix (rows: true [Neg, Neu, Pos], cols: pred):')
    print(cm.tolist())
    print()
    return {
        'name': name,
        'count': len(subset),
        'accuracy': acc,
        'macro_precision': prec_m,
        'macro_recall': rec_m,
        'macro_f1': f1_m,
        'weighted_precision': prec_w,
        'weighted_recall': rec_w,
        'weighted_f1': f1_w,
        'class_metrics': {
            'negative': {'precision': prec_c[0], 'recall': rec_c[0], 'f1': f1_c[0], 'support': int(sup_c[0])},
            'neutral': {'precision': prec_c[1], 'recall': rec_c[1], 'f1': f1_c[1], 'support': int(sup_c[1])},
            'positive': {'precision': prec_c[2], 'recall': rec_c[2], 'f1': f1_c[2], 'support': int(sup_c[2])}
        },
        'confusion_matrix': cm.tolist()
    }

results = {}
results['validation'] = eval_subset(val_data, 'VALIDATION SET (20% Split, N=12)')
results['train'] = eval_subset(train_data, 'TRAIN SET (80% Split, N=48)')
results['full'] = eval_subset(data, 'FULL DATASET (N=60)')

langs = sorted(list(set(d['language'] for d in data)))
results['languages'] = {}
for l in langs:
    sub = [d for d in data if d['language'] == l]
    results['languages'][l] = eval_subset(sub, f'Language: {l}')

with open('/Users/bindanm/IndicSent-M/eval_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("EVALUATION COMPLETED SUCCESSFULLY! Results saved to eval_results.json")
