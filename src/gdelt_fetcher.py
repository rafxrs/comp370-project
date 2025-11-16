import datetime
from dateutil.relativedelta import relativedelta
from tqdm import tqdm
from src.gdelt_client import GDELTClient

class GDELTArticleFetcher:
    def __init__(self, search_term, sources, target, start_year=2024):
        self.client = GDELTClient()
        self.search_term = search_term
        self.allowed_sources = {s.lower() for s in sources}
        self.target = target
        self.start_year = start_year

    def fetch_articles(self):
        print("Querying GDELT month-by-month...")

        accepted = {}
        now = datetime.datetime.now(datetime.timezone.utc)
        cursor = datetime.datetime(self.start_year, 1, 1, tzinfo=datetime.timezone.utc)

        # --- build list of month slices first ---
        months = []
        tmp = cursor
        while tmp < now:
            months.append(tmp)
            tmp += relativedelta(months=1)

        # --- outer progress bar: month by month ---
        with tqdm(total=len(months), desc="Months fetched", ncols=90) as pbar_months:
            for cursor in months:
                if len(accepted) >= self.target:
                    break

                next_cursor = cursor + relativedelta(months=1)
                start = cursor.strftime("%Y%m%d%H%M%S")
                end   = next_cursor.strftime("%Y%m%d%H%M%S")

                params = {
                    "query": self.search_term,
                    "format": "json",
                    "maxrecords": 250,  # GDELT hard limit
                    "startdatetime": start,
                    "enddatetime": end
                }

                # fetch this month's data
                data = self.client.fetch(params)
                articles = data.get("articles", [])

                # --- inner progress bar: articles inside this month ---
                for a in tqdm(articles,
                              desc=f"{cursor.strftime('%Y-%m')}",
                              leave=False,
                              ncols=90):

                    source = (a.get("domain") or "").lower()

                    if not any(src in source for src in self.allowed_sources):
                        continue

                    url = a.get("url")
                    if url not in accepted:
                        accepted[url] = {
                            "id": url,
                            "source": source,
                            "headline": a.get("title") or "",
                            "opening": a.get("seendesc") or "",
                            "coding": ""
                        }

                    if len(accepted) >= self.target:
                        break

                pbar_months.update(1)

        return list(accepted.values())
