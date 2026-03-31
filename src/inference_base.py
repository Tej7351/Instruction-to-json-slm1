import os
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def is_valid_json(text: str) -> bool:
    """
    Checks whether the generated output is valid JSON.
    Attempts to strictly parse the string. Returns True if successful, False otherwise.
    """
    text = text.strip()
    
    # Strip markdown code blocks if the model generates them
    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    if text.endswith("```"):
        text = text[:-3].strip()
        
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False

def run_inference(model, tokenizer, instructions, system_prompt):
    """
    Runs inference for a list of instructions.
    Returns a list of structured results.
    """
    results = []
    
    print(f"Running inference on {len(instructions)} samples...")
    for instr in instructions:
        prompt = f"{system_prompt}\n\nInstruction: {instr}\n\nJSON Output:\n"
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
            
        input_length = inputs.input_ids.shape[1]
        generated_text = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True).strip()
        
        valid_json = is_valid_json(generated_text)
        
        results.append({
            "instruction": instr,
            "base_generated_text": generated_text,
            "is_valid_json": valid_json
        })
        
        print(f"Instruction: {instr}")
        print(f"Base Output:\n{generated_text}")
        print(f"Valid JSON: {valid_json}")
        print("-" * 50)
        
    return results

def main():
    # Resolve paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, "outputs", "base_outputs.json")
    summary_path = os.path.join(base_dir, "outputs", "base_summary.txt")
    
    model_name = "Qwen/Qwen2.5-0.5B" 
    print(f"Loading Base Model {model_name}...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
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
    
    # 1. STRICT SYSTEM PROMPT
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

    # 6. KEEP CODE CLEAN AND MODULAR
    results = run_inference(model, tokenizer, instructions, system_prompt)
    
    # 5. PRINT SUMMARY METRICS
    total_samples = len(results)
    valid_samples = sum(1 for r in results if r["is_valid_json"])
    
    # Calculate accuracy
    accuracy = valid_samples / total_samples if total_samples > 0 else 0
    accuracy_str = f"{valid_samples}/{total_samples}"
    
    print(f"\nTotal Samples: {total_samples}")
    print(f"Valid JSON Outputs: {valid_samples}")
    print(f"JSON Accuracy: {accuracy_str} ({accuracy:.1%})")
    
    # 4. SAVE CLEAN AND STRUCTURED OUTPUT
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nSaved structured outputs to {output_path}")
    
    # 7. OPTIONAL (BONUS): Save base_summary.txt
    summary_text = (
        f"Base Model Inference Summary ({model_name})\n"
        f"----------------------------------------\n"
        f"Total Samples: {total_samples}\n"
        f"Valid JSON Outputs: {valid_samples}\n"
        f"JSON Accuracy: {accuracy_str} ({accuracy:.1%})\n\n"
        f"Observations:\n"
        f"- The base model often struggles to follow strict formatting without a few-shot prompt or fine-tuning.\n"
        f"- We expect this baseline to demonstrate a low JSON validity rate.\n"
        f"- Common issues include conversational filler (e.g., 'Here is your JSON:') and generated extra text.\n"
    )
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_text)
        
    print(f"Saved summary metrics to {summary_path}")

if __name__ == "__main__":
    main()
