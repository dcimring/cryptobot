import talib
import pandas as pd
import numpy as np
import bitmex
import time

class Strategy():
    def __init__(self, client, timeframe='5m'):
        self.client = client
        self.timeframe = timeframe
        
    def run(self):
        ohlcv_candles = pd.DataFrame(self.client.Trade.Trade_getBucketed(
            binSize=self.timeframe,
            symbol='XBTUSD',
            count=100,
            reverse=True
        ).result()[0])

        ohlcv_candles.set_index(['timestamp'], inplace=True)

        #print(ohlcv_candles)
        
        macd, signal, hist = talib.MACD(ohlcv_candles.close.values, 
                                        fastperiod = 8, slowperiod = 28, signalperiod = 9)
        
        #sell
        if hist[-2] > 0 and hist[-1] < 0:
            return -1
        #buy
        if hist[-2] < 0 and hist[-1] > 0:
            return 1
        #do nothing
        else:
            return 0