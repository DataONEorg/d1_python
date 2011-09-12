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
Module d1_common.tests.test_exceptions
======================================

Unit tests for serializaton and de-serialization of the DataONEException type.

:Created: 2010-04-12
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import sys
import unittest
import xml.dom.minidom

# 3rd party.
import pyxb

# D1.
from d1_common.types import exceptions
from d1_common import const
from d1_common import xmlrunner
import d1_common.types.generated.dataoneTypes as dataoneTypes

#===============================================================================

EG_ERROR_GMN = (
  """<?xml version="1.0" encoding="UTF-8"?>
  <d1:error xmlns:d1="http://ns.dataone.org/service/types/exceptions"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://ns.dataone.org/service/types/exceptions"
  detailCode="0" errorCode="0" name="IdentifierNotUnique" pid="somedataonepid">
  <description>description0</description>
  <traceInformation>traceInformation0</traceInformation>
  </d1:error>""", 'SHA-1', '3f56de593b6ffc536253b799b429453e3673fc19'
)

# Missing detailCode.
EG_ERROR_BAD = (
  """<?xml version="1.0" encoding="UTF-8"?>
  <d1:error xmlns:d1="http://ns.dataone.org/service/types/exceptions"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://ns.dataone.org/service/types/exceptions"
  errorCode="0" name="IdentifierNotUnique" pid="somedataonepid">
  <description>description0</description>
  <traceInformation>traceInformation0</traceInformation>
  </d1:error>""", '', ''
)


class TestExceptions(unittest.TestCase):
  def deserialize_and_check(self, doc, shouldfail=False):
    try:
      obj = dataoneTypes.CreateFromDocument(doc[0])
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if shouldfail:
        return
      else:
        raise

  def test_xml_round_trip(self):
    '''Test serialization and deserialization of DataONE Exceptions
    
    Test serialization and deserialization of DataONE Exceptions by performing
    a round trip:
    
    1) Create a native DataONE Exception object.
    2) Serialize the object to XML.
    3) Deserialize XML to object.
    4) Verify that the object contains the same information as in (1). 
    '''

    # Create a native DataONE IdentifierNotUnique Exception object.
    exc = exceptions.IdentifierNotUnique(
      1010, 'description_test', 'test_pid', 'test trace information'
    )
    # Serialize to XML.
    exc_ser_xml = exc.serialize()
    # Check deserialized XML.
    dom = xml.dom.minidom.parseString(exc_ser_xml)
    root = dom.firstChild
    self.assertEqual(root.tagName, u'ns1:error')
    self.assertEqual(root.attributes['detailCode'].value, u'1010')
    self.assertEqual(root.attributes['errorCode'].value, u'409')
    self.assertEqual(root.attributes['name'].value, u'IdentifierNotUnique')
    self.assertEqual(root.attributes['pid'].value, u'test_pid')
    self.assertEqual(root.getElementsByTagName('description')[0].childNodes[0]\
                     .nodeValue, u'description_test')
    self.assertEqual(root.getElementsByTagName('traceInformation')[0]\
                     .childNodes[0].nodeValue, u'test trace information')
    # Deserialize XML.
    exc_deser = exceptions.deserialize(exc_ser_xml)
    # Check deserialized native object.
    self.assertEqual(exc_deser.detailCode, 1010)
    self.assertEqual(exc_deser.errorCode, 409)
    self.assertEqual(exc_deser.name, 'IdentifierNotUnique')
    self.assertEqual(exc_deser.pid, 'test_pid')
    self.assertEqual(exc_deser.description, 'description_test')
    self.assertEqual(exc_deser.traceInformation, 'test trace information')

  def test_serialization_gmn(self):
    '''Deserialize: XML -> Checksum (GMN)'''
    self.deserialize_and_check(EG_ERROR_GMN)

  def test_serialization_bad_1(self):
    '''Deserialize: XML -> Checksum (bad 1)'''
    self.deserialize_and_check(EG_ERROR_BAD, shouldfail=True)

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
