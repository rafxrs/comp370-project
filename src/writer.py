# src/writer.py

import csv

def write_tsv(path, rows):
    """Save article dicts to TSV."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["id", "source", "headline", "opening", "coding"])

        for r in rows:
            writer.writerow([r["id"], r["source"], r["headline"], r["opening"], r["coding"]])
