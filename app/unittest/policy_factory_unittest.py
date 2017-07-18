import unittest
from policy_factory import PolicyFactory

class MyTestCase(unittest.TestCase):
    def test_expand(self):
        policy_list = [{}]
        policy_list = PolicyFactory.expand(policy_list, "a", ["a1", "a2", "a3"])
        policy_list = PolicyFactory.expand(policy_list, "b", ["b1", "b2"])
        print policy_list


if __name__ == '__main__':
    unittest.main()
