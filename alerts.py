import warnings

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# RuntimeWarning: numpy.dtype size changed, may indicate binary incompatibility

import slack
from strategy import MAStrategy
import bitmex
import os
from time import sleep


api_key, api_secret = os.environ['BITMEX_API_KEY'], os.environ['BITMEX_API_SECRET']

client = bitmex.bitmex(
    test=True,
    api_key=api_key,
    api_secret=api_secret
)

alerts = [
    {'Name':'BTC','Symbol':'XBTUSD', 'Fast':1, 'Slow': 7},
    {'Name':'BTC','Symbol':'XBTUSD', 'Fast':10, 'Slow': 21},
    {'Name':'ETH','Symbol':'ETHU18', 'Fast':1, 'Slow': 7},
    {'Name':'BCH','Symbol':'BCHU18', 'Fast':1, 'Slow': 7},
    {'Name':'LTC','Symbol':'LTCU18', 'Fast':1, 'Slow': 14},
    {'Name':'EOS','Symbol':'EOSU18', 'Fast':1, 'Slow': 14},
    {'Name':'XRP','Symbol':'XRPU18', 'Fast':1, 'Slow': 14},
]

msg = 'Trades:\n'

for alert in alerts:
    ohlc = MAStrategy(client,timeframe='1d').get_data(symbol=alert['Symbol'],count=alert['Slow']+2)
    fast = ohlc.close.rolling(window=alert['Fast']).mean()[-1]
    slow = ohlc.close.rolling(window=alert['Slow']).mean()[-1]
    if fast >= slow:
        direction = 'Long'
    else:
        direction = 'Short'
    msg += "%s (%d,%d) %s\n" % (alert['Name'],alert['Fast'],alert['Slow'],direction)
    sleep(0.5)

slack.send(msg)
