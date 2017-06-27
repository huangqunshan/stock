# coding=utf8

import datetime
from datetime_util import DatetimeUtil
from proto.policy_pb2 import Policy


select_stock_name_list = ["BABA", "JD", "WB", "AMZN", "BIDU", "MSFT", "FB", "GOOGL", "NTES", "TSLA", "MOMO",  "NVDA", "AAPL",
                          "SPY", "QQQ", "IWM", "IWV"]
start_date_str = "20150101"
end_date_str = DatetimeUtil.to_datetime_str(datetime.datetime.now())
cash_taken_in = 30000
max_train_watch_days = 0
max_predict_watch_days = 0
max_hold_days = 360
WATCH_DAYS_LIST = range(5, 15, 5) + range(15, 60, 15) + range(60, 120, 30) + range(120, 240 + 1, 60)
PRICE_PERCENT_LIST = range(0, 120 + 1, 10)
POSITION_PERCENT_LIST = range(0, 100+1, 10)
BUY_MODE_LIST = [Policy.TradePolicy.Percent.LOW, Policy.TradePolicy.Percent.HIGH, Policy.TradePolicy.Percent.MEDIUM, Policy.TradePolicy.Percent.OPEN, Policy.TradePolicy.Percent.CLOSE]
SELL_MODE_LIST = BUY_MODE_LIST
DEFAULT_TIMEOUT_SECONDS = 2.0
EXPIRE_AFTER_MS = 10000
EXPIRE_AFTER_DAYS = 100



select_stock_name_list = ["BABA", "JD", "WB",
                          "SPY", "IWM"]
start_date_str = "20161201"
end_date_str = DatetimeUtil.to_datetime_str(datetime.datetime.now())
cash_taken_in = 30000
max_train_watch_days = 0
max_predict_watch_days = 0
max_hold_days = 30
BUY_WATCH_DAYS_LIST = [5, 10, 20, 40, 60]
SELL_WATCH_DAYS_LIST = [5, 10, 15, 20, 30]
BUY_PRICE_PERCENT_LIST = range(0, 40 + 1, 10)
SELL_PRICE_PERCENT_LIST = range(80, 120 + 1, 10)
POSITION_PERCENT_LIST = range(0, 100+1, 10)
BUY_MODE_LIST = [Policy.TradePolicy.Percent.MEDIUM]
SELL_MODE_LIST = [Policy.TradePolicy.Percent.MEDIUM]


# for test
# start_date_str = "20170101"
# select_stock_name_list = ["BABA"]
# max_hold_days = 30
# BUY_WATCH_DAYS_LIST = [5]
# SELL_WATCH_DAYS_LIST = [5]
# BUY_PRICE_PERCENT_LIST = range(0, 40 + 1, 10)
# SELL_PRICE_PERCENT_LIST = range(80, 120 + 1, 10)
# POSITION_PERCENT_LIST = range(0, 100+1, 10)
# BUY_MODE_LIST = [Policy.TradePolicy.Percent.MEDIUM]
# SELL_MODE_LIST = [Policy.TradePolicy.Percent.MEDIUM]

