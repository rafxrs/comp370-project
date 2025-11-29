import csv

def write_tsv(path, rows):
    clean = lambda x: (x or "").replace("\t", " ").replace("\n", " ").replace("\r", " ")

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")

        writer.writerow([
            "ID", "Source", "Date", "Title", "Opening",
            "Open coding", "Coding", "Sentiment"
        ])

        for i, r in enumerate(rows, start=1):
            writer.writerow([
                i,
                clean(r.get("source")),
                clean(r.get("date")),
                clean(r.get("title")),
                clean(r.get("opening")),
                clean(r.get("open_coding")),
                clean(r.get("coding")),
                clean(r.get("sentiment")),
            ])

