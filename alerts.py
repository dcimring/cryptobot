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
    actions += "LONG "
else:
    actions += "SHORT "

if ma10 >= ma21:
    actions += "LONG "
else:
    actions += "SHORT "

slack.send("Close %0.1f 7Day %0.1f 10Day %0.1f 21Day %0.1f %s" % (close, ma7, ma10, ma21, actions))

