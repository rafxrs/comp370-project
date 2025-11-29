#!/usr/bin/env python3
import sys
from pathlib import Path
# add project root to sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

import argparse
from src.utils.dataset import load_dataset
from src.tfidf.preprocessing import build_full_text, normalize_coding, load_stopwords
from src.tfidf.vectorizer import compute_global_tfidf
from src.tfidf.analysis import compute_category_tfidf
from src.tfidf.visualization import save_plot
from src.tfidf.summary import build_summary_table


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-n", "--top_n", type=int, default=10)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-s", "--stopwords", default="config/stopwords.yaml")
    return parser.parse_args()


def main():
    args = parse_args()
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = load_dataset(args.input)
    df = build_full_text(df)
    df = normalize_coding(df)

    stopwords = load_stopwords(args.stopwords)

    texts = df["full_text"].tolist()
    matrix, terms = compute_global_tfidf(texts, stopwords)

    category_results = compute_category_tfidf(df, matrix, terms)

    for coding, tfidf_df in category_results.items():
        top_df = tfidf_df.head(args.top_n)
        save_plot(top_df, coding, out_dir)

    summary_df = build_summary_table(category_results, args.top_n)
    summary_df.to_csv(out_dir / "summary.csv", index=True)


if __name__ == "__main__":
    main()
