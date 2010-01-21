'''
Unit tests for pyd1.client

:Author: Dave Vieglais

:Created: 20100108

..autoclass:: TestPyD1Client
  :members:
'''

import unittest
import logging
import urlparse
from xml.dom.minidom import parseString
import lxml
from pyd1 import d1const
from pyd1 import d1client
from pyd1 import d1sysmeta
from pyd1 import d1exceptions

TEST_EG_SYSMETA = '''<?xml version="1.0" encoding="UTF-8"?>
<d1:SystemMetadata xmlns:d1="http://dataone.org/coordinating_node_sysmeta_0.1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://dataone.org/coordinating_node_sysmeta_0.1 https://repository.dataone.org/software/cicore/trunk/schemas/coordinating_node_sysmeta.xsd">
    <Identifier>Identifier0</Identifier>
    <Created>2006-05-04T18:13:51.0Z</Created>
    <Expires>2006-05-04T18:13:51.0Z</Expires>
    <SysMetadataCreated>2006-05-04T18:13:51.0Z</SysMetadataCreated>
    <SysMetadataModified>2006-05-04T18:13:51.0Z</SysMetadataModified>
    <ObjectFormat>http://dataone.org/coordinating_node_sysmeta_0.1</ObjectFormat>
    <Size>0</Size>
    <Submitter>Submitter0</Submitter>
    <RightsHolder>RightsHolder0</RightsHolder>
    <OriginMemberNode>OriginMemberNode0</OriginMemberNode>
    <AuthoritativeMemberNode>AuthoritativeMemberNode0</AuthoritativeMemberNode>
    <Obsoletes>Obsoletes0</Obsoletes>
    <Obsoletes>Obsoletes1</Obsoletes>
    <ObsoletedBy>ObsoletedBy0</ObsoletedBy>
    <ObsoletedBy>ObsoletedBy1</ObsoletedBy>
    <DerivedFrom>DerivedFrom0</DerivedFrom>
    <DerivedFrom>DerivedFrom1</DerivedFrom>
    <Describes>Describes0</Describes>
    <Describes>Describes1</Describes>
    <DescribedBy>DescribedBy0</DescribedBy>
    <DescribedBy>DescribedBy1</DescribedBy>
    <Replica>
        <ReplicaMemberNode>ReplicaMemberNode0</ReplicaMemberNode>
        <ReplicationStatus>Queued</ReplicationStatus>
        <ReplicaVerified>2006-05-04T18:13:51.0Z</ReplicaVerified>
    </Replica>
    <Replica>
        <ReplicaMemberNode>ReplicaMemberNode1</ReplicaMemberNode>
        <ReplicationStatus>Queued</ReplicationStatus>
        <ReplicaVerified>2006-05-04T18:13:51.0Z</ReplicaVerified>
    </Replica>
    <Checksum>Checksum0</Checksum>
    <ChecksumAlgorithm>SHA-1</ChecksumAlgorithm>
    <EmbargoExpires>2006-05-04T18:13:51.0Z</EmbargoExpires>
    <AccessRule RuleType="Allow" Service="Read" Principal="Principal0"/>
    <AccessRule RuleType="Allow" Service="Read" Principal="Principal1"/>
</d1:SystemMetadata>
'''

#Missing Identifier
TEST_BAD_EG_SYSMETA = '''<?xml version="1.0" encoding="UTF-8"?>
<d1:SystemMetadata xmlns:d1="http://dataone.org/coordinating_node_sysmeta_0.1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://dataone.org/coordinating_node_sysmeta_0.1 https://repository.dataone.org/software/cicore/trunk/schemas/coordinating_node_sysmeta.xsd">
    <Created>2006-05-04T18:13:51.0Z</Created>
    <Expires>2006-05-04T18:13:51.0Z</Expires>
    <SysMetadataCreated>2006-05-04T18:13:51.0Z</SysMetadataCreated>
    <SysMetadataModified>2006-05-04T18:13:51.0Z</SysMetadataModified>
    <ObjectFormat>http://dataone.org/coordinating_node_sysmeta_0.1</ObjectFormat>
    <Size>0</Size>
    <Submitter>Submitter0</Submitter>
    <RightsHolder>RightsHolder0</RightsHolder>
    <OriginMemberNode>OriginMemberNode0</OriginMemberNode>
    <AuthoritativeMemberNode>AuthoritativeMemberNode0</AuthoritativeMemberNode>
    <Obsoletes>Obsoletes0</Obsoletes>
    <Obsoletes>Obsoletes1</Obsoletes>
    <ObsoletedBy>ObsoletedBy0</ObsoletedBy>
    <ObsoletedBy>ObsoletedBy1</ObsoletedBy>
    <DerivedFrom>DerivedFrom0</DerivedFrom>
    <DerivedFrom>DerivedFrom1</DerivedFrom>
    <Describes>Describes0</Describes>
    <Describes>Describes1</Describes>
    <DescribedBy>DescribedBy0</DescribedBy>
    <DescribedBy>DescribedBy1</DescribedBy>
    <Replica>
        <ReplicaMemberNode>ReplicaMemberNode0</ReplicaMemberNode>
        <ReplicationStatus>Queued</ReplicationStatus>
        <ReplicaVerified>2006-05-04T18:13:51.0Z</ReplicaVerified>
    </Replica>
    <Replica>
        <ReplicaMemberNode>ReplicaMemberNode1</ReplicaMemberNode>
        <ReplicationStatus>Queued</ReplicationStatus>
        <ReplicaVerified>2006-05-04T18:13:51.0Z</ReplicaVerified>
    </Replica>
    <Checksum>Checksum0</Checksum>
    <ChecksumAlgorithm>SHA-1</ChecksumAlgorithm>
    <EmbargoExpires>2006-05-04T18:13:51.0Z</EmbargoExpires>
    <AccessRule RuleType="Allow" Service="Read" Principal="Principal0"/>
    <AccessRule RuleType="Allow" Service="Read" Principal="Principal1"/>
</d1:SystemMetadata>
'''


