#!/usr/bin/env python3
import argparse
import pandas as pd
import os


def add_numbering(input_path, output_path):
    # Load TSV
    df = pd.read_csv(input_path, sep="\t")

    # Add numbering column at the front
    df.insert(0, "n", range(1, len(df) + 1))

    # Add annotation columns if missing
    if "open_coding" not in df.columns:
        df["open_coding"] = ""
    if "coding" not in df.columns:
        df["coding"] = ""

    # Save TSV
    df.to_csv(output_path, sep="\t", index=False)
    print(f"Saved updated TSV to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Add numbering + open_coding + coding columns to a TSV dataset."
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Path to input TSV file"
    )
    parser.add_argument(
        "-o", "--output", required=False,
        help="Output TSV path (default: <input>_numbered.tsv)"
    )

    args = parser.parse_args()

    input_path = args.input

    # auto-generate output path if not specified
    if args.output:
        output_path = args.output
    else:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_numbered{ext}"

    add_numbering(input_path, output_path)


if __name__ == "__main__":
    main()
