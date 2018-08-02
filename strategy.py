import talib
import pandas as pd
import numpy as np
import bitmex
import time
import logging

class MAStrategy():

    def __init__(self, client, timeframe='5m', mas=1, mal=7):
        self.client = client
        self.timeframe = timeframe
        self.name = "MA(%d,%d)" % (mas,mal)
        self.mas=mas
        self.mal=mal
        self.logger = logging.getLogger('cryptobot')
        

    def crossabove(self,mas,mal):
        ''' Returns True if mas has just crossed ABOVE mal
        Inputs
        mas - list of short moving averages
        mal - list of long moving averages'''
        
        if (mas[-1] > mal[-1]) and (mas[-2] < mal[-2]):
            return True
        else:
            return False

    def crossunder(self,mas,mal):
        ''' Returns True if mas has just crossed UNDER mal
        Inputs
        mas - list of short moving averages
        mal - list of long moving averages'''
        
        if (mas[-1] < mal[-1]) and (mas[-2] > mal[-2]):
            return True
        else:
            return False

    def get_data(self, symbol='XBTUSD'):

        ohlcv_candles = pd.DataFrame(self.client.Trade.Trade_getBucketed(
            binSize=self.timeframe,
            symbol=symbol,
            count=50,
            reverse=True
        ).result()[0])

        # reverse param was needed in order to get the latest values
        # now we need to sort them into date order so that MA calcs work correctly

        ohlcv_candles.set_index(['timestamp'], inplace=True)
        ohlcv_candles.sort_index(inplace=True)

        return ohlcv_candles

    def run(self):
        
        ohlcv_candles = self.get_data()

        # macd, signal, hist = talib.MACD(ohlcv_candles.close.values, 
        #                                 fastperiod = 8, slowperiod = 28, signalperiod = 9)
        
        # mas = talib.SMA(ohlcv_candles.close.values, timeperiod=self.mas)
        # mal = talib.SMA(ohlcv_candles.close.values, timeperiod=self.mal)

        mas = ohlcv_candles.close.rolling(window=self.mas).mean()
        mal = ohlcv_candles.close.rolling(window=self.mal).mean()

        self.logger.debug('Closing prices %s',ohlcv_candles.close.values)
        self.logger.debug('%s day MA is %0.2f',self.mas,mas[-1])
        self.logger.debug('%s day MA is %0.2f',self.mal,mal[-1])

        if self.crossabove(mas,mal):
            return "BUY"

        if self.crossunder(mas,mal):
            return "SELL"
        
        return "HOLD"