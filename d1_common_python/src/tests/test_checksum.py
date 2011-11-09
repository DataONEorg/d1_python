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
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import sys
import logging
import unittest
import xml.sax

# 3rd party.
import pyxb

# D1.
from d1_common import xmlrunner
import d1_common.const
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App
import util

EG_CHECKSUM_GMN = (
  """<?xml version="1.0" ?><ns1:checksum algorithm="SHA-1" xmlns:ns1="http://ns.dataone.org/service/types/v1">3f56de593b6ffc536253b799b429453e3673fc19</ns1:checksum>""",
  'SHA-1', '3f56de593b6ffc536253b799b429453e3673fc19'
)

# TODO.
EG_CHECKSUM_KNB = ("""""", '', '')

EG_BAD_CHECKSUM_1 = (
  """<?xml version="1.0" ?><ns1:checksum invalid_attribute="invalid" algorithm="SHA-1" xmlns:ns1="http://ns.dataone.org/service/types/v1">3f56de593b6ffc536253b799b429453e3673fc19</ns1:checksum>""",
  '', ''
)

EG_BAD_CHECKSUM_2 = (
  """<?xml version="1.0" ?><ns1:checksumINVALID algorithm="SHA-1" xmlns:ns1="http://ns.dataone.org/service/types/v1">3f56de593b6ffc536253b799b429453e3673fc19</ns1:checksum>""",
  '', ''
)


class TestChecksum(unittest.TestCase):
  def deserialize_checksum_and_check(self, doc, shouldfail=False):
    try:
      obj = dataoneTypes.CreateFromDocument(doc[0])
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if shouldfail:
        return
      else:
        raise
    else:
      self.assertEqual(obj.algorithm, doc[1])
      self.assertEqual(obj.value(), doc[2])

  def test_serialization_gmn(self):
    '''Deserialize: XML -> Checksum (GMN)'''
    self.deserialize_checksum_and_check(EG_CHECKSUM_GMN)

  def test_serialization_knb(self):
    '''Deserialize: XML -> Checksum (KNB)'''
    # TODO.
    #self.doctest(EG_CHECKSUM_KNB)

  def test_serialization_bad_1(self):
    '''Deserialize: XML -> Checksum (bad 1)'''
    self.deserialize_checksum_and_check(EG_BAD_CHECKSUM_1, shouldfail=True)

  def test_serialization_bad_2(self):
    '''Deserialize: XML -> Checksum (bad 2)'''
    self.deserialize_checksum_and_check(EG_BAD_CHECKSUM_2, shouldfail=True)

  def test_serialization_roundtrip(self):
    '''Serialization: Checksum -> XML -> Checksum.
    '''
    checksum_obj_in = dataoneTypes.checksum('1' * 32)
    checksum_obj_in.algorithm = 'MD5'
    checksum_xml = checksum_obj_in.toxml()
    checksum_obj_out = dataoneTypes.CreateFromDocument(checksum_xml)
    self.assertEqual(checksum_obj_in.value(), checksum_obj_out.value())
    self.assertEqual(checksum_obj_in.algorithm, checksum_obj_out.algorithm)

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
