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
import sys
import os
import csv
import StringIO
import types
import json

try:
  from functools import update_wrapper
except ImportError:
  from django.utils.functional import update_wrapper

# 3rd party.
# Lxml
try:
  from lxml import etree
except ImportError, e:
  sys_log.error('Import error: %s' % str(e))
  sys_log.error('Try: sudo apt-get install python-lxml')
  sys.exit(1)

import mimeparser

# Django.
from django.utils.html import escape
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import Context
from django.template import RequestContext

# App
import settings
import sys_log
import util


def content_negotiation_required(f):
  """Decorator that parses the Accept header and sets a module variable to
  the appropriate serializer function.
  """

  def wrap(request, *args, **kwargs):
    global serializer
    # If no client does not supply HTTP_ACCEPT, we default to JSON.
    if 'HTTP_ACCEPT' not in request.META:
      serializer = serializer_json
    else:
      serializer = content_types[mimeparser.best_match(
        content_types_pri, request.META['HTTP_ACCEPT']
      )]
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__

  return wrap


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
def serializer_json(obj, pretty=False):
  """Serialize object to JSON.
  """

  if pretty:
    return json.dumps(obj, indent=2)
  else:
    return json.dumps(obj)


# #<start>,<count>,<total>
# 'guid',otype,hash,modified,size
# <identifier>,<object class>,<SHA1 hash of object>,<date time last modified>,<byte size of object>
def serializer_csv(obj, pretty=False):
  """Serialize object to CSV.
  """

  io = StringIO.StringIO()
  # Comment containint start, count and object.
  try:
    io.write('#%d,%d,%d\n' % (obj['start'], obj['count'], obj['total']))
  except KeyError:
    # If start, count or total don't exist, we don't return any of them.
    pass

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
def serializer_xml(obj, pretty=False):
  """Serialize object to XML.
  """

  # Set up namespace for the xml response.
  RESPONSE_NS = 'http://ns.dataone.org/core/objects'
  RESPONSE = '{%s}' % RESPONSE_NS
  NSMAP = {'d1': RESPONSE_NS} # the default namespace
  xml = etree.Element(RESPONSE + 'response', nsmap=NSMAP)

  try:
    start = etree.SubElement(xml, 'start')
    count = etree.SubElement(xml, 'count')
    total = etree.SubElement(xml, 'total')

    start.text = unicode(obj['start'])
    count.text = unicode(obj['count'])
    total.text = unicode(obj['total'])
  except KeyError:
    # If start, count or total don't exist, we don't return any of them.
    pass

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
def serializer_rdf_xml(obj, pretty=False):
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

  try:
    start = etree.SubElement(description, D1 + 'start')
    count = etree.SubElement(description, D1 + 'count')
    total = etree.SubElement(description, D1 + 'total')

    start.text = unicode(obj['start'])
    count.text = unicode(obj['count'])
    total.text = unicode(obj['total'])
  except KeyError:
    # If start, count or total don't exist, we don't return any of them.
    pass

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


content_types = {
  'application/json': serializer_json,
  'text/csv': serializer_csv,
  'text/xml': serializer_xml,
  'application/rdf+xml': serializer_rdf_xml,
}

content_types_pri = ('application/json', 'text/csv', 'text/xml', 'application/rdf+xml', )
