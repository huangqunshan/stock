# coding=utf8

import logging

import localconfig
from proto.person_pb2 import Person
from proto.policy_pb2 import Policy
import random
import hashlib


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
LAST_CLOSE_PRICE_PERCENT = "last_close_price_percent"



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
        policy.buy.last_close_price_percent = getattr(self, LAST_CLOSE_PRICE_PERCENT)
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
        policy.sell.last_close_price_percent = getattr(self, LAST_CLOSE_PRICE_PERCENT)
        policy.id = self.build_policy_id()
        policy.id_md5 = PolicyItem.md5(policy.id)
        logging.info("build policy:%s", policy.id)

    @staticmethod
    def md5(content):
        md5sum = hashlib.md5()
        md5sum.update(content)
        return md5sum.hexdigest()

    def build_policy_id(self):
        result = []
        for attr in self.current_policy_dict.keys():
            result.append("%s:%s" % (attr, getattr(self, attr)))
        return ",".join(result)


    @staticmethod
    def build(repeated_policy, current_policy_dict, partial_policy_set, full_policy_set, is_random_for_best):
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
                            PolicyItem.build(repeated_policy, dict(current_policy_dict), partial_policy_set, full_policy_set, is_random_for_best)
                        else:
                            PolicyItem.build_core(repeated_policy, current_policy_dict, partial_policy_set, full_policy_set)
                else:
                    assert best_item
                    if is_random_for_best:
                        current_policy_dict[k] = best_item[int(random.random()*100) % len(best_item)]
                    else:
                        current_policy_dict[k] = best_item[0]
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
        SELL_TREND_DAYS_WATCH: localconfig.SELL_TREND_DAYS_WATCH,
        LAST_CLOSE_PRICE_PERCENT: localconfig.LAST_CLOSE_PRICE_PERCENT
    }


    @staticmethod
    def generate_policy_list_for_train(repeated_policy, is_random_for_best):
        logging.info("begin generate policy list for train")
        for policy_type, item_value in PolicyFactory.policy_value_dict.iteritems():
            assert isinstance(item_value.range, list)
            PolicyFactory.generate_policy_list_with_policy_type(repeated_policy, policy_type, item_value.range, is_random_for_best)
        logging.info("end generate policy list for train")


    @staticmethod
    def generate_policy_list_for_validate(repeated_policy, is_random_for_best):
        logging.info("begin generate policy list for validate")
        PolicyItem.build(repeated_policy, {}, set(), set(), is_random_for_best)
        logging.info("end generate policy list for validate")


    @staticmethod
    def generate_policy_list_with_policy_type(repeated_policy, policy_type, policy_value_list, is_random_for_best):
        policy_str_set = set()
        policy_id_set = set()
        for policy_value in policy_value_list:
            PolicyItem.build(repeated_policy, {policy_type: policy_value}, policy_str_set, policy_id_set, is_random_for_best)


if __name__ == "__main__":
    person = Person()
    PolicyFactory.generate_policy_list_for_train(person.policy_info, False)
    print person.policy_info