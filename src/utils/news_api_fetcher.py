# src/news_api_fetcher.py

import time
import re
from datetime import datetime
from src.utils.news_api_client import NewsAPIClient
from config.config import DEFAULT_LANG, DEFAULT_LIMIT
from src.utils.cleaning import clean_text

class ArticleFetcher:
    def __init__(self, search_term, sources, target_count, lang=DEFAULT_LANG, start_date=None):
        self.client = NewsAPIClient()
        self.search_term = search_term
        self.lang = lang
        self.limit = DEFAULT_LIMIT
        self.target_count = target_count
        self.start_date = self._parse_start_date(start_date)  # normalized YYYY-MM-DD or None
        
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


    def _parse_start_date(self, raw):
        """Parse user-supplied start date.
        Accepts formats:
        - YYYY (becomes YYYY-01-01)
        - YYYY-MM (becomes YYYY-MM-01)
        - YYYY-MM-DD (validated)
        Returns normalized 'YYYY-MM-DD' or None if raw is falsy.
        Raises ValueError for invalid formats.
        """
        if not raw:
            return None
        raw = raw.strip()
        year_pat = r"^(\d{4})$"
        ym_pat = r"^(\d{4})-(\d{2})$"
        ymd_pat = r"^(\d{4})-(\d{2})-(\d{2})$"

        if re.match(year_pat, raw):
            return f"{raw}-01-01"
        m = re.match(ym_pat, raw)
        if m:
            return f"{m.group(1)}-{m.group(2)}-01"
        if re.match(ymd_pat, raw):
            # validate actual date (e.g., month/day ranges)
            try:
                datetime.strptime(raw, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid date: {raw}")
            return raw
        raise ValueError(f"Unsupported date format: '{raw}'. Use YYYY, YYYY-MM, or YYYY-MM-DD")

    def fetch_articles(self):
        params = {
            "search": self.search_term,
            "language": self.lang,
            "limit": self.limit,
        }

        start_dt = None
        if self.start_date:
            start_dt = datetime.strptime(self.start_date, "%Y-%m-%d")

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

                # Source filter
                if not self._source_matches(src):
                    continue

                # Date filter (client-side)
                if start_dt:
                    ts = a.get("published_at")
                    if ts:
                        try:
                            art_dt = datetime.strptime(ts[:10], "%Y-%m-%d")
                            if art_dt < start_dt:
                                continue
                        except:
                            pass  # If parsing fails, ignore filtering

                headline = clean_text(a.get("title") or "")
                opening  = clean_text(a.get("snippet") or "")

                # Format date: YYYY-MM-DD → MM-DD-YYYY
                raw_date = a.get("published_at") or ""
                date_val = ""
                if raw_date:
                    try:
                        dt = datetime.strptime(raw_date[:10], "%Y-%m-%d")
                        date_val = dt.strftime("%m-%d-%Y")
                    except:
                        date_val = raw_date[:10]

                collected.append({
                    "id": a.get("uuid"),
                    "source": src,
                    "date": date_val,
                    "title": headline,
                    "opening": opening
                })


                if len(collected) >= self.target_count:
                    break

            page += 1
            time.sleep(0.4)

        return collected

