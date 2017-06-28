# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/person.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from proto import stock_info_pb2 as proto_dot_stock__info__pb2
from proto import policy_pb2 as proto_dot_policy__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/person.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\x12proto/person.proto\x1a\x16proto/stock_info.proto\x1a\x12proto/policy.proto\"\x85\x0e\n\x06Person\x12\x15\n\rcash_taken_in\x18\x01 \x01(\x01\x12!\n\x14max_train_watch_days\x18\x02 \x01(\x05:\x03\x31\x32\x30\x12#\n\x16max_predict_watch_days\x18\x03 \x01(\x05:\x03\x31\x32\x30\x12\x1a\n\rmax_hold_days\x18\x12 \x01(\x05:\x03\x33\x36\x30\x12\x1b\n\x10max_policy_count\x18\x04 \x01(\x05:\x01\x31\x12\x18\n\x0cstock_holder\x18\x05 \x01(\t:\x02ib\x12\x18\n\x10stock_start_date\x18\x10 \x01(\t\x12\x16\n\x0estock_end_date\x18\x11 \x01(\t\x12\x1e\n\nstock_info\x18\x06 \x03(\x0b\x32\n.StockInfo\x12\x1c\n\x0bpolicy_info\x18\x07 \x03(\x0b\x32\x07.Policy\x12\x34\n\x0c\x61\x63tion_items\x18\x08 \x03(\x0b\x32\x1e.Person.StockPolicyActionsItem\x12\x36\n\x13stock_policy_report\x18\n \x03(\x0b\x32\x19.Person.StockPolicyReport\x12=\n\x1asorted_stock_policy_report\x18\x0b \x03(\x0b\x32\x19.Person.StockPolicyReport\x12:\n\x15policy_summary_report\x18\x0c \x03(\x0b\x32\x1b.Person.PolicySummaryReport\x12\x41\n\x1csorted_policy_summary_report\x18\r \x03(\x0b\x32\x1b.Person.PolicySummaryReport\x12\x36\n\x13policy_group_report\x18\x0e \x03(\x0b\x32\x19.Person.PolicyGroupReport\x12=\n\x1asorted_policy_group_report\x18\x0f \x03(\x0b\x32\x19.Person.PolicyGroupReport\x12\x41\n\x19stock_policy_group_report\x18\x14 \x03(\x0b\x32\x1e.Person.StockPolicyGroupReport\x12H\n sorted_stock_policy_group_report\x18\x15 \x03(\x0b\x32\x1e.Person.StockPolicyGroupReport\x1a\x94\x03\n\x16StockPolicyActionsItem\x12\x15\n\rcash_taken_in\x18\x01 \x01(\x01\x12\x10\n\x08stock_id\x18\x02 \x01(\t\x12\x11\n\tpolicy_id\x18\x03 \x01(\t\x12\x1e\n\x16trade_watch_start_date\x18\x04 \x01(\t\x12\x44\n\x10\x62uy_stock_action\x18\x05 \x03(\x0b\x32*.Person.StockPolicyActionsItem.StockAction\x12\x45\n\x11sell_stock_action\x18\x06 \x03(\x0b\x32*.Person.StockPolicyActionsItem.StockAction\x12\x1d\n\x06report\x18\x07 \x01(\x0b\x32\r.PolicyReport\x1ar\n\x0bStockAction\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\x12\x10\n\x08\x61t_price\x18\x02 \x01(\x01\x12\x0e\n\x06volumn\x18\x03 \x01(\x01\x12\x18\n\x10stock_trade_cost\x18\x04 \x01(\x01\x12\x19\n\x11option_trade_cost\x18\x05 \x01(\x01\x1a\x46\n\x13PercentPolicyReport\x12\x10\n\x08position\x18\x01 \x01(\x05\x12\x1d\n\x06report\x18\x02 \x01(\x0b\x32\r.PolicyReport\x1a\x66\n\x11StockPolicyReport\x12\x10\n\x08stock_id\x18\x01 \x01(\t\x12\x11\n\tpolicy_id\x18\x03 \x01(\t\x12,\n\x07reports\x18\x04 \x03(\x0b\x32\x1b.Person.PercentPolicyReport\x1aV\n\x13PolicySummaryReport\x12\x11\n\tpolicy_id\x18\x03 \x01(\t\x12,\n\x07reports\x18\x04 \x03(\x0b\x32\x1b.Person.PercentPolicyReport\x1ax\n\x11PolicyGroupReport\x12\x19\n\x11policy_group_type\x18\x01 \x01(\t\x12\x1a\n\x12policy_group_value\x18\x02 \x01(\t\x12,\n\x07reports\x18\x03 \x03(\x0b\x32\x1b.Person.PercentPolicyReport\x1a\x8f\x01\n\x16StockPolicyGroupReport\x12\x10\n\x08stock_id\x18\x01 \x01(\t\x12\x19\n\x11policy_group_type\x18\x02 \x01(\t\x12\x1a\n\x12policy_group_value\x18\x03 \x01(\t\x12,\n\x07reports\x18\x04 \x03(\x0b\x32\x1b.Person.PercentPolicyReport')
  ,
  dependencies=[proto_dot_stock__info__pb2.DESCRIPTOR,proto_dot_policy__pb2.DESCRIPTOR,])




