# scripts/fetch_gdelt_articles.py

import argparse
from src.gdelt_fetcher import GDELTArticleFetcher
from src.writer import write_tsv

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch articles (2024-present) using GDELT")
    parser.add_argument("--search", "-f", required=True, help="Search term (e.g. 'Netanyahu')")
    parser.add_argument("--sources", "-s", required=True, nargs="+", help="Allowed source domains")
    parser.add_argument("--target", "-t", type=int, required=True, help="Number of articles to collect")
    parser.add_argument("--output", "-o", required=True, help="Output TSV path")
    parser.add_argument("--start_year", "-y", type=int, default=2024, help="Start year (default 2024)")
    return parser.parse_args()

def main():
    args = parse_args()
    fetcher = GDELTArticleFetcher(
        search_term=args.search,
        sources=args.sources,
        target=args.target,
        start_year=args.start_year
    )

    articles = fetcher.fetch_articles()
    write_tsv(args.output, articles)

    print(f"Saved {len(articles)} articles → {args.output}")

if __name__ == "__main__":
    main()
