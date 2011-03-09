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

:Author: Vieglais, Dahl

..autoclass:: TestExceptions
  :members:
'''

import logging
import sys
import unittest
import xml.dom.minidom
import json

from d1_common.types import exceptions
from d1_common.types import exception_serialization
from d1_common import const

import d1_common.xmlrunner as xmlrunner
from d1_common import svnrevision

#===============================================================================


class TestExceptions(unittest.TestCase):
  def test_xml_round_trip(self):
    '''XML round trip.
    
    Example XML:
    <error detailCode="1010" 
           errorCode="409" 
           name="IdentifierNotUnique"
           pid="test_pid">
      <description>description_test</description>
      <traceInformation>trace_test_1</traceInformation>
    </error>"""
    '''

    # Create a DataONE IdentifierNotUnique Exception.
    exc = exceptions.IdentifierNotUnique(
      '1010', 'description_test', 'test_pid', ['trace_test_1', 'trace_test_2',
                                               'trace_test_3']
    )
    # Check serialization to XML.
    exc_ser = exception_serialization.DataONEExceptionSerialization(exc)
    xml_str, content_type = exc_ser.serialize(const.MIMETYPE_XML)
    self.assertEqual(content_type, const.MIMETYPE_XML)
    # Check deserialized XML.
    dom = xml.dom.minidom.parseString(xml_str)
    root = dom.firstChild
    self.assertEqual(root.tagName, u'error')
    self.assertEqual(root.attributes['detailCode'].value, u'1010')
    self.assertEqual(root.attributes['errorCode'].value, u'409')
    self.assertEqual(root.attributes['name'].value, u'IdentifierNotUnique')
    self.assertEqual(root.attributes['pid'].value, u'test_pid')
    self.assertEqual(
      root.getElementsByTagName('description')[0].childNodes[0].nodeValue,
      u'description_test'
    )
    # TODO: For now, we exclude traceInformation from the XML round trip test
    # because traceInformation has been disabled until the Java stack can be
    # updated to match.
    #    self.assertEqual(root.getElementsByTagName('traceInformation')[0].childNodes[0].nodeValue, u'trace_test_1')
    #    self.assertEqual(root.getElementsByTagName('traceInformation')[1].childNodes[0].nodeValue, u'trace_test_2')
    #    self.assertEqual(root.getElementsByTagName('traceInformation')[2].childNodes[0].nodeValue, u'trace_test_3')
    # Check deserialize XML to exception (includes test of exception factory).
    exc_deser = exception_serialization.DataONEExceptionSerialization(None)
    e_deser = exc_deser.deserialize(xml_str, content_type)
    self.assertEqual(e_deser.detailCode, '1010')
    self.assertEqual(e_deser.errorCode, 409)
    self.assertEqual(e_deser.name, 'IdentifierNotUnique')
    self.assertEqual(e_deser.pid, 'test_pid')
    self.assertEqual(e_deser.description, 'description_test')
#    self.assertEqual(e_deser.traceInformation, ["trace_test_1", "trace_test_2", "trace_test_3"])

  def test_json_round_trip(self):
    '''JSON round trip.
    
    Example JSON:
    {"name": "NotFound", "pid": "test_pid", "errorCode": 404, "detailCode": "1010", "traceInformation": ["trace_test_1", "trace_test_2", "trace_test_3"], "description": "description_test"}"""
    '''

    # Create a DataONE NotFound Exception.
    exc = exceptions.NotFound(
      '1010', 'description_test', 'test_pid', [
        'trace_test_1', 'trace_test_2', 'trace_test_3'
      ]
    )
    # Check serialization to JSON.
    exc_ser = exception_serialization.DataONEExceptionSerialization(exc)
    json_str, content_type = exc_ser.serialize(const.MIMETYPE_JSON)
    self.assertEqual(content_type, const.MIMETYPE_JSON)
    # Check deserialize JSON to native.
    json_obj = json.loads(json_str)
    self.assertEqual(json_obj['errorCode'], 404)
    self.assertEqual(json_obj['name'], 'NotFound')
    self.assertEqual(json_obj['detailCode'], '1010')
    self.assertEqual(
      json_obj['traceInformation'], "trace_test_1\ntrace_test_2\ntrace_test_3"
    )
    # Check deserialize JSON to exception (includes test of exception factory).
    exc_deser = exception_serialization.DataONEExceptionSerialization(None)
    e_deser = exc_deser.deserialize(json_str, content_type)
    self.assertEqual(e_deser.errorCode, 404)
    self.assertEqual(e_deser.name, 'NotFound')
    self.assertEqual(e_deser.detailCode, '1010')
    self.assertEqual(e_deser.traceInformation, "trace_test_1\ntrace_test_2\ntrace_test_3")

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  svnrevision.getSvnRevision(update_static=True)
  unittest.main(testRunner=xmlrunner.XmlTestRunner(sys.stdout))
