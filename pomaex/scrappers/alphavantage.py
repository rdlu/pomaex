import os
import requests
from requests.exceptions import HTTPError
import urllib.parse

class AlphaVantage(object):
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    endpoint = "https://www.alphavantage.co/query?"

    def __init__(self, api_key: str = api_key):
        self.api_key = api_key

    def fetch_data(self, params: dict) -> dict:
        response = None

        url_params = urllib.parse.urlencode(params)
        link = self.endpoint + url_params
        try:
            response = requests.get(link)
            response.raise_for_status()
            response = response.json()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        return response

    def _clean_av_header(self, title: str) -> str:
        return title[3:].lower().replace(' ', '_')

    def _clean_all_av_headers(self, metadata: dict) -> dict:
        return { self._clean_av_header(key): value for key, value in metadata.items() }