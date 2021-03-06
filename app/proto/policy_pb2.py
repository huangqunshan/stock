# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/policy.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/policy.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\x12proto/policy.proto\"\xf1\t\n\x06Policy\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06id_md5\x18\x02 \x01(\t\x12(\n\x1dprefer_max_splited_trade_unit\x18\x03 \x01(\x05:\x01\x31\x12!\n\x16prefer_max_stock_count\x18\x04 \x01(\x05:\x01\x31\x12\x17\n\x0fmin_stock_price\x18\x05 \x01(\x01\x12 \n\x03\x62uy\x18\x06 \x01(\x0b\x32\x13.Policy.TradePolicy\x12!\n\x04sell\x18\x07 \x01(\x0b\x32\x13.Policy.TradePolicy\x1a\x9f\x08\n\x0bTradePolicy\x12\x12\n\ndays_watch\x18\x01 \x01(\x05\x12\x1a\n\x12\x64\x61ys_hold_for_sell\x18\x02 \x01(\x05\x12/\n\nat_percent\x18\x03 \x01(\x0b\x32\x1b.Policy.TradePolicy.Percent\x12\x38\n\x07\x61t_mode\x18\x04 \x01(\x0e\x32\'.Policy.TradePolicy.Percent.PercentMode\x12\x1f\n\x17sell_at_loss_thousandth\x18\x05 \x01(\x05\x12!\n\x19sell_at_profit_thousandth\x18\x06 \x01(\x05\x12\x38\n\x0f\x61t_stock_change\x18\x07 \x01(\x0b\x32\x1f.Policy.TradePolicy.StockChange\x12(\n\x05trend\x18\x08 \x01(\x0b\x32\x19.Policy.TradePolicy.Trend\x12 \n\x18last_close_price_percent\x18\t \x01(\x05\x1a\x96\x01\n\x07Percent\x12\x35\n\x04mode\x18\x01 \x01(\x0e\x32\'.Policy.TradePolicy.Percent.PercentMode\x12\x11\n\tpercent_n\x18\x02 \x01(\x05\"A\n\x0bPercentMode\x12\x07\n\x03LOW\x10\x01\x12\x08\n\x04HIGH\x10\x02\x12\n\n\x06MEDIUM\x10\x03\x12\x08\n\x04OPEN\x10\x04\x12\t\n\x05\x43LOSE\x10\x05\x1a\x86\x01\n\x0bStockChange\x12\x10\n\x08\x64ividend\x18\x02 \x01(\x08\x12\r\n\x05yield\x18\x03 \x01(\x08\x12\x17\n\x0fmarket_capacity\x18\x04 \x01(\x01\x12\x1f\n\x17medium_price_volatility\x18\x05 \x01(\x01\x12\x1c\n\x14max_price_volatility\x18\x06 \x01(\x01\x1a\x88\x03\n\x05Trend\x12\x12\n\ndays_watch\x18\x01 \x01(\x05\x12\x16\n\x0egrowth_percent\x18\x02 \x01(\x05\x12\x1a\n\x12half_trend_percent\x18\x03 \x01(\x05\x12#\n\x1blast_sequential_trend_count\x18\x04 \x01(\x05\x12\x37\n\ntrend_enum\x18\x05 \x01(\x0e\x32#.Policy.TradePolicy.Trend.TrendEnum\x12;\n\ntrend_mode\x18\x06 \x01(\x0e\x32\'.Policy.TradePolicy.Percent.PercentMode\"\x9b\x01\n\tTrendEnum\x12\x0c\n\x08GROWP_UP\x10\x01\x12\r\n\tFAIL_DOWN\x10\x02\x12\x1b\n\x17GROWP_UP_THEN_FAIL_DOWN\x10\x03\x12\x1b\n\x17\x46\x41IL_DOWN_THEN_GROWP_UP\x10\x04\x12\x1a\n\x16SUDDEN_GREATE_GROWP_UP\x10\x05\x12\x1b\n\x17SUDDEN_GREATE_FAIL_DOWN\x10\x06\"\xc9\x02\n\x0cPolicyReport\x12\x18\n\x10stock_watch_days\x18\x01 \x01(\x01\x12\x0e\n\x03roi\x18\x02 \x01(\x01:\x01\x31\x12\x15\n\rcash_taken_in\x18\x03 \x01(\x01\x12\x16\n\x0e\x63\x61sh_taken_out\x18\x04 \x01(\x01\x12\x17\n\x0fstock_buy_times\x18\x05 \x01(\x01\x12\x18\n\x10stock_sell_times\x18\x06 \x01(\x01\x12 \n\x18stock_hold_no_sell_times\x18\x07 \x01(\x01\x12\x1a\n\x12trade_profit_times\x18\x08 \x01(\x01\x12\x18\n\x10trade_loss_times\x18\t \x01(\x01\x12\x17\n\x0fstock_hold_days\x18\n \x01(\x01\x12\x1e\n\x16stock_hold_profit_days\x18\x0b \x01(\x01\x12\x1c\n\x14stock_hold_loss_days\x18\x0c \x01(\x01')
)



