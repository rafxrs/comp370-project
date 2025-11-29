#!/usr/bin/env python3
import argparse
import pandas as pd
import os

def process_tsv(input_path, output_path):
    df = pd.read_csv(input_path, sep="\t")

    # Normalize column names
    df.columns = [c.lower().strip() for c in df.columns]

    # Ensure required raw columns exist
    expected = {"id", "source", "date", "title", "opening"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in raw TSV: {missing}")

    # Add annotation columns
    if "open_coding" not in df.columns:
        df["open_coding"] = ""
    if "coding" not in df.columns:
        df["coding"] = ""
    if "sentiment" not in df.columns:
        df["sentiment"] = ""

    # Reorder columns EXACTLY as required
    final_columns = [
        "id",
        "source",
        "date",
        "title",
        "opening",
        "open_coding",
        "coding",
        "sentiment"
    ]

    df = df[final_columns]

    # Save TSV
    df.to_csv(output_path, sep="\t", index=False)
    print(f"Saved updated TSV to: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Add annotation columns (open coding, coding, sentiment) to raw TSV."
    )
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output")
    args = parser.parse_args()

    output_path = args.output
    if not output_path:
        base, ext = os.path.splitext(args.input)
        output_path = f"{base}_processed{ext}"

    process_tsv(args.input, output_path)

if __name__ == "__main__":
    main()
