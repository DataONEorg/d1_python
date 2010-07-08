'''
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
import d1common
import d1common.exceptions
import d1common.ext.mimeparser

try:
  import d1common.types.generated.objectlist
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo easy_install pyxb\n')
  raise

#===============================================================================


class ObjectList(d1common.types.generated.objectlist.ObjectList):
  def __init__(self):
    self.serialize_map = {
      'application/json': self.serializeJSON,
      'text/csv': self.serializeCSV,
      'text/xml': self.serializeXML,
      'application/rdf+xml': self.serializeRDFXML,
      #'text/html': self.serializeNULL, #TODO: Not in current REST spec.
      #'text/log': self.serializeNULL, #TODO: Not in current REST spec.
    }

    self.deserialize_map = {
      'application/json': self.deserializeJSON,
      'text/csv': self.deserializeCSV,
      'text/xml': self.deserializeXML,
      'application/rdf+xml': self.deserializeRDFXML,
      #'text/html': self.deserializeNULL, #TODO: Not in current REST spec.
      #'text/log': self.deserializeNULL, #TODO: Not in current REST spec.
    }

    self.pri = [
      'application/json',
      'text/csv',
      'text/xml',
      'application/rdf+xml',
      #'text/html',
      #'text/log',
    ]

    self.object_list = d1common.types.generated.objectlist.objectList()

  def serialize(self, accept='application/json', pretty=False, jsonvar=False):
    # Determine which serializer to use. If client does not supply accept, we
    # default to JSON.
    try:
      content_type = d1common.ext.mimeparser.best_match(self.pri, accept)
    except ValueError:
      # An invalid Accept header causes mimeparser to throw a ValueError.
      sys_log.debug('Invalid HTTP_ACCEPT value. Defaulting to JSON')
      content_type = accept

    # Deserialize object
    return self.serialize_map[content_type](pretty, jsonvar), content_type

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
  def serializeXML(self, pretty=False, jsonvar=False):
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
  def serializeJSON(self, pretty=False, jsonvar=False):
    '''Serialize ObjectList to JSON.
    '''
    obj = {}
    obj['objectInfo'] = []

    for o in self.object_list.objectInfo:
      objectInfo = {}
      objectInfo['identifier'] = o.identifier
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
  def serializeCSV(self, pretty=False, jsonvar=False):
    '''Serialize ObjectList to JSON.
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

      csv_line.append(o.identifier)
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
  def serializeRDFXML(self, pretty=False, jsonvar=False):
    '''Serialize ObjectList to RDFXML.
    '''

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

  def serializeNULL(self, doc, pretty=False, jsonvar=False):
    raise d1common.exceptions.NotImplemented(0, 'Serialization method not implemented.')

    #===============================================================================

  def deserialize(self, doc, content_type='application/json'):
    return self.deserialize_map[content_type](doc)

  def deserializeXML(self, doc):
    self.object_list = d1common.types.generated.objectlist.CreateFromDocument(doc)

  def deserializeRDFXML(self, doc):
    raise d1common.exceptions.NotImplemented(0, 'deserializeRDFXML not implemented.')

  def deserializeJSON(self, doc):
    j = json.loads(doc)

    self.object_list.start = j['start']
    self.object_list.count = j['count']
    self.object_list.total = j['total']

    objectInfos = []

    for o in j['objectInfo']:
      objectInfo = d1common.types.generated.objectlist.ObjectInfo()

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

  # #<start>,<count>,<total>
  # <identifier>,<object format>,<algorithm used for checksum>,<checksum of object>,<date time last modified>,<byte size of object>
  def deserializeCSV(self, doc):
    '''Serialize object to CSV.
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

      objectInfo = d1common.types.generated.objectlist.ObjectInfo()

      objectInfo.identifier = csv_line[0]
      objectInfo.objectFormat = csv_line[1]
      objectInfo.checksum = csv_line[2]
      objectInfo.checksum.algorithm = csv_line[3]
      objectInfo.dateSysMetadataModified = csv_line[4]
      objectInfo.size = csv_line[5]

      objectInfos.append(objectInfo)

    self.object_list.objectInfo = objectInfos

  def deserializeNULL(self, doc):
    raise d1common.exceptions.NotImplemented(
      0, 'De-serialization method not implemented.'
    )
