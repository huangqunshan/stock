# coding=utf8

import sys
from policy_util import PolicyUtil
from proto.person_pb2 import Person


# person = Person()
# person.cash_taken_in = 100
# person_string = person.SerializeToString()
# print "person:%s" % person

new_person = Person()
new_person.ParseFromString(sys.stdin.read())
print "sorted_policy_group_report:%s" % new_person.sorted_policy_group_report
print "sorted_policy_summary_report:%s" % new_person.sorted_policy_summary_report
print "sorted_stock_policy_report:%s" % new_person.sorted_stock_policy_report