#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`response_handler`
=========================

:platform: Linux
:Synopsis:
  Serialize DataONE response objects according to Accept header and set header
  (Size and Content-Type) accordingly.

.. moduleauthor:: Roger Dahl
"""

# Stdlib.
import csv
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
  import mimeparser
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('mimeparser.py is included in mn_service\n')
  raise

# Django.
#from django.utils.html import escape
#from django.conf import settings
#from django.shortcuts import render_to_response
#from django.template import Context
#from django.template import RequestContext

from django.http import HttpResponse

# MN API.
import d1common.exceptions

# App.
import mn_service.models as models
import mn_service.sys_log as sys_log
import mn_service.util as util
import settings


#{
#  'start': <integer>,
#  'count': <integer>,
#  'total': <integer>,
#  'data':
#  [
#    {
#      'guid':<identifier>,
#      'oclass':<object class>,
#      'checksum':<SHA1 checksum of object>,
#      'modified':<date time last modified>,
#      'size':<byte size of object>
#    },
#    ...
#  ]
#}
def serialize_json(obj, pretty=False, jsonvar=False):
  """
  Serialize object to JSON.
  """

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
# 'guid',otype,checksum,modified,size
# <identifier>,<object class>,<SHA1 checksum of object>,<date time last modified>,<byte size of object>
def serialize_csv(obj, pretty=False, jsonvar=False):
  """
  Serialize object to CSV.
  """

  io = StringIO.StringIO()
  # Comment containing start, count and object.
  try:
    io.write('#{0},{1},{2}\n'.format(obj['start'], obj['count'], obj['total']))
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
#    <checksum>_SHA1 checksum of object</checksum>
#    <modified>_date time last modified_</modified>
#    <size>_byte size of object_</size>
#  </data>
#  ...
#</response>
def serialize_xml(obj, pretty=False, jsonvar=False):
  """
  Serialize object to XML.
  """

  # Set up namespace for the xml response.
  RESPONSE_NS = 'http://ns.dataone.org/core/objects'
  RESPONSE = '{{{0}}}'.format(RESPONSE_NS)
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
    urllib.quote(
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
#        <d1:checksum>_SHA1 checksum of object</d1:checksum>
#        <d1:modified>_date time last modified_</d1:modified>
#        <d1:size>_byte size of object_</d1:size>
#      </rdf:Description>
#    </d1:data>
#  </rdf:Description>
#</rdf:RDF>
def serialize_rdf_xml(obj, pretty=False, jsonvar=False):
  """
  Serialize object to RDF XML.
  """

  # Set up namespaces for the XML response.
  RDF_NS = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
  D1_NS = 'http://ns.dataone.org/core/objects'
  RDF = '{{{0}}}'.format(RDF_NS)
  D1 = '{{{0}}}'.format(D1_NS)
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
    urllib.quote(
      etree.tostring(
        xml, pretty_print=pretty,
        encoding='UTF-8', xml_declaration=True
      )
    )
  )
  return io.getvalue()


def serialize_null(obj, pretty=False, jsonvar=False):
  """
  For now, this NULL serializer just calls out to the json serializer.
  """
  return serialize_json(obj, pretty, jsonvar)


def serialize_object(request, response, obj):
  map = {
    'application/json': serialize_json,
    'text/csv': serialize_csv,
    'text/xml': serialize_xml,
    'application/rdf+xml': serialize_rdf_xml,
    'text/html': serialize_null, #TODO: Not in current REST spec.
    'text/log': serialize_null, #TODO: Not in current REST spec.
  }

  pri = [
    'application/json',
    'text/csv',
    'text/xml',
    'application/rdf+xml',
    'text/html',
    'text/log',
  ]

  # The "pretty" parameter generates pretty response.
  pretty = 'pretty' in request.GET

  # For JSON, we support giving a variable name.
  if 'jsonvar' in request.GET:
    jsonvar = request.GET['jsonvar']
  else:
    jsonvar = False

  # Determine which serializer to use.

  # If no client does not supply HTTP_ACCEPT, we default to JSON.
  if 'HTTP_ACCEPT' not in request.META:
    sys_log.debug('No HTTP_ACCEPT header')
    obj_ser = serialize_json(obj, pretty, jsonvar)
  else:
    sys_log.debug(request.META['HTTP_ACCEPT'])
    content_type = mimeparser.best_match(pri, request.META['HTTP_ACCEPT'])
    obj_ser = map[content_type](obj, pretty, jsonvar)

    # If pretty formatting was used, we wrap the serialized object for web page
    # presentation (good for debugging).
  if pretty:
    obj_ser = '<pre>' + obj_ser + '</pre>'

  # Add the serialized object to the response.
  response.write(obj_ser)

  # Set headers.
  set_header(response, None, len(obj_ser), content_type)

  return response


def set_header(response, last_modified, content_length, content_type):
  """
  Add Last-Modified, Content-Length and Content-Type headers to response.

  If last_modified is None, we pull the date from the one stored in the db.
  """
  if last_modified is None:
    try:
      status_row = models.DB_update_status.objects.all()[0]
    except IndexError:
      raise d1common.exceptions.ServiceFailure(0, 'DB update status has not been set')
    else:
      last_modified = status_row.mtime

  response['Last-Modified'] = wsgiref.handlers.format_date_time(
    time.mktime(
      last_modified.timetuple(
      )
    )
  )
  response['Content-Length'] = content_length
  response['Content-Type'] = content_type


class response_handler():
  def process_response(self, request, response):

    # If there was no res object in the response, we return the response
    # unprocessed.
    try:
      obj = response.obj
      print obj
    except AttributeError:
      pass
    else:
      serialize_object(request, response, obj)

    return response
