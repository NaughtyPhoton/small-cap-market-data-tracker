from register_apis import get_td_key
import requests


class TdApi:
    def __init__(self):
        self.td_key = get_td_key()

    def get_price_history(self, **kwargs):
        kwargs.update({'apikey':self.td_key})
        url = f'https://api.tdameritrade.com/v1/marketdata/{kwargs.get("symbol")}/pricehistory'
        return requests.get(url, params=kwargs).json()

    def get_quotes(self, **kwargs):
        kwargs.update({'apikey':self.td_key})
        url = f'https://api.tdameritrade.com/v1/marketdata/{kwargs.get("symbol")}/quotes'
        return requests.get(url, params=kwargs).json()
