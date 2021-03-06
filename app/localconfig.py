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


# policy_id: "sell_days_watch:30,trend_mode:2,buy_days_watch:20,buy_price_percent:90,buy_mode:1,loss_stop_thousandth:100,prefer_max_stock_count:1,sell_price_percent:100,last_sell_sequential_trend_count:-9999,sell_profit_thousandth:0,buy_trend_days_watch:40,buy_trend_percent:-9999,sell_trend_percent:-9999,last_buy_sequential_trend_count:-9999,days_hold_for_sell:2,min_stock_price:20,last_close_price_percent:-9999,sell_mode:2,sell_trend_days_watch:40,prefer_max_splited_trade_unit:1"
# policy_id_md5: "02c0e71023cdcf1c3de9d8f963633ac0"
# roi_more_than_one_rate: 0.81


DEFAULT_CONFIG = -9999
POSITION_PERCENT_LIST = range(0, 100+1, 10)
SUMMARY_POSITION_PERCENT_LIST = range(0, 100+1, 10)
DEFAULT_TIMEOUT_SECONDS = 2.0
EXPIRE_AFTER_DAYS = 100
EXPIRE_AFTER_MS = 10000
end_date_str = DatetimeUtil.to_datetime_str(datetime.datetime.now())
cash_taken_in = 30000
TOP_PERCENT = 0
MIN_TRADE_DAYS_PERCENT = 5
MIN_TRADE_DAYS = 4
MAX_MEAN_DAYS_HOLD_FOR_SALE = 15
# max_train_watch_days = 0
# max_predict_watch_days = 0

max_watch_jump_times = 6
JUMPS_PER_WATCH = 1
LAST_GROWTH_PART = 2

PREFER_MAX_SPLITED_TRADE_UNIT = PolicyValueRange([1], 1)
PREFER_MAX_STOCK_COUNT = PolicyValueRange([1], 1)


DAYS_HOLD_FOR_SALE = PolicyValueRange([2, 5, 10], [5, 10])


MIN_STOCK_PRICE = PolicyValueRange([5, 10, 20, 50], [20, 10])

BUY_MODE = PolicyValueRange([Policy.TradePolicy.Percent.LOW, Policy.TradePolicy.Percent.MEDIUM],
                            [Policy.TradePolicy.Percent.LOW])
SELL_MODE = PolicyValueRange([Policy.TradePolicy.Percent.HIGH, Policy.TradePolicy.Percent.MEDIUM],
                             [Policy.TradePolicy.Percent.HIGH])

BUY_WATCH_DAYS = PolicyValueRange([10, 20, 30], [20, 10] + [30])
SELL_WATCH_DAYS = PolicyValueRange([10, 20, 30], [20, 30] + [10])

BUY_PRICE_PERCENT = PolicyValueRange(range(70, 100 + 1, 10), [90, 70, 80] + [100])
SELL_PRICE_PERCENT = PolicyValueRange(range(70, 100 + 1, 10), [100, 90, 80] + [70])

LOSS_STOP_THOUSANDTH = PolicyValueRange([10, 20, 50, 100, 200, 500], [100, 50, 20])
SELL_PROFIT_THOUSANDTH = PolicyValueRange([0, 10, 20, 50, 100, 150, 1000], [0, 100, 50])


# best: 100
LAST_CLOSE_PRICE_PERCENT = PolicyValueRange([DEFAULT_CONFIG] + range(80, 120, 1), DEFAULT_CONFIG)


TREND_MODE = PolicyValueRange([Policy.TradePolicy.Percent.LOW, Policy.TradePolicy.Percent.HIGH, Policy.TradePolicy.Percent.MEDIUM],
                              [Policy.TradePolicy.Percent.HIGH, Policy.TradePolicy.Percent.LOW])


BUY_TREND_DAYS_WATCH = PolicyValueRange([DEFAULT_CONFIG] + range(10, 50+1, 10) + range(60, 120+1, 20),
                                        [40, 20])
SELL_TREND_DAYS_WATCH = PolicyValueRange([40],
                                        [40])
BUY_TREND_PERCENT = PolicyValueRange([DEFAULT_CONFIG] + range(0, 100 + 1, 10),
                                     DEFAULT_CONFIG,
                                     [50])
SELL_TREND_PERCENT = PolicyValueRange([DEFAULT_CONFIG] + range(0, 100 + 1, 10),
                                      DEFAULT_CONFIG,
                                      None)
LAST_BUY_SEQUENTIAL_TREND_COUNT = PolicyValueRange([DEFAULT_CONFIG] + range(-20, 20 + 1, 1),
                                                   DEFAULT_CONFIG,
                                                   [1] + [-1, -2]
                                                   # None
                                                   )
LAST_SELL_SEQUENTIAL_TREND_COUNT = PolicyValueRange(range(-20, 20 + 1, 1),
                                                    DEFAULT_CONFIG,
                                                    None)

# BUY_TREND_DAYS_WATCH = PolicyValueRange([40],
#                                         [40])
# SELL_TREND_DAYS_WATCH = PolicyValueRange([40],
#                                         [40])
# BUY_TREND_PERCENT = PolicyValueRange([],
#                                      DEFAULT_CONFIG,
#                                      None,
#                                      )
# LAST_BUY_SEQUENTIAL_TREND_COUNT = PolicyValueRange([],
#                                                    DEFAULT_CONFIG,
#                                                    #[-1, -2, 2, 1]
#                                                    None
#                                                    )


try:
    # fin_stock = open('stock_list.sina_more20_500')
    fin_stock = open('stock_list.easy')
    select_stock_name_list = fin_stock.read().split('\n')
    fin_stock.close()
except Exception:
    select_stock_name_list = []


# BUY_PRICE_PERCENT_LIST = [10]

# SELL_TREND_GROW_RECENT_LIST = range(0, 100+1, 10)

# select_stock_name_list = ["BABA", "JD", "WB", "AMZN", "BIDU", "MSFT", "FB", "GOOGL", "NTES", "TSLA", "MOMO",  "NVDA", "AAPL",
#                           "SPY", "QQQ", "IWM", "IWV"]
# start_date_str = "20150101"
start_date_str = "20160101"
end_date_str = "20171230"

short_stock_name_list = ["JD", "BABA", "WBAI", "GOOGL", "TSLA"]
