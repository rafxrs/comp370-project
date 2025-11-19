# scripts/merge_tsv.py

import argparse
import csv
import glob

def parse_args():
    parser = argparse.ArgumentParser(description="Merge multiple TSV article files.")
    parser.add_argument("--input_glob", "-i", required=True,
                        help="Glob pattern for TSV files (e.g. 'data/raw/*.tsv')")
    parser.add_argument("--output", "-o", required=True,
                        help="Path to merged TSV output")
    return parser.parse_args()

def main():
    args = parse_args()

    files = glob.glob(args.input_glob)
    print(f"Found {len(files)} TSV files")

    combined = []
    for f in files:
        with open(f, encoding="utf-8") as infile:
            reader = csv.DictReader(infile, delimiter="\t")
            combined.extend(reader)

    with open(args.output, "w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(
            out,
            fieldnames=["id", "source", "headline", "opening", "published_at", "coding"],
            delimiter="\t"
        )
        writer.writeheader()
        writer.writerows(combined)

    print(f"Merged {len(files)} files → {args.output}")

if __name__ == "__main__":
    main()
