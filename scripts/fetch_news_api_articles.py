#!/usr/bin/env python3
import sys
from pathlib import Path
# add project root to sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

import argparse
from src.utils.news_api_fetcher import ArticleFetcher
from src.utils.writer import write_tsv

def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch articles about a political figure from selected news sources."
    )

    parser.add_argument("--search", "-f", required=True,
                        help="Search term (e.g., 'Netanyahu')")
    parser.add_argument("--sources", "-s", required=True, nargs="+",
                        help="List of source domains (e.g., nbcnews.com abcnews.go.com)")
    parser.add_argument("--target", "-t", type=int, default=167,
                        help="Number of articles to collect")
    parser.add_argument("--date", "-d", required=False,
                        help="Start date (YYYY | YYYY-MM | YYYY-MM-DD). Results from that day forward.")
    parser.add_argument("--output", "-o", required=True,
                        help="Path to output TSV file")

    return parser.parse_args()

def main():
    args = parse_args()

    fetcher = ArticleFetcher(
        search_term=args.search,
        sources=args.sources,
        target_count=args.target,
        start_date=args.date
    )

    articles = fetcher.fetch_articles()

    write_tsv(args.output, articles)

    print(f"\nSaved {len(articles)} articles → {args.output}")

if __name__ == "__main__":
    main()
