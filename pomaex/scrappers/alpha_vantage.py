import os
import requests
from requests.exceptions import HTTPError
import urllib.parse


class AlphaVantage(object):
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    endpoint = "https://www.alphavantage.co/query?"
    default_symbol = 'MSFT'
    default_format = 'json'

    def __init__(self, api_key: str = api_key):
        self.api_key = api_key

    def symbol_search(self, keyword: str = default_symbol) -> dict:
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': keyword,
            'apikey': self.api_key,
            'datatype': 'json'
        }
        return self._fetch_data(params)

    def timeseries(self, symbol: str = default_symbol, period: str = 'daily',
                   interval: str = '5min', outputsize: str = 'compact') -> (dict, dict):

        params = {
            'apikey': self.api_key,
            'symbol': symbol,
            'function': 'TIME_SERIES_{}'.format(period.upper()),
            'outputsize': outputsize,
            'datatype': 'json'
        }

        if period == 'intraday':
            params['interval'] = interval

        metadata, data = self._fetch_data(params)
        metadata = self._clean_metadata_headers(metadata)
        data = self._clean_data_headers(data)
        return (data, metadata)

    def daily(self, symbol: str = default_symbol,
              outputsize: str = 'compact') -> (dict, dict):
        return self.timeseries(symbol, period='daily', outputsize=outputsize)

    def daily_adjusted(self, symbol: str = default_symbol,
                       outputsize: str = 'compact') -> (dict, dict):
        return self.timeseries(symbol, period='daily_adjusted', outputsize=outputsize)

    def weekly(self, symbol: str = default_symbol,
               outputsize: str = 'compact') -> (dict, dict):
        return self.timeseries(symbol, period='weekly', outputsize=outputsize)

    def weekly_adjusted(self, symbol: str = default_symbol,
                        outputsize: str = 'compact') -> (dict, dict):
        return self.timeseries(symbol, period='weekly_adjusted', outputsize=outputsize)

    def intraday(self, symbol: str = default_symbol,
                 interval: str = '5min', outputsize: str = 'compact') -> (dict, dict):
        return self.timeseries(symbol, period='intraday', interval=interval, outputsize=outputsize)

    def _fetch_data(self, params: dict) -> dict:
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

    def _clean_metadata_headers(self, metadata: dict) -> dict:
        return {self._clean_header(key): value for key, value in metadata.items()}

    def _clean_data_headers(self, data: dict) -> dict:
        return {datapoint: self._clean_datapoint(values) for datapoint, values in data.items()}

    def _clean_datapoint(self, data: dict) -> dict:
        return self._clean_metadata_headers(data)

    def _clean_header(self, title: str) -> str:
        return title[3:].lower().replace(' ', '_')
