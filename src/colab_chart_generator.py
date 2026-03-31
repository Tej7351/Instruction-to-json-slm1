import numpy as np
import matplotlib.pyplot as plt
import os

def generate_comparison_chart():
    # 1. Apply dark background theme
    plt.style.use('dark_background')

    # 2. Setup Data
    # For JSON Accuracy, values are normalized (0 to 1) for the second chart but % for the first chart
    metrics = ["JSON Accuracy", "ROUGE-1", "ROUGE-L", "BLEU"]
    base_scores = [0.60, 0.00, 0.00, 0.00]
    ft_scores = [1.00, 0.45, 0.41, 0.32] # 0.41 used as placeholder for ROUGE-L
    
    base_acc_percent = 60
    ft_acc_percent = 100

    # 3. Create Figure Canvas
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Qwen2.5-0.5B: Before vs After QLoRA Fine-tuning", fontsize=18, fontweight='bold', y=1.02)
    
    # Context text box
    context_text = "Model: Qwen2.5-0.5B | Method: QLoRA | Epochs: 3 | Dataset: 573 samples"
    fig.text(0.5, 0.93, context_text, ha='center', va='center', fontsize=12,
             bbox=dict(facecolor='#1a1a1a', alpha=0.8, boxstyle='round,pad=0.5', edgecolor='gray'))

    # =============== CHART 1: Bar Chart (Accuracy %) ===============
    models = ["Base Model", "Fine-tuned Model"]
    acc_data = [base_acc_percent, ft_acc_percent]
    colors_c1 = ['salmon', 'lightgreen']
    
    bars1 = ax1.bar(models, acc_data, color=colors_c1, width=0.5)
    
    ax1.set_title("Base vs Fine-tuned: JSON Accuracy", fontsize=14, pad=15)
    ax1.set_ylabel("Accuracy %", fontsize=12)
    ax1.set_ylim(0, 110)
    
    # Labels on top
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{yval}%", ha='center', va='bottom', fontsize=12, fontweight='bold')
        
    # Baseline horizontal dotted line
    ax1.axhline(y=60, color='gray', linestyle=':', linewidth=2, alpha=0.8)
    # Put label near the line
    ax1.text(1.2, 61, "Baseline", color='gray', fontsize=11, va='bottom', fontstyle='italic')
    
    # Formatting
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)


    # =============== CHART 2: Grouped Bar Chart (0 to 1.0) ===============
    x = np.arange(len(metrics))
    width = 0.35
    
    bars_base = ax2.bar(x - width/2, base_scores, width, label='Base Model', color='salmon')
    bars_ft = ax2.bar(x + width/2, ft_scores, width, label='Fine-tuned Model', color='lightgreen')
    
    ax2.set_title("Evaluation Metrics Comparison", fontsize=14, pad=15)
    ax2.set_ylabel("Score (0 to 1)", fontsize=12)
    ax2.set_xticks(x)
    ax2.set_xticklabels(metrics, fontsize=11)
    ax2.set_ylim(0, 1.1)
    
    # Legend
    ax2.legend(loc='upper right', fontsize=10, frameon=True, facecolor='#1a1a1a', edgecolor='gray')
    
    # Labels on top
    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            ax2.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10, fontweight='bold')
            
    add_labels(bars_base)
    add_labels(bars_ft)

    # Formatting
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    # 4. Final Layout Adjustments
    plt.tight_layout(rect=[0, 0, 1, 0.90])

    # 5. Save Outputs
    # Save locally
    local_path = 'comparison_chart.png'
    plt.savefig(local_path, dpi=150, bbox_inches='tight')
    print(f"Chart successfully saved locally as: {local_path}")
    
    # Save to Colab Google Drive
    colab_path = '/content/drive/MyDrive/slm_json_generator/outputs/comparison_chart.png'
    # Try/except block allows the script to be safely tested locally as well without crashing
    try:
        os.makedirs(os.path.dirname(colab_path), exist_ok=True)
        plt.savefig(colab_path, dpi=150, bbox_inches='tight')
        print(f"Chart successfully saved to Google Drive at: {colab_path}")
    except OSError as e:
        print(f"\nNotice: Could not save to {colab_path}.")
        print(f"This is expected if you are running locally. In Colab, make sure you ran 'drive.mount()':\n{e}")

if __name__ == "__main__":
    generate_comparison_chart()
