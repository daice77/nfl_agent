import requests

class WebSearch:
    def __init__(self, api_key):
        self.api_key = api_key
        self.search_url = 'https://api.perplexity.ai/search'

    def search(self, query):
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        params = {
            'q': query
        }
        response = requests.get(self.search_url, headers=headers, params=params)
        if response.status_code == 200:
            results = response.json()
            return results.get('results', [])
        else:
            return f"Error fetching search results: {response.status_code}"