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
Module d1_common.types.objectlist_serialization
===============================================

Serializaton and deserialization of the DataONE ObjectList type.

:Created: 2010-06-28
:Author: DataONE (dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import StringIO
import csv
import datetime
import logging
import sys
import xml
import json

#try:
#  from lxml import etree
#except ImportError, e:
#  sys.stderr.write('Import error: {0}\n'.format(str(e)))
#  sys.stderr.write('Try: sudo apt-get install python-lxml\n')
#  raise
try:
  import iso8601
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-setuptools\n')
  sys.stderr.write(
    '     sudo easy_install http://pypi.python.org/packages/2.5/i/iso8601/iso8601-0.1.4-py2.5.egg\n'
  )
  raise

# App.
try:
  import d1_common
  import d1_common.types.exceptions
  import d1_common.const
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/api-common-python/src/d1_common\n'
  )
  raise
try:
  import d1_common.types.generated.dataoneTypes
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo easy_install pyxb\n')
  raise
import serialization_base


class ObjectList(serialization_base.Serialization):
  def __init__(self):
    '''Serializaton and deserialization of the DataONE ObjectList type.
    '''
    serialization_base.Serialization.__init__(self)

    self.log = logging.getLogger('ObjectListSerialization')

    self.pri = [
      d1_common.const.MIMETYPE_XML,
      d1_common.const.MIMETYPE_APP_XML,
      d1_common.const.MIMETYPE_JSON,
      d1_common.const.MIMETYPE_CSV,
      d1_common.const.MIMETYPE_RDF,
      #d1_common.const.MIMETYPE_HTML,
      #d1_common.const.MIMETYPE_LOG,
    ]

    self.object_list = d1_common.types.generated.dataoneTypes.objectList()

    #<?xml version="1.0" encoding="UTF-8"?>
    #<p:objectList count="0" start="0" total="0"
    #  xmlns:p="http://ns.dataone.org/service/types/ObjectList/0.1"
    #  xmlns:p1="http://ns.dataone.org/service/types/common/0.1"
    #  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    #  xsi:schemaLocation="http://ns.dataone.org/service/types/ObjectList/0.1 objectlist.xsd ">
    #  <objectInfo>
    #    <identifier>identifier</identifier>
    #    <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
    #    <checksum algorithm="SHA-1">checksum</checksum>
    #    <dateSysMetadataModified>2001-12-31T12:00:00</dateSysMetadataModified>
    #    <size>0</size>
    #  </objectInfo>
    #</p:objectList>
  def serialize_xml(self, pretty=False, jsonvar=False):
    '''Serialize ObjectList to XML.
    '''
    return self.object_list.toxml()

  def serialize_json(self, pretty=False, jsonvar=False):
    '''Serialize ObjectList to JSON.
    '''
    obj = {}
    obj['objectInfo'] = []

    for o in self.object_list.objectInfo:
      objectInfo = {}
      objectInfo['identifier'] = o.identifier.value()
      objectInfo['objectFormat'] = o.objectFormat
      objectInfo['checksumAlgorithm'] = o.checksum.algorithm
      objectInfo['checksum'] = o.checksum.value()
      objectInfo['dateSysMetadataModified'] = datetime.datetime.isoformat(
        o.dateSysMetadataModified
      )
      objectInfo['size'] = o.size

      # Append object to response.
      obj['objectInfo'].append(objectInfo)

    obj['start'] = self.object_list.start
    obj['count'] = self.object_list.count
    obj['total'] = self.object_list.total

    if pretty:
      if jsonvar is not False:
        return jsonvar + ' = ' + json.dumps(obj, indent=2)
      else:
        return json.dumps(obj, indent=2)
    else:
      if jsonvar is not False:
        return jsonvar + '=' + json.dumps(obj)
      else:
        return json.dumps(obj)

  # #<start>,<count>,<total>
  # <pid>,<object format>,<algorithm used for checksum>,<checksum of object>,<date time last modified>,<byte size of object>
  def serialize_csv(self, pretty=False, jsonvar=False):
    '''Serialize ObjectList to CSV.
    '''

    io = StringIO.StringIO()

    # Comment containing start, count and total.
    io.write(
      '#{0},{1},{2}\n'.format(
        self.object_list.start, self.object_list.count, self.object_list.total
      )
    )

    csv_writer = csv.writer(
      io, dialect=csv.excel,
      quotechar='"', quoting=csv.QUOTE_MINIMAL
    )

    for o in self.object_list.objectInfo:
      csv_line = []

      csv_line.append(o.identifier.value())
      csv_line.append(o.objectFormat)
      csv_line.append(o.checksum.value())
      csv_line.append(o.checksum.algorithm)
      csv_line.append(datetime.datetime.isoformat(o.dateSysMetadataModified))
      csv_line.append(o.size)

      csv_writer.writerow(csv_line)

    return io.getvalue()

  #<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  #    xmlns:d1='http://ns.dataone.org/core/objects/'>
  #  <rdf:Description rdf:about="_requesting URL_">
  #    <d1:start>_integer_</d1:start>
  #    <d1:count>_integer_</d1:count>
  #    <d1:total>_integer_</d1:total>
  #  </rdf:Description>
  #  <rdf:Description rdf:about="_requesting URL_">
  #    <d1:data rdf:parseType="Collection">
  #      <rdf:Description rdf:about="http://mn1.dataone.org/object/_pid_">
  #        <d1:oclass>_object class_</d1:oclass>
  #        <d1:checksum>
  #          <d1:algorithm>_algorithm used for checksum_</d1:algorithm>
  #          <d1:value>_checksum of object_</d1:value>
  #        </d1:checksum>
  #        <d1:modified>_date time last modified_</d1:modified>
  #        <d1:size>_byte size of object_</d1:size>
  #      </rdf:Description>
  #    </d1:data>
  #  </rdf:Description>
  #</rdf:RDF>
  def serialize_rdf_xml(self, pretty=False, jsonvar=False):
    '''Serialize ObjectList to RDF XML.
    '''
    raise d1_common.types.exceptions.NotImplemented('serialize_rdf_xml')
    # Set up namespaces for the XML response.
    #    RDF_NS = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    #    D1_NS = 'http://ns.dataone.org/core/objects'
    #    RDF = '{{{0}}}'.format(RDF_NS)
    #    D1 = '{{{0}}}'.format(D1_NS)
    #    NSMAP = {'rdf' : RDF_NS, 'd1' : D1_NS}
    #    xml = etree.Element(RDF + 'rdf', nsmap=NSMAP)
    #  
    #    description = etree.SubElement(xml, RDF + 'Description')
    #    description.set(RDF + 'about', '_requesting URL_')
    #      
    #    description = etree.SubElement(xml, RDF + 'Description')
    #    description.set(RDF + 'about', 'http://mn1.dataone.org/object/_pid_')
    #  
    #    for o in self.object_list.objectInfo:
    #      objectInfo = etree.SubElement(description, u'objectInfo')
    #      
    #      ele = etree.SubElement(objectInfo, u'identifier')
    #      ele.text = unicode(o.identifier)
    #    
    #      ele = etree.SubElement(objectInfo, u'objectFormat')
    #      ele.text = unicode(o.objectFormat)
    #    
    #      ele = etree.SubElement(objectInfo, u'checksum')
    #      ele.text = unicode(o.checksum.value())
    #      ele.attrib[u'algorithm'] = unicode(o.checksum.algorithm)
    #    
    #      # Get modified date in an ISO 8601 string.
    #      ele = etree.SubElement(objectInfo, u'dateSysMetadataModified')
    #      ele.text = unicode(datetime.datetime.isoformat(o.dateSysMetadataModified))
    #    
    #      ele = etree.SubElement(objectInfo, u'size')
    #      ele.text = unicode(o.size)
    #
    #    # Return xml as string.
    #    return etree.tostring(xml, pretty_print=pretty,  encoding='UTF-8', xml_declaration=True)

    #============================================================================

  def deserialize_xml(self, doc):
    '''Deserialize ObjectList from XML.
    '''
    self.object_list = d1_common.types.generated.dataoneTypes.CreateFromDocument(doc)
    return self.object_list

  def deserialize_json(self, doc):
    '''Deserialize ObjectList from JSON.
    '''
    j = json.loads(doc)
    self.object_list.start = j['start']
    self.object_list.count = j['count']
    self.object_list.total = j['total']
    objectInfos = []
    for o in j['objectInfo']:
      objectInfo = d1_common.types.generated.dataoneTypes.ObjectInfo()
      objectInfo.identifier = o['identifier']
      objectInfo.objectFormat = o['objectFormat']
      objectInfo.checksum = o['checksum']
      objectInfo.checksum.algorithm = o['checksumAlgorithm']
      objectInfo.dateSysMetadataModified = iso8601.parse_date(
        o['dateSysMetadataModified']
      )
      objectInfo.size = o['size']
      objectInfos.append(objectInfo)

    self.object_list.objectInfo = objectInfos
    return self.object_list

    # #<start>,<count>,<total>
    # <pid>,<object format>,<algorithm used for checksum>,<checksum of object>,<date time last modified>,<byte size of object>
  def deserialize_csv(self, doc):
    '''Deserialize ObjectList from CSV.
    '''
    io = StringIO.StringIO(doc)
    csv_reader = csv.reader(
      io, dialect=csv.excel,
      quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    objectInfos = []
    for csv_line in csv_reader:
      # Get start, count and total from first comment.
      if csv_line[0][0] == '#':
        self.object_list.start = csv_line[0][1:]
        self.object_list.count = csv_line[1]
        self.object_list.total = csv_line[2]
        continue

      objectInfo = d1_common.types.generated.dataoneTypes.ObjectInfo()
      objectInfo.identifier = csv_line[0]
      objectInfo.objectFormat = csv_line[1]
      objectInfo.checksum = csv_line[2]
      objectInfo.checksum.algorithm = csv_line[3]
      objectInfo.dateSysMetadataModified = csv_line[4]
      objectInfo.size = csv_line[5]
      objectInfos.append(objectInfo)

    self.object_list.objectInfo = objectInfos
    return self.object_list
