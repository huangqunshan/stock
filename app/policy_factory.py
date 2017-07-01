# coding=utf8

import logging

import localconfig
from proto.person_pb2 import Person


class PolicyFactory:


    @staticmethod
    # repeated_policy: repated Policy
    def generate_policy_list(repeated_policy):
        logging.info("begin generate policy list")
        for prefer_max_splited_trade_unit in [1]:
            logging.debug("begin generate policy list for prefer_max_splited_trade_unit:%s", prefer_max_splited_trade_unit)
            for prefer_max_stock_count in [1]:
                logging.debug("begin generate policy list for prefer_max_splited_trade_unit:%s, prefer_max_stock_count:%s",
                             prefer_max_splited_trade_unit, prefer_max_stock_count)
                PolicyFactory.generate_policy_list_impl(prefer_max_splited_trade_unit, prefer_max_stock_count, repeated_policy)
                logging.debug("end generate policy list for prefer_max_splited_trade_unit:%s, prefer_max_stock_count:%s",
                             prefer_max_splited_trade_unit, prefer_max_stock_count)
            logging.debug("end generate policy list for prefer_max_splited_trade_unit")
        logging.info("end generate policy list")

    @staticmethod
    def generate_policy_list_impl(prefer_max_splited_trade_unit, prefer_max_stock_count, repeated_policy):
        PolicyFactory.generate_policy_list_for_percent(prefer_max_splited_trade_unit, prefer_max_stock_count, repeated_policy)

    @staticmethod
    def generate_policy_list_for_percent(prefer_max_splited_trade_unit, prefer_max_stock_count, repeated_policy):
        logging.debug("begin generate_policy_list_for_percent")
        for buy_days_watch in localconfig.BUY_WATCH_DAYS_LIST:
            for sell_days_watch in localconfig.SELL_WATCH_DAYS_LIST:
                for buy_mode in localconfig.BUY_MODE_LIST:
                    for buy_percent_n in localconfig.BUY_PRICE_PERCENT_LIST:
                        for sell_mode in localconfig.SELL_MODE_LIST:
                            for sell_loss_thousandth in localconfig.LOSS_STOP_THOUSANDTH_LIST:
                                for sell_percent_n in localconfig.SELL_PRICE_PERCENT_LIST:
                                    policy = repeated_policy.add()
                                    policy.id = "buy_days_watch:%s,sell_days_watch:%s,buy_percent_n:%s,sell_percent_n:%s,buy_mode:%s,sell_mode:%s,loss_stop_thousandth:%s" % (
                                        buy_days_watch, sell_days_watch, buy_percent_n, sell_percent_n, buy_mode, sell_mode, sell_loss_thousandth)
                                    policy.prefer_max_splited_trade_unit = prefer_max_splited_trade_unit
                                    policy.prefer_max_stock_count = prefer_max_stock_count
                                    policy.buy.days_watch = buy_days_watch
                                    policy.buy.at_percent.mode = buy_mode
                                    policy.buy.at_percent.percent_n = buy_percent_n
                                    policy.sell.days_watch = sell_days_watch
                                    policy.sell.at_percent.mode = sell_mode
                                    policy.sell.at_percent.percent_n = sell_percent_n
                                    policy.sell.sell_at_loss_thousandth = sell_loss_thousandth
                                for sell_profit_thousandth_n in localconfig.SELL_PROFIT_THOUSANDTH_LIST:
                                    policy = repeated_policy.add()
                                    policy.id = "buy_days_watch:%s,sell_days_watch:%s,buy_percent_n:%s,sell_profit_thousandth_n:%s,buy_mode:%s,sell_mode:%s,loss_stop_thousandth:%s" % (
                                        buy_days_watch, sell_days_watch, buy_percent_n, sell_profit_thousandth_n, buy_mode, sell_mode, sell_loss_thousandth)
                                    policy.prefer_max_splited_trade_unit = prefer_max_splited_trade_unit
                                    policy.prefer_max_stock_count = prefer_max_stock_count
                                    policy.buy.days_watch = buy_days_watch
                                    policy.buy.at_percent.mode = buy_mode
                                    policy.buy.at_percent.percent_n = buy_percent_n
                                    policy.sell.days_watch = sell_days_watch
                                    policy.sell.at_percent.mode = sell_mode
                                    policy.sell.sell_at_profit_thousandth = sell_profit_thousandth_n
                                    policy.sell.sell_at_loss_thousandth = sell_loss_thousandth
        logging.debug("end generate_policy_list_for_percent")


if __name__ == "__main__":
    person = Person()
    PolicyFactory.generate_policy_list(person.policy_info)
    print person.policy_info