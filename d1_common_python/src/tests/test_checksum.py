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
Module d1_common.tests.test_checksum
====================================

Unit tests for serializaton and de-serialization of the Checksum type.

:Author: Vieglais, Dahl

..autoclass:: TestChecksum
  :members:
'''

import sys
import logging
import unittest
from d1_common import xmlrunner
from d1_common.types import checksum_serialization

EG_CHECKSUM_GMN = (
  """<?xml version="1.0" ?><ns1:checksum algorithm="SHA-1" xmlns:ns1="http://dataone.org/service/types/0.5.1">3f56de593b6ffc536253b799b429453e3673fc19</ns1:checksum>""",
  'SHA-1', '3f56de593b6ffc536253b799b429453e3673fc19'
)

# TODO.
EG_CHECKSUM_KNB = ("""""", '', '')

EG_BAD_CHECKSUM_1 = (
  """<?xml version="1.0" ?><ns1:checksum algorithm="INVALID" xmlns:ns1="http://dataone.org/service/types/0.5.1">3f56de593b6ffc536253b799b429453e3673fc19</ns1:checksum>""",
  '', ''
)

EG_BAD_CHECKSUM_2 = (
  """<?xml version="1.0" ?><ns1:checksumINVALID algorithm="SHA-1" xmlns:ns1="http://dataone.org/service/types/0.5.1">3f56de593b6ffc536253b799b429453e3673fc19</ns1:checksum>""",
  '', ''
)


class TestChecksum(unittest.TestCase):
  def test_serialization(self):
    loader = checksum_serialization.Checksum('dummy')

    def doctest(doc, shouldfail=False):
      try:
        checksum = loader.deserialize(doc[0], content_type="text/xml")
      except:
        if shouldfail:
          pass
        else:
          raise
      else:
        self.assertEqual(checksum.algorithm, doc[1])
        self.assertEqual(checksum.value(), doc[2])

    doctest(EG_CHECKSUM_GMN)
    # TODO.
    #doctest(EG_CHECKSUM_KNB)
    doctest(EG_BAD_CHECKSUM_1, shouldfail=True)
    doctest(EG_BAD_CHECKSUM_2, shouldfail=True)

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
