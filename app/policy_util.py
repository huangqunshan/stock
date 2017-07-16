# coding=utf8

import datetime
import logging
import math
import numpy as np
from operator import attrgetter
from datetime_util import DatetimeUtil
from price_util import PercentPriceUtil
from policy_predict_util import PolicyPredictUtil
from proto.policy_pb2 import Policy
import localconfig
from policy_report_util import PolicyReportUtil


class PolicyUtil:
    # [stock_id][current_date_str][days_watch] = trend
    stock_trend_dict = {}

    @staticmethod
    def train(person):
        logging.info("begin train, stock info size:%s, policy info size:%s", len(person.stock_info), len(person.policy_info))
        for policy in person.policy_info:
            logging.info("begin train for policy_id:%s", policy.id)
            for stock_info in person.stock_info:
                if not stock_info.daily_info or stock_info.daily_info[-1].low < policy.min_stock_price:
                    continue
                logging.info("begin train for stock_id:%s,policy_id:%s,stock_daily_info_size:%s",
                             stock_info.stock_id, policy.id, len(stock_info.daily_info))
                watch_days = max(policy.buy.days_watch, policy.sell.days_watch)
                trade_watch_date_list = PolicyUtil.get_trade_watch_date_list(stock_info.daily_info,
                                                                             watch_days,
                                                                             localconfig.max_watch_jump_times,
                                                                             localconfig.JUMPS_PER_WATCH)
                logging.debug("trade_watch_date_list:%s", trade_watch_date_list)
                for item in trade_watch_date_list:
                    trade_watch_start_date_str, trade_watch_end_date_str = item
                    action_item = person.action_items.add()
                    action_item.cash_taken_in = person.cash_taken_in
                    action_item.stock_id = stock_info.stock_id
                    action_item.policy_id = policy.id
                    action_item.trade_watch_start_date = trade_watch_start_date_str
                    action_item.trade_watch_end_date = trade_watch_end_date_str
                    PolicyUtil.build_policy_actions(stock_info, action_item, policy)
                    PolicyReportUtil.build_action_item_report(stock_info, action_item, action_item.report)
                    # clear memory now
                    del action_item.buy_stock_action[:]
                    del action_item.sell_stock_action[:]
                logging.info("end train for policy_id, stock_id")
                PolicyReportUtil.build_summary_policy_report_for_stock_policy(person)
                del person.action_items[:]
            logging.info("end train for policy_id:%s", policy.id)
        PolicyReportUtil.build_summary_policy_report_for_policy(person)
        PolicyReportUtil.build_summary_policy_report_for_policy_group(person)
        PolicyReportUtil.build_summary_policy_report_for_stock_policy_group(person)
        PolicyReportUtil.build_sort_report(person)
        # clear other empty
        del person.stock_info[:]
        del person.policy_info[:]
        PolicyReportUtil.print_summary(person)
        logging.info("end train")
        return


    @staticmethod
    def build_policy_actions(stock_info, action_item, action_item_policy):
        logging.debug("begin build_policy_actions")
        start_date = DatetimeUtil.from_date_str(action_item.trade_watch_start_date)
        end_date = DatetimeUtil.from_date_str(action_item.trade_watch_end_date)
        current_date = start_date
        while current_date < end_date:
            PolicyUtil.do_trade_by_policy(stock_info, action_item, action_item_policy, current_date)
            current_date = current_date + datetime.timedelta(days=1)
        logging.debug("end build_policy_actions")


    @staticmethod
    def do_trade_by_policy(stock_info, action_item, action_item_policy, current_date):
        logging.debug("begin try_trade_by_policy, current_date:%s", current_date)
        current_date_str = DatetimeUtil.to_datetime_str(current_date)
        current_stock_daily_info = PolicyReportUtil.get_the_stock_daily_info(stock_info, current_date_str)
        if current_stock_daily_info is None:
            logging.debug("no stock info for %s", current_date_str)
            return
        assert 0 <= len(action_item.buy_stock_action) - len(action_item.sell_stock_action)
        assert len(action_item.buy_stock_action) - len(action_item.sell_stock_action) <= 1
        if not PolicyUtil.check_if_allow_trade(action_item, current_date):
            logging.debug("not allow trade for %s", current_date)
            logging.debug("end try_trade_by_policy")
            return
        if len(action_item.buy_stock_action) == len(action_item.sell_stock_action):
            stock_daily_info_list = PolicyUtil.filter_stock_daily_info_list(stock_info,
                                                                        action_item_policy.buy.days_watch,
                                                                        current_date_str)
            trend_daily_info_list = PolicyUtil.filter_stock_daily_info_list(stock_info,
                                                                        action_item_policy.buy.trend.days_watch,
                                                                        current_date_str)
            if stock_daily_info_list:
                PolicyUtil.check_if_buy(stock_info.stock_id, stock_daily_info_list, trend_daily_info_list,
                                        action_item, action_item_policy, current_date_str, current_stock_daily_info)
        else:
            assert len(action_item.buy_stock_action) == len(action_item.sell_stock_action) + 1
            stock_daily_info_list = PolicyUtil.filter_stock_daily_info_list(stock_info,
                                                                        action_item_policy.sell.days_watch,
                                                                        current_date_str)
            trend_daily_info_list = PolicyUtil.filter_stock_daily_info_list(stock_info,
                                                                        action_item_policy.sell.trend.days_watch,
                                                                        current_date_str)
            if stock_daily_info_list:
                PolicyUtil.check_if_sell(stock_info.stock_id, stock_daily_info_list, trend_daily_info_list,
                                         action_item, action_item_policy, current_date_str, current_stock_daily_info)
        logging.debug("end try_trade_by_policy")


    @staticmethod
    def check_if_buy(stock_id, stock_daily_info_list, trend_daily_info_list, action_item, action_item_policy,
                     current_date_str, current_stock_daily_info):
        the_low_price, the_high_price = current_stock_daily_info.low, current_stock_daily_info.high
        if len(action_item.sell_stock_action) < len(action_item.buy_stock_action):
            logging.debug("quit buy for wait sell")
            return
        assert len(action_item.buy_stock_action) == len(action_item.sell_stock_action)

        full_trend = PolicyUtil.get_flow_trend_cachable(stock_id, current_date_str, action_item_policy.buy.trend.days_watch,
                                                        trend_daily_info_list, action_item_policy.buy.trend.trend_mode)
        if action_item_policy.buy.trend.growth_percent == localconfig.DEFAULT_CONFIG:
            if_continue = full_trend in localconfig.BUY_TREND_PERCENT.filter if localconfig.BUY_TREND_PERCENT.filter else True
        else:
            if_continue = action_item_policy.buy.trend.growth_percent == full_trend
        if not if_continue:
            return

        last_sequential_trend = PolicyPredictUtil.get_sequential_trend(trend_daily_info_list, action_item_policy.buy.trend.trend_mode)
        if action_item_policy.buy.trend.last_sequential_trend_count == localconfig.DEFAULT_CONFIG:
            if_continue = last_sequential_trend in localconfig.LAST_BUY_SEQUENTIAL_TREND_COUNT.filter if localconfig.LAST_BUY_SEQUENTIAL_TREND_COUNT.filter else True
        else:
            if_continue = action_item_policy.buy.trend.last_sequential_trend_count == last_sequential_trend
        if not if_continue:
            logging.debug("ignore trend:%s vs %s", last_sequential_trend, action_item_policy.buy.trend.last_sequential_trend_count)
            return

        current_price = PercentPriceUtil.get_percent_price(stock_id,
                                                           action_item_policy.buy.days_watch,
                                                           current_date_str,
                                                           stock_daily_info_list,
                                                           action_item_policy.buy.at_percent)
        if current_price is None:
            logging.debug("quit buy for empty percent price")
            return

        # current_price = (last_daily_info.low + last_daily_info.high)/2.0


        if current_price <= the_low_price:
            logging.debug("quit buy for too low percent_price:%s < low_price:%s", current_price, the_low_price)
            return
        current_price = min(current_price, the_high_price)
        cash_value_left_to_buy = PolicyReportUtil.get_cash_value_available(action_item)

        logging.debug("cash value left:%s", cash_value_left_to_buy)
        if cash_value_left_to_buy <= 0:
            return
        if current_price < action_item_policy.min_stock_price:
            return
        stock_action = action_item.buy_stock_action.add()
        stock_action.date = current_date_str
        stock_action.at_price = current_price
        stock_action.volumn, stock_action.stock_trade_cost = PolicyUtil.get_volumn_and_trade_cost(cash_value_left_to_buy, current_price)
        stock_action.option_trade_cost = 0
        logging.debug("do buy stock, id:%s, date:%s, at_price:%s(%s-%s), volumn:%s", stock_id, stock_action.date,
                      stock_action.at_price, the_low_price, the_high_price, stock_action.volumn)


    @staticmethod
    def check_if_sell(stock_id, stock_daily_info_list, trend_daily_info_list, action_item, action_item_policy,
                      current_date_str, current_stock_daily_info):
        the_low_price, the_high_price = current_stock_daily_info.low, current_stock_daily_info.high
        if len(action_item.buy_stock_action) <= len(action_item.sell_stock_action):
            logging.debug("quit sell for empty stock hold list")
            return
        assert len(action_item.buy_stock_action) == len(action_item.sell_stock_action) + 1

        full_trend = PolicyUtil.get_flow_trend_cachable(stock_id, current_date_str, action_item_policy.sell.trend.days_watch,
                                                        trend_daily_info_list, action_item_policy.sell.trend.trend_mode)
        if action_item_policy.sell.trend.growth_percent == localconfig.DEFAULT_CONFIG:
            if_continue = full_trend in localconfig.SELL_TREND_PERCENT.filter if localconfig.SELL_TREND_PERCENT.filter else True
        else:
            if_continue = action_item_policy.sell.trend.growth_percent == full_trend
        if not if_continue:
            return

        last_sequential_trend = PolicyPredictUtil.get_sequential_trend(trend_daily_info_list, action_item_policy.sell.trend.trend_mode)
        if action_item_policy.sell.trend.last_sequential_trend_count == localconfig.DEFAULT_CONFIG:
            if_continue = last_sequential_trend in localconfig.LAST_SELL_SEQUENTIAL_TREND_COUNT.filter if localconfig.LAST_SELL_SEQUENTIAL_TREND_COUNT.filter else True
        else:
            if_continue = action_item_policy.sell.trend.last_sequential_trend_count == last_sequential_trend

        if not if_continue:
            logging.debug("ignore trend:%s vs %s", last_sequential_trend,
                         action_item_policy.sell.trend.last_sequential_trend_count)
            return


        last_buy_price = action_item.buy_stock_action[-1].at_price
        loss_stop_price = last_buy_price * (1000-action_item_policy.sell.sell_at_loss_thousandth)/1000.0
        sell_price = last_buy_price * 100
        if 0 < action_item_policy.sell.sell_at_loss_thousandth and the_low_price <= loss_stop_price:
            # 悲观假设： 卖在最低
            sell_price = the_low_price + 0.0001
            # 乐观假设： 卖在最高
            sell_price = loss_stop_price
        elif 0 < action_item_policy.sell.at_percent.percent_n:
            sell_price = PercentPriceUtil.get_percent_price(stock_id,
                                                            action_item_policy.sell.days_watch,
                                                            current_date_str,
                                                            stock_daily_info_list,
                                                            action_item_policy.sell.at_percent)
        elif 0 < action_item_policy.sell.sell_at_profit_thousandth:
            sell_price = last_buy_price * (1 + action_item_policy.sell.sell_at_profit_thousandth/1000.0)
        else:
            assert False
        if the_high_price <= sell_price:
            logging.debug("quit sell for too high price:%s > high_price:%s", sell_price, the_high_price)
            return
        logging.debug("debug sell_price:%s, the_low_price:%s", sell_price, the_low_price)
        sell_price = max(the_low_price, sell_price)
        stock_action = action_item.sell_stock_action.add()
        stock_action.date = current_date_str
        stock_action.at_price = sell_price
        stock_action.volumn = action_item.buy_stock_action[-1].volumn
        stock_action.stock_trade_cost = action_item.buy_stock_action[-1].stock_trade_cost
        stock_action.option_trade_cost = 0
        logging.debug("do sell stock, id:%s, date:%s, at_price:%s(%s-%s), volumn:%s", stock_id, stock_action.date,
                      stock_action.at_price, the_low_price, the_high_price, stock_action.volumn)

        return


    @staticmethod
    def get_trade_watch_date_list(repeated_daily_info, days_before, max_watch_jump_times, jumps_per_range):
        logging.debug("begin get_trade_watch_date_str_list:%s, pre_train_watch_days:%s, max_watch_jump_times:%s, jumps_per_range:%s",
                      repeated_daily_info, days_before, max_watch_jump_times, jumps_per_range)
        cut_daily_info_list = repeated_daily_info[days_before:]
        if not cut_daily_info_list:
            return []
        jump_step = len(cut_daily_info_list) / max_watch_jump_times
        if 0 == jump_step:
            return [(cut_daily_info_list[0].date, cut_daily_info_list[-1].date)]
        begin_index = 0
        result = []
        while begin_index + 1 < len(cut_daily_info_list):
            end_index = begin_index+jumps_per_range*jump_step
            end_index = min(end_index, len(cut_daily_info_list)-1)
            result.append((cut_daily_info_list[begin_index].date, cut_daily_info_list[end_index].date))
            begin_index += jump_step
        return result


    @staticmethod
    def filter_stock_daily_info_list(stock_info, days_watch, current_date_str):
        end_date = DatetimeUtil.from_date_str(current_date_str)
        result = []
        for i in range(days_watch, 0, -1):
            the_date = end_date - datetime.timedelta(days=i)
            the_daily_info = PolicyReportUtil.get_the_stock_daily_info(stock_info,
                                                                 DatetimeUtil.to_datetime_str(the_date))
            if the_daily_info:
                result.append(the_daily_info)
        return result


    @staticmethod
    def check_if_allow_trade(action_item, current_date):
        T0_NO_LIMIT_MIN_ASSET = 25000
        if action_item.cash_taken_in > T0_NO_LIMIT_MIN_ASSET:
            return True
        TO_DAYS_WATCH = 5
        TO_MAX_ALLOW_TRADE_COUNT = 3
        # NOTE: 日内多次交易算多次
        return True

    @staticmethod
    def get_volumn_and_trade_cost(max_buy_asset_value, percent_price):
        assert percent_price > 0
        predict_cost = max(max_buy_asset_value / percent_price * 0.005, 1)
        volumn = int((max_buy_asset_value - predict_cost) / percent_price)
        final_cost = max(volumn * 0.005, 1)
        return volumn, final_cost


    @staticmethod
    def get_flow_trend_cachable(stock_id, current_date_str, days_watch, repeated_stock_daily_info, trend_mode):
        # [stock_id][current_date_str][days_watch] = trend
        PolicyUtil.stock_trend_dict.setdefault(stock_id, {})
        PolicyUtil.stock_trend_dict[stock_id].setdefault(current_date_str, {})
        if days_watch in PolicyUtil.stock_trend_dict[stock_id][current_date_str]:
            return PolicyUtil.stock_trend_dict[stock_id][current_date_str][days_watch]
        flow_detail_list = PolicyPredictUtil.get_flow_detail_list(repeated_stock_daily_info, trend_mode)
        current_trend = PolicyPredictUtil.get_flow_trend(flow_detail_list)
        PolicyUtil.stock_trend_dict[stock_id][current_date_str][days_watch] = current_trend
        logging.debug("get trend:%s for %s", current_trend, flow_detail_list)
        return current_trend