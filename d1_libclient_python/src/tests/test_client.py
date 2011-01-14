'''
Unit tests for pyd1.d1client

:Author: Dave Vieglais

:Created: 20100108

..autoclass:: TestPyD1Client
  :members:
'''

import sys
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

from d1_common import xmlrunner
from d1_common import exceptions
from d1_common.types import systemmetadata
from d1_client import const
from d1_client import client

MEMBER_NODES = {
  'dryad': 'http://dev-dryad-mn.dataone.org/mn',
  'daac': 'http://daacmn.dataone.utk.edu/mn',
  'metacat': 'http://knb-mn.ecoinformatics.org/knb/d1',
}

COORDINATING_NODES = {'cn-dev': 'http://cn-dev.dataone.org/cn', }


class TestCaseWithURLCompare(unittest.TestCase):
  '''Utility class that check whether two URLs are equal.  Not really as simple
  as it migh seem at first.
  '''

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


class TestRestClient(TestCaseWithURLCompare):
  '''Run a couple of tests with the low level REST client.
  '''

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
    #This should fail
    try:
      cli.GET('http://some.bogus.address/')
    except Exception, e:
      pass
    self.assertTrue(isinstance(e, urllib2.URLError))
    #self.assertEqual(e.errno, socket.EAI_NONAME)

    #===============================================================================


class TestDataOneClient(TestCaseWithURLCompare):
  def setUp(self):
    self.target = MEMBER_NODES['metacat']

  def testGet(self):
    return
    cli = client.DataOneClient(target=self.target)
    #try loading some random object
    start = 23
    count = 1
    startTime = None
    endTime = None
    requestFormat = 'text/xml'
    objlist = cli.listObjects(
      start=start,
      count=count,
      startTime=startTime,
      endTime=endTime,
      requestFormat=requestFormat
    )
    id = objlist.objectInfo[0].pid
    logging.info("Attempting to get ID=%s" % id)
    bytes = cli.get(id).read()
    headers = cli.headers
    headers['Accept'] = 'text/xml'
    sysmeta = cli.getSystemMetadata(id, headers=headers)
    self.assertEqual(sysmeta.identifier, id)

  def testGetFail(self):
    cli = client.DataOneClient(target=self.target)
    # see if failure works
    id = 'some bogus id'
    self.assertRaises(exceptions.NotFound, cli.get, id)

  def testGetSystemMetadata(self):
    #TODO: test getSystemMetadata()
    pass

  def _subListObjectTest(self, requestformat):
    cli = client.DataOneClient(target=self.target)
    start = 0
    count = 10
    startTime = None
    endTime = None
    requestFormat = 'text/xml'
    objlist = cli.listObjects(
      start=start,
      count=count,
      startTime=startTime,
      endTime=endTime,
      requestFormat=requestFormat
    )
    self.assertEqual(objlist.count, len(objlist.objectInfo))
    obj = objlist.objectInfo[0]
    tmp = obj.size
    tmp = obj.checksum
    tmp = obj.dateSysMetadataModified
    tmp = obj.identifier
    tmp = obj.objectFormat

    start = 4
    count = 3
    objlist2 = cli.listObjects(
      start=start,
      count=count,
      startTime=startTime,
      endTime=endTime,
      requestFormat=requestFormat
    )
    self.assertEqual(objlist2.count, len(objlist2.objectInfo))
    self.assertEqual(objlist2.count, count)
    i = 0
    for obj in objlist2.objectInfo:
      self.assertEqual(objlist.objectInfo[4 + i].identifier, obj.identifier)
      logging.info(obj.identifier)
      i += 1

  def testListObjectsJson(self):
    #requestFormat = 'application/json'
    #self._subListObjectTest(requestFormat)
    pass

  def testListObjectsXml(self):
    requestFormat = 'text/xml'
    self._subListObjectTest(requestFormat)

#===============================================================================


class TestListObjects(unittest.TestCase):
  def setUp(self):
    self.target = MEMBER_NODES['dryad']

  def testValidListObjects(self):
    return
    objectListUrl = "https://repository.dataone.org/software/cicore/trunk/schemas/dataoneTypes.xsd"
    cli = client.DataOneClient(target=self.target)
    response = cli.listObjects(start=0, count=5)
    logging.error("====")
    logging.error(response)
    #not needed any more since the pxyb parser will validate
    #xmlvalidator.validate(response, objectListUrl)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
  #unittest.main(testRunner=xmlrunner.XmlTestRunner(sys.stdout))
