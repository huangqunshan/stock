# coding=utf8

from datetime import date, datetime
import logging

class DatetimeUtil:
    PATTERN_STR = "%Y%m%d"

    @staticmethod
    def from_date_str(datetimestr):
        return datetime.strptime(datetimestr, DatetimeUtil.PATTERN_STR)

    @staticmethod
    def to_datetime_str(datetimeobj):
        return datetimeobj.strftime(DatetimeUtil.PATTERN_STR)


