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


class PolicyUtil:
    # [stock_id][date_str] = (stock_daily_info, last_stock_daily_info)
    stock_date_dict = {}
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
                    PolicyUtil.build_action_item_report(stock_info, action_item, action_item.report, policy,
                                                        DatetimeUtil.from_date_str(person.stock_end_date))
                    # clear memory now
                    del action_item.buy_stock_action[:]
                    del action_item.sell_stock_action[:]
                logging.info("end train for policy_id, stock_id")
                PolicyUtil.build_percent_policy_report_for_stock_policy(person)
                del person.action_items[:]
            logging.info("end train for policy_id:%s", policy.id)
        PolicyUtil.build_percent_policy_report_for_policy(person)
        PolicyUtil.build_percent_policy_report_for_policy_group(person)
        PolicyUtil.build_percent_policy_report_for_stock_policy_group(person)
        PolicyUtil.build_sort_report(person)
        # clear other empty
        del person.stock_info[:]
        del person.policy_info[:]
        logging.info("begin print_summary")
        PolicyUtil.print_summary(person)
        logging.info("end print_summary")
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
        current_stock_daily_info = PolicyUtil.get_the_stock_daily_info(stock_info, current_date_str)
        if current_stock_daily_info is None:
            logging.debug("no stock info for %s", current_date_str)
            return
        assert 0 <= len(action_item.buy_stock_action) - len(action_item.sell_stock_action)
        assert len(action_item.buy_stock_action) - len(action_item.sell_stock_action) <= 1
        if not PolicyUtil.check_if_allow_trade(action_item, current_date):
            logging.debug("not allow trade for %s", current_date)
            logging.debug("end try_trade_by_policy")
            return
        # TODO: 添加趋势的过滤条件
        # TODO: 优化， 提前计算percent list， 以及有效的序列
        if len(action_item.buy_stock_action) == len(action_item.sell_stock_action):
            stock_daily_info_list = PolicyUtil.filter_stock_daily_info_list(stock_info,
                                                                        action_item_policy.buy.days_watch,
                                                                        current_date_str)
            if stock_daily_info_list:
                PolicyUtil.check_if_buy(stock_info.stock_id, stock_daily_info_list, action_item, action_item_policy,
                                        current_date_str, current_stock_daily_info)
        else:
            assert len(action_item.buy_stock_action) == len(action_item.sell_stock_action) + 1
            stock_daily_info_list = PolicyUtil.filter_stock_daily_info_list(stock_info,
                                                                        action_item_policy.sell.days_watch,
                                                                        current_date_str)
            if stock_daily_info_list:
                PolicyUtil.check_if_sell(stock_info.stock_id, stock_daily_info_list, action_item, action_item_policy,
                                     current_date_str, current_stock_daily_info)
        logging.debug("end try_trade_by_policy")


    @staticmethod
    def check_if_buy(stock_id, stock_daily_info_list, action_item, action_item_policy, current_date_str,
                     current_stock_daily_info):
        the_low_price, the_high_price = current_stock_daily_info.low, current_stock_daily_info.high
        if len(action_item.sell_stock_action) < len(action_item.buy_stock_action):
            logging.debug("quit buy for wait sell")
            return
        assert len(action_item.buy_stock_action) == len(action_item.sell_stock_action)

        full_trend = PolicyUtil.get_flow_trend_cachable(stock_id, current_date_str, action_item_policy.buy.days_watch,
                                                        stock_daily_info_list, action_item_policy.buy.trend.trend_mode)
        if action_item_policy.buy.trend.growth_percent == localconfig.DEFAULT_CONFIG:
            if_continue = full_trend in localconfig.BUY_TREND_PERCENT.filter
        else:
            if_continue = action_item_policy.buy.trend.growth_percent == full_trend
        if not if_continue:
            return

        last_half_trend = PolicyUtil.get_flow_trend_cachable(stock_id, current_date_str, action_item_policy.buy.days_watch,
                                                             stock_daily_info_list[-len(stock_daily_info_list)/localconfig.LAST_GROWTH_PART:],
                                                             action_item_policy.buy.trend.trend_mode)
        if action_item_policy.buy.trend.growth_percent_last_half == localconfig.DEFAULT_CONFIG:
            if_continue = last_half_trend in localconfig.HALF_BUY_TREND_PERCENT.filter
        else:
            if_continue = action_item_policy.buy.trend.growth_percent_last_half == last_half_trend
        if not if_continue:
            return

        last_sequential_trend = PolicyPredictUtil.get_sequential_trend(stock_daily_info_list, action_item_policy.buy.trend.trend_mode)
        if action_item_policy.buy.trend.last_sequential_growth_percent == localconfig.DEFAULT_CONFIG:
            if_continue = last_sequential_trend in localconfig.LAST_BUY_SEQUENTIAL_TREND_COUNT.filter
        else:
            if_continue = action_item_policy.buy.trend.last_sequential_growth_percent == last_sequential_trend
        if not if_continue:
            logging.debug("ignore trend:%s vs %s", last_sequential_trend, action_item_policy.buy.trend.last_sequential_growth_percent)
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
        cash_value_left_to_buy = PolicyUtil.get_cash_value_available(action_item)

        logging.debug("cash value left:%s", cash_value_left_to_buy)
        if cash_value_left_to_buy <= 0:
            return
        stock_action = action_item.buy_stock_action.add()
        stock_action.date = current_date_str
        stock_action.at_price = current_price
        stock_action.volumn, stock_action.stock_trade_cost = PolicyUtil.get_volumn_and_trade_cost(cash_value_left_to_buy, current_price)
        stock_action.option_trade_cost = 0
        logging.debug("do buy stock, id:%s, date:%s, at_price:%s(%s-%s), volumn:%s", stock_id, stock_action.date,
                      stock_action.at_price, the_low_price, the_high_price, stock_action.volumn)


    @staticmethod
    def check_if_sell(stock_id, stock_daily_info_list, action_item, action_item_policy, current_date_str,
                      current_stock_daily_info):
        the_low_price, the_high_price = current_stock_daily_info.low, current_stock_daily_info.high
        if len(action_item.buy_stock_action) <= len(action_item.sell_stock_action):
            logging.debug("quit sell for empty stock hold list")
            return
        assert len(action_item.buy_stock_action) == len(action_item.sell_stock_action) + 1

        full_trend = PolicyUtil.get_flow_trend_cachable(stock_id, current_date_str, action_item_policy.sell.days_watch,
                                                        stock_daily_info_list, action_item_policy.sell.trend.trend_mode)
        if action_item_policy.sell.trend.growth_percent == localconfig.DEFAULT_CONFIG:
            if_continue = full_trend in localconfig.SELL_TREND_RERCENT.filter
        else:
            if_continue = action_item_policy.sell.trend.growth_percent == full_trend
        if not if_continue:
            return

        last_half_trend = PolicyUtil.get_flow_trend_cachable(stock_id, current_date_str, action_item_policy.sell.days_watch,
                                                             stock_daily_info_list[-len(stock_daily_info_list)/localconfig.LAST_GROWTH_PART:],
                                                             action_item_policy.sell.trend.trend_mode)
        if action_item_policy.sell.trend.growth_percent_last_half == localconfig.DEFAULT_CONFIG:
            if_continue = last_half_trend in localconfig.HALF_SELL_TREND_PERCENT.filter
        else:
            if_continue = action_item_policy.sell.trend.growth_percent_last_half == last_half_trend
        if not if_continue:
            return

        last_sequential_trend = PolicyPredictUtil.get_sequential_trend(stock_daily_info_list, action_item_policy.sell.trend.trend_mode)
        if action_item_policy.sell.trend.last_sequential_growth_percent == localconfig.DEFAULT_CONFIG:
            if_continue = last_sequential_trend in localconfig.LAST_SELL_SEQUENTIAL_TREND_COUNT.filter
        else:
            if_continue = action_item_policy.sell.trend.last_sequential_growth_percent == last_sequential_trend

        if not if_continue:
            logging.debug("ignore trend:%s vs %s", last_sequential_trend,
                         action_item_policy.sell.trend.last_sequential_growth_percent)
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
    def print_summary(person):
        logging.info("-----------------------")
        for item_report in person.sorted_policy_group_report:
            logging.info("policy_group_report:\t%s:%s\t2|%s|%s\t5|%s|%s\t8|%s|%s\t0|%s|%s",
                         item_report.policy_group_type, item_report.policy_group_value,
                         item_report.reports[2].report.roi,
                         item_report.reports[2].report.stock_sell_times,
                         item_report.reports[5].report.roi,
                         item_report.reports[5].report.stock_sell_times,
                         item_report.reports[8].report.roi,
                         item_report.reports[8].report.stock_sell_times,
                         item_report.reports[0].report.roi,
                         item_report.reports[0].report.stock_sell_times)
        logging.info("-----------------------")
        for item_report in person.sorted_policy_summary_report:
            logging.info("policy_summary_report:\t%s\t2|%s|%s\t5|%s|%s\t8|%s|%s\t0|%s|%s",
                         item_report.policy_id,
                         item_report.reports[2].report.roi,
                         item_report.reports[2].report.stock_sell_times,
                         item_report.reports[5].report.roi,
                         item_report.reports[5].report.stock_sell_times,
                         item_report.reports[8].report.roi,
                         item_report.reports[8].report.stock_sell_times,
                         item_report.reports[0].report.roi,
                         item_report.reports[0].report.stock_sell_times)
        logging.info("-----------------------")
        for item_report in person.sorted_stock_policy_group_report:
            logging.info("stock_policy_group_report:\t%s\t%s:%s\t2|%s|%s\t5|%s|%s\t8|%s|%s\t0|%s|%s",
                         item_report.stock_id,
                         item_report.policy_group_type,
                         item_report.policy_group_value,
                         item_report.reports[2].report.roi,
                         item_report.reports[2].report.stock_sell_times,
                         item_report.reports[5].report.roi,
                         item_report.reports[5].report.stock_sell_times,
                         item_report.reports[8].report.roi,
                         item_report.reports[8].report.stock_sell_times,
                         item_report.reports[0].report.roi,
                         item_report.reports[0].report.stock_sell_times)
        logging.info("-----------------------")
        for item_report in person.sorted_stock_policy_report:
            logging.info("stock_policy_report:\t%s\t%s\t2|%s|%s\t5|%s|%s\t8|%s|%s\t0|%s|%s",
                         item_report.stock_id,
                         item_report.policy_id,
                         item_report.reports[2].report.roi,
                         item_report.reports[2].report.stock_sell_times,
                         item_report.reports[5].report.roi,
                         item_report.reports[5].report.stock_sell_times,
                         item_report.reports[8].report.roi,
                         item_report.reports[8].report.stock_sell_times,
                         item_report.reports[0].report.roi,
                         item_report.reports[0].report.stock_sell_times)
        logging.info("-----------------------")


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
    def get_asset_value_out(stock_info, action_item, action_item_policy, stock_end_date):
        cash_value = PolicyUtil.get_cash_value_available(action_item)
        asset_value_taken_out = cash_value
        if len(action_item.sell_stock_action) < len(action_item.buy_stock_action):
            the_stock_daily_info = PolicyUtil.get_the_last_stock_daily_info(stock_info, action_item)
            the_stock_mean_price = (the_stock_daily_info.high + the_stock_daily_info.low) / 2.0
            # 最后一笔持有的仍然计算手续费
            asset_value_taken_out += (the_stock_mean_price * action_item.buy_stock_action[-1].volumn - action_item.buy_stock_action[-1].stock_trade_cost)
        logging.debug("cash_value:%s, asset_value_out:%s", cash_value, asset_value_taken_out)
        return asset_value_taken_out


    @staticmethod
    def get_cash_value_available(action_item):
        cash_buy = 0
        cash_sell = 0
        for stock_action in action_item.buy_stock_action:
            cash_buy += (stock_action.at_price * stock_action.volumn + stock_action.stock_trade_cost)
        for stock_action in action_item.sell_stock_action:
            cash_sell += (stock_action.at_price * stock_action.volumn - stock_action.stock_trade_cost)
        cash_left = action_item.cash_taken_in + cash_sell - cash_buy
        logging.debug("buy_size:%s, sell_size:%s, cash_buy:%s, cash_sell:%s, cash_left:%s, sell_stock_action:%s",
                      len(action_item.buy_stock_action), len(action_item.sell_stock_action), cash_buy, cash_sell,
                     cash_left, action_item.sell_stock_action)
        return cash_left


    @staticmethod
    def get_the_last_stock_daily_info(stock_info, action_item):
        return PolicyUtil.get_the_stock_daily_info(stock_info, action_item.trade_watch_end_date)


    @staticmethod
    def filter_stock_daily_info_list(stock_info, days_watch, current_date_str):
        end_date = DatetimeUtil.from_date_str(current_date_str)
        result = []
        for i in range(days_watch, 0, -1):
            the_date = end_date - datetime.timedelta(days=i)
            the_daily_info = PolicyUtil.get_the_stock_daily_info(stock_info,
                                                                 DatetimeUtil.to_datetime_str(the_date))
            if the_daily_info:
                result.append(the_daily_info)
        return result


    @staticmethod
    def get_the_stock_daily_info(stock_info, current_date_str):
        stock_id = stock_info.stock_id
        if stock_id in PolicyUtil.stock_date_dict:
            if current_date_str in PolicyUtil.stock_date_dict[stock_id]:
                return PolicyUtil.stock_date_dict[stock_id][current_date_str]
            else:
                return None
        else:
            PolicyUtil.stock_date_dict.setdefault(stock_id, {})
            for stock_daily_info in stock_info.daily_info:
                PolicyUtil.stock_date_dict[stock_id][stock_daily_info.date] = stock_daily_info
            if stock_id in PolicyUtil.stock_date_dict and current_date_str in PolicyUtil.stock_date_dict[stock_id]:
                return PolicyUtil.stock_date_dict[stock_id][current_date_str]
            else:
                return None


    @staticmethod
    def build_percent_policy_report_for_stock_policy(person):
        logging.info("begin build_percent_policy_report_for_stock_policy")
        # [stock_id][policy_id] = [PolicyReport]
        stock_policy_to_policy_report_dict = {}
        for action_item in person.action_items:
            stock_policy_to_policy_report_dict.setdefault(action_item.stock_id, {})
            stock_policy_to_policy_report_dict[action_item.stock_id].setdefault(action_item.policy_id, [])
            stock_policy_to_policy_report_dict[action_item.stock_id][action_item.policy_id].append(action_item.report)
        for stock_id, value_item in stock_policy_to_policy_report_dict.iteritems():
            for policy_id, policy_report_list in value_item.iteritems():
                stock_policy_report = person.stock_policy_report.add()
                stock_policy_report.stock_id = stock_id
                stock_policy_report.policy_id = policy_id
                PolicyUtil.build_percent_policy_report(policy_report_list, stock_policy_report.reports)
        logging.info("end build_percent_policy_report_for_stock_policy")


    @staticmethod
    def build_percent_policy_report_for_policy(person):
        logging.info("begin build_percent_policy_report_for_policy")
        # [policy_id] = [PolicyReport]
        policy_position_to_report_dict = {}
        for stock_policy_report in person.stock_policy_report:
            policy_position_to_report_dict.setdefault(stock_policy_report.policy_id, [])
            for percent_policy_report in stock_policy_report.reports:
                # add all position
                policy_position_to_report_dict[stock_policy_report.policy_id].append(percent_policy_report.report)
        for policy_id, policy_report_list in policy_position_to_report_dict.iteritems():
            policy_summary_report = person.policy_summary_report.add()
            policy_summary_report.policy_id = policy_id
            PolicyUtil.build_percent_policy_report(policy_report_list, policy_summary_report.reports)
        logging.info("end build_percent_policy_report_for_policy")


    @staticmethod
    def build_percent_policy_report_for_policy_group(person):
        logging.info("begin build_percent_policy_report_for_policy_group")
        # [policy_group_type][policy_group_value] = [PolicyReport]
        policy_group_position_to_report_dict = {}
        for policy_summary_report in person.policy_summary_report:
            for policy_group in policy_summary_report.policy_id.split(","):
                policy_group_type, policy_group_value = policy_group.split(":")
                policy_group_position_to_report_dict.setdefault(policy_group_type, {})
                policy_group_position_to_report_dict[policy_group_type].setdefault(policy_group_value, [])
                for report in policy_summary_report.reports:
                    # add all position
                    policy_group_position_to_report_dict[policy_group_type][policy_group_value].append(report.report)
        for policy_group_type, item_value in policy_group_position_to_report_dict.iteritems():
            for policy_group_value, policy_report_list in item_value.iteritems():
                policy_group_report = person.policy_group_report.add()
                policy_group_report.policy_group_type = policy_group_type
                policy_group_report.policy_group_value = policy_group_value
                PolicyUtil.build_percent_policy_report(policy_report_list, policy_group_report.reports)
        logging.info("end build_percent_policy_report_for_policy_group")

    @staticmethod
    def build_percent_policy_report_for_stock_policy_group(person):
        logging.info("begin build_percent_policy_report_for_stock_policy_group")
        # [stock_id][policy_group_type][policy_group_value] = [PolicyReport]
        stock_policy_group_to_report_dict = {}
        for stock_policy_report in person.stock_policy_report:
            stock_policy_group_to_report_dict.setdefault(stock_policy_report.stock_id, {})
            for policy_group in stock_policy_report.policy_id.split(","):
                policy_group_type, policy_group_value = policy_group.split(":")
                stock_policy_group_to_report_dict[stock_policy_report.stock_id].setdefault(policy_group_type, {})
                stock_policy_group_to_report_dict[stock_policy_report.stock_id][policy_group_type].setdefault(policy_group_value, [])
                for report in stock_policy_report.reports:
                    stock_policy_group_to_report_dict[stock_policy_report.stock_id][policy_group_type][policy_group_value].append(report.report)
        for stock_id, policy_group_item in stock_policy_group_to_report_dict.iteritems():
            for policy_group_type, policy_group_value_item in policy_group_item.iteritems():
                for policy_group_value, policy_report_list in policy_group_value_item.iteritems():
                    report = person.stock_policy_group_report.add()
                    report.stock_id = stock_id
                    report.policy_group_type = policy_group_type
                    report.policy_group_value = policy_group_value
                    PolicyUtil.build_percent_policy_report(policy_report_list, report.reports)
        logging.info("end build_percent_policy_report_for_stock_policy_group")

    @staticmethod
    def build_sort_report(person):
        logging.info("begin build_sort_report")
        sorted_stock_policy_report_list = sorted(person.stock_policy_report, key=PolicyUtil.get_percent_policy_report_roi_top, reverse=True)
        sorted_stock_policy_report_list = sorted(sorted_stock_policy_report_list, key=attrgetter('stock_id'), reverse=False)
        del person.stock_policy_report[:]
        person.sorted_stock_policy_report.extend(sorted_stock_policy_report_list)
        del sorted_stock_policy_report_list[:]

        sorted_policy_summary_report_list = sorted(person.policy_summary_report, key=PolicyUtil.get_percent_policy_report_roi_top, reverse=True)
        del person.policy_summary_report[:]
        person.sorted_policy_summary_report.extend(sorted_policy_summary_report_list)
        del sorted_policy_summary_report_list[:]

        sorted_policy_group_report_list = sorted(person.policy_group_report, key=PolicyUtil.get_percent_policy_report_roi_top, reverse=True)
        del person.policy_group_report[:]
        sorted_policy_group_report_list = sorted(sorted_policy_group_report_list, key=attrgetter('policy_group_type'), reverse=False)
        person.sorted_policy_group_report.extend(sorted_policy_group_report_list)


        del sorted_policy_group_report_list[:]

        sorted_stock_policy_group_report_list = sorted(person.stock_policy_group_report, key=PolicyUtil.get_percent_policy_report_roi_top, reverse=True)
        del person.stock_policy_group_report[:]
        sorted_stock_policy_group_report_list = sorted(sorted_stock_policy_group_report_list, key=attrgetter('policy_group_type'), reverse=False)
        sorted_stock_policy_group_report_list = sorted(sorted_stock_policy_group_report_list, key=attrgetter('stock_id'), reverse=False)
        person.sorted_stock_policy_group_report.extend(sorted_stock_policy_group_report_list)
        del sorted_stock_policy_group_report_list[:]
        logging.info("end build_sort_report")


    @staticmethod
    def get_percent_policy_report_roi_top(item):
        TOP_POSISTION_FOR_ROI = 0
        MIDDLE_POSISTION_INDEX = 0
        assert item.reports[MIDDLE_POSISTION_INDEX].position == TOP_POSISTION_FOR_ROI, item.reports[MIDDLE_POSISTION_INDEX].position
        return item.reports[MIDDLE_POSISTION_INDEX].report.roi

    @staticmethod
    def get_percent_policy_report_roi_50(item):
        MIDDLE_POSISTION_FOR_ROI = 50
        MIDDLE_POSISTION_INDEX = 5
        assert item.reports[MIDDLE_POSISTION_INDEX].position == MIDDLE_POSISTION_FOR_ROI
        return item.reports[MIDDLE_POSISTION_INDEX].report.roi

    @staticmethod
    def build_percent_policy_report(policy_report_list, repeated_stock_policy_report):
        position_to_report_dict = {}
        for position in localconfig.POSITION_PERCENT_LIST:
            position_report = repeated_stock_policy_report.add()
            position_report.position = position
            position_to_report_dict[position] = position_report.report
        for field_name in ["roi", "cash_taken_in", "cash_taken_out", "stock_buy_times", "stock_sell_times", "stock_hold_days",
                           "stock_hold_loss_days", "stock_hold_profit_days", "trade_profit_times", "trade_loss_times"]:
            PolicyUtil.build_percent_policy_report_for_field(policy_report_list, position_to_report_dict,
                                                             field_name)

    @staticmethod
    def build_percent_policy_report_for_field(policy_report_list, position_to_report_dict, field_name):
        field_value_list = []
        for report in policy_report_list:
            field_value_list.append(getattr(report, field_name))
        np_array = np.array(field_value_list)
        for position, policy_report in position_to_report_dict.iteritems():
            assert position <= 100
            percent_value = np.percentile(np_array, 100 - position)
            setattr(policy_report, field_name, percent_value)


    @staticmethod
    def build_action_item_report(stock_info, action_item, report, action_item_policy, stock_end_date):
        report.cash_taken_in = action_item.cash_taken_in
        report.cash_taken_out = PolicyUtil.get_asset_value_out(stock_info, action_item, action_item_policy, stock_end_date)
        report.roi = report.cash_taken_out / float(report.cash_taken_in) if report.cash_taken_in > 0 else 1
        report.stock_buy_times = len(action_item.buy_stock_action)
        report.stock_sell_times = len(action_item.sell_stock_action)
        report.stock_hold_days = 0
        report.stock_hold_loss_days = 0
        report.stock_hold_profit_days = 0
        report.trade_profit_times = 0
        report.trade_loss_times = 0
        for i in range(0, len(action_item.sell_stock_action)):
            if action_item.buy_stock_action[i].at_price < action_item.sell_stock_action[i].at_price:
                report.trade_profit_times += 1
            else:
                report.trade_loss_times += 1
            report.stock_hold_days += (DatetimeUtil.from_date_str(action_item.sell_stock_action[i].date)
                                      - DatetimeUtil.from_date_str(action_item.buy_stock_action[i].date)).days
        if len(action_item.sell_stock_action) < len(action_item.buy_stock_action):
            the_stock_daily_info = PolicyUtil.get_the_last_stock_daily_info(stock_info, action_item)
            the_stock_mean_price = (the_stock_daily_info.high + the_stock_daily_info.low) / 2.0
            if action_item.buy_stock_action[-1].at_price < the_stock_mean_price:
                report.trade_profit_times += 1
            else:
                report.trade_loss_times += 1
            report.stock_hold_days += (DatetimeUtil.from_date_str(the_stock_daily_info.date)
                                       - DatetimeUtil.from_date_str(action_item.buy_stock_action[-1].date)).days
        # TODO: 有效持仓亏损天数, 盈利天数
        return report


    @staticmethod
    def check_if_allow_trade(action_item, current_date):
        T0_NO_LIMIT_MIN_ASSET = 25000
        if action_item.cash_taken_in > T0_NO_LIMIT_MIN_ASSET:
            return True
        TO_DAYS_WATCH = 5
        TO_MAX_ALLOW_TRADE_COUNT = 3
        # TODO: 日内多次交易算多次
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