from typing import Any, Dict, List
import requests
from requests.exceptions import RequestException
from ytid.youtubevideo import YoutubeVideo

class YouTube_ETL:
    """YouTube Data API.

    Attributes:
        url (str): url for youtube API.
        api_key (str): API key.
    """
    url: str
    api_key: str
    def __init__(self, api_key, url):
        self.api_key = api_key
        self.url = url

    def _get(self, payload: Dict[str, Any]):
        try:
            res = requests.get(self.url, params=payload)
            res.raise_for_status()
        except RequestException:
            print(f"Error while retrieving based on payload: {format(payload)}")
        else:
            return res.json()

    def get_trendings(self, region_code: str = "ID",
                      result_per_page: int = 20) -> List[YoutubeVideo]:
        payload = {
            "key": self.api_key,
            "chart": "mostPopular",
            "part": "snippet,contentDetails,statistics",
            "regionCode": region_code,
            "maxResults": result_per_page,
        }

        response = self._get(payload)
        youtubevideos = response.get("items")
        
        youtubevideos = [
            YoutubeVideo(
                id=youtubevideo.get("id"),
                snippet=youtubevideo.get("snippet"),
                content_detail=youtubevideo.get("contentDetails"),
                statistic=youtubevideo.get("statistics")
            )
            for youtubevideo in youtubevideos
        ]

        return youtubevideos