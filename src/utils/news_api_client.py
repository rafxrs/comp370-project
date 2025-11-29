# src/news_api_client.py

import requests
from config.config import API_KEY, BASE_URL

class NewsAPIClient:
    """Lightweight wrapper for TheNewsAPI."""
    def __init__(self):
        self.base_url = BASE_URL
        self.token = API_KEY

    def fetch(self, params):
        params["api_token"] = self.token
        response = requests.get(self.base_url, params=params)

        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text}")

        return response.json()
