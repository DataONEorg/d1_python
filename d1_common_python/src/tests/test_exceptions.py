'''
Unit tests for d1_common.types.exceptions

:Author: Dave Vieglais

:Created: 20100108

..autoclass:: TestExceptions
  :members:
'''

import logging
import sys
import unittest
import xml.dom.minidom

try:
  import cjson as json
except:
  import json

from d1_common.types import exceptions
from d1_common.types import exception_serialization
from d1_common import const

import d1_common.xmlrunner as xmlrunner

#===============================================================================


class TestExceptions(unittest.TestCase):
  def test_xml_round_trip(self):
    '''XML round trip.
    
    Example XML:
    <error detailCode="1010" errorCode="409" name="IdentifierNotUnique"><pid>test_pid</pid><description>description_test</description><traceInformation>trace_test_1</traceInformation><traceInformation>trace_test_2</traceInformation><traceInformation>trace_test_3</traceInformation></error>"""
    '''

    # Create a DataONE IdentifierNotUnique Exception.
    exc = exceptions.IdentifierNotUnique(
      '1010', 'description_test', 'test_pid', [
        'trace_test_1', 'trace_test_2', 'trace_test_3'
      ]
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
    self.assertEqual(
      root.getElementsByTagName('pid')[0].childNodes[0].nodeValue, u'test_pid'
    )
    self.assertEqual(
      root.getElementsByTagName('description')[0].childNodes[0].nodeValue,
      u'description_test'
    )
    self.assertEqual(
      root.getElementsByTagName('traceInformation')[0].childNodes[0].nodeValue,
      u'trace_test_1'
    )
    self.assertEqual(
      root.getElementsByTagName('traceInformation')[1].childNodes[0].nodeValue,
      u'trace_test_2'
    )
    self.assertEqual(
      root.getElementsByTagName('traceInformation')[2].childNodes[0].nodeValue,
      u'trace_test_3'
    )
    # Check deserialize XML to exception (includes test of exception factory).
    exc_deser = exception_serialization.DataONEExceptionSerialization(None)
    e_deser = exc_deser.deserialize(xml_str, content_type)
    self.assertEqual(e_deser.detailCode, '1010')
    self.assertEqual(e_deser.errorCode, 409)
    self.assertEqual(e_deser.name, 'IdentifierNotUnique')
    self.assertEqual(e_deser.pid, 'test_pid')
    self.assertEqual(e_deser.description, 'description_test')
    self.assertEqual(
      e_deser.traceInformation, [
        "trace_test_1", "trace_test_2", "trace_test_3"
      ]
    )

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
      json_obj['traceInformation'], [
        "trace_test_1", "trace_test_2", "trace_test_3"
      ]
    )
    # Check deserialize JSON to exception (includes test of exception factory).
    exc_deser = exception_serialization.DataONEExceptionSerialization(None)
    e_deser = exc_deser.deserialize(json_str, content_type)
    self.assertEqual(e_deser.errorCode, 404)
    self.assertEqual(e_deser.name, 'NotFound')
    self.assertEqual(e_deser.detailCode, '1010')
    self.assertEqual(
      e_deser.traceInformation, [
        "trace_test_1", "trace_test_2", "trace_test_3"
      ]
    )


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  unittest.main(testRunner=xmlrunner.XmlTestRunner(sys.stdout))
