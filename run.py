import warnings

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# RuntimeWarning: numpy.dtype size changed, may indicate binary incompatibility

from strategy import MAStrategy
from trader import Trader
import bitmex
import logging
import logging.handlers
import os


# unit tests eg for crossabove and crossunder
# todo - cater for different strategies 
# todo - add image to slack message

logger = logging.getLogger('cryptobot')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.WatchedFileHandler('cryptobot.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.debug('Starting')

api_key, api_secret = os.environ['BITMEX_API_KEY'], os.environ['BITMEX_API_SECRET']

client = bitmex.bitmex(
    test=True,
    api_key=api_key,
    api_secret=api_secret
)

logger.debug('Connected to bitmex')

strategy = MAStrategy(client, timeframe='1d', mas=1, mal=7)
trader = Trader(client, strategy, money_to_trade=4000, leverage=1)
trader.execute_trade()

logger.info('Done')
