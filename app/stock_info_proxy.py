# coding=utf8


from datetime_util import DatetimeUtil
from proto.person_pb2 import Person
import pandas_datareader.data as web
import datetime
import logging
import math
import requests
import requests_cache
import pandas_datareader as pdr
from pandas_datareader.google import daily, options
import socket
import sqlite3
import localconfig

# cache transparently
requests_cache.install_cache('stock_cache', backend='sqlite', expire_after=localconfig.EXPIRE_AFTER_MS)
session = requests_cache.CachedSession(cache_name='stock_cache', backend='sqlite',
                                       expire_after=datetime.timedelta(days=localconfig.EXPIRE_AFTER_DAYS))
socket.setdefaulttimeout(localconfig.DEFAULT_TIMEOUT_SECONDS)


class StockInfoProxy:
    @staticmethod
    def get_stock_name_list():
        # TODO
        return localconfig.select_stock_name_list

    @staticmethod
    def generate_stock_info_list(stock_name_list, start_date, end_date, repeated_stock_info):
        # TODO(#P1) cache result for future use, and split multi range
        logging.info("begin generate stock list:%s, start_date:%s, end_date:%s", stock_name_list, start_date, end_date)
        for stock_name in stock_name_list:
            try:
                StockInfoProxy.generate_stock(stock_name, start_date, end_date, repeated_stock_info)
            except Exception as e:
                logging.error("fail to get stock %s, e:%s", stock_name, e)
        logging.info("end generate stock list")

    @staticmethod
    def generate_stock(stock_name, start_date, end_date, repeated_stock_info):
        logging.info("begin generate stock:%s, start_date:%s, end_date:%s", stock_name, start_date, end_date)
        logging.info("begin fetch stock info from google")
        dataFrame = daily.GoogleDailyReader(stock_name, start=start_date, end=end_date, retry_count=1, pause=0.1,
                                            chunksize=200, session=session).read()
        logging.info("end fetch stock info from google")
        stock = repeated_stock_info.add()
        stock.stock_id = stock_name
        for row in dataFrame.iterrows():
            timestamp, info = row[0], row[1]
            # ignore nan num
            if math.isnan(info.Close) or math.isnan(info.Open):
                continue
            daily_info = stock.daily_info.add()
            daily_info.open = info.Open
            daily_info.close = info.Close
            daily_info.high = info.High
            daily_info.low = info.Low
            daily_info.volumn = info.Volume
            daily_info.date = timestamp.strftime(DatetimeUtil.PATTERN_STR)
            # TODO: yield ...
        logging.info("end generate stock")

if __name__ == "__main__":
    start_date_str = "20170601"
    end_date_str = "20170616"
    person = Person()
    person.stock_start_date = start_date_str
    person.stock_end_date = end_date_str
    StockInfoProxy.generate_stock_info_list(["BABA", "AAPL"],
                                            DatetimeUtil.from_date_str(start_date_str),
                                            DatetimeUtil.from_date_str(end_date_str),
                                            person.stock_info)
    print person
