import requests

class GDELTClient:
    def __init__(self):
        self.base_url = "https://api.gdeltproject.org/api/v2/doc/doc"

    def fetch(self, params):
        response = requests.get(self.base_url, params=params)

        # print("REQUEST URL:", response.url) 

        try:
            return response.json()
        except Exception as e:
            print("RAW RESPONSE FROM GDELT:")
            print(response.text[:500])   # print first 500 chars
            raise RuntimeError(f"GDELT fetch error: {e}")
