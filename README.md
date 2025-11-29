# COMP370 Final Project: Media Coverage Analysis Pipeline

## Overview

Analysis of North American media coverage of **Benjamin Netanyahu**. The pipeline collects articles, filters sources, cleans text, and prepares structured TSVs for qualitative coding, topic modeling, and sentiment analysis.

## Features

- Fetch articles via TheNewsAPI.com
- Source domain filtering (by date, news provider, keyword, etc)
- Clean text (remove boilerplate/login/video UI noise)
- Output TSV with `published_at` ISO timestamps
- Processing script to add numbering & coding columns
- Merge multiple TSVs

## Setup

```bash
git clone https://github.com/rafxrs/comp370-project
mkdir -p data/raw data/processed
pip install -r requirements.txt
export NEWS_API_KEY="your_api_key"  # or set in PowerShell: $env:NEWS_API_KEY="your_api_key"
```

## Fetch Articles

Basic example:

```bash
python -m scripts.fetch_news_api_articles -f Netanyahu -s nbcnews.com abcnews.go.com cbsnews.com cbc.ca -d 2024 -t 167 -o data/raw/netanyahu.tsv
```

### Date Start Filtering (-d / --date)

Limit results to articles published **from the specified start date up to the present** (no end date yet).

Accepted input formats (normalized to midnight UTC start):

| Input        | Normalized Start | Range Covered    |
| ------------ | ---------------- | ---------------- |
| `2024`       | `2024-01-01`     | 2024-01-01 → now |
| `2024-07`    | `2024-07-01`     | 2024-07-01 → now |
| `2024-07-15` | `2024-07-15`     | 2024-07-15 → now |

Examples:

```bash
# All of 2024
python -m scripts.fetch_news_api_articles -f Netanyahu -s nbcnews.com abcnews.go.com -d 2024 -t 120 -o data/raw/netanyahu_2024.tsv

# July 2024 onward
python -m scripts.fetch_news_api_articles -f Netanyahu -s nbcnews.com abcnews.go.com -d 2024-07 -t 80 -o data/raw/netanyahu_2024_07.tsv

# Specific date
python -m scripts.fetch_news_api_articles -f Netanyahu -s nbcnews.com abcnews.go.com -d 2024-07-15 -t 50 -o data/raw/netanyahu_2024_07_15.tsv
```

Implementation details:

- Internally sets `published_after=YYYY-MM-DDT00:00:00Z`.
- Invalid format raises a clear error.
- Omit `-d` to use provider default window.
- End-date filtering (e.g. `--until`) not implemented yet.

## Output Columns

`id`, `source`, `headline`, `opening`, `published_at`, `coding` (plus `open_coding` / numbering after processing).

## Process TSV (add numbering & coding placeholders)

```bash
python -m scripts.process_tsv -i data/raw/netanyahu.tsv -o data/processed/netanyahu_processed.tsv
```

## Merge Multiple TSVs

```bash
python -m scripts.merge_tsv -i "data/raw/*.tsv" -o data/processed/netanyahu_merged.tsv
```

## Cleaning Rules (see `src/cleaning.py`)

Removes login prompts, stray UI text, duration labels, boilerplate, excess whitespace.

## Environment Variables

`NEWS_API_KEY` – your API token (never commit the actual key; rotate if leaked).

## Coding / Analysis Next Steps

- Open coding & topic typology (3–8 topics)
- TF‑IDF and summary generation
- Sentiment annotation (pos/neg/neutral)

## Notes

- High targets may exhaust free tier quotas.
- Add an end-date flag in future if needed.

## License / Usage

Academic / course project. Verify terms of TheNewsAPI for data usage.

