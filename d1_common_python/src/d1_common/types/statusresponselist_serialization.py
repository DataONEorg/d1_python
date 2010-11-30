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
Module d1_common.types.statusresponselist_serialization
======================================================

Implements serializaton and de-serialization for the StatusResponseList.
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


class StatusResponseList(object):
  def __init__(self):
    self.log = logging.getLogger('StatusResponseList')
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

    self.object_location_list = d1_common.types.generated.dataoneTypes.statusResponseList(
    )

  def serialize(self, accept='text/xml', pretty=False, jsonvar=False):
    # Determine which serializer to use. If client does not supply accept, we
    # default to JSON.
    try:
      content_type = d1_common.ext.mimeparser.best_match(self.pri, accept)
    except ValueError:
      content_type = 'text/xml'
    self.log.debug("serializing, content-type=%s" % content_type)

    # Deserialize object
    return self.serialize_map[d1_common.util.get_content_type(content_type)](
      pretty, jsonvar
    ), content_type

  def serialize_xml(self, pretty=False, jsonvar=False):
    self.log.debug("serialize_xml")
    return self.object_location_list.toxml()

  def serialize_null(self, doc, pretty=False, jsonvar=False):
    raise d1_common.exceptions.NotImplemented(0, 'Serialization method not implemented.')

    #===============================================================================

  def deserialize(self, doc, content_type='text/xml'):
    self.log.debug("de-serialize, content-type=%s" % content_type)
    return self.deserialize_map[d1_common.util.get_content_type(content_type)](doc)

  def deserialize_xml(self, doc):
    self.log.debug('deserialize xml')
    self.object_location_list = d1_common.types.generated.dataoneTypes.CreateFromDocument(
      doc
    )
    return self.object_location_list

  def deserialize_null(self, doc):
    self.log.debug('deserialize NULL')
    raise d1_common.exceptions.NotImplemented(
      0, 'De-serialization method not implemented.'
    )
