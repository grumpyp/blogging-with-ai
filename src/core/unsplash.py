import requests
from utils.configparser import parse_config
from typing import Dict, Any


class Unsplash:
    def __init__(self, api_key: str | None = None):
        self.config = parse_config()
        self.api_key = api_key if api_key is not None else self.config['unsplash']['accesskey']

    # TODO: cache header
    def generate_header(self) -> Dict[str, str]:
        headers = {"Authorization": f"Client-ID {self.api_key}"}
        return headers

    def search_by_keyword(self, keyword: str) -> Dict[str, str] | None:
        url = f"https://api.unsplash.com/search/photos?query={keyword}&per_page=10"
        headers = self.generate_header()
        response = requests.get(url, headers=headers)
        print("Downloaded pictures from Unsplash")
        # use first photo of search response
        try:
            data = {'description': response.json()['results'][0]['description'],
                    'id': response.json()['results'][0]['id'],
                    'photo_url': response.json()['results'][0]['urls']['small']}
        except Exception as e:
            f"No photo found: {e}"
            return None
        return data

    def get_photo_by_id(self, photo_id: str) -> Any:
        url = f"https://api.unsplash.com/photos/{photo_id}/download"
        response = requests.get(url)
        return response["url"]
