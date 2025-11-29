# COMP370 Final Project — Media Coverage Analysis Pipeline

## Overview

A complete, modular Python pipeline for analyzing North American media coverage of political figures (default: Benjamin Netanyahu). The toolkit supports:

- Fetching news articles from TheNewsAPI
- Cleaning and preprocessing text
- TSV formatting for qualitative coding
- Merging multiple datasets
- Topic characterization using global unigram TF‑IDF
- Sentiment annotation workflows
- Easily switch to a different politician by changing input flags

## Setup

```
git clone https://github.com/rafxrs/comp370-project
mkdir -p data/raw data/processed data/tfidf
pip install -r requirements.txt

export NEWS_API_KEY="your_api_key"
# PowerShell:
# $env:NEWS_API_KEY="your_api_key"
```

## FULL WORKFLOW

### 1. Fetch Articles

Fetch articles mentioning a politician across selected news sources:

```
python -m scripts.fetch_news_api_articles     -f Netanyahu     -s nbcnews.com abcnews.go.com cbsnews.com cbc.ca     -d 2024     -t 150     -o data/raw/netanyahu_raw.tsv
```

**Date filtering (`-d`)** accepts formats:

- `2024` → 2024‑01‑01 → now  
- `2024-07` → 2024‑07‑01 → now  
- `2024-07-15` → exact day → now  

### 2. Process into Standardized TSV for Coding

Adds numbering, normalizes timestamps, cleaning, and inserts coding columns:

```
python -m scripts.process_tsv     -i data/raw/netanyahu_raw.tsv     -o data/processed/netanyahu_processed.tsv
```
This will create 'open_coding', 'coding' and 'sentiment' columns for you to annotate.

### 3. Merge Multiple Files (optional)

```
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

```
python scripts/tf_idf.py     -i data/processed/netanyahu_annotated.xlsx     -n 10     -o data/tfidf
```

Produces:

- `data/tfidf/summary.csv` — condensed table of top N terms per coding category  
- `data/tfidf/tfidf_<category>.png` — bar charts for each coding typology  

## Notes

- Supports easily swapping target politician (simply change `-f` keyword and your coding scheme)
- Stopword list may be extended using `config/stopwords.yaml`
- High API usage may exceed free-tier quota

## License

For academic use (COMP370 coursework)