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
    current_date = datetime.datetime.now()
    person = Person()
    person.cash_taken_in = localconfig.cash_taken_in
    stock_start_date = current_date - datetime.timedelta(days=15)
    stock_end_date = current_date
    predict_date_str = DatetimeUtil.to_datetime_str(current_date)
    StockInfoProxy.generate_stock_info_list(select_stock_name_list,
                                            stock_start_date,
                                            stock_end_date,
                                            person.stock_info)
    for stock in person.stock_info:
        if len(stock.daily_info) > 0 and stock.daily_info[-1].close > 20:
            print stock.stock_id

if __name__ == "__main__":
    main()