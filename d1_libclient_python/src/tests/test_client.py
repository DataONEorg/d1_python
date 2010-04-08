'''
Unit tests for pyd1.d1client

:Author: Dave Vieglais

:Created: 20100108

..autoclass:: TestPyD1Client
  :members:
'''

import unittest
import logging
import urlparse
import urllib2
from xml.dom.minidom import parseString
import lxml
try:
  import cjson as json
except:
  import json
from d1pythonitk import const
from d1pythonitk import client
from d1pythonitk import systemmetadata
from d1pythonitk import exceptions


class TestCaseWithURLCompare(unittest.TestCase):
  def assertUrlEqual(self, a, b):
    '''Given two URLs, test if they are equivalent.  This means decomposing into
    their parts and comparing all the pieces.  See RFC 1738 for details.
    
    :param a: URL #1
    :param b: URL #2
    :raises: AssertionError, accumulation of differences between a and b. 
    '''
    ## Accumulator gathers all errors before reporting.
    accumulator = []
    a_parts = urlparse.urlparse(a)
    b_parts = urlparse.urlparse(b)
    #scheme and net location are case insensitive
    try:
      self.assertEqual(
        a_parts.scheme.lower(), b_parts.scheme.lower(),
        u'Schemes of %s and %s differ' % (a, b)
      )
    except AssertionError, e:
      accumulator.append(unicode(e))
    try:
      self.assertEqual(
        a_parts.netloc.lower(), b_parts.netloc.lower(),
        u'Network location of %s and %s differ' % (a, b)
      )
    except AssertionError, e:
      accumulator.append(unicode(e))
    #compare paths
    try:
      self.assertEqual(a_parts.path, b_parts.path, u'Paths of %s and %s differ' % (a, b))
    except AssertionError, e:
      accumulator.append(unicode(e))
    #fragments
    try:
      self.assertEqual(
        a_parts.fragment, b_parts.fragment, u'Fragments differ: %s <> %s' % (
          a_parts.fragment, b_parts.fragment
        )
      )
    except AssertionError, e:
      accumulator.append(unicode(e))
    #parameters
    aparams = a_parts.params.split(";")
    bparams = b_parts.params.split(";")
    try:
      self.assertEqual(
        len(aparams), len(bparams),
        u'Number of parameters differs between %s and %s' % (a, b)
      )
    except AssertionError, e:
      accumulator.append(unicode(e))

    for aparam in aparams:
      try:
        self.assertTrue(
          aparam in bparams, u'Parameter %s not present in URL %s' % (aparam, b)
        )
      except AssertionError, e:
        accumulator.append(unicode(e))

    #query portion
    a_qry = urlparse.parse_qs(a_parts.query)
    b_qry = urlparse.parse_qs(b_parts.query)
    try:
      self.assertEqual(
        len(a_qry.keys()), len(b_qry.keys()),
        u'Number of query keys differs between %s and %s' % (a, b)
      )
    except AssertionError, e:
      accumulator.append(unicode(e))
    bkeys = b_qry.keys()
    for ak in a_qry.keys():
      try:
        self.assertTrue(ak in bkeys, u'The query key %s not present in %s' % (ak, b))
        for v in a_qry[ak]:
          try:
            self.assertTrue(
              v in b_qry[ak], u'The value %s of key %s not present in %s' % (v, ak, b)
            )
          except AssertionError, e:
            accumulator.append(unicode(e))

      except AssertionError, e:
        accumulator.append(unicode(e))

    if len(accumulator) > 0:
      raise AssertionError(u"\n".join(accumulator))

  def test_assertUrlEqual(self):
    '''Test the Url comparison tester...
    '''
    #According to RFC  these URLs are equivalent
    a = "HTTP://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k1=20&k2=abc#frag"
    b = "Http://www.SOME.host:999/a/b/c/;p2;p1;p3?k1=10&k2=abc&k1=20#frag"
    self.assertUrlEqual(a, b)
    #and these are not
    b = "Http://www.SOME.host:999/a/b/c/;p2;p4;p3?k1=10&k2=abc&k1=20#frag"
    self.failUnlessRaises(AssertionError, self.assertUrlEqual, a, b)

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

#===============================================================================


