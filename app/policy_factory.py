# coding=utf8

import logging

import localconfig
from proto.person_pb2 import Person
from proto.policy_pb2 import Policy


class PolicyFactory:
    # [policy_key] = [policy_value]


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
        for buy_percent_n in localconfig.BUY_PRICE_PERCENT_LIST:
            for sell_loss_thousandth in localconfig.LOSS_STOP_THOUSANDTH_LIST:
                buy_days_watch = 20
                sell_days_watch = 10
                days_hold_for_sell = 2
                buy_mode = Policy.TradePolicy.Percent.LOW
                sell_mode = Policy.TradePolicy.Percent.HIGH
                last_half_buy_grow_percent_n = -1
                last_half_sell_grow_percent_n = -1
                buy_grow_percent_n = -1
                sell_grow_percent_n = -1
                last_sequential_buy_trend = -1
                last_sequential_sell_trend = -1
                trend_mode = Policy.TradePolicy.Percent.MEDIUM

                for sell_percent_n in localconfig.SELL_PRICE_PERCENT_LIST:
                    policy = repeated_policy.add()
                    policy.id = "buy_days_watch:%s,sell_days_watch:%s,days_hold_for_sell:%s,"  \
                                "buy_percent_n:%s,sell_percent_n:%s,buy_mode:%s,sell_mode:%s,"  \
                                "loss_stop_thousandth:%s,buy_growth:%s,sell_growth:%s,"  \
                                "half_buy_growth:%s,half_sell_growth:%s," \
                                "last_sequential_buy_trend:%s,last_sequential_sell_trend:%s" % (
                        buy_days_watch, sell_days_watch, days_hold_for_sell,
                        buy_percent_n, sell_percent_n, buy_mode, sell_mode,
                        sell_loss_thousandth, buy_grow_percent_n, sell_grow_percent_n,
                        last_half_buy_grow_percent_n, last_half_sell_grow_percent_n,
                        last_sequential_buy_trend,last_sequential_sell_trend
                    )

                    # policy_key_dict = {
                    #     "buy_days_watch": localconfig.BUY_WATCH_DAYS_LIST,
                    #     "sell_days_watch": localconfig.SELL_WATCH_DAYS_LIST,
                    #     "days_hold_for_sell": localconfig.DAYS_HOLD_FOR_SALE_LIST,
                    #     "buy_mode": localconfig.BUY_MODE_LIST,
                    #     "sell_mode": localconfig.SELL_MODE_LIST,
                    #     "buy_percent_n": localconfig.BUY_PRICE_PERCENT_LIST,
                    #     "buy_grow_percent_n": [-1],
                    #     "sell_grow_percent_n": [-1],
                    #     "sell_loss_thousandth": localconfig.LOSS_STOP_THOUSANDTH_LIST,
                    #     "last_half_buy_grow_percent_n": [-1],
                    #     "last_half_sell_grow_percent_n": [-1],
                    #     "sell_percent_n": localconfig.SELL_PRICE_PERCENT_LIST,
                    # }
                    #
                    # set_attr(object, attr_name, policy_key_name)

                    policy.prefer_max_splited_trade_unit = prefer_max_splited_trade_unit
                    policy.prefer_max_stock_count = prefer_max_stock_count
                    policy.buy.days_watch = buy_days_watch
                    policy.buy.at_percent.mode = buy_mode
                    policy.buy.at_percent.percent_n = buy_percent_n
                    policy.buy.trend.growth_percent = buy_grow_percent_n
                    policy.buy.trend.growth_percent_last_half = last_half_buy_grow_percent_n
                    policy.buy.trend.last_sequential_growth_percent = last_sequential_buy_trend
                    policy.buy.trend.trend_mode = trend_mode
                    policy.sell.days_watch = sell_days_watch
                    policy.sell.at_percent.mode = sell_mode
                    policy.sell.at_percent.percent_n = sell_percent_n
                    policy.sell.sell_at_loss_thousandth = sell_loss_thousandth
                    policy.sell.days_hold_for_sell = days_hold_for_sell
                    policy.sell.trend.growth_percent = sell_grow_percent_n
                    policy.sell.trend.growth_percent_last_half = last_half_sell_grow_percent_n
                    policy.sell.trend.last_sequential_growth_percent = last_sequential_sell_trend
                    policy.sell.trend.trend_mode = trend_mode

                for sell_profit_thousandth_n in localconfig.SELL_PROFIT_THOUSANDTH_LIST:
                    policy = repeated_policy.add()
                    policy.id = "buy_days_watch:%s,sell_days_watch:%s,days_hold_for_sell:%s,"  \
                                "buy_percent_n:%s,sell_profit_thousandth_n:%s,buy_mode:%s,"  \
                                "sell_mode:%s,loss_stop_thousandth:%s,buy_growth:%s,sell_growth:%s," \
                                "half_buy_growth:%s,half_sell_growth:%s," \
                                "last_sequential_buy_trend:%s,last_sequential_sell_trend:%s" % (
                                    buy_days_watch, sell_days_watch, days_hold_for_sell,
                                    buy_percent_n, sell_profit_thousandth_n, buy_mode,
                                    sell_mode, sell_loss_thousandth, buy_grow_percent_n,
                                    sell_grow_percent_n,
                                    last_half_buy_grow_percent_n, last_half_sell_grow_percent_n,
                                    last_sequential_buy_trend, last_sequential_sell_trend
                    )
                    policy.prefer_max_splited_trade_unit = prefer_max_splited_trade_unit
                    policy.prefer_max_stock_count = prefer_max_stock_count
                    policy.buy.days_watch = buy_days_watch
                    policy.buy.at_percent.mode = buy_mode
                    policy.buy.at_percent.percent_n = buy_percent_n
                    policy.buy.trend.growth_percent = buy_grow_percent_n
                    policy.buy.trend.growth_percent_last_half = last_half_buy_grow_percent_n
                    policy.buy.trend.last_sequential_growth_percent = last_sequential_buy_trend
                    policy.buy.trend.trend_mode = trend_mode
                    policy.sell.days_watch = sell_days_watch
                    policy.sell.at_percent.mode = sell_mode
                    policy.sell.sell_at_profit_thousandth = sell_profit_thousandth_n
                    policy.sell.sell_at_loss_thousandth = sell_loss_thousandth
                    policy.sell.days_hold_for_sell = days_hold_for_sell
                    policy.sell.trend.growth_percent = sell_grow_percent_n
                    policy.sell.trend.growth_percent_last_half = last_half_sell_grow_percent_n
                    policy.sell.trend.last_sequential_growth_percent = last_sequential_sell_trend
                    policy.sell.trend.trend_mode = trend_mode
        logging.debug("end generate_policy_list_for_percent")


if __name__ == "__main__":
    person = Person()
    PolicyFactory.generate_policy_list(person.policy_info)
    print person.policy_info