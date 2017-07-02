# coding=utf8

import datetime
import logging
import numpy as np
from proto.policy_pb2 import Policy
import localconfig


class PercentPriceUtil:

    # [stock_id][days_watch][current_date_str][percent_mode] = {percent_n: price}
    stock_percent_map = {}

    @staticmethod
    def is_existing(stock_id, days_watch, current_date_str, percent_mode):
        if stock_id not in PercentPriceUtil.stock_percent_map:
            return False
        if days_watch not in PercentPriceUtil.stock_percent_map[stock_id]:
            return False
        if current_date_str not in PercentPriceUtil.stock_percent_map[stock_id][days_watch]:
            return False
        if percent_mode not in PercentPriceUtil.stock_percent_map[stock_id][days_watch][current_date_str]:
            return False
        return True

    @staticmethod
    def get(stock_id, days_watch, current_date_str, percent_mode):
        logging.debug("begin percent_map get:stock_id:%s, days_watch:%s, current_date_str:%s, percent_mode:%s",
                     stock_id, days_watch, current_date_str, percent_mode)
        percent_map = PercentPriceUtil.stock_percent_map[stock_id][days_watch][current_date_str][percent_mode]
        logging.debug("end percent_map get:stock_id:%s, days_watch:%s, current_date_str:%s, percent_mode:%s, percent_map:%s",
                     stock_id, days_watch, current_date_str, percent_mode, percent_map)
        return percent_map

    @staticmethod
    def put(stock_id, days_watch, current_date_str, percent_mode, percent_map):
        logging.debug("begin percent_map put:stock_id:%s, days_watch:%s, current_date_str:%s, percent_mode:%s, percent_map:%s",
                     stock_id, days_watch, current_date_str, percent_mode, percent_map)
        PercentPriceUtil.stock_percent_map.setdefault(stock_id, {})
        PercentPriceUtil.stock_percent_map[stock_id].setdefault(days_watch, {})
        PercentPriceUtil.stock_percent_map[stock_id][days_watch].setdefault(current_date_str, {})
        PercentPriceUtil.stock_percent_map[stock_id][days_watch][current_date_str][percent_mode] = percent_map
        logging.debug("end percent_map put")


    @staticmethod
    def get_percent_price(stock_id, days_watch, current_date_str, stock_daily_info_list, at_percent):
        logging.debug("begin get_percent_price, stock_id:%s, days_watch:%s, current_date_str:%s, at_percent:%s",
                     stock_id, days_watch, current_date_str, at_percent)
        assert stock_daily_info_list
        if PercentPriceUtil.is_existing(stock_id, days_watch, current_date_str, at_percent.mode):
            percent_map = PercentPriceUtil.get(stock_id, days_watch, current_date_str, at_percent.mode)
            logging.debug("end get_percent_price")
            return percent_map.get(at_percent.percent_n)
        #return PercentPriceUtil.generate_percent(stock_daily_info_list, at_percent.mode, at_percent.percent_n)
        # cost time: at least 30:26
        price_percent_list = localconfig.BUY_PRICE_PERCENT_LIST + localconfig.SELL_PRICE_PERCENT_LIST
        percent_map = PercentPriceUtil.generate_percent_map(stock_daily_info_list, at_percent.mode, price_percent_list)
        PercentPriceUtil.put(stock_id, days_watch, current_date_str, at_percent.mode, percent_map)
        logging.debug("end get_percent_price")
        assert at_percent.percent_n in percent_map, "%s vs %s" % (at_percent.percent_n, percent_map)
        return percent_map.get(at_percent.percent_n)

    @staticmethod
    def generate_percent_map(stock_daily_info_list, percent_mode, price_percent_list):
        logging.debug("begin generate_percent_map, stock_daily_info_list:%s, percent_mode:%s",
                      stock_daily_info_list, percent_mode)
        stock_price_list = []
        for stock_daily_info in stock_daily_info_list:
            if percent_mode == Policy.TradePolicy.Percent.LOW:
                stock_price_list.append(stock_daily_info.low)
            elif percent_mode == Policy.TradePolicy.Percent.HIGH:
                stock_price_list.append(stock_daily_info.high)
            elif percent_mode == Policy.TradePolicy.Percent.MEDIUM:
                stock_price_list.append((stock_daily_info.high+stock_daily_info.low)/2.0)
            elif percent_mode == Policy.TradePolicy.Percent.CLOSE:
                stock_price_list.append(stock_daily_info.close)
            elif percent_mode == Policy.TradePolicy.Percent.OPEN:
                stock_price_list.append(stock_daily_info.open)
            else:
                assert False, "unknown mode"
        percent_map = {}
        numpy_array = np.array(stock_price_list)
        for percent_n in price_percent_list:
            if percent_n <= 100:
                percent_map[percent_n] = np.percentile(numpy_array, percent_n)
            else:
                percent_map[percent_n] = np.percentile(numpy_array, 100) * (percent_n/100.0)
        logging.debug("end generate_percent_map")
        return percent_map

    @staticmethod
    def generate_percent(stock_daily_info_list, percent_mode, percent_n):
        assert stock_daily_info_list
        logging.debug("begin generate_percent, stock_daily_info_list:%s, percent_mode:%s",
                      stock_daily_info_list, percent_mode)
        stock_price_list = []
        for stock_daily_info in stock_daily_info_list:
            if percent_mode == Policy.TradePolicy.Percent.LOW:
                stock_price_list.append(stock_daily_info.low)
            elif percent_mode == Policy.TradePolicy.Percent.HIGH:
                stock_price_list.append(stock_daily_info.high)
            elif percent_mode == Policy.TradePolicy.Percent.MEDIUM:
                stock_price_list.append((stock_daily_info.high+stock_daily_info.low)/2.0)
            elif percent_mode == Policy.TradePolicy.Percent.CLOSE:
                stock_price_list.append(stock_daily_info.close)
            elif percent_mode == Policy.TradePolicy.Percent.OPEN:
                stock_price_list.append(stock_daily_info.open)
            else:
                assert False, "unknown mode"
        numpy_array = np.array(stock_price_list)
        # logging.info("test: %s, %s", percent_n, stock_price_list)
        result = None
        if percent_n <= 100:
            result = np.percentile(numpy_array, percent_n)
        else:
            result = np.percentile(numpy_array, 100) * (percent_n/100.0)
        logging.debug("end generate_percent")
        return result
