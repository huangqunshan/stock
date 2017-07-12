# coding=utf8

import logging

import localconfig
from proto.person_pb2 import Person
from proto.policy_pb2 import Policy
import random


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
PREFER_MAX_SPLITED_TRADE_UNIT = "prefer_max_splited_trade_unit"
PREFER_MAX_STOCK_COUNT = "prefer_max_stock_count"
LAST_BUY_SEQUENTIAL_TREND_COUNT = "last_buy_sequential_trend_count"
LAST_SELL_SEQUENTIAL_TREND_COUNT = "last_sell_sequential_trend_count"
TREND_MODE = "trend_mode"
MIN_STOCK_PRICE = "min_stock_price"
SELL_PROFIT_THOUSANDTH = "sell_profit_thousandth"
BUY_TREND_PERCENT = "buy_trend_percent"
BUY_TREND_DAYS_WATCH = "buy_trend_days_watch"
SELL_TREND_DAYS_WATCH = "sell_trend_days_watch"



class PolicyItem:
    def __init__(self, current_policy_dict):
        self.current_policy_dict = current_policy_dict
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
        policy.buy.trend.last_sequential_trend_count = getattr(self, LAST_BUY_SEQUENTIAL_TREND_COUNT)
        policy.buy.trend.trend_mode = getattr(self, TREND_MODE)
        policy.buy.trend.days_watch = getattr(self, BUY_TREND_DAYS_WATCH)
        policy.sell.days_watch = getattr(self, SELL_DAYS_WATCH)
        policy.sell.at_percent.mode = getattr(self, SELL_MODE)
        policy.sell.at_percent.percent_n = getattr(self, SELL_PRICE_PERCENT)
        policy.sell.sell_at_loss_thousandth = getattr(self, LOSS_STOP_THOUSANDTH)
        policy.sell.days_hold_for_sell = getattr(self, DAYS_HOLD_FOR_SELL)
        policy.sell.trend.growth_percent = getattr(self, SELL_TREND_PERCENT)
        policy.sell.trend.last_sequential_trend_count = getattr(self, LAST_SELL_SEQUENTIAL_TREND_COUNT)
        policy.sell.trend.trend_mode = getattr(self, TREND_MODE)
        policy.sell.trend.days_watch = getattr(self, SELL_TREND_DAYS_WATCH)
        policy.sell.sell_at_profit_thousandth = getattr(self, SELL_PROFIT_THOUSANDTH)
        policy.id = self.build_policy_id()
        logging.info("build policy:%s", policy.id)


    def build_policy_id(self):
        result = []
        for attr in self.current_policy_dict.keys():
            result.append("%s:%s" % (attr, getattr(self, attr)))
        return ",".join(result)


    @staticmethod
    def build(repeated_policy, current_policy_dict, partial_policy_set, full_policy_set):
        if str(current_policy_dict) in partial_policy_set:
            return
        partial_policy_set.add(str(current_policy_dict))
        if len(current_policy_dict) == len(PolicyFactory.policy_value_dict):
            PolicyItem.build_core(repeated_policy, current_policy_dict, partial_policy_set, full_policy_set)
            return
        assert len(current_policy_dict) < len(PolicyFactory.policy_value_dict)
        for k,v in PolicyFactory.policy_value_dict.iteritems():
            if len(PolicyFactory.policy_value_dict) <= len(current_policy_dict):
                break
            if k in current_policy_dict:
                continue
            best_item = v.best
            if isinstance(best_item, list):
                if 1 < len(best_item) and False:
                    for item in best_item:
                        current_policy_dict[k] = item
                        if len(current_policy_dict) < len(PolicyFactory.policy_value_dict):
                            # 必须拷贝而非直接修改
                            PolicyItem.build(repeated_policy, dict(current_policy_dict), partial_policy_set, full_policy_set)
                        else:
                            PolicyItem.build_core(repeated_policy, current_policy_dict, partial_policy_set, full_policy_set)
                else:
                    assert best_item
                    # 取random
                    current_policy_dict[k] = best_item[int(random.random()*100) % len(best_item)]
                    if len(current_policy_dict) == len(PolicyFactory.policy_value_dict):
                        PolicyItem.build_core(repeated_policy, current_policy_dict, partial_policy_set, full_policy_set)
                        return
            else:
                current_policy_dict[k] = best_item
                if len(current_policy_dict) == len(PolicyFactory.policy_value_dict):
                    PolicyItem.build_core(repeated_policy, current_policy_dict, partial_policy_set, full_policy_set)
                    return



    @staticmethod
    def build_core(repeated_policy, current_policy_dict, partial_policy_set, full_policy_set):
        if str(current_policy_dict) in partial_policy_set:
            return
        partial_policy_set.add(str(current_policy_dict))
        assert len(current_policy_dict) == len(PolicyFactory.policy_value_dict)
        if str(current_policy_dict) not in full_policy_set:
            policy_item = PolicyItem(current_policy_dict)
            # 判断policy_id是考虑到str(current_policy_dict)可能是无序的
            policy_id = policy_item.build_policy_id()
            if policy_id in full_policy_set:
                return
            policy = repeated_policy.add()
            policy_item.build_policy(policy)
            full_policy_set.add(str(current_policy_dict))
            full_policy_set.add(policy_id)


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
        LAST_BUY_SEQUENTIAL_TREND_COUNT: localconfig.LAST_BUY_SEQUENTIAL_TREND_COUNT,
        LAST_SELL_SEQUENTIAL_TREND_COUNT: localconfig.LAST_SELL_SEQUENTIAL_TREND_COUNT,
        TREND_MODE: localconfig.TREND_MODE,
        PREFER_MAX_SPLITED_TRADE_UNIT: localconfig.PREFER_MAX_SPLITED_TRADE_UNIT,
        PREFER_MAX_STOCK_COUNT: localconfig.PREFER_MAX_STOCK_COUNT,
        MIN_STOCK_PRICE: localconfig.MIN_STOCK_PRICE,
        SELL_PROFIT_THOUSANDTH: localconfig.SELL_PROFIT_THOUSANDTH,
        BUY_TREND_DAYS_WATCH: localconfig.BUY_TREND_DAYS_WATCH,
        SELL_TREND_DAYS_WATCH: localconfig.SELL_TREND_DAYS_WATCH
    }


    @staticmethod
    def generate_policy_list(repeated_policy):
        logging.info("begin generate policy list")
        PolicyFactory.generate_policy_list_impl_auto(repeated_policy)
        logging.info("end generate policy list")


    @staticmethod
    def generate_policy_list_impl_auto(repeated_policy):
        for policy_type, item_value in PolicyFactory.policy_value_dict.iteritems():
            assert isinstance(item_value.range, list)
            PolicyFactory.generate_policy_list_impl_for_policy_type(repeated_policy, policy_type, item_value.range)


    @staticmethod
    def generate_policy_list_impl_for_policy_type(repeated_policy, policy_type, policy_value_list):
        policy_str_set = set()
        policy_id_set = set()
        for policy_value in policy_value_list:
            PolicyItem.build(repeated_policy, {policy_type: policy_value}, policy_str_set, policy_id_set)


if __name__ == "__main__":
    person = Person()
    PolicyFactory.generate_policy_list(person.policy_info)
    print person.policy_info