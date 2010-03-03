#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""serialize
==============

:module: serialize
:platform: Linux
:synopsis:

.. moduleauthor:: Roger Dahl
"""

# Stdlib.
import csv
import StringIO
import types

# 3rd party.
# Lxml
try:
  from lxml import etree
except ImportError, e:
  sys_log.error('Import error: %s' % str(e))
  sys_log.error('Try: sudo apt-get install python-lxml')
  sys.exit(1)

# Django.
from django.http import HttpResponseServerError
from django.utils.html import escape

# App
import settings
import sys_log


def serialize(obj, serialization_format, pretty=False):
  """Serialize to JSON, CSV, XML or RDF XML.
  """

  # Branch out to specific serializers.
  if serialization_format == 'json':
    return to_json(obj, pretty)
  if serialization_format == 'csv':
    return to_csv(obj, pretty)
  if serialization_format == 'xml':
    return to_xml(obj, pretty)
  if serialization_format == 'rdf_xml':
    return to_rdf_xml(obj, pretty)

  # Unknown serialization format.
  sys_log.error(
    'Internal server error: Unrecognized serialization format: %s' % serialization_format
  )
  return HttpResponseServerError()


#{
#  'start': <integer>,
#  'count': <integer>,
#  'total': <integer>,
#  'data':
#  [
#    {
#      'guid':<identifier>,
#      'oclass':<object class>,
#      'hash':<SHA1 hash of object>,
#      'modified':<date time last modified>,
#      'size':<byte size of object>
#    },
#    ...
#  ]
#}
def to_json(obj, pretty):
  """Serialize object to JSON.
  """
  if pretty:
    return json.dumps(obj, indent=2)
  else:
    return json.dumps(obj)


# #<start>,<count>,<total>
# 'guid',otype,hash,modified,size
# <identifier>,<object class>,<SHA1 hash of object>,<date time last modified>,<byte size of object>
def to_csv(obj, pretty):
  """Serialize object to CSV.
  """

  io = StringIO.StringIO()
  # Comment containint start, count and object.
  io.write('#%d,%d,%d\n' % (obj['start'], obj['count'], obj['total']))

  csv_writer = csv.writer(io, dialect=csv.excel, quotechar='"', quoting=csv.QUOTE_MINIMAL)

  first = True
  for d in obj['data']:
    if first == True:
      # Don't know if it's possible for the order of the keys to change during
      # iteration of the data objects, so grab the keys once here and use those
      # for iteration.
      keys = d.keys()
      # Header containing names of fields.
      io.write(','.join(keys) + '\n')
      first = False

    row = []

    for key in keys:
      val = d[key]
      if type(val) is types.IntType:
        row.append(val)
      else:
        row.append(val.encode('utf-8'))

    csv_writer.writerow(row)

  return io.getvalue()


#<response xmlns='http://ns.dataone.org/core/objects'
#          start='_integer_'
#          count='_integer_'
#          total='_integer_'>
#  <data guid='_identifier_'>
#    <oclass>_object class_</oclass>
#    <hash>_SHA1 hash of object</hash>
#    <modified>_date time last modified_</modified>
#    <size>_byte size of object_</size>
#  </data>
#  ...
#</response>
def to_xml(obj, pretty):
  """Serialize object to XML.
  """

  # Set up namespace for the xml response.
  RESPONSE_NS = 'http://ns.dataone.org/core/objects'
  RESPONSE = '{%s}' % RESPONSE_NS
  NSMAP = {'d1': RESPONSE_NS} # the default namespace
  xml = etree.Element(RESPONSE + 'response', nsmap=NSMAP)

  start = etree.SubElement(xml, 'start')
  start.text = unicode(obj['start'])

  start = etree.SubElement(xml, 'count')
  start.text = unicode(obj['count'])

  start = etree.SubElement(xml, 'total')
  start.text = unicode(obj['total'])

  for d in obj['data']:
    data = etree.SubElement(xml, 'data')

    for key in sorted(d.keys()):
      ele = etree.SubElement(data, unicode(key))
      ele.text = unicode(d[key])

  # Return xml as string.
  io = StringIO.StringIO()
  io.write(
    escape(
      etree.tostring(
        xml, pretty_print=pretty,
        encoding='UTF-8', xml_declaration=True
      )
    )
  )
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
#        <d1:hash>_SHA1 hash of object</d1:hash>
#        <d1:modified>_date time last modified_</d1:modified>
#        <d1:size>_byte size of object_</d1:size>
#      </rdf:Description>
#    </d1:data>
#  </rdf:Description>
#</rdf:RDF>
def to_rdf_xml(obj, pretty):
  """Serialize object to RDF XML.
  """

  # Set up namespaces for the XML response.
  RDF_NS = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
  D1_NS = 'http://ns.dataone.org/core/objects'
  RDF = '{%s}' % RDF_NS
  D1 = '{%s}' % D1_NS
  NSMAP = {'rdf': RDF_NS, 'd1': D1_NS}
  xml = etree.Element(RDF + 'rdf', nsmap=NSMAP)

  description = etree.SubElement(xml, RDF + 'Description')
  description.set(RDF + 'about', '_requesting URL_')

  start = etree.SubElement(description, D1 + 'start')
  start.text = unicode(obj['start'])

  start = etree.SubElement(description, D1 + 'count')
  start.text = unicode(obj['count'])

  start = etree.SubElement(description, D1 + 'total')
  start.text = unicode(obj['total'])

  description = etree.SubElement(xml, RDF + 'Description')
  description.set(RDF + 'about', 'http://mn1.dataone.org/object/_identifier_')

  for d in obj['data']:
    data = etree.SubElement(description, D1 + 'data')

    for key in sorted(d.keys()):
      ele = etree.SubElement(data, unicode(D1 + key))
      ele.text = unicode(d[key])

  # Return xml as string.
  io = StringIO.StringIO()
  io.write(
    escape(
      etree.tostring(
        xml, pretty_print=pretty,
        encoding='UTF-8', xml_declaration=True
      )
    )
  )
  return io.getvalue()
