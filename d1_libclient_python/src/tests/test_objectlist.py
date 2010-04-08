'''
Unit tests for pyd1.d1objectlist

:Author: Dave Vieglais

:Created: 20100108

..autoclass:: TestD1ObjectList
  :members:
'''

import unittest
import logging
from d1pythonitk import objectlist


class TestD1ObjectList(unittest.TestCase):
  def setUp(self):
    pass

  def test_ListSlice(self):
    olist = objectlist.D1ObjectList(None)
    a = olist[1:10]


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  unittest.main(testRunner=unittest.TextTestRunner)
