import json
import os
import re

def article_fix(text):
    for tone in ["empathetic", "urgent", "informative", "enthusiastic"]:
        # Case sensitive replacement
        text = text.replace(f"a {tone}", f"an {tone}")
        text = text.replace(f"A {tone}", f"An {tone}")
    return text

def empathetic_content(task, topic):
    # Tone: Kind, understanding, supportive responses
    if task == "tweet":
        return f"I know dealing with {topic} can feel really overwhelming sometimes. Remember to take a step back and breathe; you are doing better than you think. Sending positive energy your way today. ❤️"
    elif task == "linkedin_post":
        return f"If you are struggling with {topic} right now, please know that your feelings are entirely valid and you are not alone. It takes time to navigate these challenges, and it is okay to ask for help. Feel free to reach out if you need someone to talk to."
    elif task == "summarization":
        return f"Understanding {topic} is difficult and can understandably cause anxiety. At its core, it simply involves navigating a few complex ideas that will become clearer with time. Take it one step at a time, and don't be too hard on yourself."
    elif task == "qa":
        return f"It's completely normal to have questions about '{topic}', and many people find it confusing at first! The simplest way to understand it is to take it piece by piece. You are asking great questions, and you will definitely get the hang of it!"
    elif task == "email":
        return f"Hi there, I understand that {topic} has been a source of stress lately. Please don't worry, we are here to support you through this process. Take all the time you need, and let me know how I can make things easier for you."
    elif task == "product_description":
        return f"We recognize that dealing with loud or uncomfortable environments is genuinely exhausting. That's why this product was thoughtfully designed to give you a gentle, comforting break. We hope it helps provide the peace of mind you truly deserve."
    return ""

def extract_topic(instruction):
    if "about " in instruction:
        return instruction.split("about ")[-1].replace(".", "").replace("?", "").strip()
    elif "regarding: " in instruction:
        return instruction.split("regarding: ")[-1].replace(".", "").replace("?", "").strip()
    elif "focusing on " in instruction:
        return instruction.split("focusing on ")[-1].split(".")[0].strip()
    elif "discussing " in instruction:
        return instruction.split("discussing ")[-1].replace(".", "").replace("?", "").strip()
    return "this situation"

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    # 1. Process files
    for filename in ["dataset.json", "train.json", "test.json", "sample_preview.json"]:
        path = os.path.join(data_dir, filename)
        if not os.path.exists(path):
            continue
            
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        for item in data:
            # Fix Grammar
            item["instruction"] = article_fix(item["instruction"])
            
            # Ensure Empathy Tone Consistency
            if item["output"]["tone"] == "empathetic":
                topic = extract_topic(item["instruction"])
                item["output"]["content"] = empathetic_content(item["output"]["task"], topic)
                
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            
    # 2. Validation & Anomaly Detection on Final Dataset
    with open(os.path.join(data_dir, "dataset.json"), "r", encoding="utf-8") as f:
        full_data = json.load(f)
        
    invalid_count = 0
    anomalies = []
    
    for idx, item in enumerate(full_data):
        try:
            out = item["output"]
            if not isinstance(out, dict):
                invalid_count += 1
                anomalies.append(f"Sample {idx}: Output is not a JSON object")
                continue
            
            required_keys = {"task", "content", "tone", "format"}
            if set(out.keys()) != required_keys:
                invalid_count += 1
                anomalies.append(f"Sample {idx}: Missing or extra keys. Found {list(out.keys())}")
                continue
            
            if out["format"] != "json":
                invalid_count += 1
                anomalies.append(f"Sample {idx}: Format is not exactly 'json'")
                
            if not isinstance(item["instruction"], str) or len(item["instruction"]) < 5:
                anomalies.append(f"Sample {idx}: Instruction is suspiciously short or invalid")
                invalid_count += 1
                
        except Exception as e:
            invalid_count += 1
            anomalies.append(f"Sample {idx}: Unhandled exception {str(e)}")
            
    # Write validation report
    val_path = os.path.join(data_dir, "dataset_validation.txt")
    with open(val_path, "w", encoding="utf-8") as f:
        f.write("=== Dataset Validation Report ===\n")
        f.write(f"Total Samples: {len(full_data)}\n")
        f.write(f"Invalid JSON/Structure Count: {invalid_count}\n")
        f.write("\nAnomalies Detected:\n")
        if anomalies:
            for a in anomalies:
                f.write(f"- {a}\n")
        else:
            f.write("- None. Entire dataset is perfectly structured valid JSON.\n")
            
    print(f"Validation complete. Report saved to {val_path}")

if __name__ == "__main__":
    main()
