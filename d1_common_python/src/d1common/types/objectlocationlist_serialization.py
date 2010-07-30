'''
Module d1common.types.objectlocationlist_serialization
==============================================

Implements serializaton and de-serialization for the ObjectLocationList.
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
import d1common
import d1common.exceptions
import d1common.ext.mimeparser

try:
  import d1common.types.generated.objectlocationlist
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo easy_install pyxb\n')
  raise

#===============================================================================


class ObjectLocationList(object):
  def __init__(self):
    self.log = logging.getLogger('ObjectLocationList')
    self.serialize_map = {
      'application/json': self.serialize_null, #TODO: Not in current REST spec.
      'text/csv': self.serialize_null, #TODO: Not in current REST spec.
      'text/xml': self.serialize_xml,
      'application/xml': self.serialize_xml,
      'application/rdf+xml': self.serialize_null, #TODO: Not in current REST spec.
      'text/html': self.serialize_null, #TODO: Not in current REST spec.
      'text/log': self.serialize_null, #TODO: Not in current REST spec.
    }

    self.deserialize_map = {
      'application/json': self.deserialize_null, #TODO: Not in current REST spec.
      'text/csv': self.deserialize_null, #TODO: Not in current REST spec.
      'text/xml': self.deserialize_xml,
      'application/xml': self.deserialize_xml,
      'application/rdf+xml': self.deserialize_null, #TODO: Not in current REST spec.
      'text/html': self.deserialize_null, #TODO: Not in current REST spec.
      'text/log': self.deserialize_null, #TODO: Not in current REST spec.
    }

    self.pri = [
      #'application/json',
      #'text/csv',
      'text/xml',
      'application/xml',
      #'application/rdf+xml',
      #'text/html',
      #'text/log',
    ]

    self.object_location_list = d1common.types.generated.objectlocationlist.objectLocationList(
    )

  def serialize(self, accept='text/xml', pretty=False, jsonvar=False):
    # Determine which serializer to use. If client does not supply accept, we
    # default to JSON.
    try:
      content_type = d1common.ext.mimeparser.best_match(self.pri, accept)
    except ValueError:
      content_type = 'text/xml'
    self.log.debug("serializing, content-type=%s" % content_type)

    # Deserialize object
    return self.serialize_map[content_type](pretty, jsonvar), content_type

  def serialize_xml(self, pretty=False, jsonvar=False):
    self.log.debug("serialize_xml")
    return self.object_location_list.toxml()

  def serialize_null(self, doc, pretty=False, jsonvar=False):
    raise d1common.exceptions.NotImplemented(0, 'Serialization method not implemented.')

    #===============================================================================

  def deserialize(self, doc, content_type='text/xml'):
    self.log.debug("de-serialize, content-type=%s" % content_type)
    return self.deserialize_map[content_type](doc)

  def deserialize_xml(self, doc):
    self.log.debug('deserialize xml')
    self.object_location_list = d1common.types.generated.objectlocationlist.CreateFromDocument(
      doc
    )
    return self.object_location_list

  def deserialize_null(self, doc):
    self.log.debug('deserialize NULL')
    raise d1common.exceptions.NotImplemented(
      0, 'De-serialization method not implemented.'
    )
