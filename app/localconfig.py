# coding=utf8

import datetime
from datetime_util import DatetimeUtil
from proto.policy_pb2 import Policy


cash_taken_in = 30000
max_train_watch_days = 0
max_predict_watch_days = 0
max_watch_jump_times = 20
RECENT_PREDICT_STOCK_DAYS = 20
DEFAULT_TIMEOUT_SECONDS = 2.0
EXPIRE_AFTER_MS = 10000
EXPIRE_AFTER_DAYS = 100
POSITION_PERCENT_LIST = range(0, 100+1, 10)
end_date_str = DatetimeUtil.to_datetime_str(datetime.datetime.now())
JUMPS_PER_WATCH = 2
MINIMUM_STOCK_PRICE = 10


BUY_WATCH_DAYS_LIST = [20]
SELL_WATCH_DAYS_LIST = BUY_WATCH_DAYS_LIST
DAYS_HOLD_FOR_SALE_LIST = [5]
BUY_MODE_LIST = [Policy.TradePolicy.Percent.LOW]
SELL_MODE_LIST = [Policy.TradePolicy.Percent.HIGH, Policy.TradePolicy.Percent.MEDIUM]



BUY_PRICE_PERCENT_LIST = range(20, 40 + 1, 10)


SELL_PRICE_PERCENT_LIST = []
SELL_PRICE_PERCENT_LIST = range(20, 50 + 1, 10)


LOSS_STOP_THOUSANDTH_LIST = [50]


# SELL_PROFIT_THOUSANDTH_LIST = range(10, 100+1, 10) + [200, 1000]
# SELL_PROFIT_THOUSANDTH_LIST = range(10, 150, 10) + [200, 1000]
SELL_PROFIT_THOUSANDTH_LIST = []


BUY_TREND_GROW_PERCENT_LIST = range(30, 60+1, 10)


LAST_HALF_BUY_TREND_GROW_PERCENT_LIST = BUY_TREND_GROW_PERCENT_LIST


SELL_TREND_GROW_RECENT_LIST = range(0, 40+1, 10) + range(80, 100+1, 10)


LAST_HALF_SELL_TREND_GROW_PERCENT_LIST = SELL_TREND_GROW_RECENT_LIST


LAST_BUY_SEQUENTIAL_TREND_LIST = [1, 2, 3]
LAST_SELL_SEQUENTIAL_TREND_LIST = range(-10, -5 + 1, 1) + range(5, 10+1, 1)


LAST_GROWTH_PART = 2

# BUY_TREND_GROW_PERCENT_LIST = [-1]
# SELL_TREND_GROW_RECENT_LIST = [-1]


# fin_stock = open('stock_list.sina_more20_50')

fin_stock = open('stock_list.easy')
select_stock_name_list = fin_stock.read().split('\n')
fin_stock.close()


# BUY_PRICE_PERCENT_LIST = [10]

# SELL_TREND_GROW_RECENT_LIST = range(0, 100+1, 10)

# select_stock_name_list = ["BABA", "JD", "WB", "AMZN", "BIDU", "MSFT", "FB", "GOOGL", "NTES", "TSLA", "MOMO",  "NVDA", "AAPL",
#                           "SPY", "QQQ", "IWM", "IWV"]
# start_date_str = "20150101"
start_date_str = "20170101"
end_date_str = "20171230"

# start_date_str = "20160101"
# end_date_str = "20161230"

#
# select_stock_name_list = ["JD"]
# DAYS_HOLD_FOR_SALE_LIST = [30]
# start_date_str = "20170101"

