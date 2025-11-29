import matplotlib.pyplot as plt

def save_plot(top_df, coding_value, out_dir):
    plt.figure(figsize=(12, 6))
    plt.bar(top_df["term"], top_df["score"])
    plt.xticks(rotation=70, ha='right', fontsize=8)
    plt.ylabel("TF-IDF Score")
    plt.xlabel("Term")
    plt.title(f"Top TF-IDF Terms for Coding: {coding_value}")
    plt.tight_layout()

    out_path = out_dir / f"tfidf_{coding_value}.png"
    plt.savefig(out_path, dpi=300)
    plt.close()