_PERSON_STOCKPOLICYACTIONSITEM_STOCKACTION = _descriptor.Descriptor(
  name='StockAction',
  full_name='Person.StockPolicyActionsItem.StockAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='date', full_name='Person.StockPolicyActionsItem.StockAction.date', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='at_price', full_name='Person.StockPolicyActionsItem.StockAction.at_price', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='volumn', full_name='Person.StockPolicyActionsItem.StockAction.volumn', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stock_trade_cost', full_name='Person.StockPolicyActionsItem.StockAction.stock_trade_cost', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='option_trade_cost', full_name='Person.StockPolicyActionsItem.StockAction.option_trade_cost', index=4,
      number=5, type=1, cpp_type=5, label=1,
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
  serialized_start=1218,
  serialized_end=1332,
)

_PERSON_STOCKPOLICYACTIONSITEM = _descriptor.Descriptor(
  name='StockPolicyActionsItem',
  full_name='Person.StockPolicyActionsItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cash_taken_in', full_name='Person.StockPolicyActionsItem.cash_taken_in', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stock_id', full_name='Person.StockPolicyActionsItem.stock_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='policy_id', full_name='Person.StockPolicyActionsItem.policy_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='trade_watch_start_date', full_name='Person.StockPolicyActionsItem.trade_watch_start_date', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buy_stock_action', full_name='Person.StockPolicyActionsItem.buy_stock_action', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sell_stock_action', full_name='Person.StockPolicyActionsItem.sell_stock_action', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='report', full_name='Person.StockPolicyActionsItem.report', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_PERSON_STOCKPOLICYACTIONSITEM_STOCKACTION, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=928,
  serialized_end=1332,
)

_PERSON_PERCENTPOLICYREPORT = _descriptor.Descriptor(
  name='PercentPolicyReport',
  full_name='Person.PercentPolicyReport',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='position', full_name='Person.PercentPolicyReport.position', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='report', full_name='Person.PercentPolicyReport.report', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=1334,
  serialized_end=1404,
)

_PERSON_STOCKPOLICYREPORT = _descriptor.Descriptor(
  name='StockPolicyReport',
  full_name='Person.StockPolicyReport',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='stock_id', full_name='Person.StockPolicyReport.stock_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='policy_id', full_name='Person.StockPolicyReport.policy_id', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='reports', full_name='Person.StockPolicyReport.reports', index=2,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=1406,
  serialized_end=1508,
)

_PERSON_POLICYSUMMARYREPORT = _descriptor.Descriptor(
  name='PolicySummaryReport',
  full_name='Person.PolicySummaryReport',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='policy_id', full_name='Person.PolicySummaryReport.policy_id', index=0,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='reports', full_name='Person.PolicySummaryReport.reports', index=1,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=1510,
  serialized_end=1596,
)

_PERSON_POLICYGROUPREPORT = _descriptor.Descriptor(
  name='PolicyGroupReport',
  full_name='Person.PolicyGroupReport',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='policy_group_type', full_name='Person.PolicyGroupReport.policy_group_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='policy_group_value', full_name='Person.PolicyGroupReport.policy_group_value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='reports', full_name='Person.PolicyGroupReport.reports', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=1598,
  serialized_end=1718,
)

_PERSON_STOCKPOLICYGROUPREPORT = _descriptor.Descriptor(
  name='StockPolicyGroupReport',
  full_name='Person.StockPolicyGroupReport',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='stock_id', full_name='Person.StockPolicyGroupReport.stock_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='policy_group_type', full_name='Person.StockPolicyGroupReport.policy_group_type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='policy_group_value', full_name='Person.StockPolicyGroupReport.policy_group_value', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='reports', full_name='Person.StockPolicyGroupReport.reports', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=1721,
  serialized_end=1864,
)

