# COMP370 Final Project — Media Coverage Analysis Pipeline

## Overview

A complete, modular Python pipeline for analyzing North American media coverage of political figures (default: Benjamin Netanyahu). The toolkit supports:

- Fetching news articles from TheNewsAPI
- Cleaning and preprocessing text
- TSV formatting for qualitative coding
- Merging multiple datasets
- Topic characterization using global unigram TF-IDF
- Sentiment annotation workflows
- Easily switch to a different politician by changing input flags

## Setup

Linux / macOS

```bash
git clone https://github.com/rafxrs/comp370-project
cd comp370-project

mkdir -p data/raw data/processed data/tfidf
pip install -r requirements.txt

export NEWS_API_KEY="your_api_key"

pytest -v
```

Windows Powershell

```bash
git clone https://github.com/rafxrs/comp370-project
cd comp370-project

mkdir data\raw
mkdir data\processed
mkdir data\tfidf

pip install -r requirements.txt

$env:NEWS_API_KEY="your_api_key"

pytest -v
```

## Project Structure

project/  
│  
├── config/ (API keys, stopwords, configuration)  
├── data/  
│ ├── raw/ (Raw TSVs pulled from API)  
│ ├── processed/ (Cleaned TSVs: ready for coding and coded analysis)  
│  
├── results/  
│ ├── charts/ (All generated charts)  
│ ├── percentages/ (Text summaries via awk scripts)  
│ └── tfidf/ (TF-IDF plots and summary table)  
│  
├── scripts/  
│ ├── fetch_news_api_articles.py  
│ ├── process_tsv.py  
│ ├── merge_tsv.py  
│ ├── tf_idf.py  
│ └── create_charts.py  
│  
├── src/  
│ ├── tfidf/  
│ └── utils/  
│  
└── test/

## FULL WORKFLOW

### 1. Fetch Articles

Fetch articles mentioning a politician across selected news sources:

```bash
python -m scripts.fetch_news_api_articles     -f Netanyahu     -s nbcnews.com abcnews.go.com cbsnews.com cbc.ca     -d 2024     -t 150     -o data/raw/netanyahu_raw.tsv
```

**Date filtering (`-d`)** accepts formats:

- `2024` → 2024‑01‑01 → now
- `2024-07` → 2024‑07‑01 → now
- `2024-07-15` → exact day → now

### 2. Process into Standardized TSV for Coding

Adds numbering, normalizes timestamps, cleaning, and inserts coding columns:

```bash
python -m scripts.process_tsv     -i data/raw/netanyahu_raw.tsv     -o data/processed/netanyahu_processed.tsv
```

This will create 'open_coding', 'coding' and 'sentiment' columns for you to annotate.

### 3. Merge Multiple Files (optional)

```bash
python -m scripts.merge_tsv     -i "data/raw/*.tsv"     -o data/processed/netanyahu_merged.tsv
```

### 4. Manual Coding & Sentiment Work

The cleaned TSV contains:

- `open_coding` → notes from qualitative coding
- `coding` → your assigned typology category. See our 'coding_typology' document for Benjamin Netanyahu.
- `sentiment` → pos / neg / neutral. See our 'sentiment_typology' document

This file is what you annotate manually before running the TF‑IDF.

### 5. Run TF‑IDF Topic Characterization

Uses **global unigram TF‑IDF** and averages scores per coding category.

```bash
python -m scripts.tf_idf     -i data/processed/netanyahu_annotated.xlsx     -n 10     -o data/tfidf
```

Produces:

- `data/tfidf/summary.csv` — condensed table of top N terms per coding category
- `data/tfidf/tfidf_<category>.png` — bar charts for each coding typology

### 6. Chart Generation

To generate result charts:

```bash
python -m scripts.create_charts \
 -i data/processed/netanyahu_500_annotated.tsv \
 -s "\t" \
 -o results/charts
```

This produces:

- sentiment_distribution.png
- coding_distribution.png
- providers_distribution.png
- providers_positive.png
- providers_negative.png
- providers_neutral.png

The script automatically:

- normalizes category names
- sorts bars
- annotates percentages
- saves outputs to results/charts/

## Notes

- You can easily swap the target politician by changing the -f argument
- Custom stopwords can be added/removed in config/stopwords.yaml for tf-idf
- API usage may exceed free-tier quotas if fetching large numbers of articles with restrictive date ranges or news sources

## License

For academic use (COMP370 coursework)


