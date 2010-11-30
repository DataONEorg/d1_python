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
==============================================

Implements serializaton and de-serialization for the ObjectList.
'''

# Stdlib.
import csv
import datetime
import os
import StringIO
import sys
import types
import urllib
import wsgiref.handlers
import time
import logging

try:
  import cjson as json
except:
  import json

# 3rd party.
# Lxml
try:
  from lxml import etree
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-lxml\n')
  raise

try:
  import iso8601
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-setuptools\n')
  sys.stderr.write(
    '     sudo easy_install http://pypi.python.org/packages/2.5/i/iso8601/iso8601-0.1.4-py2.5.egg\n'
  )
  raise

# MN API.
try:
  import d1_common
  import d1_common.exceptions
  import d1_common.ext.mimeparser
  import d1_common.util
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

#===============================================================================


class ObjectList(object):
  def __init__(self):
    self.log = logging.getLogger('ObjectList')
    self.serialize_map = {
      'application/json': self.serialize_json,
      'text/csv': self.serialize_csv,
      'text/xml': self.serialize_xml,
      'application/xml': self.serialize_xml,
      'application/rdf+xml': self.serialize_rdf_xml,
      #'text/html': self.serialize_null, #TODO: Not in current REST spec.
      #'text/log': self.serialize_null, #TODO: Not in current REST spec.
    }

    self.deserialize_map = {
      'application/json': self.deserialize_json,
      'text/csv': self.deserialize_csv,
      'text/xml': self.deserialize_xml,
      'application/xml': self.deserialize_xml,
      'application/rdf+xml': self.deserialize_rdf_xml,
      #'text/html': self.deserialize_null, #TODO: Not in current REST spec.
      #'text/log': self.deserialize_null, #TODO: Not in current REST spec.
    }

    self.pri = [
      'application/json',
      'text/csv',
      'text/xml',
      'application/xml',
      'application/rdf+xml',
      #'text/html',
      #'text/log',
    ]

    self.object_list = d1_common.types.generated.dataoneTypes.objectList()

  def serialize(self, accept='application/json', pretty=False, jsonvar=False):
    # Determine which serializer to use. If client does not supply accept, we
    # default to JSON.
    try:
      content_type = d1_common.ext.mimeparser.best_match(self.pri, accept)
    except ValueError:
      # An invalid Accept header causes mimeparser to throw a ValueError.
      #sys_log.debug('Invalid HTTP_ACCEPT value. Defaulting to JSON')
      content_type = 'application/json'
    self.log.debug("serializing, content-type=%s" % content_type)

    # Deserialize object
    return self.serialize_map[d1_common.util.get_content_type(content_type)](
      pretty, jsonvar
    ), content_type

  #<?xml version="1.0" encoding="UTF-8"?>
  #<p:objectList count="0" start="0" total="0"
  #  xmlns:p="http://dataone.org/service/types/ObjectList/0.1"
  #  xmlns:p1="http://dataone.org/service/types/common/0.1"
  #  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  #  xsi:schemaLocation="http://dataone.org/service/types/ObjectList/0.1 objectlist.xsd ">
  #  <objectInfo>
  #    <identifier>identifier</identifier>
  #    <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
  #    <checksum algorithm="SHA-1">checksum</checksum>
  #    <dateSysMetadataModified>2001-12-31T12:00:00</dateSysMetadataModified>
  #    <size>0</size>
  #  </objectInfo>
  #</p:objectList>
  def serialize_xml(self, pretty=False, jsonvar=False):
    self.log.debug("serialize_xml")
    return self.object_list.toxml()

  #{
  #  'start': <integer>,
  #  'count': <integer>,
  #  'total': <integer>,
  #  'objectInfo':
  #  [
  #    {
  #      'guid':<identifier>,
  #      'oclass':<object class>,
  #      'checksum': {'algorithm': <algorithm used for checksum>, 'value': <checksum of object> }
  #      'modified':<date time last modified>,
  #      'size':<byte size of object>
  #    },
  #    ...
  #  ]
  #}
  def serialize_json(self, pretty=False, jsonvar=False):
    '''Serialize ObjectList to JSON.
    '''
    self.log.debug("serialize_json")
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
  # <identifier>,<object format>,<algorithm used for checksum>,<checksum of object>,<date time last modified>,<byte size of object>
  def serialize_csv(self, pretty=False, jsonvar=False):
    '''Serialize ObjectList to CSV.
    '''
    self.log.debug("serialize_csv")

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
  #      <rdf:Description rdf:about="http://mn1.dataone.org/object/_identifier_">
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
    '''Serialize ObjectList to RDFXML.
    '''
    self.log.debug("serialize_rdf_xml")

    # Set up namespaces for the XML response.
    RDF_NS = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    D1_NS = 'http://ns.dataone.org/core/objects'
    RDF = '{{{0}}}'.format(RDF_NS)
    D1 = '{{{0}}}'.format(D1_NS)
    NSMAP = {'rdf': RDF_NS, 'd1': D1_NS}
    xml = etree.Element(RDF + 'rdf', nsmap=NSMAP)

    description = etree.SubElement(xml, RDF + 'Description')
    description.set(RDF + 'about', '_requesting URL_')

    description = etree.SubElement(xml, RDF + 'Description')
    description.set(RDF + 'about', 'http://mn1.dataone.org/object/_identifier_')

    for o in self.object_list.objectInfo:
      objectInfo = etree.SubElement(description, u'objectInfo')

      ele = etree.SubElement(objectInfo, u'identifier')
      ele.text = unicode(o.identifier)

      ele = etree.SubElement(objectInfo, u'objectFormat')
      ele.text = unicode(o.objectFormat)

      ele = etree.SubElement(objectInfo, u'checksum')
      ele.text = unicode(o.checksum.value())
      ele.attrib[u'algorithm'] = unicode(o.checksum.algorithm)

      # Get modified date in an ISO 8601 string.
      ele = etree.SubElement(objectInfo, u'dateSysMetadataModified')
      ele.text = unicode(datetime.datetime.isoformat(o.dateSysMetadataModified))

      ele = etree.SubElement(objectInfo, u'size')
      ele.text = unicode(o.size)

    # Return xml as string.
    return etree.tostring(
      xml, pretty_print=pretty,
      encoding='UTF-8', xml_declaration=True
    )

  def serialize_null(self, doc, pretty=False, jsonvar=False):
    raise d1_common.exceptions.NotImplemented(0, 'Serialization method not implemented.')

    #===============================================================================

  def deserialize(self, doc, content_type='application/json'):
    self.log.debug("de-serialize, content-type=%s" % content_type)
    return self.deserialize_map[d1_common.util.get_content_type(content_type)](doc)

  def deserialize_xml(self, doc):
    self.log.debug('deserialize xml')
    self.object_list = d1_common.types.generated.dataoneTypes.CreateFromDocument(doc)
    return self.object_list

  def deserialize_rdf_xml(self, doc):
    self.log.debug('deserialize rdf xml')
    raise d1_common.exceptions.NotImplemented(0, 'deserialize_rdf_xml not implemented.')

  def deserialize_json(self, doc):
    self.log.debug('deserialize json')
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
  # <identifier>,<object format>,<algorithm used for checksum>,<checksum of object>,<date time last modified>,<byte size of object>
  def deserialize_csv(self, doc):
    '''Serialize object to CSV.
    '''
    self.log.debug('deserialize csv')
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

  def deserialize_null(self, doc):
    self.log.debug('deserialize NULL')
    raise d1_common.exceptions.NotImplemented(
      0, 'De-serialization method not implemented.'
    )