class TestPyD1Client(unittest.TestCase):
  def setUp(self):
    self.target = "http://localhost:8000/mn"

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

  def test_getObjectsUrl(self):
    '''Verify proper construction for getObjects
    '''
    cli = d1client.D1Client()
    expected = "%s/object/" % self.target
    self.assertUrlEqual(expected, cli.getObjectsURL(self.target))
    start = 10
    count = 100
    oclass = None
    expected = "%s/object/?start=10&count=100" % self.target
    self.assertUrlEqual(
      expected,
      cli.getObjectsURL(
        self.target, start=start, count=count,
        oclass=oclass
      )
    )
    oclass = d1const.OBJECT_CLASSES[0]
    expected = "%s/object/?start=10&count=100&oclass=%s" % (self.target, oclass)
    self.assertUrlEqual(
      expected,
      cli.getObjectsURL(
        self.target, start=start, count=count,
        oclass=oclass
      )
    )
    count = d1const.MAX_LISTOBJECTS + 1
    self.assertRaises(
      ValueError, cli.getObjectsURL,
      self.target, start=start,
      count=count
    )
    count = 1
    oclass = 'booga'
    self.assertRaises(
      ValueError,
      cli.getObjectsURL,
      self.target,
      start=start,
      count=count,
      oclass=oclass
    )

  def test_getObjectUrl(self):
    '''Verify proper url construction for getObject
    '''
    cli = d1client.D1Client()
    guid = '1234&^abc'
    expected = "%s/object/1234%%26%%5Eabc" % self.target
    self.assertUrlEqual(expected, cli.getObjectURL(self.target, guid))

  def test_getObjectMetaUrl(self):
    '''Verify proper url construction for getObjectMetadata
    '''
    cli = d1client.D1Client()
    guid = '1234&^abc'
    expected = "%s/object/1234%%26%%5Eabc/meta" % self.target
    self.assertUrlEqual(expected, cli.getObjectMetadataURL(self.target, guid))

  def test_getObjects(self):
    '''Retrieve a list of entries from a target (MN or CN)
    '''
    cli = d1client.D1Client()
    self.assertRaises(
      d1exceptions.TargetNotAvailableException, cli.listObjects,
      'http://dataone.org/__no_such_target', 0, 10
    )
    res = cli.listObjects(self.target, 0, 10)
    self.assertEqual(10, len(res['data']))

  def test_getSysMetaSchema(self):
    '''Get the system metadata schema
    '''
    cli = d1client.D1Client()
    doc = cli.getSystemMetadataSchema()
    dom = parseString(doc)
    root = dom.childNodes[0]
    interest = root.getAttribute('targetNamespace')
    self.assertEqual(interest, 'http://dataone.org/coordinating_node_sysmeta_0.1')

  def testValidateSystemMetadata(self):
    '''Try validating an example system metadata doc
    '''
    cli = d1client.D1Client()
    schema = cli.getSystemMetadataSchema()
    sysm = d1sysmeta.D1SystemMetadata(TEST_EG_SYSMETA)
    self.assertEqual(True, sysm.isValid(schema))
    sysm = d1sysmeta.D1SystemMetadata(TEST_BAD_EG_SYSMETA)
    self.assertRaises(lxml.etree.DocumentInvalid, sysm.isValid, schema)

  def testWrapSystemMetadata(self):
    '''Checking out the system metdata wrapper.
    '''
    sysm = d1sysmeta.D1SystemMetadata(TEST_EG_SYSMETA)
    self.assertEqual(sysm.Size, 0)
    self.assertEqual(sysm.Identifier, u'Identifier0')
    self.assertEqual(2006, sysm.Created.year)

  def testGetSystemMetadata(self):
    '''Retrieve system metdata for the first object in listObjects'
    '''
    cli = d1client.D1Client()
    url = cli.getObjectsURL(
      self.target, start=0,
      count=1, oclass=d1const.OBJECT_CLASSES[0]
    )
    objects = cli.listObjects(
      self.target, start=0,
      count=1, oclass=d1const.OBJECT_CLASSES[0]
    )
    guid = objects['data'][0]['guid']
    sysm = cli.getSystemMetadata(guid, target=self.target)
    self.assertEqual(sysm.Checksum, objects['data'][0]['hash'])
    self.assertEqual(sysm.Size, objects['data'][0]['size'])

  def testGetObject(self):
    '''Try getting the 5th object from listObjects'
    '''
    cli = d1client.D1Client()
    objects = cli.listObjects(self.target, start=4, count=1)
    guid = objects['data'][0]['guid']
    res = cli.get(guid, target=self.target)
    self.assertTrue(len(res) > 0)


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  unittest.main(testRunner=unittest.TextTestRunner)
