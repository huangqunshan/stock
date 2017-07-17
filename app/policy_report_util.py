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
from policy_factory import PolicyItem
import localconfig


class PolicyReportUtil:
    # [stock_id][date_str] = (stock_daily_info, last_stock_daily_info)
    stock_date_dict = {}


    @staticmethod
    def build_summary_policy_report_for_stock_policy(person, is_validate):
        logging.info("begin build_summary_policy_report_for_stock_policy")
        # [stock_id][policy_id] = [PolicyReport]
        stock_policy_to_policy_report_dict = {}
        for action_item in person.action_items:
            stock_policy_to_policy_report_dict.setdefault(action_item.stock_id, {})
            stock_policy_to_policy_report_dict[action_item.stock_id].setdefault(action_item.policy_id, [])
            stock_policy_to_policy_report_dict[action_item.stock_id][action_item.policy_id].append(action_item.report)
        for stock_id, value_item in stock_policy_to_policy_report_dict.iteritems():
            for policy_id, policy_report_list in value_item.iteritems():
                report = person.stock_policy_report.add()
                report.stock_id = stock_id
                report.policy_id = policy_id
                report.policy_id_md5 = PolicyItem.md5(policy_id)
                PolicyReportUtil.build_summary_policy_report(policy_report_list, report.reports, is_validate)
                if not report.reports:
                    del person.stock_policy_report[-1]
                report.roi_more_than_one_rate = PolicyReportUtil.build_roi_more_than_one_rate(report.reports)
        logging.info("end build_summary_policy_report_for_stock_policy")


    @staticmethod
    def build_summary_policy_report_for_policy(person, is_validate):
        logging.info("begin build_summary_policy_report_for_policy")
        # [policy_id] = [PolicyReport]
        policy_position_to_report_dict = {}
        for stock_policy_report in person.stock_policy_report:
            policy_position_to_report_dict.setdefault(stock_policy_report.policy_id, [])
            for percent_policy_report in stock_policy_report.reports:
                # add all position
                policy_position_to_report_dict[stock_policy_report.policy_id].append(percent_policy_report.report)
        for policy_id, policy_report_list in policy_position_to_report_dict.iteritems():
            report = person.summary_policy_report.add()
            report.policy_id = policy_id
            report.policy_id_md5 = PolicyItem.md5(policy_id)
            PolicyReportUtil.build_summary_policy_report(policy_report_list, report.reports, is_validate)
            if not report.reports:
                del person.summary_policy_report[-1]
            report.roi_more_than_one_rate = PolicyReportUtil.build_roi_more_than_one_rate(report.reports)
        logging.info("end build_summary_policy_report_for_policy")


    @staticmethod
    def build_summary_policy_report_for_policy_group(person, is_validate):
        logging.info("begin build_summary_policy_report_for_policy_group")
        # [policy_group_type][policy_group_value] = [PolicyReport]
        policy_group_position_to_report_dict = {}
        for summary_policy_report in person.summary_policy_report:
            for policy_group in summary_policy_report.policy_id.split(","):
                policy_group_type, policy_group_value = policy_group.split(":")
                policy_group_position_to_report_dict.setdefault(policy_group_type, {})
                policy_group_position_to_report_dict[policy_group_type].setdefault(policy_group_value, [])
                for report in summary_policy_report.reports:
                    # add all position
                    policy_group_position_to_report_dict[policy_group_type][policy_group_value].append(report.report)
        for policy_group_type, item_value in policy_group_position_to_report_dict.iteritems():
            for policy_group_value, policy_report_list in item_value.iteritems():
                report = person.policy_group_report.add()
                report.policy_group_type = policy_group_type
                report.policy_group_value = policy_group_value
                PolicyReportUtil.build_summary_policy_report(policy_report_list, report.reports, is_validate)
                if not report.reports:
                    del person.policy_group_report[-1]
                report.roi_more_than_one_rate = PolicyReportUtil.build_roi_more_than_one_rate(report.reports)
        logging.info("end build_summary_policy_report_for_policy_group")


    @staticmethod
    def build_summary_policy_report_for_stock_policy_group(person, is_validate):
        logging.info("begin build_summary_policy_report_for_stock_policy_group")
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
                    PolicyReportUtil.build_summary_policy_report(policy_report_list, report.reports, is_validate)
                    if not report.reports:
                        del person.stock_policy_group_report[-1]
                    report.roi_more_than_one_rate = PolicyReportUtil.build_roi_more_than_one_rate(report.reports)
        logging.info("end build_summary_policy_report_for_stock_policy_group")


    @staticmethod
    def build_sort_report(person):
        logging.info("begin build_sort_report")

        # compare_method = PolicyReportUtil.greater_summary_policy_report_roi_top
        compare_method = PolicyReportUtil.greater_roi_more_than_one_rate

        sorted_stock_policy_report_list = sorted(person.stock_policy_report, cmp=compare_method)
        sorted_stock_policy_report_list = sorted(sorted_stock_policy_report_list, key=attrgetter('stock_id'), reverse=False)
        del person.stock_policy_report[:]
        person.sorted_stock_policy_report.extend(sorted_stock_policy_report_list)
        sorted_policy_stock_report_list = sorted(sorted_stock_policy_report_list, cmp=compare_method)
        del sorted_stock_policy_report_list[:]
        sorted_policy_stock_report_list = sorted(sorted_policy_stock_report_list, key=attrgetter('policy_id'), reverse=False)
        person.sorted_policy_stock_report.extend(sorted_policy_stock_report_list)
        del sorted_policy_stock_report_list[:]


        sorted_summary_policy_report_list = sorted(person.summary_policy_report, cmp=compare_method)
        del person.summary_policy_report[:]
        person.sorted_summary_policy_report.extend(sorted_summary_policy_report_list)
        del sorted_summary_policy_report_list[:]

        sorted_policy_group_report_list = sorted(person.policy_group_report, cmp=compare_method)
        del person.policy_group_report[:]
        sorted_policy_group_report_list = sorted(sorted_policy_group_report_list, key=attrgetter('policy_group_type'), reverse=False)
        person.sorted_policy_group_report.extend(sorted_policy_group_report_list)

        del sorted_policy_group_report_list[:]

        sorted_stock_policy_group_report_list = sorted(person.stock_policy_group_report, cmp=compare_method)
        del person.stock_policy_group_report[:]
        sorted_stock_policy_group_report_list = sorted(sorted_stock_policy_group_report_list, key=attrgetter('policy_group_type'), reverse=False)
        sorted_stock_policy_group_report_list = sorted(sorted_stock_policy_group_report_list, key=attrgetter('stock_id'), reverse=False)
        person.sorted_stock_policy_group_report.extend(sorted_stock_policy_group_report_list)
        del sorted_stock_policy_group_report_list[:]
        logging.info("end build_sort_report")


    @staticmethod
    def build_summary_policy_report(policy_report_list, repeated_stock_policy_report, is_validate):
        # TODO
        # if is_validate:
        #     filter_policy_report_list = policy_report_list
        # else:
        #     filter_policy_report_list = PolicyReportUtil.build_filter_report_list(policy_report_list)
        filter_policy_report_list = policy_report_list

        filter_sorted_policy_report_list = sorted(filter_policy_report_list, cmp=PolicyReportUtil.greater_policy_report_roi)
        if not filter_sorted_policy_report_list:
            return
        for position in localconfig.SUMMARY_POSITION_PERCENT_LIST:
            assert position <= 100
            # position: 0: roi最大， position 100: roi最小
            float_index = np.percentile(np.array(range(0, len(filter_sorted_policy_report_list))),
                                        position)
            index = int(float_index)
            position_report = repeated_stock_policy_report.add()
            position_report.position = position
            position_report.report.CopyFrom(filter_sorted_policy_report_list[index])
        #logging.info("sorted info: %s, %s", sorted_policy_report_list, repeated_stock_policy_report)


    @staticmethod
    def build_action_item_report(stock_info, action_item, report):
        report.Clear()
        report.stock_watch_days = PolicyReportUtil.build_watch_days(stock_info.daily_info, action_item)
        report.cash_taken_in = action_item.cash_taken_in
        report.cash_taken_out = PolicyReportUtil.get_asset_value_out(stock_info, action_item)
        # 增加float是因为python弱类型，会导致protobuf中float声明类型无效
        report.roi = float(report.cash_taken_out) / report.cash_taken_in if report.cash_taken_in > 0 else 1
        report.stock_buy_times = len(action_item.buy_stock_action)
        report.stock_sell_times = len(action_item.sell_stock_action)
        report.stock_hold_days = 0
        report.stock_hold_loss_days = 0
        report.stock_hold_profit_days = 0
        report.trade_profit_times = 0
        report.trade_loss_times = 0
        report.stock_hold_no_sell_times = 0
        for i in range(0, len(action_item.sell_stock_action)):
            buy_action_item = action_item.buy_stock_action[i]
            sell_action_item = action_item.sell_stock_action[i]
            if buy_action_item.at_price < sell_action_item.at_price:
                report.trade_profit_times += 1
            else:
                report.trade_loss_times += 1
            buy_date = DatetimeUtil.from_date_str(buy_action_item.date)
            sell_date = DatetimeUtil.from_date_str(sell_action_item.date)
            current_date = buy_date + datetime.timedelta(days=1)
            while current_date <= sell_date:
                current_date_str = DatetimeUtil.to_datetime_str(current_date)
                # advance to next date
                current_date = current_date + datetime.timedelta(days=1)
                the_stock_daily_info = PolicyReportUtil.get_the_stock_daily_info(stock_info, current_date_str)
                if not the_stock_daily_info:
                    continue
                if current_date <= sell_date:
                    the_check_price = the_stock_daily_info.low
                else:
                    the_check_price = sell_action_item.at_price
                if buy_action_item.at_price < the_check_price:
                    report.stock_hold_profit_days += 1
                else:
                    report.stock_hold_loss_days += 1
            report.stock_hold_days = report.stock_hold_profit_days + report.stock_hold_loss_days
        # 考虑没有卖出持有在手的情况, 以观察周期最后一天的下一天的close作为卖出价格
        if len(action_item.sell_stock_action) < len(action_item.buy_stock_action):
            report.stock_hold_no_sell_times = 1
            buy_action_item = action_item.buy_stock_action[-1]
            the_last_stock_daily_info = PolicyReportUtil.get_the_last_stock_daily_info(stock_info, action_item)
            the_stock_mean_price = PolicyReportUtil.get_medium_price(the_last_stock_daily_info)
            if buy_action_item.at_price < the_stock_mean_price:
                report.trade_profit_times += 1
            else:
                report.trade_loss_times += 1
            buy_date = DatetimeUtil.from_date_str(buy_action_item.date)
            last_date = DatetimeUtil.from_date_str(the_last_stock_daily_info.date)
            current_date = buy_date + datetime.timedelta(days=1)
            while current_date <= last_date:
                current_date_str = DatetimeUtil.to_datetime_str(current_date)
                # advance to next date
                current_date = current_date + datetime.timedelta(days=1)
                the_stock_daily_info = PolicyReportUtil.get_the_stock_daily_info(stock_info, current_date_str)
                if not the_stock_daily_info:
                    continue
                if buy_action_item.at_price < the_stock_daily_info.low:
                    report.stock_hold_profit_days += 1
                else:
                    report.stock_hold_loss_days += 1
            report.stock_hold_days = report.stock_hold_profit_days + report.stock_hold_loss_days
        return report


    @staticmethod
    def build_filter_report_list(policy_report_list):
        result = []
        for report in policy_report_list:
            min_sell_day = report.stock_watch_days * localconfig.MIN_TRADE_DAYS_PERCENT / 100.0
            if max(min_sell_day,localconfig.MIN_TRADE_DAYS) <= report.stock_sell_times \
                    and (float(report.stock_hold_days)/report.stock_buy_times <= localconfig.MAX_MEAN_DAYS_HOLD_FOR_SALE):
                result.append(report)
        return result

    @staticmethod
    def build_watch_days(repeated_daily_info, action_item):
        stock_watch_days = 0
        for stock in repeated_daily_info:
            if action_item.trade_watch_start_date <= stock.date and stock.date < action_item.trade_watch_end_date:
                stock_watch_days += 1
        return stock_watch_days


    @staticmethod
    def get_asset_value_out(stock_info, action_item):
        cash_value = PolicyReportUtil.get_cash_value_available(action_item)
        asset_value_taken_out = cash_value
        if len(action_item.sell_stock_action) < len(action_item.buy_stock_action):
            the_stock_daily_info = PolicyReportUtil.get_the_last_stock_daily_info(stock_info, action_item)
            the_stock_mean_price = PolicyReportUtil.get_medium_price(the_stock_daily_info)
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
        # 以观察周期最后一天的下一天的close作为卖出价格
        return PolicyReportUtil.get_the_stock_daily_info(stock_info, action_item.trade_watch_end_date)


    @staticmethod
    def get_previous_stock_daily_info(stock_info, trade_watch_start_date_str, current_date_str):
        begin_date = DatetimeUtil.from_date_str(trade_watch_start_date_str)
        previous_date = DatetimeUtil.from_date_str(current_date_str) + datetime.timedelta(days=-1)
        while begin_date <= previous_date:
            the_daily_info = PolicyReportUtil.get_the_stock_daily_info(stock_info,
                                                                       DatetimeUtil.to_datetime_str(previous_date))
            if not the_daily_info:
                previous_date += datetime.timedelta(days=-1)
                continue
            return the_daily_info
        return None


    @staticmethod
    def get_the_stock_daily_info(stock_info, current_date_str):
        stock_id = stock_info.stock_id
        if stock_id in PolicyReportUtil.stock_date_dict:
            if current_date_str in PolicyReportUtil.stock_date_dict[stock_id]:
                return PolicyReportUtil.stock_date_dict[stock_id][current_date_str]
            else:
                return None
        else:
            PolicyReportUtil.stock_date_dict.setdefault(stock_id, {})
            for stock_daily_info in stock_info.daily_info:
                PolicyReportUtil.stock_date_dict[stock_id][stock_daily_info.date] = stock_daily_info
            if stock_id in PolicyReportUtil.stock_date_dict and current_date_str in PolicyReportUtil.stock_date_dict[stock_id]:
                return PolicyReportUtil.stock_date_dict[stock_id][current_date_str]
            else:
                return None


    @staticmethod
    def greater_policy_report_roi(left, right):
        if left.roi != right.roi:
            return -1 if right.roi < left.roi else 1
        if left.stock_sell_times != right.stock_sell_times:
            return -1 if right.stock_sell_times < left.stock_sell_times else 1
        if left.stock_buy_times != right.stock_buy_times:
            return -1 if right.stock_buy_times < left.stock_buy_times else 1
        if right.trade_profit_times != left.trade_profit_times:
            return -1 if right.trade_profit_times < left.trade_profit_times else 1
        return 0


    @staticmethod
    def greater_summary_policy_report_roi_top(left, right):
        # compare with the best roi for report
        top_percent = int(localconfig.TOP_PERCENT / 10)
        return PolicyReportUtil.greater_policy_report_roi(left.reports[top_percent].report, right.reports[top_percent].report)


    @staticmethod
    def greater_roi_more_than_one_rate(left, right):
        # compare with the best roi for report
        top_percent = int(localconfig.TOP_PERCENT / 10)
        if left.roi_more_than_one_rate != right.roi_more_than_one_rate:
            return -1 if right.roi_more_than_one_rate < left.roi_more_than_one_rate else 1
        return PolicyReportUtil.greater_summary_policy_report_roi_top(left, right)


    @staticmethod
    def print_summary(person):
        logging.info("-----------------------")
        for item_report in person.sorted_policy_group_report:
            logging.info("policy_group_report:\t%s:%s\t%s",
                         item_report.policy_group_type, item_report.policy_group_value,
                         PolicyReportUtil.build_percent_policy_report_msg(item_report))
        logging.info("-----------------------")
        for item_report in person.sorted_summary_policy_report:
            logging.info("summary_policy_report:\t%s\t%s",
                         item_report.policy_id,
                         PolicyReportUtil.build_percent_policy_report_msg(item_report))
        logging.info("-----------------------")
        for item_report in person.sorted_stock_policy_group_report:
            logging.info("stock_policy_group_report:\t%s\t%s:%s\t%s",
                         item_report.stock_id,
                         item_report.policy_group_type,
                         item_report.policy_group_value,
                         PolicyReportUtil.build_percent_policy_report_msg(item_report))
        logging.info("-----------------------")
        for item_report in person.sorted_stock_policy_report:
            logging.info("stock_policy_report:\t%s\t%s\t%s",
                         item_report.stock_id,
                         item_report.policy_id,
                         PolicyReportUtil.build_percent_policy_report_msg(item_report))
        logging.info("-----------------------")


    @staticmethod
    def build_percent_policy_report_msg(percent_policy_report):
        result = "P20:(%s,%s)\tP50:(%s,%s)\tP80:(%s,%s)\tP100:(%s,%s)\tP0:(%s,%s)" % (
            percent_policy_report.reports[2].report.roi,
            percent_policy_report.reports[2].report.stock_sell_times,
            percent_policy_report.reports[5].report.roi,
            percent_policy_report.reports[5].report.stock_sell_times,
            percent_policy_report.reports[8].report.roi,
            percent_policy_report.reports[8].report.stock_sell_times,
            percent_policy_report.reports[10].report.roi,
            percent_policy_report.reports[10].report.stock_sell_times,
            percent_policy_report.reports[0].report.roi,
            percent_policy_report.reports[0].report.stock_sell_times
        )
        return result


    @staticmethod
    def build_roi_more_than_one_rate(repeated_percent_policy_report):
        if not repeated_percent_policy_report:
            return 1
        size = len(repeated_percent_policy_report)
        more_than_one_count = 0
        for item in repeated_percent_policy_report:
            if item.report.roi > 1:
                more_than_one_count += 1
        return int(float(more_than_one_count) * 100/size) / 100.0


    @staticmethod
    def get_medium_price(stock_daily_info):
        return (stock_daily_info.high + stock_daily_info.low) / 2.0