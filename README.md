# COMP370 Final Project: Media Coverage Analysis Pipeline

## Overview

This project analyzes North American media coverage of a selected political figure.
Our team selected **Benjamin Netanyahu**.

The pipeline provides:

- Automated article collection from TheNewsAPI
- Source filtering for 12 pre‑chosen outlets
- TSV dataset export
- Text cleaning (removal of boilerplate, login prompts, video UI text)
- Preparation for open coding, topic modeling, and sentiment annotation
- Modular, argparse‑driven scripts
- Reusable `src/` modules for API requests, filtering, and cleaning

## How to Fetch Articles

0. Install dependencies and get API key [https://thenewsapi.com/](https://thenewsapi.com/):

   ```bash
   pip install -r requirements.txt
   ```

1. Export your API key:

   ```bash
   export NEWS_API_KEY="your_api_key"
   ```

   **WARNING**: Running the fetcher with 167 articles may consume your free tier quota.

2. Run the fetcher:

   ```bash
   python -m scripts.fetch_news_api_articles -f Netanyahu -s nbcnews.com abcnews.go.com cbsnews.com cbc.ca -t 167 -o data/raw/netanyahu.tsv
   ```

3. The fetcher will:

   - Iterate through pages
   - Filter by source domain
   - Clean text (whitespace, boilerplate)
   - Stop when target number of articles is reached

4. After the fetch, prepare the data for coding:

   ```bash
   python -m scripts.process_tsv -i data/raw/netanyahu.tsv -o data/processed/netanyahu_processed.tsv
   ```

## Environment Variables

- `NEWS_API_KEY` — required for API access

## Cleaning Rules

`src/cleaning.py` removes:

- NBC login prompts
- “Copied”
- CBC “Duration 2:01”
- embedded newlines
- excessive whitespace

## Coding Workflow (Next Steps)

- Open code articles
- Define a typology of 3–8 topics
- Annotate remaining articles
- Compute TF‑IDF top words per topic
- Generate LLM summaries (ChatGPT)
- Apply sentiment labels (pos/neg/neutral)
