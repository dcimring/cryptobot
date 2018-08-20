import warnings

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# RuntimeWarning: numpy.dtype size changed, may indicate binary incompatibility

import slack
from strategy import MAStrategy
import bitmex
import os
from time import sleep
#from IPython.core.debugger import set_trace


api_key, api_secret = os.environ['BITMEX_API_KEY'], os.environ['BITMEX_API_SECRET']

client = bitmex.bitmex(
    test=True,
    api_key=api_key,
    api_secret=api_secret
)

alerts = [
    {'Name':'BTC','Symbol':'.BXBT', 'Fast':1, 'Slow': 7, 'EMA': True},
    {'Name':'BTC','Symbol':'.BXBT', 'Fast':10, 'Slow': 21, 'EMA': False},
    {'Name':'ETH','Symbol':'.ETHXBT', 'Fast':1, 'Slow': 7, 'EMA': False},
    {'Name':'BCH','Symbol':'.BCHXBT', 'Fast':1, 'Slow': 7, 'EMA': False},
    {'Name':'LTC','Symbol':'.LTCXBT', 'Fast':1, 'Slow': 14, 'EMA': False},
    {'Name':'EOS','Symbol':'.EOSXBT', 'Fast':1, 'Slow': 14, 'EMA': False},
    {'Name':'XRP','Symbol':'.XRPXBT', 'Fast':1, 'Slow': 14, 'EMA': False},
]

msg = 'Trades:\n'
strategy = MAStrategy(client,timeframe='1d')

# NewHigh strategy alert
# If price within 5% of 7 day high then long, else short

lookback = 7
tolerance = 0.05
extra = ''

ohlc = strategy.get_data(symbol='.BXBT',count=lookback+4)

high = ohlc.close.rolling(window=lookback).max() * (1 - tolerance)

if ohlc.close[-1] >= high[-1]:
    direction = 'Long'
    if strategy.crossabove(ohlc.close,high): extra="*"
else:
    direction = 'Short'
    if strategy.crossunder(ohlc.close,high): extra="*"

msg += "BTC within %0.1f%% of %dd high %s%s\n" % (tolerance*100,lookback,direction,extra)

for alert in alerts:
    extra = ''
    ohlc = strategy.get_data(symbol=alert['Symbol'],count=alert['Slow']+4)
    
    if alert['EMA']:
        fast = ohlc.close.ewm(span=alert['Fast'], adjust=False).mean()
        slow = ohlc.close.ewm(span=alert['Slow'], adjust=False).mean()
    else:
        fast = ohlc.close.rolling(window=alert['Fast']).mean()
        slow = ohlc.close.rolling(window=alert['Slow']).mean()
    
    if fast[-1] >= slow[-1]:
        direction = 'Long'
        if strategy.crossabove(fast,slow): extra="*"
    else:
        direction = 'Short'
        if strategy.crossunder(fast,slow): extra="*"
        
    msg += "%s (%d,%d) %s%s\n" % (alert['Name'],alert['Fast'],alert['Slow'],direction,extra)
    sleep(0.5)

slack.send(msg)
