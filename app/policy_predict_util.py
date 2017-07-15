# coding=utf8

import datetime
import logging
import math
import numpy as np
from operator import attrgetter
from datetime_util import DatetimeUtil
from price_util import PercentPriceUtil
from proto.policy_pb2 import Policy
import localconfig


class PolicyPredictUtil:

    @staticmethod
    def predict(stock_info, check_date_str, trend_mode):
        # TODO: filter stock_info for old date
        # [stock_id] = {(trend, trend_buy, trend_sell, last_close, [price1, price2, ...], [price1, price2, ...])}
        buy_policy_list = PolicyPredictUtil.get_best_buy_policy_list()
        stock_price_dict = {}
        for stock in stock_info:
            if not stock.daily_info:
                logging.error("failed to get daily info for %s", stock.stock_id)
                continue
            # ignore low price stock for cost for trade
            if stock.daily_info[-1].close < localconfig.MIN_STOCK_PRICE.best[0]:
                continue
            full_trend = PolicyPredictUtil.get_flow_trend(PolicyPredictUtil.get_flow_detail_list(stock.daily_info, trend_mode))
            # half_trend = PolicyPredictUtil.get_flow_trend(PolicyPredictUtil.get_flow_detail_list(stock.daily_info[len(stock.daily_info)/2:], trend_mode))
            last_sequential_trend = PolicyPredictUtil.get_sequential_trend(stock.daily_info, trend_mode)
            for policy in buy_policy_list:
                price = PercentPriceUtil.generate_percent(stock.daily_info[-policy.buy.days_watch:],
                                                          policy.buy.at_percent.mode,
                                                          policy.buy.at_percent.percent_n)
                stock_price_dict.setdefault(stock.stock_id, [full_trend, 1, 1, 0, [], [], 0])
                stock_price_dict[stock.stock_id][3] = stock.daily_info[-1].close
                stock_price_dict[stock.stock_id][4].append(price)
                if full_trend in localconfig.BUY_TREND_PERCENT.filter:
                    stock_price_dict[stock.stock_id][1] = 1
                else:
                    stock_price_dict[stock.stock_id][1] = 0
                # if half_trend in localconfig.HALF_BUY_TREND_PERCENT.filter:
                #     stock_price_dict[stock.stock_id][1] += 2
                if last_sequential_trend in localconfig.LAST_BUY_SEQUENTIAL_TREND_COUNT.filter:
                    stock_price_dict[stock.stock_id][1] += 4
                stock_price_dict[stock.stock_id][6] = last_sequential_trend
        sell_policy_list = PolicyPredictUtil.get_best_sell_policy_list()
        for stock in stock_info:
            if not stock.daily_info:
                logging.error("failed to get daily info for %s", stock.stock_id)
                continue
            # ignore low price stock for cost for trade
            if stock.daily_info[-1].close < localconfig.MIN_STOCK_PRICE.best[0]:
                continue
            full_trend = PolicyPredictUtil.get_flow_trend(PolicyPredictUtil.get_flow_detail_list(stock.daily_info, trend_mode))
            # half_trend = PolicyPredictUtil.get_flow_trend(PolicyPredictUtil.get_flow_detail_list(stock.daily_info[len(stock.daily_info)/2:], trend_mode))
            last_sequential_trend = PolicyPredictUtil.get_sequential_trend(stock.daily_info, trend_mode)
            for policy in sell_policy_list:
                price = PercentPriceUtil.generate_percent(stock.daily_info[-policy.sell.days_watch:],
                                                          policy.sell.at_percent.mode,
                                                          policy.sell.at_percent.percent_n)
                stock_price_dict.setdefault(stock.stock_id, [full_trend, 1,1, 0, [], []])
                stock_price_dict[stock.stock_id][3] = stock.daily_info[-1].close
                stock_price_dict[stock.stock_id][5].append(price)
                if full_trend in localconfig.SELL_TREND_PERCENT.filter:
                    stock_price_dict[stock.stock_id][2] = 1
                else:
                    stock_price_dict[stock.stock_id][2] = 0
                # if half_trend in localconfig.HALF_SELL_TREND_PERCENT.filter:
                #     stock_price_dict[stock.stock_id][2] += 2
                if last_sequential_trend in localconfig.LAST_SELL_SEQUENTIAL_TREND_COUNT.filter:
                    stock_price_dict[stock.stock_id][2] += 4
        return stock_price_dict


    @staticmethod
    def get_best_buy_policy_list(limit_count=100):
        policy_best = Policy()
        policy_best.buy.days_watch = localconfig.BUY_WATCH_DAYS.best[0]
        policy_best.buy.at_percent.mode = localconfig.BUY_MODE.best[0]
        policy_best.buy.at_percent.percent_n = localconfig.BUY_PRICE_PERCENT.best[0]
        return [policy_best]

    @staticmethod
    def get_best_sell_policy_list(limit_count=100):
        policy_best = Policy()
        policy_best.sell.days_watch = localconfig.SELL_WATCH_DAYS.best[0]
        policy_best.sell.at_percent.mode = localconfig.SELL_MODE.best[0]
        policy_best.sell.at_percent.percent_n = localconfig.SELL_PRICE_PERCENT.best[0]
        return [policy_best]

    @staticmethod
    def get_flow_trend(flow_detail_list):
        # return 0 for empty list
        if not flow_detail_list:
            return 0
        growth = 0.0
        for flow in flow_detail_list:
            if flow > 0:
                growth = growth + 1
            # elif flow < -1.1:
            #     growth -= 1
        # logging.debug("growth:%s, flow_detail_list:%s", growth, flow_detail_list)
        return int(10 * growth/len(flow_detail_list)) * 10


    @staticmethod
    def get_flow_detail_list(repeated_stock_daily_info, mode):
        # return PolicyPredictUtil.get_flow_detail_list_weighted(repeated_stock_daily_info)

        result = []
        for i in range(1, len(repeated_stock_daily_info)):
            current_info = repeated_stock_daily_info[i]
            last_info = repeated_stock_daily_info[i-1]
            current_medium = PolicyPredictUtil.get_price(current_info, mode)
            last_medium = PolicyPredictUtil.get_price(last_info, mode)
            if current_medium > last_medium:
                result.append(1)
            else:
                result.append(-1)
        return result

    @staticmethod
    def get_price(stock_daily_info, mode):
        assert mode in [Policy.TradePolicy.Percent.HIGH,
                        Policy.TradePolicy.Percent.LOW,
                        Policy.TradePolicy.Percent.MEDIUM]
        if Policy.TradePolicy.Percent.LOW == mode:
            return stock_daily_info.low
        if Policy.TradePolicy.Percent.HIGH == mode:
            return stock_daily_info.high
        assert mode == Policy.TradePolicy.Percent.MEDIUM
        return 0.5 * (stock_daily_info.high + stock_daily_info.low)


    # @staticmethod
    # # 复杂策略，如突破高点与低点权重变大
    # def get_flow_detail_list_weighted(repeated_stock_daily_info):
    #     result = []
    #     the_max = -1
    #     the_min = repeated_stock_daily_info[0].high * 100
    #     for i in range(1, len(repeated_stock_daily_info)):
    #         current_info = repeated_stock_daily_info[i]
    #         last_info = repeated_stock_daily_info[i-1]
    #         current_medium = 0.5 * (current_info.high+current_info.low)
    #         last_medium = 0.5 * (last_info.high + last_info.low)
    #         if current_medium > last_medium:
    #             if the_max == -1 or current_medium < the_max:
    #                 result.append(1)
    #             else:
    #                 result.append(2)
    #         else:
    #             if the_min == -1 or the_min < current_medium:
    #                 result.append(-1)
    #             else:
    #                 result.append(-2)
    #         the_max = max(the_max, current_medium)
    #         the_min = min(the_min, current_medium)
    #     return result


    @staticmethod
    def get_sequential_trend(repeated_stock_daily_info, mode):
        trend_list = PolicyPredictUtil.get_flow_detail_list(repeated_stock_daily_info, mode)
        if not trend_list:
            return 0
        sign = trend_list[-1]
        assert sign in [1, -1], sign
        count = 1
        for i in range(len(trend_list)-2, -1, -1):
            if trend_list[i] != sign:
                break
            count += 1
        result = sign * count
        logging.debug("sequential trend:%s, list:%s", result, trend_list)
        return result


