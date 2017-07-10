import unittest
from policy_util import PolicyUtil
from policy_predict_util import PolicyPredictUtil
from proto.policy_pb2 import Policy
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
        self.assertTrue(PolicyUtil.get_the_stock_daily_info(stock_info, "20170101"))
        self.assertTrue(PolicyUtil.get_the_stock_daily_info(stock_info, "20170102"))
        self.assertTrue(not PolicyUtil.get_the_stock_daily_info(stock_info, "20170103"))
        self.assertTrue(PolicyUtil.get_the_stock_daily_info(stock_info, "20170105"))



if __name__ == '__main__':
    unittest.main()
