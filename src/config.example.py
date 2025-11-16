# Example config without secrets. Copy to config.py or set env vars.

import os

API_KEY = os.getenv("NEWS_API_KEY", "your-api-key-here")
BASE_URL = "https://api.thenewsapi.com/v1/news/all"
DEFAULT_SEARCH_TERM = "Netanyahu"
DEFAULT_LANG = "en"
DEFAULT_LIMIT = 50   # API max
