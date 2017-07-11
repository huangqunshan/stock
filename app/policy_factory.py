# coding=utf8

import logging

import localconfig
from proto.person_pb2 import Person
from proto.policy_pb2 import Policy


BUY_DAYS_WATCH = "buy_days_watch"
SELL_DAYS_WATCH = "sell_days_watch"
DAYS_HOLD_FOR_SELL = "days_hold_for_sell"
BUY_MODE = "buy_mode"
SELL_MODE = "sell_mode"
BUY_PERCENT_N = "buy_percent_n"
SELL_PERCENT_N = "sell_percent_n"
BUY_GROW_PERCENT_N = "buy_grow_percent_n"
SELL_GROW_PERCENT_N = "sell_grow_percent_n"
SELL_LOSS_THOUSANDTH = "sell_loss_thousandth"
LAST_HALF_BUY_GROW_PERCENT_N = "last_half_buy_grow_percent_n"
LAST_HALF_SELL_GROW_PERCENT_N = "last_half_sell_grow_percent_n"
PREFER_MAX_SPLITED_TRADE_UNIT = "prefer_max_splited_trade_unit"
PREFER_MAX_STOCK_COUNT = "prefer_max_stock_count"
LAST_SEQUENTIAL_BUY_TREND = "last_sequential_buy_trend"
LAST_SEQUENTIAL_SELL_TREND = "last_sequential_sell_trend"
TREND_MODE = "trend_mode"


class PolicyItem:
    def __init__(self, current_policy_dict):
        for item_type, item_value in current_policy_dict:
            setattr(self, item_type, item_value)

    def build_policy(self, policy):
        policy.prefer_max_splited_trade_unit = getattr(self, PREFER_MAX_SPLITED_TRADE_UNIT)
        policy.prefer_max_stock_count = getattr(self, PREFER_MAX_STOCK_COUNT)
        policy.buy.days_watch = getattr(self, BUY_DAYS_WATCH)
        policy.buy.at_percent.mode = getattr(self, BUY_MODE)
        policy.buy.at_percent.percent_n = getattr(self, BUY_PERCENT_N)
        policy.buy.trend.growth_percent = getattr(self, BUY_GROW_PERCENT_N)
        policy.buy.trend.growth_percent_last_half = getattr(self, LAST_HALF_BUY_GROW_PERCENT_N)
        policy.buy.trend.last_sequential_growth_percent = getattr(self, LAST_SEQUENTIAL_BUY_TREND)
        policy.buy.trend.trend_mode = getattr(self, TREND_MODE)
        policy.sell.days_watch = getattr(self, SELL_DAYS_WATCH)
        policy.sell.at_percent.mode = getattr(self, SELL_MODE)
        policy.sell.at_percent.percent_n = getattr(self, SELL_PERCENT_N)
        policy.sell.sell_at_loss_thousandth = getattr(self, SELL_LOSS_THOUSANDTH)
        policy.sell.days_hold_for_sell = getattr(self, DAYS_HOLD_FOR_SELL)
        policy.sell.trend.growth_percent = getattr(self, SELL_GROW_PERCENT_N)
        policy.sell.trend.growth_percent_last_half = getattr(self, LAST_HALF_SELL_GROW_PERCENT_N)
        policy.sell.trend.last_sequential_growth_percent = getattr(self, LAST_SEQUENTIAL_SELL_TREND)
        policy.sell.trend.trend_mode = getattr(self, TREND_MODE)


    @staticmethod
    def build(repeated_policy, policy_type, policy_value):
        PolicyItem.build_internal(repeated_policy, {policy_type: policy_value})


    @staticmethod
    def build_internal(repeated_policy, current_policy_dict):
        if len(current_policy_dict) < len(PolicyFactory.policy_value_dict):
            for k,v in PolicyFactory.policy_value_dict.iteritems():
                if k in current_policy_dict:
                    continue
                if isinstance(v, list):
                    # TODO: just pick first one here
                    current_policy_dict.set(k, v[0])
                else:
                    current_policy_dict.set(k, v)
        policy_item = PolicyItem(current_policy_dict)
        policy = repeated_policy.add()
        policy_item.build_policy(policy)


class PolicyFactory:
    # [policy_key] = [policy_value]
    policy_value_dict = {}
    policy_value_dict = {
        BUY_DAYS_WATCH: localconfig.BUY_WATCH_DAYS_LIST,
        SELL_DAYS_WATCH: localconfig.SELL_WATCH_DAYS_LIST,
        DAYS_HOLD_FOR_SELL: localconfig.DAYS_HOLD_FOR_SALE_LIST,
        BUY_MODE: localconfig.BUY_MODE_LIST,
        SELL_MODE: localconfig.SELL_MODE_LIST,
        BUY_PERCENT_N: localconfig.BUY_PRICE_PERCENT_LIST,
        SELL_PERCENT_N: localconfig.SELL_PRICE_PERCENT_LIST,
        BUY_GROW_PERCENT_N: localconfig.LAST_BUY_SEQUENTIAL_TREND_LIST,
        SELL_GROW_PERCENT_N: localconfig.LAST_SELL_SEQUENTIAL_TREND_LIST,
        SELL_LOSS_THOUSANDTH: localconfig.LOSS_STOP_THOUSANDTH_LIST,
        LAST_HALF_BUY_GROW_PERCENT_N: localconfig.LAST_HALF_BUY_TREND_GROW_PERCENT_LIST,
        LAST_HALF_SELL_GROW_PERCENT_N: localconfig.LAST_HALF_SELL_TREND_GROW_PERCENT_LIST,
        LAST_SEQUENTIAL_BUY_TREND: localconfig.LAST_BUY_SEQUENTIAL_TREND_LIST,
        LAST_SEQUENTIAL_SELL_TREND: localconfig.LAST_SELL_SEQUENTIAL_TREND_LIST,
        TREND_MODE: localconfig.TREND_MODE_LIST
    }

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
    def generate_policy_list_impl_auto(repeated_policy):
        for policy_type, item_value in PolicyFactory.policy_value_dict().iteritems():
            Policy.generate_policy_list_impl_for_policy_type(repeated_policy, policy_type)
            return


    @staticmethod
    def generate_policy_list_impl_for_policy_type(repeated_policy, policy_type):
        for policy_value in PolicyFactory.policy_value_dict.get(policy_type):
            PolicyFactory.build_policy_item(repeated_policy, policy_type, policy_value)


    @staticmethod
    def build_policy_item(repeated_policy, policy_type, policy_value):
        if isinstance(policy_value, list):
            for policy_value_item in policy_value:
                PolicyItem.build(repeated_policy, policy_type, policy_value_item)
        else:
            PolicyItem.build(repeated_policy, policy_type, policy_value)


    @staticmethod
    def generate_policy_list_for_percent(prefer_max_splited_trade_unit, prefer_max_stock_count, repeated_policy):
        logging.debug("begin generate_policy_list_for_percent")
        for buy_percent_n in localconfig.BUY_PRICE_PERCENT_LIST:
            for sell_loss_thousandth in localconfig.LOSS_STOP_THOUSANDTH_LIST:
                buy_days_watch = 20
                sell_days_watch = 10
                days_hold_for_sell = 5
                buy_mode = Policy.TradePolicy.Percent.LOW
                sell_mode = Policy.TradePolicy.Percent.HIGH
                last_half_buy_grow_percent_n = -1
                last_half_sell_grow_percent_n = -1
                buy_grow_percent_n = -1
                sell_grow_percent_n = -1
                last_sequential_buy_trend = -1
                last_sequential_sell_trend = -1
                trend_mode = Policy.TradePolicy.Percent.HIGH

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