_PERSON = _descriptor.Descriptor(
  name='Person',
  full_name='Person',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cash_taken_in', full_name='Person.cash_taken_in', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_train_watch_days', full_name='Person.max_train_watch_days', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=120,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_predict_watch_days', full_name='Person.max_predict_watch_days', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=120,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_hold_days', full_name='Person.max_hold_days', index=3,
      number=18, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=360,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_policy_count', full_name='Person.max_policy_count', index=4,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stock_holder', full_name='Person.stock_holder', index=5,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("ib").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stock_start_date', full_name='Person.stock_start_date', index=6,
      number=16, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stock_end_date', full_name='Person.stock_end_date', index=7,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stock_info', full_name='Person.stock_info', index=8,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='policy_info', full_name='Person.policy_info', index=9,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='action_items', full_name='Person.action_items', index=10,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stock_policy_report', full_name='Person.stock_policy_report', index=11,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sorted_stock_policy_report', full_name='Person.sorted_stock_policy_report', index=12,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='policy_summary_report', full_name='Person.policy_summary_report', index=13,
      number=12, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sorted_policy_summary_report', full_name='Person.sorted_policy_summary_report', index=14,
      number=13, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='policy_group_report', full_name='Person.policy_group_report', index=15,
      number=14, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sorted_policy_group_report', full_name='Person.sorted_policy_group_report', index=16,
      number=15, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stock_policy_group_report', full_name='Person.stock_policy_group_report', index=17,
      number=20, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sorted_stock_policy_group_report', full_name='Person.sorted_stock_policy_group_report', index=18,
      number=21, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_PERSON_STOCKPOLICYACTIONSITEM, _PERSON_PERCENTPOLICYREPORT, _PERSON_STOCKPOLICYREPORT, _PERSON_POLICYSUMMARYREPORT, _PERSON_POLICYGROUPREPORT, _PERSON_STOCKPOLICYGROUPREPORT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=67,
  serialized_end=1864,
)

