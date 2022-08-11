

import ccxt
from datetime import datetime

binance = ccxt.binance()
ohlcvs = binance.fetch_ohlcv('BTC/USDT', timeframe='1m')

for ohlc in ohlcvs:
    print(datetime.fromtimestamp(ohlc[0]/1000).strftime('%Y-%m-%d %H:%M:%S'),ohlc[1],ohlc[2],ohlc[3],ohlc[4])
print(type(ohlcvs))
print(len(ohlcvs))

