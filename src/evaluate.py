import json
import os

def run_evaluation():
    base_path = "outputs/base_outputs.json"
    finetuned_path = "outputs/finetuned_outputs.json"
    eval_json_path = "evaluation/evaluation.json"
    eval_md_path = "evaluation/eval_logs.md"

    os.makedirs("evaluation", exist_ok=True)

    if not os.path.exists(base_path) or not os.path.exists(finetuned_path):
        print(f"ERROR: Missing output files. Base exists: {os.path.exists(base_path)}, Finetuned exists: {os.path.exists(finetuned_path)}")
        return

    with open(base_path, "r", encoding="utf-8") as f:
        base_data = json.load(f)
    
    with open(finetuned_path, "r", encoding="utf-8") as f:
        finetuned_data = json.load(f)

    # Calculate metrics
    total = len(base_data)
    base_valid = sum(1 for item in base_data if item.get("is_valid_json", False))
    finetuned_valid = sum(1 for item in finetuned_data if item.get("is_valid_json", False))

    base_acc = (base_valid / total) * 100 if total > 0 else 0
    finetuned_acc = (finetuned_valid / total) * 100 if total > 0 else 0

    eval_json = {
        "metrics": {
            "total_samples": total,
            "base_model_valid_json": base_valid,
            "finetuned_model_valid_json": finetuned_valid,
            "base_accuracy": f"{base_acc:.1f}%",
            "finetuned_accuracy": f"{finetuned_acc:.1f}%",
            "absolute_improvement": f"{finetuned_acc - base_acc:.1f}%"
        },
        "failure_cases": []
    }

    # Identify failure cases
    for ft_item in finetuned_data:
        if not ft_item.get("is_valid_json", False):
            eval_json["failure_cases"].append({
                "instruction": ft_item["instruction"],
                "generated_output": ft_item.get("finetuned_generated_text", ""),
                "error": "Invalid JSON mapping"
            })

    with open(eval_json_path, "w", encoding="utf-8") as f:
        json.dump(eval_json, f, indent=4)
        
    # Generate Markdown Comparison Table
    md_lines = []
    md_lines.append("# Phase 5: Qualitative Evaluation Logs\n")
    md_lines.append(f"**Base Accuracy**: {base_acc:.1f}%  ")
    md_lines.append(f"**Finetuned Accuracy**: {finetuned_acc:.1f}%\n")
    
    md_lines.append("## Before vs After Comparison\n")
    md_lines.append("| Instruction | Base Model (Accuracy) | Fine-Tuned Model (Accuracy) |")
    md_lines.append("|-------------|-----------------------|-----------------------------|")

    for i in range(total):
        b_item = base_data[i]
        f_item = finetuned_data[i]
        
        instr = b_item["instruction"].replace("\n", " ")
        b_valid = "✅ Valid" if b_item.get("is_valid_json", False) else "❌ Invalid"
        f_valid = "✅ Valid" if f_item.get("is_valid_json", False) else "❌ Invalid"
        
        # Clean up text for markdown table rendering
        b_text = b_item.get("base_generated_text", "").replace("\n", "<br>").replace("|", "\\|")
        f_text = f_item.get("finetuned_generated_text", "").replace("\n", "<br>").replace("|", "\\|")

        # Truncate to keep the table readable
        if len(b_text) > 150: b_text = b_text[:147] + "..."
        if len(f_text) > 150: f_text = f_text[:147] + "..."

        md_lines.append(f"| {instr} | {b_valid}<br><br>`{b_text}` | {f_valid}<br><br>`{f_text}` |")

    # Generate failure case deep dive
    md_lines.append("\n## Failure Analysis\n")
    if not eval_json["failure_cases"]:
        md_lines.append("No failure cases! The fine-tuned model achieved 100% strict JSON accuracy.")
    else:
        for fail in eval_json["failure_cases"]:
            md_lines.append(f"### Instruction: {fail['instruction']}")
            md_lines.append(f"**Issue**: {fail['error']}")
            md_lines.append("```json\n" + fail['generated_output'] + "\n```\n")

    with open(eval_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Evaluation Complete!")
    print(f"Metrics saved to -> {eval_json_path}")
    print(f"Markdown Logs saved to -> {eval_md_path}")
    print(f"Base Accuracy: {base_acc:.1f}% -> Fine-Tuned Accuracy: {finetuned_acc:.1f}%")

if __name__ == "__main__":
    run_evaluation()
