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
    {'Name':'BTC','Symbol':'.BXBT', 'Fast':1, 'Slow': 7},
    {'Name':'BTC','Symbol':'.BXBT', 'Fast':10, 'Slow': 21},
    {'Name':'ETH','Symbol':'.ETHXBT', 'Fast':1, 'Slow': 7},
    {'Name':'BCH','Symbol':'.BCHXBT', 'Fast':1, 'Slow': 7},
    {'Name':'LTC','Symbol':'.LTCXBT', 'Fast':1, 'Slow': 14},
    {'Name':'EOS','Symbol':'.EOSXBT', 'Fast':1, 'Slow': 14},
    {'Name':'XRP','Symbol':'.XRPXBT', 'Fast':1, 'Slow': 14},
]

msg = 'Trades:\n'
strategy = MAStrategy(client,timeframe='1d')

for alert in alerts:
    extra = ''
    ohlc = strategy.get_data(symbol=alert['Symbol'],count=alert['Slow']+2)
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
