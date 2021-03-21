import pandas
import requests
from pandas import DataFrame

from td_api import TdApi


def get_all_tickers() -> dict:
    url = 'https://api.nasdaq.com/api/screener/stocks?&download=true'
    headers = {
        "Accept-Language":"en-US,en;q=0.9",
        "Accept-Encoding":"gzip, deflate, br",
        "User-Agent":"Java-http-client"
    }
    return requests.get(url, timeout=5, headers=headers).json()


def filter_market_cap(row, max_market_cap) -> bool:
    try:
        num = float(row)
        return num > 0 and num < max_market_cap
    except ValueError:
        return False


def filter_market_volume(row, min_volume) -> bool:
    try:
        num = float(row)
        return num > min_volume
    except ValueError:
        return False


def get_small_cap_tickers(
        min_price: int = 1,
        max_price: int = 20,
        max_market_cap: int = 150_000_000,
        min_volume: int = 5_000_000,
) -> DataFrame:

    all_tickers = get_all_tickers()

    df = pandas.DataFrame(all_tickers['data']['rows'])

    price_filter = (df['lastsale'].apply(lambda row:float(row[1:])) < max_price) & (
            df['lastsale'].apply(lambda row:float(row[1:])) > min_price)

    name_filter = (df['symbol'].str.len() < 5)

    market_cap_filter = (df['marketCap'].apply(lambda row:filter_market_cap(row, max_market_cap)))

    volume_filter = (df['volume'].apply(lambda row:filter_market_volume(row, min_volume)))

    df = df[price_filter & name_filter & market_cap_filter & volume_filter]

    df = df.convert_dtypes()

    return df
