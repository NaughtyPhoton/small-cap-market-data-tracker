import time
from datetime import date

import pandas
from gspread import Spreadsheet, Worksheet
from pandas import DataFrame

from get_small_cap_tickers import get_small_cap_tickers
from td_api import TdApi
from register_apis import get_gspread_sheet


def update_all_small_cap_sheet(sh: Spreadsheet):
    all_small_cap_df: DataFrame = get_small_cap_tickers(min_volume=1)
    all_small_cap_df = all_small_cap_df.drop(columns=['url'])
    all_small_cap_df['volume'] = pandas.to_numeric(all_small_cap_df['volume'])

    stocks_in_play_worksheet: Worksheet = sh.worksheet("All Small Cap Stocks")
    stocks_in_play_worksheet.clear()
    stocks_in_play_worksheet.update([all_small_cap_df.columns.values.tolist()] + all_small_cap_df.values.tolist())

    stocks_in_play_worksheet.format(
        "F2:F",
        {'numberFormat':{
            "pattern":"###,###",
            "type":"NUMBER"
        }}
    )

    print('c')


if __name__ == '__main__':
    tdApi = TdApi()
    today = date.today()

    spreadsheet: Spreadsheet = get_gspread_sheet()

    update_all_small_cap_sheet(spreadsheet)

    print('c')

    # for index, row in small_cap_df.iterrows():
    #     symbol = row['symbol']
    #     td = tdApi.get_price_history(**{
    #         'symbol':symbol,
    #         'period':2,
    #         'periodType':'day',
    #         'frequency':1,
    #     })
    #
    #     candles = td['candles']
    # epoch = candles[0]['datetime']
    # timestamp = time.gmtime(epoch / 1000)
    # formattedTime = time.strftime('%m/%d/%Y %H:%M:%S', timestamp)

    # for candle in candles:
    #     priceOpen = candle['open']
    #     print(priceOpen)

    print('c')
