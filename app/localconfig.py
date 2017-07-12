# coding=utf8

import datetime
from datetime_util import DatetimeUtil
from proto.policy_pb2 import Policy

class PolicyValueRange:
    def __init__(self, value_list, best_value, filter=None):
        self.range = value_list
        self.best = best_value
        if filter is not None:
            self.filter = filter
        else:
            self.filter = self.range


DEFAULT_CONFIG = -9999
POSITION_PERCENT_LIST = range(0, 100+1, 10)
DEFAULT_TIMEOUT_SECONDS = 2.0
EXPIRE_AFTER_DAYS = 100
EXPIRE_AFTER_MS = 10000
end_date_str = DatetimeUtil.to_datetime_str(datetime.datetime.now())
cash_taken_in = 30000
# max_train_watch_days = 0
# max_predict_watch_days = 0

max_watch_jump_times = 20
JUMPS_PER_WATCH = 2
LAST_GROWTH_PART = 2

PREFER_MAX_SPLITED_TRADE_UNIT = PolicyValueRange([1], 1)
PREFER_MAX_STOCK_COUNT = PolicyValueRange([1], 1)

MIN_STOCK_PRICE = PolicyValueRange([5, 10, 15, 20, 30], 10)
BUY_WATCH_DAYS = PolicyValueRange([10, 20, 30], 20)
SELL_WATCH_DAYS = PolicyValueRange([10, 20, 30], 20)
DAYS_HOLD_FOR_SALE = PolicyValueRange([2, 5, 10, 15], 5)
BUY_MODE = PolicyValueRange([Policy.TradePolicy.Percent.LOW, Policy.TradePolicy.Percent.MEDIUM], Policy.TradePolicy.Percent.LOW)
SELL_MODE = PolicyValueRange([Policy.TradePolicy.Percent.HIGH, Policy.TradePolicy.Percent.MEDIUM],
                             Policy.TradePolicy.Percent.HIGH)
TREND_MODE = PolicyValueRange([Policy.TradePolicy.Percent.LOW, Policy.TradePolicy.Percent.HIGH, Policy.TradePolicy.Percent.MEDIUM],
                              Policy.TradePolicy.Percent.LOW)

BUY_PRICE_PERCENT = PolicyValueRange(range(10, 100 + 1, 10), 30)
SELL_PRICE_PERCENT = PolicyValueRange(range(10, 100 + 1, 10), 40)
LOSS_STOP_THOUSANDTH = PolicyValueRange([10, 20, 50, 100, 200, 500], 50)

SELL_PROFIT_THOUSANDTH = PolicyValueRange([0, 10, 20, 50, 100, 150, 1000], 0)

BUY_TREND_PERCENT = PolicyValueRange(range(0, 100 + 1, 10),
                                     DEFAULT_CONFIG,
                                     None
                                     # range(40, 60 + 1, 10)
                                     )
SELL_TREND_PERCENT = PolicyValueRange(range(0, 100 + 1, 10),
                                      DEFAULT_CONFIG,
                                      None
                                      # range(10, 40+1, 10) + range(80, 100+1, 10)
                                      )
HALF_BUY_TREND_PERCENT = PolicyValueRange(range(0, 100 + 1, 10),
                                          DEFAULT_CONFIG,
                                          None
                                          #range(40, 60 + 1, 10),
                                          )
HALF_SELL_TREND_PERCENT = PolicyValueRange(range(0, 100 + 1, 10),
                                           DEFAULT_CONFIG,
                                           None
                                           #range(10, 40 + 1, 10) + range(80, 100 + 1, 10),
                                           )

LAST_BUY_SEQUENTIAL_TREND_COUNT = PolicyValueRange(range(-20, 20 + 1, 1),
                                                   DEFAULT_CONFIG,
                                                   None)
LAST_SELL_SEQUENTIAL_TREND_COUNT = PolicyValueRange(range(-20, 20 + 1, 1),
                                                    DEFAULT_CONFIG,
                                                    None)




# BUY_TREND_GROW_PERCENT_LIST = [-1]
# SELL_TREND_GROW_RECENT_LIST = [-1]


# fin_stock = open('stock_list.sina_more20_500')

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
select_stock_name_list = ["JD"]
# DAYS_HOLD_FOR_SALE_LIST = [30]
# start_date_str = "20170101"

