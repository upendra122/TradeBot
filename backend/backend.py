import logging
from kiteconnect import KiteConnect
import requests
import datetime
import backtest
import connection
import orderAndData
import pickle

logging.basicConfig(level=logging.ERROR)


kite = connection.connect_to_zerodha(
    "cpwuaxis8s2c02jd", "rd312y0g445fyx2q5ynhxkr6v0zqvh1l")
stock_stretegy_one = orderAndData.get_stock_list_stgy_one(kite)
backtest.backtest_stretegy_one(kite,stock_stretegy_one)
