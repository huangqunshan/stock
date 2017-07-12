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


policy_value_dict = {
    "a": [1, 2, 3],
    "b": [4, 5, 6],
    "c": [7, 8, 9],
    "d": [10, 11, 12],
    "e": "e"
}

def build(current_policy_dict, final_set, final_id_set):
    if str(current_policy_dict) in final_set:
        return
    final_set.add(str(current_policy_dict))
    if len(current_policy_dict) < len(policy_value_dict):
        for k, v in policy_value_dict.iteritems():
            if k in current_policy_dict:
                continue
            best_item = v
            if isinstance(best_item, list):
                if 1 < len(best_item):
                    for item in best_item[:2]:
                        current_policy_dict[k] = item
                        if len(current_policy_dict) < len(policy_value_dict):
                            build(dict(current_policy_dict), final_set, final_id_set)
                        else:
                            build(current_policy_dict, final_set, final_id_set)
                else:
                    current_policy_dict[k] = best_item[0]
                    if len(current_policy_dict) == len(policy_value_dict):
                        build(current_policy_dict, final_set, final_id_set)
            else:
                current_policy_dict[k] = best_item
                if len(current_policy_dict) == len(policy_value_dict):
                    build(current_policy_dict, final_set, final_id_set)
    else:
        if str(current_policy_dict) not in final_id_set:
            print current_policy_dict
            final_id_set.add(str(current_policy_dict))



def main():
    final_set = set()
    final_id_set = set()
    build({}, final_set, final_id_set)
    return

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