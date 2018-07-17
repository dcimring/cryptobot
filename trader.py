import talib
import pandas as pd
import numpy as np
import bitmex
import time
import logging

class Trader():
    def __init__(self, client, strategy, money_to_trade=100, leverage=5):
        self.client = client
        self.strategy = strategy
        self.logger = logging.getLogger('cryptobot')
        self.money_to_trade = money_to_trade
        self.leverage = leverage
        
    def execute_trade(self):
        
        decision = self.strategy.run()
        self.logger.info('Strategy %s decision %s',self.strategy.name, decision)
        
        try:
            if decision == "SELL":
                self.logger.info("Trying to %s %0.2f",decision,self.money_to_trade * self.leverage)
                response = self.client.Order.Order_new(
                    symbol="XBTUSD",
                    side="Sell",
                    orderQty=self.money_to_trade * self.leverage,
                ).result()

            if decision == "BUY":
                self.logger.info("Trying to %s %0.2f",decision,self.money_to_trade * self.leverage)
                response = self.client.Order.Order_new(
                    symbol="XBTUSD",
                    side="Buy",
                    orderQty=self.money_to_trade * self.leverage,
                ).result()

            self.logger.info("Response %s",response)

        except Exception as e:
            self.logger.error("Trading exception %s",str(e))
        
        return