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
Module d1_client.d1sysmeta
============================

:Created: 20100111
:Author: vieglais

:Dependencies:

  - dateutil useful python library for parsing dates, available from
    http://labix.org/python-dateutil or easy_install python-dateutil

  - lxml, (optional) a python binding for libxml2 and libxslt available from 
    http://codespeak.net/lxml/  required for validation against schemas and for 
    pretty printing

This module implements a wrapper that makes it a bit simpler to pull values from
an instance of SystemMetadata.

Example:
  >>> target = "http://localhost:8000/mn"
  >>> from d1_client import client
  >>> cli = client.DataOneClient()
  >>> objects = cli.listObjects(target=target,count=3)
  >>> objects['data'][0]['guid']
  u'02c3f67e-b2e1-4550-8fae-f6d90e9f15f6'
  >>> sysm = cli.getSystemMetadata(objects['data'][0]['guid'], target=target)
  >>> sysm.Checksum
  '2e01e17467891f7c933dbaa00e1459d23db3fe4f'
'''

# StdLib.
import logging
import sys

# 3rd party.

try:
  from dateutil.parser import parse as parseDateString
except ImportError, e:
  sys.stderr.write('Import error: %s\n' % str(e))
  sys.stderr.write('Try: sudo easy_install python-dateutil\n')
  sys.stderr.write('Home: http://labix.org/python-dateutil\n')
  raise

try:
  import xml.etree.cElementTree as ET
except:
  import xml.etree.ElementTree as ET

  # Local.
import d1_common.const


class SystemMetadata(object):
  '''Wrapper around a system metadata entry.  Provides convenience properties
  for accessing the parsed content of the document.
  '''

  def __init__(self, xmldoc):
    ''':param xmldoc: (Unicode) The XML document to parse as system metadata.
    '''
    self.etree = None
    self.xmldoc = xmldoc
    self._parse(xmldoc)

  def isValid(self, schemaUrl=d1_common.const.SCHEMA_URL):
    '''This is kind of expensive as we're trying to minimize external 
    dependencies (ie. lxml and libxml2). Here we import lxml.etree, parse the 
    schema, reparse the document then check that the document is valid according 
    to the schema.
    
    :param schemaDoc: unicode or open file containing the XML Schema
    :type schemaDoc: unicode or file
    :rtype: (bool) True if all good, otherwise an exception is raised.
    '''
    try:
      from d1_client import xmlvalidator
    except:
      logging.warn('Could not import lxml. Validation not available.')
      return False
    xmlvalidator.validate(self.xmldoc, schemaUrl)
    return True

  def _parse(self, xmldoc):
    '''Parse the content and generate the internal "etree" which is the 
    element tree instance that results from parsing.
    
    :param xmldoc: (Unicode) The system metadata document to parse.
    '''
    if not isinstance(xmldoc, basestring):
      xmldoc = xmldoc.read()
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

  def __getattr__(self, name):
    '''Try and automate getting the simple properties of the schema. This works
    for elements that are simple string values.  Multiple values or things that
    require type casting need their own accessor method.
    '''
    #First try the inherited method
    try:
      return super(SystemMetadata, self).__getattr__(name)
    except AttributeError, e:
      pass
    res = self._getValues(name)
    if res is None:
      raise AttributeError("Property '%s' not found" % name)
    return res

  # <checksum algorithm="MD5">4a8565eddcef66b2147d3aa313f3ebbb</checksum>
  @property
  def checksum(self):
    '''
    '''
    return self._getValues(u'checksum')

  @property
  def checksumAlgorithm(self):
    '''
    '''
    try:
      checksumNode = self.etree.findall(u'checksum')[0]
      return checksumNode.attrib['algorithm']
    except IndexError, KeyError:
      raise AttributeError("Property 'checksumAlgorithm' not found")

  @property
  def dateUploaded(self):
    ''':rtype: (DateTime)
    '''
    return parseDateString(self._getValues(u'dateUploaded'))

  @property
  def dateSysMetadataModified(self):
    ''':rtype: (DateTime or None)
    '''
    try:
      return parseDateString(self._getValues(u'dateSysMetadataModified'))
    except:
      pass
    return None

  @property
  def size(self):
    ''':rtype: (integer) The reported size of the object from the sysmeta
    '''
    return int(self._getValues(sys._getframe().f_code.co_name))

  @property
  def obsoletes(self):
    ''':rtype: (list of unicode)
    '''
    return self._getValues(u'obsoletes', multiple=True)

  @property
  def obsoletedBy(self):
    ''':rtype: (list of unicode)
    '''
    return self._getValues(u'obsoletedBy', multiple=True)

  @property
  def derivedFrom(self):
    ''':rtype: (list of unicode)
    '''
    return self._getValues(u'derivedFrom', multiple=True)

  @property
  def describes(self):
    ''':rtype: (list of unicode)
    '''
    return self._getValues(u'describes', multiple=True)

  @property
  def describedBy(self):
    ''':rtype: (lsit of unicode)
    '''
    return self._getValues(u'describedBy', multiple=True)

  ## Replication properties
  @property
  def replica(self):
    ''':rtype: (list of dictionaries)  Each entry contains replica details
    '''
    result = []
    replicas = self.etree.findall(u'replica')
    for replica in replicas:
      entry = {}
      entry['replicaMemberNode'] = self._getValues(u'replicaMemberNode', replica)
      entry['replicationStatus'] = self._getValues(u'replicationStatus', replica)
      entry['replicaVerified'] = self._getValues(u'replicaVerified', replica)
      entry['replicationPolicy'] = self._getValues(u'replicationPolicy', replica)
      result.append(entry)
    return result

  ## Access control properties
  @property
  def embargoExpires(self):
    ''':rtype: (DateTime or None)
    '''
    try:
      return parseDateString(self._getValues(u'embargoExpires'))
    except:
      pass
    return None

  @property
  def accessRule(self):
    ''':rtype: (list of 3-tuple) [(type, service, principal), ... ]
    '''
    entries = self._getValues(u'accessRule', multiple=True)
    results = []
    for entry in entries:
      values = entry.split(u",")
      if len(values) == 3:
        results.append(values)
    return results
