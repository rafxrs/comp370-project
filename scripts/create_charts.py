import pandas as pd
import matplotlib.pyplot as plt
import argparse
import re
from pathlib import Path

def normalize_dashes(text):
    if pd.isna(text):
        return text
    return re.sub(r"[–—−-]", "-", str(text))

def normalize_coding(text):
    if pd.isna(text):
        return text
    text = normalize_dashes(text)
    # collapse whitespace and trim
    text = re.sub(r"\s+", " ", text.strip())
    # canonicalize US-Israel label (case-insensitive)
    if text.lower() == "us-israel diplomatic relations":
        return "US-Israel diplomatic relations"
    return text

def load_data(file_path, sep=","):
    df = pd.read_csv(file_path, sep=sep)

    required = {"Coding", "Sentiment", "Source"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")

    df["Coding"] = df["Coding"].apply(normalize_coding)
    return df

def plot_bar(counts, title, output_dir=None, filename=None, horizontal=False):
    plt.figure(figsize=(10, 6))

    if horizontal:
        counts_sorted = counts.sort_values()
        counts_sorted.plot(kind="barh")
    else:
        counts_sorted = counts.sort_values(ascending=False)
        counts_sorted.plot(kind="bar")

    plt.title(title)
    plt.xlabel("Category")
    plt.ylabel("Count")

    total = counts.sum()

    if horizontal:
        for i, v in enumerate(counts_sorted):
            pct = f"{(v/total)*100:.1f}%"
            plt.text(v * 1.01, i, pct, va="center")
        plt.margins(x=0.2)
    else:
        for i, v in enumerate(counts_sorted):
            pct = f"{(v/total)*100:.1f}%"
            plt.text(i, v * 1.01, pct, ha="center")
        plt.xticks(rotation=30, ha="right")

    plt.margins(y=0.1)
    plt.tight_layout()

    if output_dir and filename:
        path = Path(output_dir) / filename
        plt.savefig(path, dpi=300)
        print(f"Saved: {path}")
        plt.close()
    else:
        plt.show()

def sentiment_bar(df, out):
    counts = df["Sentiment"].value_counts()
    plot_bar(counts, "Sentiment Distribution", out, "sentiment_distribution.png")

def coding_bar(df, out):
    counts = df["Coding"].value_counts()
    plot_bar(counts, "Coding Distribution", out, "coding_distribution.png", horizontal=True)

def providers_distribution_bar(df, out):
    counts = df["Source"].value_counts()
    plot_bar(counts, "News Provider Distribution", out, "providers_distribution.png")

def provider_sentiment_bar(df, sentiment, out):
    subset = df[df["Sentiment"].str.lower() == sentiment.lower()]
    if subset.empty:
        print(f"No rows with sentiment '{sentiment}'")
        return

    counts = subset["Source"].value_counts()
    filename = f"providers_{sentiment.lower()}.png"
    title = f"News Providers for Sentiment = {sentiment.capitalize()}"
    plot_bar(counts, title, out, filename)

def main():
    parser = argparse.ArgumentParser(description="Generate bar charts for sentiment & coding.")
    parser.add_argument("-i", "--input", required=True, help="Path to dataset file (CSV/TSV).")
    parser.add_argument("-s", "--sep", default=",", help="Field separator (default ',').")
    parser.add_argument("-o", "--output", help="Directory to save charts (optional).")

    args = parser.parse_args()

    df = load_data(args.input, sep=args.sep)

    out_dir = None
    if args.output:
        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)

    sentiment_bar(df, out_dir)
    coding_bar(df, out_dir)
    providers_distribution_bar(df, out_dir)   # ← NEW CHART
    provider_sentiment_bar(df, "Negative", out_dir)
    provider_sentiment_bar(df, "Positive", out_dir)
    provider_sentiment_bar(df, "Neutral", out_dir)

if __name__ == "__main__":
    main()
