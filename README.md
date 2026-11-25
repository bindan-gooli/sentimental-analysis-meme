# IndicSent-M: Multimodal Sentiment Analysis for Code-Mixed Indic Memes

**IndicSent-M** is an end-to-end multimodal deep learning system and web application designed for sentiment classification (**Negative**, **Neutral**, **Positive**) of code-mixed Indian Internet memes across **Telugu**, **Bengali**, **Hindi**, **Tamil**, and **Global English**.

---

## Key Features

- **Multimodal Cross-Attention Architecture ([`model.py`](model.py)):**
  - **Text Encoder:** `bert-base-multilingual-cased` (768-dim) using a **hybrid pooling** strategy (`0.5 * [CLS] + 0.5 * Attention-Masked Mean Pooling`) to capture both global sentence structure and colloquial code-mixed tokens.
  - **Vision Encoder:** Pretrained `ResNet-50` (2048-dim global average pooled features).
  - **Cross-Modal Fusion:** 4-head Multi-Head Cross-Attention (`Q = text`, `K = V = vision`) in a shared 256-dim latent space with `LayerNorm`, `GELU`, and residual skip connections.
- **Balanced 5-Language Meme Corpus ([`build_full_360_dataset.py`](build_full_360_dataset.py) / [`memes.db`](memes.db)):**
  - **360** curated memes (**72** per language: Telugu, Bengali, Hindi, Tamil, Global).
  - Exact `1:1:1` sentiment distribution (**120** Negative, **120** Neutral, **120** Positive).
- **Strict Quarantined Benchmark ([`train_dataset.py`](train_dataset.py)):**
  - Stratified **80/20** split (**288** train / **72** strictly quarantined held-out validation) with zero data leakage.
- **Full-Stack Web App ([`app.py`](app.py) + [`frontend/`](frontend/)):**
  - FastAPI inference backend (`/health`, `/api/memes`, `/predict`) serving the React frontend UI.
- **Publication Assets:**
  - Automated PDF evaluation report ([`generate_pdf_report.py`](generate_pdf_report.py) $\rightarrow$ [`IndicSent_M_Evaluation_Report.pdf`](IndicSent_M_Evaluation_Report.pdf)).
  - 9+ page IEEE-format Overleaf research paper ([`paper/main.tex`](paper/main.tex), [`paper/references.bib`](paper/references.bib), [`IndicSent_M_Overleaf_Paper.zip`](IndicSent_M_Overleaf_Paper.zip)).

---

## Strict Held-Out Benchmark Results

Evaluated on the strictly quarantined 20% held-out validation split ($N = 72$):

| Metric | Negative ($C_0$) | Neutral ($C_1$) | Positive ($C_2$) | Macro Avg | Overall |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Precision** | 81.25% | 70.00% | 76.92% | **76.06%** | — |
| **Recall** | 54.17% | 87.50% | 83.33% | **75.00%** | — |
| **F1-Score** | 65.00% | 77.78% | 80.00% | **74.26%** | — |
| **Accuracy** | — | — | — | — | **75.00%** (54/72) |

- **Training Accuracy ($N=288$):** `76.04%`
- **Validation Accuracy ($N=72$):** `75.00%`
- **Generalization Gap:** `1.04%`

---

## Quickstart

### 1. Environment Setup
```bash
git clone https://github.com/bindan-gooli/sentimental-analysis-meme.git
cd sentimental-analysis-meme
python3 -m venv .venv
source .venv/bin/activate
pip install torch torchvision transformers fastapi uvicorn pillow matplotlib reportlab scikit-learn
```

### 2. Build the 360-Meme Dataset & Train the Model
*(Note: `indicsent_model.pt` is excluded from Git due to GitHub's 100 MB file-size limit. Run the commands below to generate `memes.db` and train `indicsent_model.pt` from scratch.)*
```bash
python build_full_360_dataset.py
USE_TF=0 TOKENIZERS_PARALLELISM=false python train_dataset.py
```

### 3. Run the Web Application
```bash
USE_TF=0 TOKENIZERS_PARALLELISM=false uvicorn app:app --host 0.0.0.0 --port 8000
```
Open **http://localhost:8000** in your browser for the React UI (or **http://localhost:8000/docs** for the FastAPI Swagger API docs).

### 4. Generate the PDF Evaluation Report
```bash
USE_TF=0 TOKENIZERS_PARALLELISM=false python generate_pdf_report.py IndicSent_M_Evaluation_Report.pdf
```

---

## Project Structure

```text
IndicSent-M/
├── app.py                            # FastAPI backend & static React UI server
├── model.py                          # IndicSentM PyTorch architecture (mBERT + ResNet-50 + Cross-Attention)
├── train_dataset.py                  # Strict 80/20 training & quarantined evaluation script
├── build_full_360_dataset.py         # 360-sample 5-language balanced dataset builder
├── generate_pdf_report.py            # ReportLab + Matplotlib PDF report generator
├── eval_results.json                 # Saved strict benchmark metrics
├── memes.db                          # SQLite database with 360 labeled memes
├── frontend/                         # React + Vite frontend (source & dist bundle)
├── paper/                            # IEEE-format Overleaf LaTeX research paper
│   ├── main.tex
│   └── references.bib
├── IndicSent_M_Evaluation_Report.pdf # Generated evaluation report PDF
└── IndicSent_M_Overleaf_Paper.zip    # Ready-to-upload Overleaf project archive
```

---

## Team Members
- **Bindan M**
- **Riya Kabra**
- **Shreya Singh**
- **Ishita Sahai**
- **Chirayu Chhajed**
