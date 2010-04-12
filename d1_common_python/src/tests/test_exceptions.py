'''
Unit tests for d1common.exceptions

:Author: Dave Vieglais

:Created: 20100108

..autoclass:: TestExceptions
  :members:
'''

import unittest
import logging
import urlparse
import urllib2
import socket #for error codes
from xml.dom.minidom import parseString
import lxml
try:
  import cjson as json
except:
  import json
from d1common import exceptions

#===============================================================================


class TestExceptions(unittest.TestCase):
  def testNotFound(self):
    xmlEg = """<error detailCode="1010" errorCode="404" name="NotFound"><description>Test data</description><traceInformation><value key="identifier">'ABCXYZ'</value></traceInformation></error>"""
    try:
      raise exceptions.NotFound('1010', 'Test data', 'ABCXYZ', {'test1': 'data1'})
    except Exception, e:
      pass
    jdata = json.loads(e.serializeToJson())
    self.assertEqual(jdata['errorCode'], 404)
    self.assertEqual(jdata['name'], 'NotFound')
    self.assertEqual(jdata['detailCode'], '1010')
    self.assertEqual(e.serializeToXml(), xmlEg)

  def testNotImplemented(self):
    xmlEg = '''<error detailCode="1011" errorCode="501" name="NotImplemented"><description>Test not implemented</description><traceInformation><value key="a">'sdgdsfg'</value></traceInformation></error>'''
    try:
      raise exceptions.NotImplemented('1011', 'Test not implemented', {'a': 'sdgdsfg'})
    except Exception, e:
      pass
    jdata = json.loads(e.serializeToJson())
    self.assertEqual(jdata['errorCode'], 501)
    self.assertEqual(jdata['name'], 'NotImplemented')
    self.assertEqual(jdata['detailCode'], '1011')
    self.assertEqual(e.serializeToXml(), xmlEg)

  def testExceptionFactory(self):
    notFoundEgJson = """{"errorCode": 404, "detailCode": "1010", "traceInformation": {"identifier": "ABCXYZ"}, "name": "NotFound", "description": "Test data"}"""
    notImplementedEgJson = """{"errorCode": 501, "detailCode": "1011", "traceInformation": {"a": "sdgdsfg"}, "name": "NotImplemented", "description": "Test not implemented"}"""
    notImplementedEgXml = '''<error detailCode="1011" errorCode="501" name="NotImplemented"><description>Test not implemented</description><traceInformation><value key="a">'sdgdsfg'</value></traceInformation></error>'''
    notFoundEgXml = """<error detailCode="1010" errorCode="404" name="NotFound"><description>Test data</description><traceInformation><value key="identifier">'ABCXYZ'</value></traceInformation></error>"""
    res = exceptions.DataOneExceptionFactory().createException(notFoundEgJson)
    self.assertTrue(isinstance(res, exceptions.NotFound))
    res = exceptions.DataOneExceptionFactory().createException(notImplementedEgJson)
    self.assertTrue(isinstance(res, exceptions.NotImplemented))
    res = exceptions.DataOneExceptionFactory().createException(notImplementedEgXml)
    self.assertTrue(isinstance(res, exceptions.NotImplemented))
    res = exceptions.DataOneExceptionFactory().createException(notFoundEgXml)
    self.assertTrue(isinstance(res, exceptions.NotFound))


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  unittest.main(testRunner=unittest.TextTestRunner)
