from datetime import date

import requests
import pandas
from io import StringIO


def get_ssr_list():
    headers = {
        "Accept-Language":"en-US,en;q=0.9",
        "Accept-Encoding":"gzip, deflate, br",
        "User-Agent":"Java-http-client"
    }
    date_formatted = date.today().strftime('%Y%m%d')
    ssr_url = f'https://www.nasdaqtrader.com/dynamic/symdir/shorthalts/shorthalts{date_formatted}.txt'

    ssr_string = requests.get(ssr_url, timeout=5, headers=headers).text

    ssr_df = pandas.read_csv(StringIO(ssr_string), sep=",")

    ssr_df = ssr_df.drop(columns=['Security Name', 'Market Category'])

    ssr_df.columns = ['symbol', 'ssr trigger time']

    return ssr_df
