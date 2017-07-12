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
BUY_PRICE_PERCENT = "buy_price_percent"
SELL_PRICE_PERCENT = "sell_price_percent"
BUY_TREND_PERCENT = "buy_trend_percent"
SELL_TREND_PERCENT = "sell_trend_percent"
LOSS_STOP_THOUSANDTH = "loss_stop_thousandth"
HALF_BUY_TREND_PERCENT = "half_buy_trend_percent"
HALF_SELL_TREND_PERCENT = "half_sell_trend_percent"
PREFER_MAX_SPLITED_TRADE_UNIT = "prefer_max_splited_trade_unit"
PREFER_MAX_STOCK_COUNT = "prefer_max_stock_count"
LAST_BUY_SEQUENTIAL_TREND_COUNT = "last_buy_sequential_trend_count"
LAST_SELL_SEQUENTIAL_TREND_COUNT = "last_sell_sequential_trend_count"
TREND_MODE = "trend_mode"
MIN_STOCK_PRICE = "min_stock_price"
SELL_PROFIT_THOUSANDTH = "sell_profit_thousandth"
BUY_TREND_PERCENT = "buy_trend_percent"



class PolicyItem:
    def __init__(self, current_policy_dict):
        for item_type, item_value in current_policy_dict.iteritems():
            setattr(self, item_type, item_value)

    def build_policy(self, policy):
        policy.prefer_max_splited_trade_unit = getattr(self, PREFER_MAX_SPLITED_TRADE_UNIT)
        policy.prefer_max_stock_count = getattr(self, PREFER_MAX_STOCK_COUNT)
        policy.min_stock_price = getattr(self, MIN_STOCK_PRICE)
        policy.buy.days_watch = getattr(self, BUY_DAYS_WATCH)
        policy.buy.at_percent.mode = getattr(self, BUY_MODE)
        policy.buy.at_percent.percent_n = getattr(self, BUY_PRICE_PERCENT)
        policy.buy.trend.growth_percent = getattr(self, BUY_TREND_PERCENT)
        policy.buy.trend.half_trend_percent = getattr(self, HALF_BUY_TREND_PERCENT)
        policy.buy.trend.last_sequential_trend_count = getattr(self, LAST_BUY_SEQUENTIAL_TREND_COUNT)
        policy.buy.trend.trend_mode = getattr(self, TREND_MODE)
        policy.sell.days_watch = getattr(self, SELL_DAYS_WATCH)
        policy.sell.at_percent.mode = getattr(self, SELL_MODE)
        policy.sell.at_percent.percent_n = getattr(self, SELL_PRICE_PERCENT)
        policy.sell.sell_at_loss_thousandth = getattr(self, LOSS_STOP_THOUSANDTH)
        policy.sell.days_hold_for_sell = getattr(self, DAYS_HOLD_FOR_SELL)
        policy.sell.trend.growth_percent = getattr(self, SELL_TREND_PERCENT)
        policy.sell.trend.half_trend_percent = getattr(self, HALF_SELL_TREND_PERCENT)
        policy.sell.trend.last_sequential_trend_count = getattr(self, LAST_SELL_SEQUENTIAL_TREND_COUNT)
        policy.sell.trend.trend_mode = getattr(self, TREND_MODE)
        policy.sell.sell_at_profit_thousandth = getattr(self, SELL_PROFIT_THOUSANDTH)
        policy.id = self.build_policy_id()
        logging.info("build policy:%s", policy.id)


    def build_policy_id(self):
        result = []
        for attr in PolicyFactory.policy_value_dict.keys():
            result.append("%s:%s" % (attr, getattr(self, attr)))
        return ",".join(result)


    @staticmethod
    def build(repeated_policy, current_policy_dict):
        if len(current_policy_dict) < len(PolicyFactory.policy_value_dict):
            for k,v in PolicyFactory.policy_value_dict.iteritems():
                if k in current_policy_dict:
                    continue
                best_item = v.best
                if isinstance(best_item, list):
                    current_policy_dict[k] = best_item[0]
                    # # TODO: iterate all best
                    # for item in best_item:
                    #     current_policy_dict[k] = item
                    #     PolicyItem.build(repeated_policy, dict(current_policy_dict))
                else:
                    current_policy_dict[k] = best_item
        policy_item = PolicyItem(current_policy_dict)
        policy_item.build_policy(repeated_policy.add())



