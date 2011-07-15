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

:Created: 2011-03-03
:Author: DataONE (vieglais, dahl)
:Dependencies:
  - python 2.6
'''

import sys
import logging
import unittest
from d1_common import xmlrunner
from d1_common.types import checksum_serialization
import d1_common.const

EG_CHECKSUM_GMN = (
  """<?xml version="1.0" ?><ns1:checksum algorithm="SHA-1" xmlns:ns1="http://ns.dataone.org/service/types/0.6.2">3f56de593b6ffc536253b799b429453e3673fc19</ns1:checksum>""",
  'SHA-1', '3f56de593b6ffc536253b799b429453e3673fc19'
)

# TODO.
EG_CHECKSUM_KNB = ("""""", '', '')

EG_BAD_CHECKSUM_1 = (
  """<?xml version="1.0" ?><ns1:checksum algorithm="INVALID" xmlns:ns1="http://ns.dataone.org/service/types/0.6.2">3f56de593b6ffc536253b799b429453e3673fc19</ns1:checksum>""",
  '', ''
)

EG_BAD_CHECKSUM_2 = (
  """<?xml version="1.0" ?><ns1:checksumINVALID algorithm="SHA-1" xmlns:ns1="http://ns.dataone.org/service/types/0.6.2">3f56de593b6ffc536253b799b429453e3673fc19</ns1:checksum>""",
  '', ''
)


class TestChecksum(unittest.TestCase):
  def doctest(self, doc, shouldfail=False):
    loader = checksum_serialization.Checksum('dummy')
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

  def test_checksum_serialization_0(self):

    self.doctest(EG_CHECKSUM_GMN)
    # TODO.
    #self.doctest(EG_CHECKSUM_KNB)
    self.doctest(EG_BAD_CHECKSUM_1, shouldfail=True)
    self.doctest(EG_BAD_CHECKSUM_2, shouldfail=True)

  def test_checksum_serialization_1(self):
    '''Serialization: Checksum -> XML -> Checksum.
    '''
    f = checksum_serialization.Checksum('1' * 32)
    f.checksum.algorithm = 'MD5'
    xml_doc, content_type = f.serialize(d1_common.const.MIMETYPE_XML)
    #<?xml version="1.0" ?><ns1:checksum algorithm="MD5" xmlns:ns1="http://ns.dataone.org/service/types/0.6.2">11111111111111111111111111111111</ns1:checksum>
    f.deserialize(xml_doc, d1_common.const.MIMETYPE_XML)

  def test_checksum_serialization_2(self):
    '''Serialization: Checksum -> JSON.
    '''
    f = checksum_serialization.Checksum('1' * 32)
    f.checksum.algorithm = 'MD5'
    json_doc, content_type = f.serialize(d1_common.const.MIMETYPE_JSON)
    # {"checksum": "11111111111111111111111111111111", "algorithm": "MD5"}
    f.deserialize(json_doc, d1_common.const.MIMETYPE_JSON)

  def test_checksum_serialization_3(self):
    '''Serialization: Checksum -> CSV.
    '''
    f = checksum_serialization.Checksum('1' * 32)
    f.checksum.algorithm = 'MD5'
    csv_doc, content_type = f.serialize(d1_common.const.MIMETYPE_CSV)
    # 11111111111111111111111111111111,MD5
    f.deserialize(csv_doc, d1_common.const.MIMETYPE_CSV)

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
