# test/test_pipeline.py
import pandas as pd
from pathlib import Path
from src.utils.news_api_fetcher import ArticleFetcher
from src.utils.writer import write_tsv
from scripts.process_tsv import process_tsv
from scripts.tf_idf import run_tfidf

def test_pipeline(tmp_output):
    # 1. Real fetch
    fetcher = ArticleFetcher(
        search_term="Netanyahu",
        sources=["globalnews.ca", "cbc.ca"],
        target_count=5,
        start_date="2024"
    )
    articles = fetcher.fetch_articles()
    assert len(articles) > 0

    # 2. Save to TSV
    raw_file = tmp_output / "raw.tsv"
    write_tsv(raw_file, articles)
    assert raw_file.exists()

    # 3. Process TSV (adds open coding + coding + sentiment placeholders)
    processed_file = tmp_output / "processed.tsv"
    process_tsv(str(raw_file), str(processed_file))
    assert processed_file.exists()

    df = pd.read_csv(processed_file, sep="\t")
    assert "open_coding" in df.columns
    assert "coding" in df.columns
    assert "sentiment" in df.columns

    # 4. Run TF-IDF
    out_dir = tmp_output / "tfidf"
    run_tfidf(processed_file, top_n=5, output_dir=out_dir)

    # Summary table exists
    summary_file = out_dir / "summary.csv"
    assert summary_file.exists()

    # At least one plot
    images = list(out_dir.glob("*.png"))
    assert len(images) > 0