class TestRestClient(TestCaseWithURLCompare):
  def testGet(self):
    cli = client.RESTClient()
    #Google runs a fairly reliable server
    res = cli.GET('http://www.google.com/')
    self.assertEqual(cli.status, 200)
    self.assertEqual(res.code, 200)

    #This should fail with a 404
    try:
      cli.GET('http://www.google.com/_bogus')
    except Exception, e:
      pass
    self.assertTrue(isinstance(e, urllib2.HTTPError))
    self.assertEqual(e.code, 404)

#===============================================================================


class TestDataOneClient(TestCaseWithURLCompare):
  def testGet(self):
    cli = client.DataOneClient()

    #===============================================================================


EG_SYSMETA = u"""<?xml version="1.0" encoding="UTF-8"?>
<d1:systemMetadata xmlns:d1="http://dataone.org/service/types/SystemMetadata/0.1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://dataone.org/service/types/SystemMetadata/0.1 https://repository.dataone.org/software/cicore/trunk/schemas/systemmetadata.xsd">
    <!-- This instance document was auto generated by oXygen XML for testing purposes.
         It contains no useful information.
    -->
    <identifier>Identifier0</identifier>
    <objectFormat>eml://ecoinformatics.org/eml-2.0.1</objectFormat>
    <size>0</size>
    <submitter>uid=jones,o=NCEAS,dc=ecoinformatics,dc=org</submitter>
    <rightsHolder>uid=jones,o=NCEAS,dc=ecoinformatics,dc=org</rightsHolder>
    <obsoletes>Obsoletes0</obsoletes>
    <obsoletes>Obsoletes1</obsoletes>
    <obsoletedBy>ObsoletedBy0</obsoletedBy>
    <obsoletedBy>ObsoletedBy1</obsoletedBy>
    <derivedFrom>DerivedFrom0</derivedFrom>
    <derivedFrom>DerivedFrom1</derivedFrom>
    <describes>Describes0</describes>
    <describes>Describes1</describes>
    <describedBy>DescribedBy0</describedBy>
    <describedBy>DescribedBy1</describedBy>
    <checksum algorithm="SHA-1">2e01e17467891f7c933dbaa00e1459d23db3fe4f</checksum>
    <embargoExpires>2006-05-04T18:13:51.0Z</embargoExpires>
    <accessRule rule="allow" service="read" principal="Principal0"/>
    <accessRule rule="allow" service="read" principal="Principal1"/>
    <replicationPolicy replicationAllowed="true" numberReplicas="2">
        <preferredMemberNode>MemberNode12</preferredMemberNode>
        <preferredMemberNode>MemberNode13</preferredMemberNode>
        <blockedMemberNode>MemberNode6</blockedMemberNode>
        <blockedMemberNode>MemberNode7</blockedMemberNode>
    </replicationPolicy>
    <dateUploaded>2006-05-04T18:13:51.0Z</dateUploaded>
    <dateSysMetadataModified>2006-05-04T18:13:51.0Z</dateSysMetadataModified>
    <originMemberNode>OriginMemberNode0</originMemberNode>
    <authoritativeMemberNode>AuthoritativeMemberNode0</authoritativeMemberNode>
    <replica>
        <replicaMemberNode>ReplicaMemberNode0</replicaMemberNode>
        <replicationStatus>queued</replicationStatus>
        <replicaVerified>2006-05-04T18:13:51.0Z</replicaVerified>
    </replica>
    <replica>
        <replicaMemberNode>ReplicaMemberNode1</replicaMemberNode>
        <replicationStatus>queued</replicationStatus>
        <replicaVerified>2006-05-04T18:13:51.0Z</replicaVerified>
    </replica>
</d1:systemMetadata>
"""


class TestSystemMetadata(unittest.TestCase):
  def testLoadSystemMetadata(self):
    sysm = systemmetadata.SystemMetadata(EG_SYSMETA)
    self.assertEqual(sysm.identifier, 'Identifier0')
    self.assertEqual(sysm.size, 0)
    self.assertEqual(sysm.checksum, '2e01e17467891f7c933dbaa00e1459d23db3fe4f')
    rep = sysm.replica
    self.assertEqual(len(rep), 2)
    self.assertEqual(rep[1]['replicationStatus'], 'queued')
    try:
      bogus = sysm.thisDoesntExist
    except Exception, e:
      pass
    self.assertTrue(isinstance(e, AttributeError))


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  unittest.main(testRunner=unittest.TextTestRunner)