class PolicyFactory:
    # [policy_key] = [policy_value]
    policy_value_dict = {
        BUY_DAYS_WATCH: localconfig.BUY_WATCH_DAYS,
        SELL_DAYS_WATCH: localconfig.SELL_WATCH_DAYS,
        DAYS_HOLD_FOR_SELL: localconfig.DAYS_HOLD_FOR_SALE,
        BUY_MODE: localconfig.BUY_MODE,
        SELL_MODE: localconfig.SELL_MODE,
        BUY_PRICE_PERCENT: localconfig.BUY_PRICE_PERCENT,
        SELL_PRICE_PERCENT: localconfig.SELL_PRICE_PERCENT,
        BUY_TREND_PERCENT: localconfig.BUY_TREND_PERCENT,
        SELL_TREND_PERCENT: localconfig.SELL_TREND_PERCENT,
        LOSS_STOP_THOUSANDTH: localconfig.LOSS_STOP_THOUSANDTH,
        HALF_BUY_TREND_PERCENT: localconfig.HALF_BUY_TREND_PERCENT,
        HALF_SELL_TREND_PERCENT: localconfig.HALF_SELL_TREND_PERCENT,
        LAST_BUY_SEQUENTIAL_TREND_COUNT: localconfig.LAST_BUY_SEQUENTIAL_TREND_COUNT,
        LAST_SELL_SEQUENTIAL_TREND_COUNT: localconfig.LAST_SELL_SEQUENTIAL_TREND_COUNT,
        TREND_MODE: localconfig.TREND_MODE,
        PREFER_MAX_SPLITED_TRADE_UNIT: localconfig.PREFER_MAX_SPLITED_TRADE_UNIT,
        PREFER_MAX_STOCK_COUNT: localconfig.PREFER_MAX_STOCK_COUNT,
        MIN_STOCK_PRICE: localconfig.MIN_STOCK_PRICE,
        SELL_PROFIT_THOUSANDTH: localconfig.SELL_PROFIT_THOUSANDTH
    }


    @staticmethod
    # repeated_policy: repated Policy
    def generate_policy_list(repeated_policy):
        logging.info("begin generate policy list")
        PolicyFactory.generate_policy_list_impl_auto(repeated_policy)
        # for prefer_max_splited_trade_unit in [1]:
        #     logging.debug("begin generate policy list for prefer_max_splited_trade_unit:%s", prefer_max_splited_trade_unit)
        #     for prefer_max_stock_count in [1]:
        #         logging.debug("begin generate policy list for prefer_max_splited_trade_unit:%s, prefer_max_stock_count:%s",
        #                      prefer_max_splited_trade_unit, prefer_max_stock_count)
        #         PolicyFactory.generate_policy_list_impl(prefer_max_splited_trade_unit, prefer_max_stock_count, repeated_policy)
        #         logging.debug("end generate policy list for prefer_max_splited_trade_unit:%s, prefer_max_stock_count:%s",
        #                      prefer_max_splited_trade_unit, prefer_max_stock_count)
        #     logging.debug("end generate policy list for prefer_max_splited_trade_unit")
        logging.info("end generate policy list")

    # @staticmethod
    # def generate_policy_list_impl(prefer_max_splited_trade_unit, prefer_max_stock_count, repeated_policy):
    #     PolicyFactory.generate_policy_list_for_percent(prefer_max_splited_trade_unit, prefer_max_stock_count, repeated_policy)


    @staticmethod
    def generate_policy_list_impl_auto(repeated_policy):
        for policy_type, item_value in PolicyFactory.policy_value_dict.iteritems():
            assert isinstance(item_value.range, list)
            PolicyFactory.generate_policy_list_impl_for_policy_type(repeated_policy, policy_type, item_value.range)


    @staticmethod
    def generate_policy_list_impl_for_policy_type(repeated_policy, policy_type, policy_value_list):
        for policy_value in policy_value_list:
            PolicyItem.build(repeated_policy, {policy_type: policy_value})

    # @staticmethod
    # def generate_policy_list_for_percent(prefer_max_splited_trade_unit, prefer_max_stock_count, repeated_policy):
    #     logging.debug("begin generate_policy_list_for_percent")
    #     for buy_percent_n in localconfig.BUY_PRICE_PERCENT:
    #         for sell_loss_thousandth in localconfig.LOSS_STOP_THOUSANDTH_LIST:
    #             buy_days_watch = 20
    #             sell_days_watch = 10
    #             days_hold_for_sell = 5
    #             buy_mode = Policy.TradePolicy.Percent.LOW
    #             sell_mode = Policy.TradePolicy.Percent.HIGH
    #             HALF_BUY_TREND_PERCENT = localconfig.DEFAULT_CONFIG
    #             HALF_SELL_TREND_PERCENT = localconfig.DEFAULT_CONFIG
    #             BUY_TREND_PERCENT = localconfig.DEFAULT_CONFIG
    #             SELL_TREND_RERCENT = localconfig.DEFAULT_CONFIG
    #             LAST_BUY_SEQUENTIAL_TREND_COUNT = localconfig.DEFAULT_CONFIG
    #             LAST_SELL_SEQUENTIAL_TREND_COUNT = localconfig.DEFAULT_CONFIG
    #             trend_mode = Policy.TradePolicy.Percent.HIGH
    #
    #             for sell_percent_n in localconfig.SELL_PRICE_PERCENT_LIST:
    #                 policy = repeated_policy.add()
    #                 policy.id = "buy_days_watch:%s,sell_days_watch:%s,days_hold_for_sell:%s,"  \
    #                             "buy_percent_n:%s,sell_percent_n:%s,buy_mode:%s,sell_mode:%s,"  \
    #                             "loss_stop_thousandth:%s,buy_growth:%s,sell_growth:%s,"  \
    #                             "half_buy_growth:%s,half_sell_growth:%s," \
    #                             "LAST_BUY_SEQUENTIAL_TREND_COUNT:%s,LAST_SELL_SEQUENTIAL_TREND_COUNT:%s" % (
    #                     buy_days_watch, sell_days_watch, days_hold_for_sell,
    #                     buy_percent_n, sell_percent_n, buy_mode, sell_mode,
    #                     sell_loss_thousandth, BUY_TREND_PERCENT, SELL_TREND_RERCENT,
    #                     HALF_BUY_TREND_PERCENT, HALF_SELL_TREND_PERCENT,
    #                     LAST_BUY_SEQUENTIAL_TREND_COUNT,LAST_SELL_SEQUENTIAL_TREND_COUNT
    #                 )
    #
    #
    #                 # set_attr(object, attr_name, policy_key_name)
    #
    #                 policy.prefer_max_splited_trade_unit = prefer_max_splited_trade_unit
    #                 policy.prefer_max_stock_count = prefer_max_stock_count
    #                 policy.buy.days_watch = buy_days_watch
    #                 policy.buy.at_percent.mode = buy_mode
    #                 policy.buy.at_percent.percent_n = buy_percent_n
    #                 policy.buy.trend.growth_percent = BUY_TREND_PERCENT
    #                 policy.buy.trend.half_trend_percent = HALF_BUY_TREND_PERCENT
    #                 policy.buy.trend.last_sequential_trend_count = LAST_BUY_SEQUENTIAL_TREND_COUNT
    #                 policy.buy.trend.trend_mode = trend_mode
    #                 policy.sell.days_watch = sell_days_watch
    #                 policy.sell.at_percent.mode = sell_mode
    #                 policy.sell.at_percent.percent_n = sell_percent_n
    #                 policy.sell.sell_at_loss_thousandth = sell_loss_thousandth
    #                 policy.sell.days_hold_for_sell = days_hold_for_sell
    #                 policy.sell.trend.growth_percent = SELL_TREND_RERCENT
    #                 policy.sell.trend.half_trend_percent = HALF_SELL_TREND_PERCENT
    #                 policy.sell.trend.last_sequential_trend_count = LAST_SELL_SEQUENTIAL_TREND_COUNT
    #                 policy.sell.trend.trend_mode = trend_mode
    #
    #             for sell_profit_thousandth_n in localconfig.SELL_PROFIT_THOUSANDTH:
    #                 policy = repeated_policy.add()
    #                 policy.id = "buy_days_watch:%s,sell_days_watch:%s,days_hold_for_sell:%s,"  \
    #                             "buy_percent_n:%s,sell_profit_thousandth_n:%s,buy_mode:%s,"  \
    #                             "sell_mode:%s,loss_stop_thousandth:%s,buy_growth:%s,sell_growth:%s," \
    #                             "half_buy_growth:%s,half_sell_growth:%s," \
    #                             "LAST_BUY_SEQUENTIAL_TREND_COUNT:%s,LAST_SELL_SEQUENTIAL_TREND_COUNT:%s" % (
    #                                 buy_days_watch, sell_days_watch, days_hold_for_sell,
    #                                 buy_percent_n, sell_profit_thousandth_n, buy_mode,
    #                                 sell_mode, sell_loss_thousandth, BUY_TREND_PERCENT,
    #                                 SELL_TREND_RERCENT,
    #                                 HALF_BUY_TREND_PERCENT, HALF_SELL_TREND_PERCENT,
    #                                 LAST_BUY_SEQUENTIAL_TREND_COUNT, LAST_SELL_SEQUENTIAL_TREND_COUNT
    #                 )
    #                 policy.prefer_max_splited_trade_unit = prefer_max_splited_trade_unit
    #                 policy.prefer_max_stock_count = prefer_max_stock_count
    #                 policy.buy.days_watch = buy_days_watch
    #                 policy.buy.at_percent.mode = buy_mode
    #                 policy.buy.at_percent.percent_n = buy_percent_n
    #                 policy.buy.trend.growth_percent = BUY_TREND_PERCENT
    #                 policy.buy.trend.half_trend_percent = HALF_BUY_TREND_PERCENT
    #                 policy.buy.trend.last_sequential_trend_count = LAST_BUY_SEQUENTIAL_TREND_COUNT
    #                 policy.buy.trend.trend_mode = trend_mode
    #                 policy.sell.days_watch = sell_days_watch
    #                 policy.sell.at_percent.mode = sell_mode
    #                 policy.sell.sell_at_profit_thousandth = sell_profit_thousandth_n
    #                 policy.sell.sell_at_loss_thousandth = sell_loss_thousandth
    #                 policy.sell.days_hold_for_sell = days_hold_for_sell
    #                 policy.sell.trend.growth_percent = SELL_TREND_RERCENT
    #                 policy.sell.trend.half_trend_percent = HALF_SELL_TREND_PERCENT
    #                 policy.sell.trend.last_sequential_trend_count = LAST_SELL_SEQUENTIAL_TREND_COUNT
    #                 policy.sell.trend.trend_mode = trend_mode
    #     logging.debug("end generate_policy_list_for_percent")
    #

if __name__ == "__main__":
    person = Person()
    PolicyFactory.generate_policy_list(person.policy_info)
    print person.policy_info