# coding=utf8

import logging
import sys
import localconfig
from datetime_util import DatetimeUtil
from policy_factory import PolicyFactory
from policy_util import PolicyUtil
from proto.person_pb2 import Person
from stock_info_proxy import StockInfoProxy

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)


def main():
    select_stock_name_list = localconfig.select_stock_name_list
    if not select_stock_name_list:
        select_stock_name_list = StockInfoProxy.get_stock_name_list()
    person = Person()
    person.cash_taken_in = localconfig.cash_taken_in
    person.stock_start_date = localconfig.start_date_str
    person.stock_end_date = localconfig.end_date_str
    person.max_train_watch_days = localconfig.max_train_watch_days
    person.max_predict_watch_days = localconfig.max_predict_watch_days
    PolicyFactory.generate_policy_list(person.policy_info)
    StockInfoProxy.generate_stock_info_list(select_stock_name_list,
                                            DatetimeUtil.from_date_str(person.stock_start_date),
                                            DatetimeUtil.from_date_str(person.stock_end_date),
                                            person.stock_info)
    PolicyUtil.train(person)
    logging.info("begin write person to file")
    # fout = open('model_out', 'w')
    # fout.write(person.SerializeToString())
    # fout.close()
    logging.info("end write person to file")
    logging.info("end train, person:%s", person)
    logging.info("end train all")


if __name__ == "__main__":
    main()