_POLICY_TRADEPOLICY_PERCENT_PERCENTMODE = _descriptor.EnumDescriptor(
  name='PercentMode',
  full_name='Policy.TradePolicy.Percent.PercentMode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LOW', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HIGH', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MEDIUM', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OPEN', index=3, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLOSE', index=4, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=691,
  serialized_end=756,
)
_sym_db.RegisterEnumDescriptor(_POLICY_TRADEPOLICY_PERCENT_PERCENTMODE)

_POLICY_TRADEPOLICY_TREND_TRENDENUM = _descriptor.EnumDescriptor(
  name='TrendEnum',
  full_name='Policy.TradePolicy.Trend.TrendEnum',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='GROWP_UP', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FAIL_DOWN', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GROWP_UP_THEN_FAIL_DOWN', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FAIL_DOWN_THEN_GROWP_UP', index=3, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUDDEN_GREATE_GROWP_UP', index=4, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUDDEN_GREATE_FAIL_DOWN', index=5, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1133,
  serialized_end=1288,
)
_sym_db.RegisterEnumDescriptor(_POLICY_TRADEPOLICY_TREND_TRENDENUM)


_POLICY_TRADEPOLICY_PERCENT = _descriptor.Descriptor(
  name='Percent',
  full_name='Policy.TradePolicy.Percent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mode', full_name='Policy.TradePolicy.Percent.mode', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='percent_n', full_name='Policy.TradePolicy.Percent.percent_n', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _POLICY_TRADEPOLICY_PERCENT_PERCENTMODE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=606,
  serialized_end=756,
)

_POLICY_TRADEPOLICY_STOCKCHANGE = _descriptor.Descriptor(
  name='StockChange',
  full_name='Policy.TradePolicy.StockChange',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dividend', full_name='Policy.TradePolicy.StockChange.dividend', index=0,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='yield', full_name='Policy.TradePolicy.StockChange.yield', index=1,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='market_capacity', full_name='Policy.TradePolicy.StockChange.market_capacity', index=2,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='medium_price_volatility', full_name='Policy.TradePolicy.StockChange.medium_price_volatility', index=3,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_price_volatility', full_name='Policy.TradePolicy.StockChange.max_price_volatility', index=4,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=759,
  serialized_end=893,
)

_POLICY_TRADEPOLICY_TREND = _descriptor.Descriptor(
  name='Trend',
  full_name='Policy.TradePolicy.Trend',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='days_watch', full_name='Policy.TradePolicy.Trend.days_watch', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='growth_percent', full_name='Policy.TradePolicy.Trend.growth_percent', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='half_trend_percent', full_name='Policy.TradePolicy.Trend.half_trend_percent', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='last_sequential_trend_count', full_name='Policy.TradePolicy.Trend.last_sequential_trend_count', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='trend_enum', full_name='Policy.TradePolicy.Trend.trend_enum', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='trend_mode', full_name='Policy.TradePolicy.Trend.trend_mode', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _POLICY_TRADEPOLICY_TREND_TRENDENUM,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=896,
  serialized_end=1288,
)

_POLICY_TRADEPOLICY = _descriptor.Descriptor(
  name='TradePolicy',
  full_name='Policy.TradePolicy',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='days_watch', full_name='Policy.TradePolicy.days_watch', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='days_hold_for_sell', full_name='Policy.TradePolicy.days_hold_for_sell', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='at_percent', full_name='Policy.TradePolicy.at_percent', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='at_mode', full_name='Policy.TradePolicy.at_mode', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sell_at_loss_thousandth', full_name='Policy.TradePolicy.sell_at_loss_thousandth', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sell_at_profit_thousandth', full_name='Policy.TradePolicy.sell_at_profit_thousandth', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='at_stock_change', full_name='Policy.TradePolicy.at_stock_change', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='trend', full_name='Policy.TradePolicy.trend', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='last_close_price_percent', full_name='Policy.TradePolicy.last_close_price_percent', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_POLICY_TRADEPOLICY_PERCENT, _POLICY_TRADEPOLICY_STOCKCHANGE, _POLICY_TRADEPOLICY_TREND, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=233,
  serialized_end=1288,
)

_POLICY = _descriptor.Descriptor(
  name='Policy',
  full_name='Policy',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Policy.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='id_md5', full_name='Policy.id_md5', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='prefer_max_splited_trade_unit', full_name='Policy.prefer_max_splited_trade_unit', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='prefer_max_stock_count', full_name='Policy.prefer_max_stock_count', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='min_stock_price', full_name='Policy.min_stock_price', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buy', full_name='Policy.buy', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sell', full_name='Policy.sell', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_POLICY_TRADEPOLICY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=1288,
)


