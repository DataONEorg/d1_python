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
Module d1_common.types.serialization
====================================
'''

# Stdlib.
import StringIO
import csv
import logging
import sys

try:
  import cjson as json
except:
  import json

# MN API.
try:
  import d1_common
  import d1_common.types.exceptions
  import d1_common.ext.mimeparser
  import d1_common.util
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

#===============================================================================


class Serialization(object):
  '''Implements the base for DataONE serialization classes.
  '''

  def __init__(self):
    self.log = logging.getLogger('Serialization')

    self.serialize_map = {
      d1_common.const.MIMETYPE_XML: self.serialize_xml,
      d1_common.const.MIMETYPE_APP_XML: self.serialize_xml,
      d1_common.const.MIMETYPE_JSON: self.serialize_json,
      d1_common.const.MIMETYPE_CSV: self.serialize_csv,
      d1_common.const.MIMETYPE_RDF: self.serialize_rdf,
      d1_common.const.MIMETYPE_HTML: self.serialize_html,
      d1_common.const.MIMETYPE_LOG: self.serialize_log,
      d1_common.const.MIMETYPE_TEXT: self.serialize_text,
    }

    self.deserialize_map = {
      d1_common.const.MIMETYPE_XML: self.deserialize_xml,
      d1_common.const.MIMETYPE_APP_XML: self.deserialize_xml,
      d1_common.const.MIMETYPE_JSON: self.deserialize_json,
      d1_common.const.MIMETYPE_CSV: self.deserialize_csv,
      d1_common.const.MIMETYPE_RDF: self.deserialize_rdf,
      d1_common.const.MIMETYPE_HTML: self.deserialize_html,
      d1_common.const.MIMETYPE_LOG: self.deserialize_log,
      d1_common.const.MIMETYPE_TEXT: self.deserialize_text,
    }

  def serialize(
    self, accept=d1_common.const.DEFAULT_MIMETYPE,
    pretty=False,
    jsonvar=False
  ):
    # Determine which serializer to use. If client does not supply accept, or
    # accept is None, we default to text/xml.
    if accept is None:
      accept = d1_common.const.DEFAULT_MIMETYPE
    try:
      # An invalid Accept header causes mimeparser to throw a ValueError
      # or to return an empty content_type.
      content_type = d1_common.ext.mimeparser.best_match(self.pri, accept)
      if content_type == '':
        raise ValueError
    except ValueError:
      self.log.debug(
        'Invalid HTTP_ACCEPT value. Defaulting to "{0}"'.format(
          d1_common.const.DEFAULT_MIMETYPE
        )
      )
      content_type = d1_common.const.DEFAULT_MIMETYPE
    self.log.debug("serializing, content-type=%s" % content_type)
    return self.serialize_map[d1_common.util.get_content_type(content_type)](
      pretty, jsonvar
    ), content_type

  def serialize_xml(self, pretty=False, jsonvar=False):
    raise d1_common.types.exceptions.NotImplemented(
      0, 'Serialization method not implemented.'
    )

  def serialize_json(self, pretty=False, jsonvar=False):
    raise d1_common.types.exceptions.NotImplemented(
      0, 'Serialization method not implemented.'
    )

  def serialize_csv(self, pretty=False, jsonvar=False):
    raise d1_common.types.exceptions.NotImplemented(
      0, 'Serialization method not implemented.'
    )

  def serialize_rdf(self, pretty=False, jsonvar=False):
    raise d1_common.types.exceptions.NotImplemented(
      0, 'Serialization method not implemented.'
    )

  def serialize_html(self, pretty=False, jsonvar=False):
    raise d1_common.types.exceptions.NotImplemented(
      0, 'Serialization method not implemented.'
    )

  def serialize_log(self, pretty=False, jsonvar=False):
    raise d1_common.types.exceptions.NotImplemented(
      0, 'Serialization method not implemented.'
    )

  def serialize_text(self, pretty=False, jsonvar=False):
    raise d1_common.types.exceptions.NotImplemented(
      0, 'Serialization method not implemented.'
    )

  #== Deserialization =========================================================

  def deserialize(self, doc, content_type=d1_common.const.DEFAULT_MIMETYPE):
    self.log.debug("de-serialize, content-type=%s" % content_type)
    return self.deserialize_map[d1_common.util.get_content_type(content_type)](doc)

  def deserialize_xml(self, pretty=False, jsonvar=False):
    raise d1_common.types.exceptions.NotImplemented(
      0, 'Serialization method not implemented.'
    )

  def deserialize_json(self, pretty=False, jsonvar=False):
    raise d1_common.types.exceptions.NotImplemented(
      0, 'Serialization method not implemented.'
    )

  def deserialize_csv(self, pretty=False, jsonvar=False):
    raise d1_common.types.exceptions.NotImplemented(
      0, 'Serialization method not implemented.'
    )

  def deserialize_rdf(self, pretty=False, jsonvar=False):
    raise d1_common.types.exceptions.NotImplemented(
      0, 'Serialization method not implemented.'
    )

  def deserialize_html(self, pretty=False, jsonvar=False):
    raise d1_common.types.exceptions.NotImplemented(
      0, 'Serialization method not implemented.'
    )

  def deserialize_log(self, pretty=False, jsonvar=False):
    raise d1_common.types.exceptions.NotImplemented(
      0, 'Serialization method not implemented.'
    )

  def deserialize_text(self, pretty=False, jsonvar=False):
    raise d1_common.types.exceptions.NotImplemented(
      0, 'Serialization method not implemented.'
    )
