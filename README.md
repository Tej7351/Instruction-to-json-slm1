<h1 align="center">🤖 SLM JSON Generator</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Model-Qwen2.5--0.5B-blue?style=for-the-badge&logo=huggingface" alt="Model">
  <img src="https://img.shields.io/badge/Fine_Tuning-QLoRA-orange?style=for-the-badge&logo=pytorch" alt="Fine-Tuning">
  <img src="https://img.shields.io/badge/Accuracy_Improvement-%2B40%25-brightgreen?style=for-the-badge" alt="Accuracy">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python" alt="Python">
</p>

## 📌 Overview
This repository contains an end-to-end Machine Learning pipeline demonstrating how to fine-tune a Highly Efficient Small Language Model (`Qwen2.5-0.5B`) to function as a deterministic, structured JSON generator.

### 🎯 What The Model Does
It takes **any natural language instruction** and strictly outputs only valid JSON following this schema:
```json
{
  "task": "<task_type>",
  "content": "<generated response>",
  "tone": "<tone>",
  "format": "json"
}
```
## Setup Instructions

1. Clone the repo
git clone https://github.com/USERNAME/slm-json-generator

2. Install dependencies
pip install -r requirements.txt

3. Open Qwen_FineTuning_Colab.ipynb in Google Colab

4. Mount Google Drive and update paths in Cell 2

5. Run all cells in order

## 📊 Evaluation Results
We evaluated the model on 10 diverse, out-of-distribution prompts (such as tweets, cold emails, plotting logic, etc.) to test robustness and structural adherence.

| Metric | Base Model (Pre-Tuning) | Fine-Tuned Model |
|--------|-------------------------|------------------|
| **Valid JSON Outputs** | 6 / 10 | **10 / 10** |
| **JSON Accuracy** | 60% | **100% (+40%)** |
| **Training Loss** | 2.27 (Initial) | **1.32 (Final)** |

## 🧠 Tech Stack & Hardware
- **Base Model**: `Qwen/Qwen2.5-0.5B`
- **Methodology**: QLoRA (4-bit Quantization) + LoRA Adapters (r=16, alpha=32)
- **Hardware**: Google Colab T4 GPU (Free Tier)
- **Training Config**: 3 Epochs, `paged_adamw_32bit` optimizer, `fp16` precision
- **Libraries**: `transformers==4.51.3`, `peft==0.15.2`, `trl==0.16.1`, `bitsandbytes==0.46.1`, `datasets==3.5.0`

## 📂 Project Structure
```text
slm_json_generator/
├── data/                        # dataset.json + processed datasets
├── src/                         # source scripts (inference, dataset generation)
├── outputs/                     # evaluation generation outputs
├── evaluation/                  # baseline comparison and metric results
├── models/                      # LoRA adapter config metadata
├── lora_adapters/               # Trained T4 GPU LoRA weights
├── Qwen_FineTuning_Colab.ipynb  # Full reproducible training notebook used in Colab
├── requirements.txt             # Virtual environment dependencies
├── README.md                    # Project documentation
└── REPORT.md                    # Detailed Internship Project Report
```

## ⚙️ How to Run & Use
**1. Environment Setup**
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

**2. Test Instructions Used For 100% Evaluation Benchmark:**
1. *Write a short tweet about AI replacing developers in a sarcastic tone.*
2. *Summarize the benefits of solar energy globally in 2 sentences.*
3. *Write a professional LinkedIn post about finishing a ML internship.*
4. *What is the capital of France and what is its population?*
5. *Write a cold email to a recruiter for a data science role.*
6. *Describe a new smart coffee mug in a persuasive tone.*
7. *Explain quantum computing to a 5 year old.*
8. *Write a tweet about drinking too much coffee while coding.*
9. *Summarize the plot of The Matrix.*
10. *Write a product description for high-end noise-cancelling headphones.*
