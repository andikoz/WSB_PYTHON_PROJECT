import pandas as pd
import time
import plotly.graph_objects as go
from binance.client import Client
from binance_keys import api_key, secret_key
from datetime import datetime



client = Client(api_key, secret_key)

coins = ['BTC','ETH','BNB']

merge = False

for coin in coins:

        print(f'Pobieram dane z gieldy {coin}  .  .  .  .')
        start_str = 'Oct 31, 2022'
        klines = client.get_historical_klines(symbol= f'{coin}USDT', interval = client.KLINE_INTERVAL_4HOUR, start_str= start_str)

        cols = ['Open_Time',
        f'{coin}-USD_Open',
        f'{coin}-USD_High',
        f'{coin}-USD_Low',
        f'{coin}-USD_Close',
        f'{coin}-USD_Volume',
        'Close_Time',
        f'{coin}-Quoteassetvolume',
        f'{coin}-Numberoftrades',
        f'{coin}-TBBAV',
        f'{coin}-TBQAV',
        f'{coin}-ignore']

        coin_df = pd.DataFrame(klines,columns=cols)

        if merge == True:
                all_coins_df = pd.merge(coin_df, all_coins_df, how = 'inner', on = ['Open_Time','Close_Time'])
        else:
                all_coins_df = coin_df
                merge = True

        time.sleep(70) # time sleep musi byc bo Binance API wyrzuca blad jesli za czesto pobieram dane

print(all_coins_df)

all_coins_df['Open_Time'].iloc[0] / 1000

datetime.fromtimestamp(all_coins_df['Open_Time'].iloc[0] / 1000)
all_coins_df['Open_Time'] = [datetime.fromtimestamp(ts /1000) for ts in all_coins_df['Open_Time']]
all_coins_df['Close_Time'] = [datetime.fromtimestamp(ts /1000) for ts in all_coins_df['Close_Time']]

# all_coins_df['LTC-USD_Open'] = all_coins_df['LTC-USD_Open'].astype(float) zamiana str na typ float tyle ze tylko jednej kolumny

print(all_coins_df)

# wszystko spoko tylko time tez sie zamieni na float ... dlatego if not
for col in all_coins_df.columns:
        if not 'Time' in col:
                all_coins_df[col] = all_coins_df[col].astype(float)

print(all_coins_df['BTC-USD_Open'].iloc[0]) # sprawdzenie czy konwersja na float dziala


print(all_coins_df.columns) # pokaż kolumny zeby bylo wiadomo co podac do wykresu  jako  4 dane wejsciowe

for coin in coins:
        fig = go.Figure(data=[go.Candlestick(x=all_coins_df['Open_Time'],
                open=all_coins_df[f'{coin}-USD_Open'],
                high=all_coins_df[f'{coin}-USD_High'],
                low=all_coins_df[f'{coin}-USD_Low'],
                close=all_coins_df[f'{coin}-USD_Close'])])


        fig.update_layout(
                 title= f'{coin}/USDT_CRYPTO_CURRENCY_CHART',
                 yaxis_title = f'{coin}_USDT',
                xaxis_rangeslider_visible=False)
        fig.show()

# zapisaie danych do pliku csv, index false  bo bazowane jest na kolumnie Open_Time


all_coins_df.to_csv('BTC_ETH_BNB_from_Oct3122_to_PRESENT.csv',index = False)

print('Dane zapisane do pliku ')