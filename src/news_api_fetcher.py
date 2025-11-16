# src/news_api_fetcher.py

import time
from src.news_api_client import NewsAPIClient
from src.config import DEFAULT_LANG, DEFAULT_LIMIT
from src.cleaning import clean_text

class ArticleFetcher:
    def __init__(self, search_term, sources, target_count, lang=DEFAULT_LANG):
        self.client = NewsAPIClient()
        self.search_term = search_term
        self.lang = lang
        self.limit = DEFAULT_LIMIT
        self.target_count = target_count
        
        # Normalize user-supplied allowed sources (important!)
        normalized = {
            "abcnews.go.com": "abcnews.com"
        }

        cleaned = set()
        for s in sources:
            s = s.lower()
            if s in normalized:
                s = normalized[s]
            cleaned.add(s)

        self.sources_requested = cleaned

    def _source_matches(self, source: str) -> bool:
        """Return True if article source matches one of the allowed domains."""
        if not source:
            return False

        src = source.lower()

        # Normalize special incoming cases
        if src == "abcnews.go.com":
            src = "abcnews.com"

        # Match by substring
        return any(allowed in src for allowed in self.sources_requested)


    def fetch_articles(self):
        params = {
            "search": self.search_term,
            "language": self.lang,
            "limit": self.limit,
        }

        page = 1
        collected = []

        while len(collected) < self.target_count:
            print(f"Fetching page {page}... (current accepted: {len(collected)})")

            params["page"] = page
            data = self.client.fetch(params)

            articles = data.get("data", [])
            if not articles:
                print("No more articles returned by API.")
                break

            for a in articles:
                src = (a.get("source") or "").lower()

                # client-side filtering by source
                if not self._source_matches(src):
                    continue

                headline = clean_text(a.get("title") or "")
                opening  = clean_text(a.get("snippet") or "")

                collected.append({
                    "id": a.get("uuid"),
                    "source": src,
                    "headline": headline,
                    "opening": opening,
                    "coding": ""
                })

                if len(collected) >= self.target_count:
                    break

            page += 1
            time.sleep(0.4)

        return collected