_PERSON_STOCKPOLICYACTIONSITEM_STOCKACTION.containing_type = _PERSON_STOCKPOLICYACTIONSITEM
_PERSON_STOCKPOLICYACTIONSITEM.fields_by_name['buy_stock_action'].message_type = _PERSON_STOCKPOLICYACTIONSITEM_STOCKACTION
_PERSON_STOCKPOLICYACTIONSITEM.fields_by_name['sell_stock_action'].message_type = _PERSON_STOCKPOLICYACTIONSITEM_STOCKACTION
_PERSON_STOCKPOLICYACTIONSITEM.fields_by_name['report'].message_type = proto_dot_policy__pb2._POLICYREPORT
_PERSON_STOCKPOLICYACTIONSITEM.containing_type = _PERSON
_PERSON_PERCENTPOLICYREPORT.fields_by_name['report'].message_type = proto_dot_policy__pb2._POLICYREPORT
_PERSON_PERCENTPOLICYREPORT.containing_type = _PERSON
_PERSON_STOCKPOLICYREPORT.fields_by_name['reports'].message_type = _PERSON_PERCENTPOLICYREPORT
_PERSON_STOCKPOLICYREPORT.containing_type = _PERSON
_PERSON_POLICYSUMMARYREPORT.fields_by_name['reports'].message_type = _PERSON_PERCENTPOLICYREPORT
_PERSON_POLICYSUMMARYREPORT.containing_type = _PERSON
_PERSON_POLICYGROUPREPORT.fields_by_name['reports'].message_type = _PERSON_PERCENTPOLICYREPORT
_PERSON_POLICYGROUPREPORT.containing_type = _PERSON
_PERSON_STOCKPOLICYGROUPREPORT.fields_by_name['reports'].message_type = _PERSON_PERCENTPOLICYREPORT
_PERSON_STOCKPOLICYGROUPREPORT.containing_type = _PERSON
_PERSON.fields_by_name['stock_info'].message_type = proto_dot_stock__info__pb2._STOCKINFO
_PERSON.fields_by_name['policy_info'].message_type = proto_dot_policy__pb2._POLICY
_PERSON.fields_by_name['action_items'].message_type = _PERSON_STOCKPOLICYACTIONSITEM
_PERSON.fields_by_name['stock_policy_report'].message_type = _PERSON_STOCKPOLICYREPORT
_PERSON.fields_by_name['sorted_stock_policy_report'].message_type = _PERSON_STOCKPOLICYREPORT
_PERSON.fields_by_name['policy_summary_report'].message_type = _PERSON_POLICYSUMMARYREPORT
_PERSON.fields_by_name['sorted_policy_summary_report'].message_type = _PERSON_POLICYSUMMARYREPORT
_PERSON.fields_by_name['policy_group_report'].message_type = _PERSON_POLICYGROUPREPORT
_PERSON.fields_by_name['sorted_policy_group_report'].message_type = _PERSON_POLICYGROUPREPORT
_PERSON.fields_by_name['stock_policy_group_report'].message_type = _PERSON_STOCKPOLICYGROUPREPORT
_PERSON.fields_by_name['sorted_stock_policy_group_report'].message_type = _PERSON_STOCKPOLICYGROUPREPORT
DESCRIPTOR.message_types_by_name['Person'] = _PERSON
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Person = _reflection.GeneratedProtocolMessageType('Person', (_message.Message,), dict(

  StockPolicyActionsItem = _reflection.GeneratedProtocolMessageType('StockPolicyActionsItem', (_message.Message,), dict(

    StockAction = _reflection.GeneratedProtocolMessageType('StockAction', (_message.Message,), dict(
      DESCRIPTOR = _PERSON_STOCKPOLICYACTIONSITEM_STOCKACTION,
      __module__ = 'proto.person_pb2'
      # @@protoc_insertion_point(class_scope:Person.StockPolicyActionsItem.StockAction)
      ))
    ,
    DESCRIPTOR = _PERSON_STOCKPOLICYACTIONSITEM,
    __module__ = 'proto.person_pb2'
    # @@protoc_insertion_point(class_scope:Person.StockPolicyActionsItem)
    ))
  ,

  PercentPolicyReport = _reflection.GeneratedProtocolMessageType('PercentPolicyReport', (_message.Message,), dict(
    DESCRIPTOR = _PERSON_PERCENTPOLICYREPORT,
    __module__ = 'proto.person_pb2'
    # @@protoc_insertion_point(class_scope:Person.PercentPolicyReport)
    ))
  ,

  StockPolicyReport = _reflection.GeneratedProtocolMessageType('StockPolicyReport', (_message.Message,), dict(
    DESCRIPTOR = _PERSON_STOCKPOLICYREPORT,
    __module__ = 'proto.person_pb2'
    # @@protoc_insertion_point(class_scope:Person.StockPolicyReport)
    ))
  ,

  PolicySummaryReport = _reflection.GeneratedProtocolMessageType('PolicySummaryReport', (_message.Message,), dict(
    DESCRIPTOR = _PERSON_POLICYSUMMARYREPORT,
    __module__ = 'proto.person_pb2'
    # @@protoc_insertion_point(class_scope:Person.PolicySummaryReport)
    ))
  ,

  PolicyGroupReport = _reflection.GeneratedProtocolMessageType('PolicyGroupReport', (_message.Message,), dict(
    DESCRIPTOR = _PERSON_POLICYGROUPREPORT,
    __module__ = 'proto.person_pb2'
    # @@protoc_insertion_point(class_scope:Person.PolicyGroupReport)
    ))
  ,

  StockPolicyGroupReport = _reflection.GeneratedProtocolMessageType('StockPolicyGroupReport', (_message.Message,), dict(
    DESCRIPTOR = _PERSON_STOCKPOLICYGROUPREPORT,
    __module__ = 'proto.person_pb2'
    # @@protoc_insertion_point(class_scope:Person.StockPolicyGroupReport)
    ))
  ,
  DESCRIPTOR = _PERSON,
  __module__ = 'proto.person_pb2'
  # @@protoc_insertion_point(class_scope:Person)
  ))
_sym_db.RegisterMessage(Person)
_sym_db.RegisterMessage(Person.StockPolicyActionsItem)
_sym_db.RegisterMessage(Person.StockPolicyActionsItem.StockAction)
_sym_db.RegisterMessage(Person.PercentPolicyReport)
_sym_db.RegisterMessage(Person.StockPolicyReport)
_sym_db.RegisterMessage(Person.PolicySummaryReport)
_sym_db.RegisterMessage(Person.PolicyGroupReport)
_sym_db.RegisterMessage(Person.StockPolicyGroupReport)


# @@protoc_insertion_point(module_scope)
