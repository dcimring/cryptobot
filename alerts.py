import warnings

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# RuntimeWarning: numpy.dtype size changed, may indicate binary incompatibility

import slack
from strategy import MAStrategy
import bitmex
import os

#slack.send('Hello from test :fire:')

api_key, api_secret = os.environ['BITMEX_API_KEY'], os.environ['BITMEX_API_SECRET']

client = bitmex.bitmex(
    test=True,
    api_key=api_key,
    api_secret=api_secret
)

ohlc = MAStrategy(client,timeframe='1d').get_data()

close = ohlc.close[-1]
ma7 = ohlc.close.rolling(window=7).mean()[-1]
ma10 = ohlc.close.rolling(window=10).mean()[-1]
ma21 = ohlc.close.rolling(window=21).mean()[-1]

actions = ""

if close >= ma7:
    actions += "LONG(1,7) "
else:
    actions += "SHORT(1,7) "

if ma10 >= ma21:
    actions += "LONG(10,21) "
else:
    actions += "SHORT(10,21) "

slack.send("%0.1f (close) %0.1f (7d) %0.1f (10d) %0.1f (21d) %s" % (close, ma7, ma10, ma21, actions))

