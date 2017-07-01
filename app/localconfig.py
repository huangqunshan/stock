# coding=utf8

import datetime
from datetime_util import DatetimeUtil
from proto.policy_pb2 import Policy


cash_taken_in = 30000
max_train_watch_days = 0
max_predict_watch_days = 0
max_hold_days = 30
max_watch_jump_times = 10
DEFAULT_TIMEOUT_SECONDS = 2.0
EXPIRE_AFTER_MS = 10000
EXPIRE_AFTER_DAYS = 100
POSITION_PERCENT_LIST = range(0, 100+1, 10)


# best policy fix for improve train speed

# buy_days_watch:15	2-5-8-9:	1.19510914734 # 14.192, 1.02821984262 # 8.4, 0.895496480751 # 2.92, 0.764960191049 # 1.811
# buy_days_watch:10	2-5-8-9:	1.20854553604 # 17.122, 1.02189637158 # 10.4, 0.8855222122 # 3.8, 0.722699301807 # 1.93
# buy_days_watch:20	2-5-8-9:	1.16628610024 # 12.32, 1.02160154956 # 7.2, 0.904542472462 # 2.42, 0.769281673976 # 1.189
# buy_days_watch:5	2-5-8-9:	1.2031678982 # 23.874, 1.02081145021 # 13.75, 0.848808013158 # 5.36, 0.665902869118 # 2.426
BUY_WATCH_DAYS_LIST = [15]
# sell_days_watch:15	2-5-8-9:	1.23013866919 # 14.912, 1.04704621872 # 8.44, 0.891200242997 # 3.0, 0.733736507942 # 1.741
# sell_days_watch:20	2-5-8-9:	1.22479592739 # 13.204, 1.04063553463 # 7.5, 0.897240429646 # 2.468, 0.730709881747 # 1.219
# sell_days_watch:10	2-5-8-9:	1.17930207727 # 17.044, 1.02475195877 # 9.8, 0.877468725376 # 3.92, 0.684441354771 # 1.93
# sell_days_watch:5	2-5-8-9:	1.11310061124 # 23.4, 0.99330735526 # 13.82, 0.860888243394 # 4.88, 0.682299132134 # 2.24
SELL_WATCH_DAYS_LIST = [15]


# buy_percent_n:20	2-5-8-10:	1.20428389305 # 12.808, 1.04677392881 # 7.9, 0.921295918214 # 3.12, 0.785876241192 # 2.0
# buy_percent_n:30	2-5-8-10:	1.20617618691 # 14.0, 1.04500483541 # 8.725, 0.901410365332 # 3.72, 0.757108894934 # 2.0
BUY_PRICE_PERCENT_LIST = range(20, 20 + 1, 10)

# sell_percent_n:110	2-5-8-9:	1.26625731137 # 11.2, 1.13306259364 # 7.2, 1.04533893279 # 3.0, 1.02193602462 # 2.0
# sell_percent_n:100	2-5-8-9:	1.26625731137 # 11.2, 1.13306259364 # 7.2, 1.04533893279 # 3.0, 1.02193602462 # 2.0
# sell_percent_n:80	2-5-8-9:	1.26102344763 # 14.0, 1.12368146811 # 8.8, 1.04223373156 # 3.8, 1.01569045808 # 2.0
# sell_percent_n:90	2-5-8-9:	1.26542120237 # 12.2, 1.12301105862 # 8.0, 1.04192526162 # 3.72, 1.01968853688 # 2.0
# sell_percent_n:70	2-5-8-9:	1.23610520233 # 14.76, 1.12165929586 # 9.4, 1.04262850752 # 4.08, 1.01869211194 # 2.48
# sell_percent_n:60	2-5-8-9:	1.21051657253 # 15.44, 1.1026040635 # 9.9, 1.03802631457 # 4.08, 1.01353593443 # 2.8
# sell_percent_n:50	2-5-8-9:	1.20158110578 # 16.18, 1.08226989692 # 10.3, 1.02682962936 # 4.08, 1.00627234815 # 2.8

SELL_PRICE_PERCENT_LIST = range(80, 80 + 1, 10)

# buy_mode:1; 2 - 5 - 8 - 10:    1.20042430959  # 14.92, 1.04264026959 # 9.25, 0.905355531836 # 3.892, 0.0261296704281 # 0.0
# buy_mode:3; 2 - 5 - 8 - 10:    1.20547857769  # 20.434, 1.02425980384 # 12.16, 0.8800411176 # 5.0, 0.0215538388489 # 0.0
BUY_MODE_LIST = [Policy.TradePolicy.Percent.LOW]
# sell_mode:2; 2 - 5 - 8 - 10:    1.21805349502  # 14.84, 1.04524164974 # 9.225, 0.896557619738 # 3.88, 0.0215538388489 # 0.0
# sell_mode:3; 2 - 5 - 8 - 10:    1.16409161087  # 20.48, 1.02165842369 # 12.46, 0.883413927914 # 5.028, 0.0221897851161 # 0.0
SELL_MODE_LIST = [Policy.TradePolicy.Percent.HIGH]

LOSS_STOP_THOUSANDTH_LIST = range(5, 100+1, 10) + [990]
SELL_PROFIT_THOUSANDTH_LIST = range(5, 100+1, 5) + [200, 1000]

fin_stock = open('stock_list.easy')
select_stock_name_list = fin_stock.read().split('\n')
fin_stock.close()


end_date_str = DatetimeUtil.to_datetime_str(datetime.datetime.now())
start_date_str = "20150101"


# select_stock_name_list = ["BABA", "JD", "WB", "AMZN", "BIDU", "MSFT", "FB", "GOOGL", "NTES", "TSLA", "MOMO",  "NVDA", "AAPL",
#                           "SPY", "QQQ", "IWM", "IWV"]
start_date_str = "20160101"



# select_stock_name_list = ["BABA"]
# start_date_str = "20170101"
# BUY_WATCH_DAYS_LIST = [10]
# SELL_WATCH_DAYS_LIST = [10]

