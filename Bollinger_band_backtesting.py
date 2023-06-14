import pandas as pd
from plot_utils import plot_results


df = pd.read_csv('BTC_ETH_BNB_from_Oct3122_to_PRESENT.csv')


# obliczenie sma = simple moving avrage o interwale 20 ostatnich cen

def sma(data, window):
    return(data.rolling(window=window).mean())

#sma(df['BTC-USD_Open'], window = 20) # sprawdzenie czy srednia dziala dla 20 ostatnich cen tylko dla BTC
#print(sma(df['BTC-USD_Open'], window = 20))

def bollinger_bands(data,sma,window, nstd): # obliczenie wstęg Bollingera 3 średnie w dól, 3 średnie w góre
    std = data.rolling(window=window).std()
    upper_band = sma + std*nstd
    lower_band = sma - std*nstd
    return upper_band, lower_band


symbols = ['BTC','ETH','BNB']
nstd = 3

for symbol in symbols:
    df[f'{symbol}_sma'] = sma(df[f'{symbol}-USD_Open'],20)
    df[f'{symbol}_upper_band'], df[f'{symbol}_lower_band'] = bollinger_bands(df[f'{symbol}-USD_Open'],df[f'{symbol}_sma'],20, nstd )


# Trzeba pominac 20 pierwszych świeczek gdzie lower band and upper band jest NaN
df = df.dropna()

#print(df.head())
#print(df)

class Trade:
    def __init__(self, balance_amount,balance_unit, trading_fee_multiplier):
        self.balance_amount = balance_amount
        self.balance_unit = balance_unit
        self.buys = []
        self.sells =[]
        self.trading_fee_multiplier = 0.99925  # zalezy od VIP level na gieldzie musimy cos przyjac, np VIP = 0

    def buy(self,symbol,buy_price, time):
         self.balance_amount = (self.balance_amount / buy_price) * self.trading_fee_multiplier
         self.balance_unit = symbol
         self.buys.append([symbol,time,buy_price])


    def sell(self,sell_price,time):
        self.balance_amount = (self.balance_amount * sell_price) * self.trading_fee_multiplier
        self.sells.append([self.balance_unit, time, sell_price])
        self.balance_unit = 'USDT'

env = Trade(balance_amount=100, balance_unit='USDT', trading_fee_multiplier= 0.99925)


print(env.balance_unit)
print(env.balance_amount)

for i in range(len(df)):
    if env.balance_unit == 'USDT': #Jeśli jestesmy w posiadaniu USDT to mamy zamiar kupowac
        for symbol in symbols:
             if df[f'{symbol}-USD_Low'].iloc[i] < df[f'{symbol}_lower_band'].iloc[i]:  # sygnał do kupna bo cena przekroczyła lower band
                env.buy(symbol,df[f'{symbol}-USD_Low'].iloc[i], df['Open_Time'].iloc[i])
                break

    if env.balance_unit != 'USDT':
        if df[f'{env.balance_unit}-USD_High'].iloc[i] > df[f'{env.balance_unit}_upper_band'].iloc[i]: # sygnał do sprzedaży, cena przekroczyła upper band
            env.sell(df[f'{env.balance_unit}-USD_High'].iloc[i],df['Open_Time'].iloc[i])


if env.balance_unit != 'USDT':
     env.sell(df[f'{env.balance_unit}-USD_High'].iloc[-1], df['Open_Time'].iloc[-1])

print(f'num buys: {symbol} {len(env.buys)}')
print(f'num sells:{symbol} {len(env.sells)}')
print(f'ending_balance:{round(env.balance_amount)} {env.balance_unit}')

#plot_results(df, 'BTC', env.buys, env.sells)
#plot_results(df, 'ETH', env.buys, env.sells)
#plot_results(df, 'BNB', env.buys, env.sells)

