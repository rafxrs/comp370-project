# src/writer.py

import csv

def write_tsv(path, rows):
    """Save article dicts to TSV."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["id", "source", "headline", "opening", "published_at", "coding"])

        for r in rows:
            writer.writerow([
                r.get("id", ""),
                r.get("source", ""),
                r.get("headline", ""),
                r.get("opening", ""),
                r.get("published_at", ""),
                r.get("coding", "")
            ])
