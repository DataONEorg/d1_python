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
import d1_common.types.generated.dataoneErrors as dataoneErrors

# App
import util

VALID_ERROR_DOC = """<?xml version="1.0" encoding="UTF-8"?>
  <error
    detailCode="123.456.789"
    errorCode="456"
    name="IdentifierNotUnique"
    identifier="SomeDataONEPID"
    nodeId="urn:node:SomeNode">
  <description>description0</description>
  <traceInformation><value>traceInformation0</value></traceInformation>
  </error>"""

#  'SHA-1',
#  '3f56de593b6ffc536253b799b429453e3673fc19'
#)

# Missing detailCode and string is stored directly in traceInformation.
INVALID_ERROR_DOC = (
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
  def test_100(self):
    '''deserialize()'''
    d1_exception = exceptions.deserialize(VALID_ERROR_DOC)
    self.assertTrue(isinstance(d1_exception, exceptions.IdentifierNotUnique))
    self.assertEqual(d1_exception.detailCode, '123.456.789')
    self.assertEqual(d1_exception.errorCode, 409)
    self.assertEqual(d1_exception.name, 'IdentifierNotUnique')
    self.assertEqual(d1_exception.identifier, 'SomeDataONEPID')
    self.assertEqual(d1_exception.nodeId, 'urn:node:SomeNode')
    self.assertEqual(d1_exception.description, 'description0')
    #self.assertEqual(d1_exception.traceInformation, '<?xml version="1.0" ?><traceInformation>traceInformation0</traceInformation>')

  def test_150(self):
    '''deserialize() of bad document raises DataONEExceptionException'''
    self.assertRaises(
      exceptions.DataONEExceptionException, exceptions.deserialize, INVALID_ERROR_DOC[0]
    )

  def test_200(self):
    '''String representation'''
    d1_exception = exceptions.deserialize(VALID_ERROR_DOC)
    self.assertTrue('name: IdentifierNotUnique' in str(d1_exception))
    self.assertTrue('errorCode: 409' in str(d1_exception))
    self.assertTrue('detailCode: 123.456.789' in str(d1_exception))

  def test_250(self):
    '''create with only detailCode then serialize()'''
    e = exceptions.ServiceFailure(123)
    self.assertEqual(
      e.serialize(
      ),
      '<?xml version="1.0" ?><error detailCode="123" errorCode="500" name="ServiceFailure"/>'
    )

  def test_260(self):
    '''create with string detailCode and description, then serialize()'''
    e = exceptions.ServiceFailure('123.456.789', 'test description')
    self.assertEqual(
      e.serialize(
      ),
      u'<?xml version="1.0" ?><error detailCode="123.456.789" errorCode="500" name="ServiceFailure"><description>test description</description></error>'
    )

  def test_270(self):
    '''create with detailCode, description and traceInformation, then serialize()'''
    e = exceptions.ServiceFailure(
      '123.456.789', 'test description', 'test traceInformation'
    )
    self.assertEqual(
      e.serialize(
      ),
      u'<?xml version="1.0" ?><error detailCode="123.456.789" errorCode="500" name="ServiceFailure"><description>test description</description><traceInformation><value>test traceInformation</value></traceInformation></error>'
    )

  def test_280(self):
    '''serialize_to_headers()'''
    e = exceptions.ServiceFailure(
      '123.456.789', 'test description', 'test traceInformation'
    )
    headers = e.serialize_to_headers()
    self.assertTrue(('DataONE-Exception-Name', u'ServiceFailure') in headers)
    self.assertTrue(('DataONE-Exception-ErrorCode', u'500') in headers)
    self.assertTrue(('DataONE-Exception-DetailCode', u'123.456.789') in headers)
    self.assertTrue(('DataONE-Exception-Description', u'test description') in headers)
    self.assertTrue(
      (
        'DataONE-Exception-TraceInformation', u'test traceInformation'
      ) in headers
    )

  def test_300(self):
    '''deserialize_from_headers()'''
    headers = {
      'DataONE-Exception-Name': 'IdentifierNotUnique', # required
      'DataONE-Exception-DetailCode': '123.456.789', # required
      'DataONE-Exception-Description': 'test description', # provided but not required
      'dataone-exception-traceinformation': 'test traceInformation', # not required but provided in lower case
      #'DataONE-Exception-Identifier' not required or provided
      #'DataONE-Exception-NodeId' not required or provided
    }
    e = exceptions.deserialize_from_headers(headers)
    self.assertEqual(e.name, 'IdentifierNotUnique')
    self.assertEqual(e.errorCode, 409)
    self.assertEqual(e.detailCode, '123.456.789')
    self.assertEqual(e.description, 'test description')
    self.assertEqual(e.traceInformation, 'test traceInformation')

  def test_400(self):
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
      1010, 'description_test', 'test trace information', 'test_pid', 'node_id'
    )
    # Serialize to XML.
    exc_ser_xml = exc.serialize()
    #print exc_ser_xml
    #return
    # Check XML.
    dom = xml.dom.minidom.parseString(exc_ser_xml)
    root = dom.firstChild
    self.assertEqual(root.tagName, u'error')
    self.assertEqual(root.attributes['detailCode'].value, u'1010')
    self.assertEqual(root.attributes['errorCode'].value, u'409')
    self.assertEqual(root.attributes['name'].value, u'IdentifierNotUnique')
    self.assertEqual(root.attributes['identifier'].value, u'test_pid')
    self.assertEqual(root.getElementsByTagName('description')[0].childNodes[0]\
                     .nodeValue, u'description_test')
    # Disabled until we have decided how to encode traceInformation.
    #self.assertEqual(root.getElementsByTagName('traceInformation')[0]\
    #                 .childNodes[0].nodeValue, u'test trace information')
    # Deserialize XML.
    exc_deser = exceptions.deserialize(exc_ser_xml)
    # Check deserialized native object.
    self.assertEqual(exc_deser.detailCode, '1010')
    self.assertEqual(exc_deser.errorCode, 409)
    self.assertEqual(exc_deser.name, 'IdentifierNotUnique')
    self.assertEqual(exc_deser.identifier, 'test_pid')
    self.assertEqual(exc_deser.description, 'description_test')
    # Disabled until we have decided how to encode traceInformation.
    #self.assertEqual(exc_deser.traceInformation, 'test trace information')

    #===============================================================================


def log_setup():
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  import optparse

  log_setup()

  # Command line opts.
  parser = optparse.OptionParser()
  parser.add_option('--debug', action='store_true', default=False, dest='debug')
  parser.add_option(
    '--test', action='store',
    default='',
    dest='test',
    help='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestExceptions
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
