# Architecture

## Pipeline Overview
Raw Instructions → Dataset (573 samples) → QLoRA Fine-tuning → JSON Output

## Model
- **Base**: Qwen2.5-0.5B (causal LM)
- **Method**: QLoRA (4-bit NF4 quantization)  
- **LoRA rank**: r=16, alpha=32
- **Target modules**: q_proj, k_proj, v_proj, o_proj
- **Precision**: Mixed Precision (fp16)

## Training Config
- **Epochs**: 3
- **Batch size**: 2 (effective: 16 with gradient accumulation steps=8)
- **Learning rate**: 2e-4 (cosine scheduler)
- **Optimizer**: paged_adamw_32bit
- **Max sequence length**: 512
- **Hardware**: T4 GPU (Google Colab free tier)

## Results
- **Base accuracy**: 60%
- **Fine-tuned accuracy**: 100%
- **Loss**: 2.27 → 1.32 (improvement: -42%)

## Data Flow Diagram
```text
[dataset.json]
      ↓
[Format as ### Instruction / ### Response template]
      ↓
[Tokenize + DataCollatorForCompletionOnlyLM]
      ↓  
[QLoRA Training - only JSON response tokens trained, masking prompts]
      ↓
[LoRA Adapters saved to models/ directory]
      ↓
[Inference: PEFT Adapter loaded over Base Model]
      ↓
[Output: 10/10 valid JSON outputs]
