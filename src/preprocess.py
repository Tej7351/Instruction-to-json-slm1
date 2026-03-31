import json
import os
from datasets import load_dataset
from transformers import AutoTokenizer

def preprocess_dataset():
    """
    Phase 3: Data Preprocessing
    We convert the structured dataset into HuggingFace dataset format,
    applies a ChatML mapping so the model learns from conversational format.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    train_path = os.path.join(data_dir, "train.json")
    test_path = os.path.join(data_dir, "test.json")
    
    if not os.path.exists(train_path) or not os.path.exists(test_path):
        print("Error: train.json or test.json not found. Please run dataset generation first.")
        return

    # Load dataset via HuggingFace robust framework
    dataset = load_dataset(
        "json", 
        data_files={"train": train_path, "test": test_path}
    )
    
    # Initialize tokenizer for Qwen2.5-0.5B
    model_name = "Qwen/Qwen2.5-0.5B"
    try:
        print(f"Loading '{model_name}' tokenizer for Chat formatting...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        # Ensure pad token is set (Qwen uses eos as pad often, but let's check)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
    except Exception as e:
        print(f"Warning: Could not load tokenizer '{model_name}'. Make sure you are connected to the internet. Error: {e}")
        print("We will skip the tokenization/saving step for HF until training, but will output formatted Chat examples.")
        tokenizer = None

    def format_chat(example):
        """
        Converts the custom layout into standard Hugging Face conversational roles.
        This allows the model to learn via ChatML.
        """
        # The target output is the strict JSON
        output_str = json.dumps(example["output"], indent=4)
        
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
        
        user_prompt = f"Instruction: {example['instruction']}\n\nJSON Output:\n"
        
        # Standard HF multi-turn dict format
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": output_str}
        ]
        
        result = {"messages": messages}
        
        # Optionally pre-tokenize text if tokenizer is present
        if tokenizer:
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
            result["text"] = text
            
        return result

    # Apply formatting
    print("Formatting dataset mapping roles...")
    processed_dataset = dataset.map(format_chat, remove_columns=dataset["train"].column_names)
    
    # Save the processed dataset
    processed_path = os.path.join(data_dir, "processed_dataset")
    processed_dataset.save_to_disk(processed_path)
    
    print(f"Saved processed dataset to {processed_path}")
    
    print("\n--- SAMPLE FORMATTED TRAINING EXAMPLE ---\n")
    sample = processed_dataset["train"][0]
    if "text" in sample:
        print(sample["text"])
    else:
        print(json.dumps(sample["messages"], indent=4))
    print("\n-----------------------------------------\n")
    print("Phase 3 Preprocessing Complete!")

if __name__ == "__main__":
    preprocess_dataset()
