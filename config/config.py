import os

API_KEY = os.getenv("NEWS_API_KEY")

if not API_KEY:
    raise RuntimeError("Missing NEWS_API_KEY environment variable!")

BASE_URL = "https://api.thenewsapi.com/v1/news/all"

DEFAULT_SEARCH_TERM = "Netanyahu"
DEFAULT_LANG = "en"
DEFAULT_LIMIT = 50