_POLICYREPORT = _descriptor.Descriptor(
  name='PolicyReport',
  full_name='PolicyReport',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='stock_watch_days', full_name='PolicyReport.stock_watch_days', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='roi', full_name='PolicyReport.roi', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cash_taken_in', full_name='PolicyReport.cash_taken_in', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cash_taken_out', full_name='PolicyReport.cash_taken_out', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stock_buy_times', full_name='PolicyReport.stock_buy_times', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stock_sell_times', full_name='PolicyReport.stock_sell_times', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stock_hold_no_sell_times', full_name='PolicyReport.stock_hold_no_sell_times', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='trade_profit_times', full_name='PolicyReport.trade_profit_times', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='trade_loss_times', full_name='PolicyReport.trade_loss_times', index=8,
      number=9, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stock_hold_days', full_name='PolicyReport.stock_hold_days', index=9,
      number=10, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stock_hold_profit_days', full_name='PolicyReport.stock_hold_profit_days', index=10,
      number=11, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stock_hold_loss_days', full_name='PolicyReport.stock_hold_loss_days', index=11,
      number=12, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1291,
  serialized_end=1620,
)

_POLICY_TRADEPOLICY_PERCENT.fields_by_name['mode'].enum_type = _POLICY_TRADEPOLICY_PERCENT_PERCENTMODE
_POLICY_TRADEPOLICY_PERCENT.containing_type = _POLICY_TRADEPOLICY
_POLICY_TRADEPOLICY_PERCENT_PERCENTMODE.containing_type = _POLICY_TRADEPOLICY_PERCENT
_POLICY_TRADEPOLICY_STOCKCHANGE.containing_type = _POLICY_TRADEPOLICY
_POLICY_TRADEPOLICY_TREND.fields_by_name['trend_enum'].enum_type = _POLICY_TRADEPOLICY_TREND_TRENDENUM
_POLICY_TRADEPOLICY_TREND.fields_by_name['trend_mode'].enum_type = _POLICY_TRADEPOLICY_PERCENT_PERCENTMODE
_POLICY_TRADEPOLICY_TREND.containing_type = _POLICY_TRADEPOLICY
_POLICY_TRADEPOLICY_TREND_TRENDENUM.containing_type = _POLICY_TRADEPOLICY_TREND
_POLICY_TRADEPOLICY.fields_by_name['at_percent'].message_type = _POLICY_TRADEPOLICY_PERCENT
_POLICY_TRADEPOLICY.fields_by_name['at_mode'].enum_type = _POLICY_TRADEPOLICY_PERCENT_PERCENTMODE
_POLICY_TRADEPOLICY.fields_by_name['at_stock_change'].message_type = _POLICY_TRADEPOLICY_STOCKCHANGE
_POLICY_TRADEPOLICY.fields_by_name['trend'].message_type = _POLICY_TRADEPOLICY_TREND
_POLICY_TRADEPOLICY.containing_type = _POLICY
_POLICY.fields_by_name['buy'].message_type = _POLICY_TRADEPOLICY
_POLICY.fields_by_name['sell'].message_type = _POLICY_TRADEPOLICY
DESCRIPTOR.message_types_by_name['Policy'] = _POLICY
DESCRIPTOR.message_types_by_name['PolicyReport'] = _POLICYREPORT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Policy = _reflection.GeneratedProtocolMessageType('Policy', (_message.Message,), dict(

  TradePolicy = _reflection.GeneratedProtocolMessageType('TradePolicy', (_message.Message,), dict(

    Percent = _reflection.GeneratedProtocolMessageType('Percent', (_message.Message,), dict(
      DESCRIPTOR = _POLICY_TRADEPOLICY_PERCENT,
      __module__ = 'proto.policy_pb2'
      # @@protoc_insertion_point(class_scope:Policy.TradePolicy.Percent)
      ))
    ,

    StockChange = _reflection.GeneratedProtocolMessageType('StockChange', (_message.Message,), dict(
      DESCRIPTOR = _POLICY_TRADEPOLICY_STOCKCHANGE,
      __module__ = 'proto.policy_pb2'
      # @@protoc_insertion_point(class_scope:Policy.TradePolicy.StockChange)
      ))
    ,

    Trend = _reflection.GeneratedProtocolMessageType('Trend', (_message.Message,), dict(
      DESCRIPTOR = _POLICY_TRADEPOLICY_TREND,
      __module__ = 'proto.policy_pb2'
      # @@protoc_insertion_point(class_scope:Policy.TradePolicy.Trend)
      ))
    ,
    DESCRIPTOR = _POLICY_TRADEPOLICY,
    __module__ = 'proto.policy_pb2'
    # @@protoc_insertion_point(class_scope:Policy.TradePolicy)
    ))
  ,
  DESCRIPTOR = _POLICY,
  __module__ = 'proto.policy_pb2'
  # @@protoc_insertion_point(class_scope:Policy)
  ))
_sym_db.RegisterMessage(Policy)
_sym_db.RegisterMessage(Policy.TradePolicy)
_sym_db.RegisterMessage(Policy.TradePolicy.Percent)
_sym_db.RegisterMessage(Policy.TradePolicy.StockChange)
_sym_db.RegisterMessage(Policy.TradePolicy.Trend)

PolicyReport = _reflection.GeneratedProtocolMessageType('PolicyReport', (_message.Message,), dict(
  DESCRIPTOR = _POLICYREPORT,
  __module__ = 'proto.policy_pb2'
  # @@protoc_insertion_point(class_scope:PolicyReport)
  ))
_sym_db.RegisterMessage(PolicyReport)


# @@protoc_insertion_point(module_scope)
