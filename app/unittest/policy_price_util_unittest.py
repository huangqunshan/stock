import unittest
from policy_predict_util import PolicyPredictUtil
from proto.policy_pb2 import Policy
from proto.person_pb2 import Person
from proto.stock_info_pb2 import StockInfo

class MyTestCase(unittest.TestCase):

    def test_get_flow_trend(self):
        self.assertEqual(0, PolicyPredictUtil.get_flow_trend([]))
        self.assertEqual(100, PolicyPredictUtil.get_flow_trend([1]))
        self.assertEqual(0, PolicyPredictUtil.get_flow_trend([-1]))
        self.assertEqual(50, PolicyPredictUtil.get_flow_trend([-1,1]))
        self.assertEqual(50, PolicyPredictUtil.get_flow_trend([1, -1]))
        self.assertEqual(70, PolicyPredictUtil.get_flow_trend([1, -1, 1, 1]))
        self.assertEqual(60, PolicyPredictUtil.get_flow_trend([1, -1, 1]))


    def test_get_flow_detail_list_empty(self):
        stock_info = StockInfo()
        self.assertEqual(0, PolicyPredictUtil.get_sequential_trend(stock_info.daily_info, Policy.TradePolicy.Percent.HIGH))
        self.assertEqual([], PolicyPredictUtil.get_flow_detail_list(stock_info.daily_info, Policy.TradePolicy.Percent.HIGH))
        daily_info = stock_info.daily_info.add()
        daily_info.high = 100
        self.assertEqual([], PolicyPredictUtil.get_flow_detail_list(stock_info.daily_info, Policy.TradePolicy.Percent.HIGH))

    def test_get_flow_detail_list_normal(self):
        stock_info = StockInfo()
        self.assertEqual(0, PolicyPredictUtil.get_sequential_trend(stock_info.daily_info, Policy.TradePolicy.Percent.HIGH))
        daily_info = stock_info.daily_info.add()
        daily_info.high = 100
        daily_info = stock_info.daily_info.add()
        daily_info.high = 101
        daily_info = stock_info.daily_info.add()
        daily_info.high = 102
        daily_info = stock_info.daily_info.add()
        daily_info.high = 101.5
        daily_info = stock_info.daily_info.add()
        daily_info.high = 99
        daily_info = stock_info.daily_info.add()
        daily_info.high = 103
        self.assertEqual([1, 1, -1, -1, 1], PolicyPredictUtil.get_flow_detail_list(stock_info.daily_info, Policy.TradePolicy.Percent.HIGH))


    def test_get_sequential_trend_empty(self):
        stock_info = StockInfo()
        self.assertEqual(0, PolicyPredictUtil.get_sequential_trend(stock_info.daily_info, Policy.TradePolicy.Percent.HIGH))
        daily_info = stock_info.daily_info.add()
        daily_info.high = 100
        self.assertEqual(0, PolicyPredictUtil.get_sequential_trend(stock_info.daily_info, Policy.TradePolicy.Percent.HIGH))
        daily_info = stock_info.daily_info.add()
        daily_info.high = 101
        self.assertEqual(1, PolicyPredictUtil.get_sequential_trend(stock_info.daily_info, Policy.TradePolicy.Percent.HIGH))

    def test_get_sequential_trend_normal(self):
        stock_info = StockInfo()
        daily_info = stock_info.daily_info.add()
        daily_info.high = 100
        daily_info = stock_info.daily_info.add()
        daily_info.high = 101
        self.assertEqual(1, PolicyPredictUtil.get_sequential_trend(stock_info.daily_info, Policy.TradePolicy.Percent.HIGH))
        daily_info = stock_info.daily_info.add()
        daily_info.high = 102
        self.assertEqual(2, PolicyPredictUtil.get_sequential_trend(stock_info.daily_info, Policy.TradePolicy.Percent.HIGH))
        daily_info = stock_info.daily_info.add()
        daily_info.high = 101
        self.assertEqual(-1, PolicyPredictUtil.get_sequential_trend(stock_info.daily_info, Policy.TradePolicy.Percent.HIGH))
        daily_info = stock_info.daily_info.add()
        daily_info.high = 100
        self.assertEqual(-2, PolicyPredictUtil.get_sequential_trend(stock_info.daily_info, Policy.TradePolicy.Percent.HIGH))

    def test_get_price(self):
        stock_info = StockInfo()
        daily_info = stock_info.daily_info.add()
        daily_info.high = 100
        daily_info.low = 20
        self.assertEqual(daily_info.high, PolicyPredictUtil.get_price(daily_info, Policy.TradePolicy.Percent.HIGH))
        self.assertEqual(daily_info.low, PolicyPredictUtil.get_price(daily_info, Policy.TradePolicy.Percent.LOW))
        self.assertEqual(60, PolicyPredictUtil.get_price(daily_info, Policy.TradePolicy.Percent.MEDIUM))


if __name__ == '__main__':
    unittest.main()
