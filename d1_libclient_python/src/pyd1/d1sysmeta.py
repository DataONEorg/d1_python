'''
Module pyd1.d1sysmeta
=====================

:Created: 20100111
:Author: vieglais

:Dependencies:

  - dateutil useful python library for parsing dates, available from
    http://labix.org/python-dateutil or easy_install python-dateutil

  - lxml, (optional) a python binding for libxml2 and libxslt available from 
    http://codespeak.net/lxml/  required for validation against schemas and for 
    pretty printing
'''

import logging
from dateutil.parser import parse as parseDateString
try:
  import xml.etree.cElementTree as ET
except:
  import xml.etree.ElementTree as ET
from pyd1 import d1const


class D1SystemMetadata(object):
  '''Wrapper around a system metadata entry.  Provides convenience properties
  for accessing the parsed content of the document.
  
  Example:
    >>> target = "http://localhost:8000/mn"
    >>> from pyd1 import d1client
    >>> cli = d1client.D1Client()
    >>> objects = cli.listObjects(target=target,count=3)
    >>> objects['data'][0]['guid']
    u'02c3f67e-b2e1-4550-8fae-f6d90e9f15f6'
    >>> sysm = cli.getSystemMetadata(objects['data'][0]['guid'], target=target)
    >>> sysm.Checksum
    '2e01e17467891f7c933dbaa00e1459d23db3fe4f'
  '''

  def __init__(self, xmldoc):
    '''
    :param xmldoc: (Unicode) The XML document to parse as system metadata.
    :param validate: (Bool) If True, then validate the supplied document against
                     the DataONE system metadata schema.
    '''
    self.etree = None
    self.xmldoc = xmldoc
    self._parse(xmldoc)

  def isValid(self, schemaDoc):
    '''This is kind of expensive as we're trying to minimize external 
    dependencies (ie. lxml and libxml2). Here we import lxml.etree, parse the 
    schema, reparse the document then check that the document is valid according 
    to the schema.
    
    :param schemaDoc: unicode or open file containing the XML Schema
    :rtype: (bool) True if all good, otherwise an exception is raised.
    '''
    try:
      from cStringIO import StringIO
    except:
      from StringIO import StringIO
    try:
      from lxml import etree as lxmletree
    except:
      logging.warn('Could not import lxml.  Validation not available.')
      return False
    fschema = schemaDoc
    if isinstance(schemaDoc, basestring):
      fschema = StringIO(schemaDoc)
    xmlschema = lxmletree.XMLSchema(file=fschema)
    xmldocument = lxmletree.fromstring(self.xmldoc)
    xmlschema.assertValid(xmldocument)
    return True

  def _parse(self, xmldoc):
    '''Parse the content and generate the internal "etree" which is the 
    element tree instance that results from parsing.
    
    :param xmldoc: (Unicode) The system metadata document to parse.
    '''
    self.xmldoc = xmldoc
    self.etree = ET.fromstring(xmldoc)

  def __repr__(self):
    return self.xmldoc

  def toXml(self, encoding='utf-8', pretty=True):
    '''Spits out representation of the parsed xml.
    
    :param pretty: Output is a bit easier for human digestion if True (requires
        lxml.etree to be installed)
    :rtype: (string) UTF-8 encoded string
    '''
    if pretty:
      try:
        from lxml import etree as lxmletree
        lxmldoc = lxmletree.fromstring(self.xmldoc)
        return lxmletree.tostring(
          lxmldoc, encoding=encoding,
          pretty_print=True,
          xml_declaration=False
        )
      except:
        pass
    return ET.tostring(self.etree, encoding)

  def _getValues(self, nodeName, root=None, multiple=False):
    nodes = []
    if root is None:
      nodes = self.etree.findall(nodeName)
    else:
      nodes = root.findall(nodeName)
    if len(nodes) == 0:
      return None
    if not multiple:
      return nodes[0].text
    res = []
    for node in nodes:
      res.append(node.text)
    return res

  ## General properties
  @property
  def Identifier(self):
    ''':rtype: (unicode) The identifier of the object described by this sysmeta
    '''
    return self._getValues(u'Identifier')

  @property
  def Created(self):
    ''':rtype: (DateTime)
    '''
    return parseDateString(self._getValues(u'Created'))

  @property
  def Expires(self):
    ''':rtype: (DateTime or None)
    '''
    try:
      return parseDateString(self._getValues(u'Expires'))
    except:
      pass
    return None

  @property
  def SysMetadataCreated(self):
    ''':rtype: (DateTime)
    '''
    return parseDateString(self._getValues(u'SysMetadataCreated'))

  @property
  def SysMetadataModified(self):
    ''':rtype: (DateTime)
    '''
    return parseDateString(self._getValues(u'SysMetadataModified'))

  @property
  def ObjectFormat(self):
    ''':rtype: (unicode)
    '''
    return self._getValues(u'ObjectFormat')

  @property
  def Size(self):
    ''':rtype: (integer) The reported size of the object from the sysmeta
    '''
    return int(self._getValues(u'Size'))

  ## Provenance properties
  @property
  def Submitter(self):
    ''':rtype: (unicode)
    '''
    return self._getValues(u'Submitter')

  @property
  def RightsHolder(self):
    ''':rtype: (unicode)
    '''
    return self._getValues(u'RightsHolder')

  @property
  def OriginMemberNode(self):
    ''':rtype: (unicode)
    '''
    return self._getValues(u'OriginMemberNode')

  @property
  def AuthoritativeMemberNode(self):
    ''':rtype: (unicode)
    '''
    return self._getValues(u'AuthoritativeMemberNode')

  @property
  def Obsoletes(self):
    ''':rtype: (list of unicode)
    '''
    return self._getValues(u'Obsoletes', multiple=True)

  @property
  def ObsoletedBy(self):
    ''':rtype: (list of unicode)
    '''
    return self._getValues(u'ObsoletedBy', multiple=True)

  @property
  def DerivedFrome(self):
    ''':rtype: (list of unicode)
    '''
    return self._getValues(u'DerivedFrom', multiple=True)

  @property
  def Describes(self):
    ''':rtype: (list of unicode)
    '''
    return self._getValues(u'Describes', multiple=True)

  @property
  def DescribedBy(self):
    ''':rtype: (lsit of unicode)
    '''
    return self._getValues(u'DescribedBy', multiple=True)

  ## Replication properties
  @property
  def Replica(self):
    ''':rtype: (list of dictionaries)  Each entry contains replica details
    '''
    result = []
    replicas = self.etree.findall(u'Replica')
    for replica in replicas:
      entry = {}
      entry['ReplicaMemberNode'] = self._getValues(u'ReplicaMemberNode', replica)
      entry['ReplicationStatus'] = self._getValues(u'ReplicationStatus', replica)
      entry['ReplicaVerified'] = self._getValues(u'ReplicaVerified', replica)
      entry['ReplicationPolicy'] = self._getValues(u'ReplicationPolicy', replica)
      result.append(entry)
    return result

  ## Data Consistency properties
  @property
  def Checksum(self):
    ''':rtype: (unicode) The checksum for the object.
    '''
    return self._getValues(u'Checksum')

  @property
  def ChecksumAlgorthm(self):
    ''':rtype: (unicode) The checksum for the object.
    '''
    return self._getValues(u'ChecksumAlgorithm')

  ## Access control properties
  @property
  def EmbargoExpires(self):
    ''':rtype: (DateTime or None)
    '''
    try:
      return parseDateString(self._getValues(u'EmbargoExpires'))
    except:
      pass
    return None

  @property
  def AccessRule(self):
    ''':rtype: (list of 3-tuple) [(type, service, principal), ... ]
    '''
    entries = self._getValues(u'AccessRule', multiple=True)
    results = []
    for entry in entries:
      values = entry.split(u",")
      if len(values) == 3:
        results.append(values)
    return results
