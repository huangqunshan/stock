# coding=utf8

import datetime
import logging
import numpy as np
from operator import attrgetter
from datetime_util import DatetimeUtil
from price_util import PercentPriceUtil
from proto.policy_pb2 import Policy
import localconfig


class PolicyUtil:

    @staticmethod
    def train(person):
        logging.info("begin train, stock info size:%s, policy info size:%s", len(person.stock_info), len(person.policy_info))
        # generate policy dict
        # [policy_id] = Policy()
        policy_dict = {}
        for policy in person.policy_info:
            policy_dict[policy.id] = policy
        logging.info("policy_dict size:%s", len(policy_dict))
        for policy in person.policy_info:
            logging.info("begin train for policy_id:%s", policy.id)
            for stock_info in person.stock_info:
                logging.info("begin train for stock_id:%s, stock_daily_info_size:%s", stock_info.stock_id, len(stock_info.daily_info))
                logging.info("begin train for stock_id:%s, policy_id:%s", stock_info.stock_id, policy.id)
                min_sell_watch_days = max(policy.buy.days_watch, policy.sell.days_watch)
                trade_watch_date_str_list = PolicyUtil.get_trade_watch_date_str_list(person.stock_start_date,
                                                                                     person.stock_end_date,
                                                                                     max(policy.buy.days_watch, policy.sell.days_watch),
                                                                                     min_sell_watch_days,
                                                                                     localconfig.max_watch_jump_times)
                for trade_watch_start_date in trade_watch_date_str_list:
                    action_item = person.action_items.add()
                    action_item.cash_taken_in = person.cash_taken_in
                    action_item.stock_id = stock_info.stock_id
                    action_item.policy_id = policy.id
                    action_item.trade_watch_start_date = trade_watch_start_date
                    PolicyUtil.generate_policy_actions(stock_info, action_item, policy_dict[policy.id], person.stock_end_date)
                    PolicyUtil.build_action_item_report(stock_info, action_item, action_item.report, policy_dict[policy.id],
                                                        DatetimeUtil.from_date_str(person.stock_end_date))
                    # clear memory now
                    del action_item.buy_stock_action[:]
                    del action_item.sell_stock_action[:]
                logging.info("end train for policy_id, stock_id")
                PolicyUtil.build_percent_policy_report_for_stock_policy(person)
                del person.action_items[:]
                logging.info("end train for stock_id:%s", stock_info.stock_id)
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
    def print_summary(person):
        for item_report in person.sorted_policy_group_report:
            logging.info("policy_group_report:\t%s:%s\t2-5-8-9:\t%s # %s, %s # %s, %s # %s, %s # %s",
                         item_report.policy_group_type, item_report.policy_group_value,
                         item_report.reports[2].report.roi,
                         item_report.reports[2].report.stock_sell_times,
                         item_report.reports[5].report.roi,
                         item_report.reports[5].report.stock_sell_times,
                         item_report.reports[8].report.roi,
                         item_report.reports[8].report.stock_sell_times,
                         item_report.reports[9].report.roi,
                         item_report.reports[9].report.stock_sell_times)
        for item_report in person.sorted_policy_summary_report:
            logging.info("policy_summary_report:\t%s\t2-5-8-9:\t%s # %s, %s # %s, %s # %s, %s # %s",
                         item_report.policy_id,
                         item_report.reports[2].report.roi,
                         item_report.reports[2].report.stock_sell_times,
                         item_report.reports[5].report.roi,
                         item_report.reports[5].report.stock_sell_times,
                         item_report.reports[8].report.roi,
                         item_report.reports[8].report.stock_sell_times,
                         item_report.reports[9].report.roi,
                         item_report.reports[9].report.stock_sell_times)
        for item_report in person.sorted_stock_policy_group_report:
            logging.info("stock_policy_group_report:\t%s\t%s:%s\t2-5-8-9:\t%s # %s, %s # %s, %s # %s, %s # %s",
                         item_report.stock_id,
                         item_report.policy_group_type,
                         item_report.policy_group_value,
                         item_report.reports[2].report.roi,
                         item_report.reports[2].report.stock_sell_times,
                         item_report.reports[5].report.roi,
                         item_report.reports[5].report.stock_sell_times,
                         item_report.reports[8].report.roi,
                         item_report.reports[8].report.stock_sell_times,
                         item_report.reports[9].report.roi,
                         item_report.reports[9].report.stock_sell_times)
        for item_report in person.sorted_stock_policy_report:
            logging.info("stock_policy_report:\t%s\t%s\t2-5-8-9:\t%s # %s, %s # %s, %s # %s, %s # %s",
                         item_report.stock_id,
                         item_report.policy_id,
                         item_report.reports[2].report.roi,
                         item_report.reports[2].report.stock_sell_times,
                         item_report.reports[5].report.roi,
                         item_report.reports[5].report.stock_sell_times,
                         item_report.reports[8].report.roi,
                         item_report.reports[8].report.stock_sell_times,
                         item_report.reports[9].report.roi,
                         item_report.reports[9].report.stock_sell_times)


    @staticmethod
    def get_trade_watch_date_str_list(start_date_str, end_date_str, pre_train_watch_days, post_train_watch_days, max_watch_jump_times):
        logging.debug("begin get_trade_watch_date_str_list, start_date_str:%s, end_date_str:%s, pre_train_watch_days:%s, post_train_watch_days:%s, max_watch_jump_times:%s",
                    start_date_str, end_date_str, pre_train_watch_days, post_train_watch_days, max_watch_jump_times)
        start_date = DatetimeUtil.from_date_str(start_date_str)
        end_date = DatetimeUtil.from_date_str(end_date_str)
        max_days_interval = (end_date - start_date).days
        result = []
        while start_date + datetime.timedelta(days=pre_train_watch_days) <= end_date \
                and start_date + datetime.timedelta(days=pre_train_watch_days + post_train_watch_days) <= end_date:
            result.append(DatetimeUtil.to_datetime_str(start_date+datetime.timedelta(days=pre_train_watch_days)))
            start_date = start_date + datetime.timedelta(days=max_days_interval/max_watch_jump_times)
        logging.debug("end get_trade_watch_date_str_list")
        return result


    @staticmethod
    def generate_policy_actions(stock_info, action_item, action_item_policy, stock_end_date_str):
        logging.debug("begin generate_policy_actions")
        stock_end_date = DatetimeUtil.from_date_str(stock_end_date_str)
        max_days_interval = (stock_end_date - DatetimeUtil.from_date_str(action_item.trade_watch_start_date)).days
        for current_date in PolicyUtil.get_date_range_list(action_item.trade_watch_start_date,
                                                           max_days_interval):
            PolicyUtil.do_trade_by_policy(stock_info, action_item, action_item_policy, current_date)
        logging.debug("end generate_policy_actions")


    @staticmethod
    def do_trade_by_policy(stock_info, action_item, action_item_policy, current_date):
        logging.debug("begin try_trade_by_policy, current_date:%s", current_date)
        assert 0 <= len(action_item.buy_stock_action) - len(action_item.sell_stock_action)
        assert len(action_item.buy_stock_action) - len(action_item.sell_stock_action) <= 1
        current_date_str = DatetimeUtil.to_datetime_str(current_date)
        if not PolicyUtil.check_if_allow_trade(action_item, current_date):
            logging.debug("not allow trade for %s", current_date)
            logging.debug("end try_trade_by_policy")
            return
        # TODO: 添加趋势的过滤条件
        if len(action_item.buy_stock_action) == len(action_item.sell_stock_action):
            PolicyUtil.check_if_buy(stock_info, action_item, action_item_policy, current_date_str)
        else:
            assert len(action_item.buy_stock_action) == len(action_item.sell_stock_action) + 1
            PolicyUtil.check_if_sell(stock_info, action_item, action_item_policy, current_date_str)
        logging.debug("end try_trade_by_policy")

    @staticmethod
    def check_if_buy(stock_info, action_item, action_item_policy, current_date_str):
        if len(action_item.sell_stock_action) < len(action_item.buy_stock_action):
            return
        assert len(action_item.buy_stock_action) == len(action_item.sell_stock_action)
        # TODO: only process at percent now policy
        if not action_item_policy.buy.HasField("at_percent"):
            return
        the_day_stock_info = PolicyUtil.get_the_stock_daily_info(stock_info, current_date_str)
        if the_day_stock_info is None:
            logging.debug("no stock info for %s", current_date_str)
            return
        percent_price = PolicyUtil.get_stock_percent_price(stock_info,
                                                           action_item_policy.buy.days_watch,
                                                           current_date_str,
                                                           action_item_policy.buy.at_percent)
        if percent_price is None:
            # empty stock list
            return
        if percent_price <= the_day_stock_info.low:
            return
        cash_value_left_to_buy = PolicyUtil.get_cash_value_available(stock_info, action_item)
        logging.debug("cash value left:%s", cash_value_left_to_buy)
        stock_action = action_item.buy_stock_action.add()
        stock_action.date = current_date_str
        stock_action.at_price = percent_price
        stock_action.volumn, stock_action.stock_trade_cost = PolicyUtil.get_volumn_and_trade_cost(cash_value_left_to_buy, percent_price)
        stock_action.option_trade_cost = 0
        logging.debug("do buy stock, id:%s, date:%s, at_price:%s, volumn:%s", stock_info.stock_id, stock_action.date,
                      stock_action.at_price, stock_action.volumn)


    @staticmethod
    def check_if_sell(stock_info, action_item, action_item_policy, current_date_str):
        if len(action_item.buy_stock_action) <= len(action_item.sell_stock_action):
            return
        assert len(action_item.buy_stock_action) == len(action_item.sell_stock_action) + 1
        # TODO: only process at percent now policy
        if not action_item_policy.sell.HasField("at_percent"):
            return
        the_stock_daily_info = PolicyUtil.get_the_stock_daily_info(stock_info, current_date_str)
        if the_stock_daily_info is None:
            logging.debug("no stock info for %s", current_date_str)
            return
        percent_price = PolicyUtil.get_stock_percent_price(stock_info,
                                                           action_item_policy.sell.days_watch,
                                                           current_date_str,
                                                           action_item_policy.sell.at_percent)
        if the_stock_daily_info.high <= percent_price:
            return
        stock_action = action_item.sell_stock_action.add()
        stock_action.date = current_date_str
        stock_action.at_price = percent_price
        stock_action.volumn = action_item.buy_stock_action[-1].volumn
        stock_action.stock_trade_cost = action_item.buy_stock_action[-1].stock_trade_cost
        stock_action.option_trade_cost = 0
        logging.debug("do buy stock, id:%s, date:%s, at_price:%s, volumn:%s", stock_info.stock_id, stock_action.date,
                      stock_action.at_price, stock_action.volumn)


    @staticmethod
    def get_asset_value_out(stock_info, action_item, action_item_policy, stock_end_date):
        cash_value = PolicyUtil.get_cash_value_available(stock_info, action_item)
        asset_value_taken_out = cash_value
        if len(action_item.sell_stock_action) < len(action_item.buy_stock_action):
            the_stock_daily_info = PolicyUtil.get_the_last_stock_daily_info(stock_info, action_item, action_item_policy, stock_end_date)
            the_stock_mean_price = (the_stock_daily_info.high + the_stock_daily_info.low) / 2.0
            # 最后一笔持有的仍然计算手续费
            asset_value_taken_out += (the_stock_mean_price * action_item.buy_stock_action[-1].volumn - action_item.buy_stock_action[-1].stock_trade_cost)
        logging.debug("cash_value:%s, asset_value_out:%s", cash_value, asset_value_taken_out)
        return asset_value_taken_out


    @staticmethod
    def get_cash_value_available(stock_info, action_item):
        cash_buy = 0
        cash_sell = 0
        for stock_action in action_item.buy_stock_action:
            cash_buy += (stock_action.at_price * stock_action.volumn + stock_action.stock_trade_cost)
        for stock_action in action_item.sell_stock_action:
            cash_sell += (stock_action.at_price * stock_action.volumn - stock_action.stock_trade_cost)
        cash_left = action_item.cash_taken_in + cash_sell - cash_buy
        logging.debug("buy_size:%s, sell_size:%s, cash_buy:%s, cash_sell:%s, cash_left:%s",
                      len(action_item.buy_stock_action), len(action_item.sell_stock_action), cash_buy, cash_sell, cash_left)
        return cash_left


    @staticmethod
    def get_the_last_stock_daily_info(stock_info, action_item, action_item_policy, stock_end_date):
        begin_date = DatetimeUtil.from_date_str(action_item.trade_watch_start_date)
        while begin_date <= stock_end_date:
            the_daily_stock_info = PolicyUtil.get_the_stock_daily_info(stock_info, DatetimeUtil.to_datetime_str(stock_end_date))
            if the_daily_stock_info:
                return the_daily_stock_info
            else:
                stock_end_date = stock_end_date - datetime.timedelta(days=1)
        return None


    @staticmethod
    def get_stock_percent_price(stock_info, days_watch, current_date_str, at_percent):
        """
        get sotck percent price
        :param stock_info:
        :param days_watch:
        :param current_date_str:
        :param at_percent:
        :return: percent price, may return None for empty list
        """
        begin_date_str = DatetimeUtil.to_datetime_str(DatetimeUtil.from_date_str(current_date_str) - datetime.timedelta(days=days_watch))
        select_stock_daily_info_list = []
        for stock_daily_info in stock_info.daily_info:
            if begin_date_str <= stock_daily_info.date and stock_daily_info.date < current_date_str:
                select_stock_daily_info_list.append(stock_daily_info)
        if not select_stock_daily_info_list:
            return None
        return PercentPriceUtil.get_percent_price(stock_info.stock_id, days_watch, current_date_str, select_stock_daily_info_list, at_percent)


    @staticmethod
    def get_the_stock_daily_info(stock_info, current_date_str):
        ''' get the stock info by current date str
        :param stock_info:
        :param current_date_str:
        :return: stock_info on success, otherwise return None
        '''
        for stock_daily_info in stock_info.daily_info:
            if stock_daily_info.date == current_date_str:
                return stock_daily_info
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
        sorted_stock_policy_report_list = sorted(person.stock_policy_report, key=PolicyUtil.get_percent_policy_report_roi_50, reverse=True)
        sorted_stock_policy_report_list = sorted(sorted_stock_policy_report_list, key=attrgetter('stock_id'), reverse=False)
        del person.stock_policy_report[:]
        person.sorted_stock_policy_report.extend(sorted_stock_policy_report_list)
        del sorted_stock_policy_report_list[:]

        sorted_policy_summary_report_list = sorted(person.policy_summary_report, key=PolicyUtil.get_percent_policy_report_roi_50, reverse=True)
        del person.policy_summary_report[:]
        person.sorted_policy_summary_report.extend(sorted_policy_summary_report_list)
        del sorted_policy_summary_report_list[:]

        sorted_policy_group_report_list = sorted(person.policy_group_report, key=PolicyUtil.get_percent_policy_report_roi_50, reverse=True)
        del person.policy_group_report[:]
        sorted_policy_group_report_list = sorted(sorted_policy_group_report_list, key=attrgetter('policy_group_type'), reverse=False)
        person.sorted_policy_group_report.extend(sorted_policy_group_report_list)
        del sorted_policy_group_report_list[:]

        sorted_stock_policy_group_report_list = sorted(person.stock_policy_group_report, key=PolicyUtil.get_percent_policy_report_roi_50, reverse=True)
        del person.stock_policy_group_report[:]
        sorted_stock_policy_group_report_list = sorted(sorted_stock_policy_group_report_list, key=attrgetter('policy_group_type'), reverse=False)
        sorted_stock_policy_group_report_list = sorted(sorted_stock_policy_group_report_list, key=attrgetter('stock_id'), reverse=False)
        person.sorted_stock_policy_group_report.extend(sorted_stock_policy_group_report_list)
        del sorted_stock_policy_group_report_list[:]
        logging.info("end build_sort_report")


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
        report.roi = report.cash_taken_out / report.cash_taken_in if report.cash_taken_in > 0 else 1
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
            the_stock_daily_info = PolicyUtil.get_the_last_stock_daily_info(stock_info, action_item, action_item_policy, stock_end_date)
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
    def predict(stock_info, check_date):
        # TODO: filter stock_info for old date
        # [stock_id] = {(last_close, [price1, price2, ...], [price1, price2, ...])}
        buy_policy_list = PolicyUtil.get_best_buy_policy_list()
        stock_price_dict = {}
        for stock in stock_info:
            for policy in buy_policy_list:
                if not stock.daily_info:
                    logging.error("failed to get daily info for %s", stock.stock_id)
                    continue
                price = PercentPriceUtil.generate_percent(stock.daily_info[-policy.buy.days_watch:],
                                                          policy.buy.at_percent.mode,
                                                          policy.buy.at_percent.percent_n)
                stock_price_dict.setdefault(stock.stock_id, [0, [], []])
                stock_price_dict[stock.stock_id][0] = stock.daily_info[-1].close
                stock_price_dict[stock.stock_id][1].append(price)
        sell_policy_list = PolicyUtil.get_best_sell_policy_list()
        for stock in stock_info:
            for policy in sell_policy_list:
                if not stock.daily_info:
                    logging.error("failed to get daily info for %s", stock.stock_id)
                    continue
                price = PercentPriceUtil.generate_percent(stock.daily_info[-policy.sell.days_watch:],
                                                          policy.sell.at_percent.mode,
                                                          policy.sell.at_percent.percent_n)
                stock_price_dict.setdefault(stock.stock_id, [0, [], []])
                stock_price_dict[stock.stock_id][0] = stock.daily_info[-1].close
                stock_price_dict[stock.stock_id][2].append(price)
        return stock_price_dict


    @staticmethod
    def get_best_buy_policy_list(limit_count=100):
        best_policy_list = []
        for day in [15]:
            for percent in [20]:
                for mode in [Policy.TradePolicy.Percent.LOW]:
                    policy_best1 = Policy()
                    policy_best1.buy.days_watch = day
                    policy_best1.buy.at_percent.mode = mode
                    policy_best1.buy.at_percent.percent_n = percent
                    best_policy_list.append(policy_best1)
        return best_policy_list[:limit_count]

    @staticmethod
    def get_best_sell_policy_list(limit_count=100):
        best_policy_list = []
        for day in [15]:
            for percent in [90]:
                for mode in [Policy.TradePolicy.Percent.HIGH]:
                    policy_best1 = Policy()
                    policy_best1.sell.days_watch = day
                    policy_best1.sell.at_percent.mode = mode
                    policy_best1.sell.at_percent.percent_n = percent
                    best_policy_list.append(policy_best1)
        return best_policy_list[:limit_count]
    

    @staticmethod
    def get_date_range_list(start_date_str, days_watch):
        start_date = DatetimeUtil.from_date_str(start_date_str)
        end_date = start_date + datetime.timedelta(days=days_watch)
        result = []
        while start_date <= end_date:
            result.append(start_date)
            start_date = start_date + datetime.timedelta(days=1)
        return result

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
        predict_cost = max(max_buy_asset_value / percent_price * 0.005, 1)
        volumn = (max_buy_asset_value - predict_cost) / percent_price
        final_cost = max(volumn * 0.005, 1)
        return volumn, final_cost