import os
import json
import torch
from datasets import load_from_disk
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig

# 1. Configuration Setup
model_name = "Qwen/Qwen2.5-0.5B"
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataset_path = os.path.join(base_dir, "data", "processed_dataset")
output_dir = os.path.join(base_dir, "models", "lora_adapters")
logging_dir = os.path.join(base_dir, "outputs", "logs")
config_path = os.path.join(base_dir, "models", "training_config.json")

learning_rate = 2e-4
batch_size = 4
num_train_epochs = 3
max_seq_length = 512

def train():
    """
    Phase 4: LoRA / QLoRA Fine-Tuning
    """
    print("Loading tokenizer and dataset...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    dataset = load_from_disk(dataset_path)
    
    print("Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32
    )
    
    # 3. LoRA Configuration
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, peft_config)
    
    # 4. Save Training Config
    training_config = {
        "learning_rate": learning_rate,
        "batch_size": batch_size,
        "num_train_epochs": num_train_epochs,
        "max_seq_length": max_seq_length,
        "lora_r": peft_config.r,
        "lora_alpha": peft_config.lora_alpha
    }
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(training_config, f, indent=4)
        
    # 5. Define Training Arguments using SFTConfig (TRL >= 0.9.0)
    training_args = SFTConfig(
        output_dir=output_dir,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=4,
        learning_rate=learning_rate,
        logging_steps=10, 
        num_train_epochs=num_train_epochs,
        optim="adamw_torch",
        fp16=False,
        bf16=False,
        save_strategy="epoch",
        logging_dir=logging_dir,
        report_to="none",
        dataset_text_field="text",
        max_length=max_seq_length,
    )
    
    # 6. SFTTrainer Initialization
    print("Starting SFTTrainer...")
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        processing_class=tokenizer,
        args=training_args,
    )
    
    trainer.train()
    
    print(f"Training complete! Saving LoRA adapters to {output_dir}")
    trainer.model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

def is_valid_json(text: str) -> bool:
    text = text.strip()
    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    if text.endswith("```"):
        text = text[:-3].strip()
    try:
        json.loads(text)
        return True
    except:
        return False

def test_inference():
    """
    6. Inference After Training
    Tests the finetuned LoRA adapter to verify format alignment.
    """
    from peft import PeftModel
    
    print("Testing Fine-tuned Model...")
    tokenizer = AutoTokenizer.from_pretrained(output_dir)
    
    base_model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32)
    
    model = PeftModel.from_pretrained(base_model, output_dir)
    
    instructions = [
        "Write a short tweet about AI replacing developers in a sarcastic tone.",
        "Summarize the benefits of solar energy globally in 2 sentences.",
        "Write a professional LinkedIn post about finishing a machine learning internship.",
        "What is the capital of France and what is its population?",
        "Write a cold email to a recruiter for a data science role emphasizing python skills.",
        "Describe a new smart coffee mug in a persuasive tone.",
        "Explain quantum computing to a 5 year old.",
        "Write a tweet about drinking too much coffee while coding.",
        "Summarize the plot of The Matrix.",
        "Write a product description for high-end noise-cancelling headphones."
    ]
    
    system_prompt = (
        "You are a strict data extraction AI. You must generate output strictly in the following JSON format:\n\n"
        "{\n"
        '  "task": "<task_type>",\n'
        '  "content": "<generated response>",\n'
        '  "tone": "<tone>",\n'
        '  "format": "json"\n'
        "}\n\n"
        "Ensure:\n"
        "* No extra text\n"
        "* No explanation\n"
        "* Only JSON output"
    )

    results = []
    
    print("Running 10 samples on Finetuned Model...")
    for instr in instructions:
        prompt = f"{system_prompt}\n\nInstruction: {instr}\n\nJSON Output:\n"
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=150, temperature=0.7, do_sample=True, pad_token_id=tokenizer.eos_token_id)
            
        input_length = inputs.input_ids.shape[1]
        generated_text = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True).strip()
        
        valid = is_valid_json(generated_text)
        results.append({
            "instruction": instr,
            "finetuned_generated_text": generated_text,
            "is_valid_json": valid
        })
        print(f"Instruction: {instr}")
        print(f"Output:\n{generated_text}")
        print(f"Valid JSON: {valid}\n{'-'*40}")
        
    out_file = os.path.join(base_dir, "outputs", "finetuned_outputs.json")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        
    total = len(results)
    valid_count = sum(1 for r in results if r["is_valid_json"])
    print(f"\n--- FINETUNED MODEL METRICS ---")
    print(f"Total Samples: {total}")
    print(f"Valid JSON Outputs: {valid_count}")
    print(f"JSON Accuracy: {valid_count}/{total} ({(valid_count/total)*100:.1f}%)")
    print(f"Base Model Accuracy was 60%. Improvement: +{((valid_count/total)*100) - 60:.1f}%\n")
        
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_inference()
    else:
        train()
