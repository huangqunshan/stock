# coding=utf8

import datetime
import logging
import sys
import localconfig
import numpy as np
from datetime_util import DatetimeUtil
from operator import attrgetter, itemgetter
from policy_factory import PolicyFactory
from policy_predict_util import PolicyPredictUtil
from proto.person_pb2 import Person
from proto.policy_pb2 import Policy
from stock_info_proxy import StockInfoProxy

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def main():
    fin_stock = sys.stdin
    select_stock_name_list = fin_stock.read().split('\n')
    fin_stock.close()

    select_stock_name_list = select_stock_name_list[:]

    # select_stock_name_list = localconfig.select_stock_name_list
    # if not select_stock_name_list:
    #     select_stock_name_list = StockInfoProxy.get_stock_name_list()
    current_date = datetime.datetime.now() + datetime.timedelta(days=1)
    person = Person()
    person.cash_taken_in = localconfig.cash_taken_in
    stock_start_date = current_date - datetime.timedelta(days=localconfig.BUY_WATCH_DAYS.best[0])
    stock_end_date = current_date
    predict_date_str = DatetimeUtil.to_datetime_str(datetime.datetime.now())
    StockInfoProxy.generate_stock_info_list(select_stock_name_list,
                                            stock_start_date,
                                            stock_end_date,
                                            person.stock_info)
    # TODO: use mode: low for trend
    stock_price_dict = PolicyPredictUtil.predict(person.stock_info, predict_date_str, localconfig.TREND_MODE.best[0])
    result = []
    for stock_id, item in stock_price_dict.iteritems():
        trend, trend_buy, trend_sell, last_close_price, buy_price_list, sell_price_list = item

        if not buy_price_list or not sell_price_list:
            continue

        buy_price_list = sorted(buy_price_list)
        buy_np_array = np.array(buy_price_list)
        buy_min = np.percentile(buy_np_array, 0)
        buy_final = np.percentile(buy_np_array, 50)
        buy_max = np.percentile(buy_np_array, 100)
        buy_prob = buy_final / float(last_close_price)

        
        sell_price_list = sorted(sell_price_list)
        sell_np_array = np.array(sell_price_list)
        sell_min = np.percentile(sell_np_array, 0)
        sell_final = np.percentile(sell_np_array, 50)
        sell_max = np.percentile(sell_np_array, 100)
        sell_profit = sell_final / float(last_close_price)
        
        buy_msg = "%s\ttrend:%s-buy:%s-sell:%s\tbuy_prob:%s\tprofit_rate:%s\t%s\tbuy:f-0-100\t%s@%s:%s" % (
            stock_id, trend, trend_buy, trend_sell, buy_prob, sell_profit, predict_date_str, buy_min, buy_final, buy_max)
        sell_msg = "\tsell:f-0-100\t%s@%s:%s" % (
            sell_min, sell_final, sell_max)
        result.append((sell_profit, trend_buy, trend_sell, buy_msg, sell_msg))
    result = sorted(result, key=itemgetter(2), reverse=True)
    result = sorted(result, key=itemgetter(0), reverse=True)
    result = sorted(result, key=itemgetter(1), reverse=True)
    for item in result:
        sell_profit, trend_buy, trend_sell, buy_msg, sell_msg = item
        print buy_msg, sell_msg


if __name__ == "__main__":
    main()