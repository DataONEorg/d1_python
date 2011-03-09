#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
Module d1_common.tests.test_monitorlist
=======================================

Unit tests for serializaton and de-serialization of the MonitorList type.

:Author: Vieglais, Dahl

..autoclass:: TestMonitorList
  :members:
'''

import logging
import sys
import unittest

from d1_common import xmlrunner
from d1_common.types import monitorlist_serialization

EG_MONITORLIST_GMN = """<?xml version="1.0" ?>
<ns1:monitorList xmlns:ns1="http://dataone.org/service/types/0.5.1">
<monitorInfo><date>2000-01-01</date><count>1</count></monitorInfo>
<monitorInfo><date>2001-03-21</date><count>2</count></monitorInfo>
<monitorInfo><date>1999-12-31</date><count>3</count></monitorInfo>
</ns1:monitorList>"""

# TODO.
EG_MONITORLIST_KNB = """"""

EG_BAD_MONITORLIST_1 = """<?xml version="1.0" ?>
<ns1:monitorList xmlns:ns1="http://dataone.org/service/types/0.5.1">
<INVALID><date>2000-01-01</date><count>1</count></monitorInfo>
<monitorInfo><date>2001-03-21</date><count>2</count></monitorInfo>
<monitorInfo><date>1999-12-31</date><count>3</count></monitorInfo>
</ns1:monitorList>"""

# Invalid date.
EG_BAD_MONITORLIST_2 = """<?xml version="1.0" ?>
<ns1:monitorList xmlns:ns1="http://dataone.org/service/types/0.5.1">
<monitorInfo><date>2000-01-01</date><count>1</count></monitorInfo>
<monitorInfo><date>2001-02-29</date><count>2</count></monitorInfo>
<monitorInfo><date>1999-12-31</date><count>3</count></monitorInfo>
</ns1:monitorList>"""


class TestMonitorList(unittest.TestCase):
  def test_serialization(self):
    loader = monitorlist_serialization.MonitorList()

    def doctest(doc, shouldfail=False):
      try:
        checksum = loader.deserialize(doc, content_type="text/xml")
      except:
        if shouldfail:
          pass
        else:
          raise

    doctest(EG_MONITORLIST_GMN)
    #doctest(EG_MONITORLIST_KNB)
    doctest(EG_BAD_MONITORLIST_1, shouldfail=True)
    doctest(EG_BAD_MONITORLIST_2, shouldfail=True)

#===============================================================================
if __name__ == "__main__":
  argv = sys.argv
  if "--debug" in argv:
    logging.basicConfig(level=logging.DEBUG)
    argv.remove("--debug")
  if "--with-xunit" in argv:
    argv.remove("--with-xunit")
    unittest.main(argv=argv, testRunner=xmlrunner.XmlTestRunner(sys.stdout))
  else:
    unittest.main(argv=argv)
