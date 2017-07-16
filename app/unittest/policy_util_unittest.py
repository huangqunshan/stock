import unittest
from policy_util import PolicyUtil
from policy_report_util import PolicyReportUtil
from policy_predict_util import PolicyPredictUtil
from proto.policy_pb2 import Policy, PolicyReport
from proto.person_pb2 import Person
from proto.stock_info_pb2 import StockInfo


class MyTestCase(unittest.TestCase):

    def test_get_volumn_and_trade_cost(self):
        volumn, final_cost = PolicyUtil.get_volumn_and_trade_cost(30001, 150)
        self.assertEqual(200, volumn)
        self.assertEqual(final_cost, 1)

        volumn, final_cost = PolicyUtil.get_volumn_and_trade_cost(30003, 100)
        self.assertEqual(300, volumn)
        self.assertEqual(final_cost, 1.5)

        volumn, final_cost = PolicyUtil.get_volumn_and_trade_cost(30093, 100)
        self.assertEqual(300, volumn)
        self.assertEqual(final_cost, 1.5)

    def test_get_trade_watch_date_list(self):
        stock_info = StockInfo()
        self.assertEqual([], PolicyUtil.get_trade_watch_date_list(stock_info.daily_info, 1, 1, 1))

        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170101"
        self.assertEqual([], PolicyUtil.get_trade_watch_date_list(stock_info.daily_info, 1, 1, 1))

        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170102"
        self.assertEqual([], PolicyUtil.get_trade_watch_date_list(stock_info.daily_info, 1, 1, 1))

        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170103"
        self.assertEqual([("20170102", "20170103")], PolicyUtil.get_trade_watch_date_list(stock_info.daily_info, 1, 1, 1))
        self.assertEqual([("20170102", "20170103")], PolicyUtil.get_trade_watch_date_list(stock_info.daily_info, 1, 1, 2))

        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170104"
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170105"
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170106"
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170107"
        self.assertEqual([("20170102", "20170107")], PolicyUtil.get_trade_watch_date_list(stock_info.daily_info, 1, 1, 1))
        self.assertEqual([("20170102", "20170107")], PolicyUtil.get_trade_watch_date_list(stock_info.daily_info, 1, 1, 2))
        self.assertEqual([("20170102", "20170107"), ("20170105", "20170107")], PolicyUtil.get_trade_watch_date_list(stock_info.daily_info, 1, 2, 2))
        self.assertEqual([("20170102", "20170106"), ("20170104", "20170107"), ("20170106", "20170107")],
                         PolicyUtil.get_trade_watch_date_list(stock_info.daily_info, 1, 3, 2))


    def test_get_the_stock_daily_info(self):
        stock_info = StockInfo()
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170101"
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170102"
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170105"
        self.assertTrue(PolicyReportUtil.get_the_stock_daily_info(stock_info, "20170101"))
        self.assertTrue(PolicyReportUtil.get_the_stock_daily_info(stock_info, "20170102"))
        self.assertTrue(not PolicyReportUtil.get_the_stock_daily_info(stock_info, "20170103"))
        self.assertTrue(PolicyReportUtil.get_the_stock_daily_info(stock_info, "20170105"))


    def test_build_watch_days(self):
        stock_info = StockInfo()
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170101"
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170102"
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170105"
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170106"
        action_item = Person.StockPolicyActionsItem()
        action_item.trade_watch_start_date = "20170103"
        action_item.trade_watch_end_date = "20170107"
        self.assertEqual(2, PolicyReportUtil.build_watch_days(stock_info.daily_info, action_item))


    def test_get_cash_value_available(self):
        action_item = Person.StockPolicyActionsItem()
        action_item.cash_taken_in = 3001
        action_item.trade_watch_start_date = "20170101"
        action_item.trade_watch_end_date = "20170102"
        buy_action = action_item.buy_stock_action.add()
        buy_action.date = "20170101"
        buy_action.at_price = 10
        buy_action.volumn = 200
        buy_action.stock_trade_cost = 1
        self.assertEqual(1000, PolicyReportUtil.get_cash_value_available(action_item))


    def test_get_asset_value_out(self):
        stock_info = StockInfo()
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170101"
        daily_info.low = daily_info.high = daily_info.close = 10
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170102"
        daily_info.low = daily_info.high = daily_info.close = 10.5
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170105"
        daily_info.low = daily_info.high = daily_info.close = 10.1
        action_item = Person.StockPolicyActionsItem()
        action_item.cash_taken_in = 5100
        action_item.trade_watch_start_date = "20170101"
        action_item.trade_watch_end_date = "20170102"
        buy_action = action_item.buy_stock_action.add()
        buy_action.date = "20170101"
        buy_action.at_price = 10
        buy_action.volumn = 200
        buy_action.stock_trade_cost = 1
        self.assertEqual(5100 - 1 - 10*200 + 10.5*200 -1, PolicyReportUtil.get_asset_value_out(stock_info, action_item))

        action_item.trade_watch_end_date = "20170105"
        self.assertEqual(5100 - 1 - 10*200 + 10.1*200 -1, PolicyReportUtil.get_asset_value_out(stock_info, action_item))

        sell_action = action_item.sell_stock_action.add()
        sell_action.date = "20170102"
        sell_action.at_price = 10.3
        sell_action.volumn = 200
        sell_action.stock_trade_cost = 1
        self.assertEqual(5100 - 1 - 10*200 + 10.3*200 -1, PolicyReportUtil.get_asset_value_out(stock_info, action_item))


    def test_build_action_item_report(self):
        stock_info = StockInfo()
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170101"
        daily_info.low = daily_info.high = daily_info.close = 10
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170102"
        daily_info.low = daily_info.high = daily_info.close = 10.5
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170105"
        daily_info.low = daily_info.high = daily_info.close = 10.1
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170106"
        daily_info.low = daily_info.high = daily_info.close = 9
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170108"
        daily_info.low = daily_info.high = daily_info.close = 10.0
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170109"
        daily_info.low = daily_info.high = daily_info.close = 10.9
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170110"
        daily_info.low = daily_info.high = daily_info.close = 9.5
        action_item = Person.StockPolicyActionsItem()
        action_item.cash_taken_in = 5100.0
        action_item.trade_watch_start_date = "20170101"
        action_item.trade_watch_end_date = "20170102"
        buy_action = action_item.buy_stock_action.add()
        buy_action.date = "20170101"
        buy_action.at_price = 10
        buy_action.volumn = 200
        buy_action.stock_trade_cost = 1
        report = PolicyReport()
        PolicyReportUtil.build_action_item_report(stock_info, action_item, report)
        self.assertEqual(1, report.stock_watch_days)
        self.assertEqual(5100, report.cash_taken_in)
        self.assertEqual(5100 - 10*200 -1 + 10.5*200 -1, report.cash_taken_out)
        self.assertEqual(float(report.cash_taken_out)/report.cash_taken_in, report.roi)
        self.assertEqual(1, report.stock_buy_times)
        self.assertEqual(0, report.stock_sell_times)
        self.assertEqual(1, report.trade_profit_times)
        self.assertEqual(0, report.trade_loss_times)
        self.assertEqual(1, report.stock_hold_days)
        self.assertEqual(1, report.stock_hold_profit_days)
        self.assertEqual(0, report.stock_hold_loss_days)
        self.assertEqual(report.stock_buy_times-report.stock_sell_times, report.stock_hold_no_sell_times)


        action_item.trade_watch_end_date = "20170105"
        PolicyReportUtil.build_action_item_report(stock_info, action_item, report)
        self.assertEqual(5100 - 10 * 200 - 1 + 10.1 * 200 - 1, report.cash_taken_out)
        self.assertEqual(report.stock_buy_times - report.stock_sell_times, report.stock_hold_no_sell_times)


        sell_action = action_item.sell_stock_action.add()
        sell_action.date = "20170102"
        sell_action.at_price = 10.2
        sell_action.volumn = 200
        sell_action.stock_trade_cost = 1
        PolicyReportUtil.build_action_item_report(stock_info, action_item, report)
        self.assertEqual(2, report.stock_watch_days)
        self.assertEqual(5100, report.cash_taken_in)
        self.assertEqual(5100 - 10*200 -1 + 10.2*200 -1, report.cash_taken_out)
        self.assertEqual(report.cash_taken_out/report.cash_taken_in, report.roi)
        self.assertEqual(1, report.stock_buy_times)
        self.assertEqual(1, report.stock_sell_times)
        self.assertEqual(1, report.trade_profit_times)
        self.assertEqual(0, report.trade_loss_times)
        self.assertEqual(1, report.stock_hold_days)
        self.assertEqual(1, report.stock_hold_profit_days)
        self.assertEqual(0, report.stock_hold_loss_days)
        self.assertEqual(report.stock_buy_times - report.stock_sell_times, report.stock_hold_no_sell_times)

        sell_action.date = "20170102"
        sell_action.at_price = 9
        sell_action.volumn = 200
        sell_action.stock_trade_cost = 1
        PolicyReportUtil.build_action_item_report(stock_info, action_item, report)
        self.assertEqual(2, report.stock_watch_days)
        self.assertEqual(5100, report.cash_taken_in)
        self.assertEqual(5100 - 10*200 -1 + 9*200 -1, report.cash_taken_out)
        self.assertEqual(report.cash_taken_out/report.cash_taken_in, report.roi)
        self.assertEqual(1, report.stock_buy_times)
        self.assertEqual(1, report.stock_sell_times)
        self.assertEqual(0, report.trade_profit_times)
        self.assertEqual(1, report.trade_loss_times)
        self.assertEqual(1, report.stock_hold_days)
        self.assertEqual(0, report.stock_hold_profit_days)
        self.assertEqual(1, report.stock_hold_loss_days)
        self.assertEqual(report.stock_buy_times - report.stock_sell_times, report.stock_hold_no_sell_times)


        buy_action = action_item.buy_stock_action.add()
        buy_action.date = "20170105"
        buy_action.at_price = 10.5
        buy_action.volumn = 200
        buy_action.stock_trade_cost = 1
        action_item.trade_watch_end_date = "20170110"
        PolicyReportUtil.build_action_item_report(stock_info, action_item, report)
        self.assertEqual(6, report.stock_watch_days)
        self.assertEqual(5100, report.cash_taken_in)
        self.assertEqual(5100 - 10*200 -1 + 9*200 -1 - 10.5*200 -1 + 9.5*200 -1, report.cash_taken_out)
        self.assertEqual(report.cash_taken_out/report.cash_taken_in, report.roi)
        self.assertEqual(2, report.stock_buy_times)
        self.assertEqual(1, report.stock_sell_times)
        self.assertEqual(0, report.trade_profit_times)
        self.assertEqual(2, report.trade_loss_times)
        self.assertEqual(5, report.stock_hold_days)
        self.assertEqual(1, report.stock_hold_profit_days)
        self.assertEqual(4, report.stock_hold_loss_days)
        self.assertEqual(report.stock_buy_times - report.stock_sell_times, report.stock_hold_no_sell_times)


    def test_greater_policy_report_roi_top(self):
        left = PolicyReport()
        left.roi = 1.0
        left.stock_sell_times = 2
        left.stock_buy_times = 2
        left.trade_profit_times = 2
        right = PolicyReport()
        right.roi = 1.0
        right.stock_sell_times = 2
        right.stock_buy_times = 2
        right.trade_profit_times = 2
        self.assertTrue(PolicyReportUtil.greater_policy_report_roi(left, right) == 0)
        left.roi = 1.1
        self.assertTrue(PolicyReportUtil.greater_policy_report_roi(left, right) < 0)
        left.roi = 1.0
        left.stock_sell_times = 3
        self.assertTrue(PolicyReportUtil.greater_policy_report_roi(left, right) < 0)
        left.stock_sell_times = 1
        self.assertTrue(not PolicyReportUtil.greater_policy_report_roi(left, right) < 0)
        left.stock_sell_times = 2
        left.stock_buy_times = 3
        self.assertTrue(PolicyReportUtil.greater_policy_report_roi(left, right) < 0)
        left.stock_buy_times = 1
        self.assertTrue(not PolicyReportUtil.greater_policy_report_roi(left, right) < 0)
        left.stock_buy_times = 2
        left.trade_profit_times = 3
        self.assertTrue(PolicyReportUtil.greater_policy_report_roi(left, right) < 0)

    def test_get_previous_stock_daily_info(self):
        stock_info = StockInfo()
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170101"
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170102"
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170105"
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170106"
        daily_info = stock_info.daily_info.add()
        daily_info.date = "20170108"
        self.assertEqual("20170102", PolicyReportUtil.get_previous_stock_daily_info(stock_info, "20170101", "20170105").date)
        self.assertEqual(None, PolicyReportUtil.get_previous_stock_daily_info(stock_info, "20170103", "20170105"))
        self.assertEqual("20170105", PolicyReportUtil.get_previous_stock_daily_info(stock_info, "20170101", "20170106").date)


if __name__ == '__main__':
    unittest.main()
