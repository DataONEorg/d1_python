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
Module d1_common.types.identifier_serialization
==============================================

Implements serializaton and de-serialization for the the identifier type.
'''

# Stdlib.
import StringIO
import csv
import sys

try:
  import cjson as json
except:
  import json

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


class Identifier(object):
  '''Implements serialization of DataONE Identifier
  '''

  def __init__(self, identifier):
    self.serialize_map = {
      'application/json': self.serialize_json,
      'text/csv': self.serialize_csv,
      'text/xml': self.serialize_xml,
      'application/xml': self.serialize_xml,
      'application/rdf+xml': self.serialize_rdf_xml,
      'text/html': self.serialize_null, #TODO: Not in current REST spec.
      'text/log': self.serialize_null, #TODO: Not in current REST spec.
    }

    self.deserialize_map = {
      'application/json': self.deserialize_json,
      'text/csv': self.deserialize_csv,
      'text/xml': self.deserialize_xml,
      'application/xml': self.deserialize_xml,
      'application/rdf+xml': self.deserialize_rdf_xml,
      'text/html': self.deserialize_null, #TODO: Not in current REST spec.
      'text/log': self.deserialize_null, #TODO: Not in current REST spec.
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

    self.identifier = d1_common.types.generated.dataoneTypes.identifier(identifier)

  def serialize(self, accept='application/json', pretty=False, jsonvar=False):
    '''
    '''
    # Determine which serializer to use. If client does not supply accept, we
    # default to JSON.
    try:
      content_type = d1_common.ext.mimeparser.best_match(self.pri, accept)
    except ValueError:
      # An invalid Accept header causes mimeparser to throw a ValueError.
      #sys_log.debug('Invalid HTTP_ACCEPT value. Defaulting to JSON')
      content_type = 'application/json'
    # Deserialize object
    return self.serialize_map[d1_common.util.get_content_type(content_type)](
      pretty, jsonvar
    ), content_type

  def serialize_xml(self, pretty=False, jsonvar=False):
    '''Serialize Identifier to XML.
    '''
    return self.identifier.toxml()

  def serialize_json(self, pretty=False, jsonvar=False):
    '''Serialize Identifier to JSON.
    '''
    return json.dumps({'identifier': self.identifier.value()})

  def serialize_csv(self, pretty=False, jsonvar=False):
    '''Serialize Identifier to CSV.
    '''
    io = StringIO.StringIO()
    csv_writer = csv.writer(
      io, dialect=csv.excel,
      quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    csv_writer.writerow([self.identifier.value()])
    return io.getvalue()

  def serialize_rdf_xml(self, doc):
    raise d1_common.exceptions.NotImplemented(0, 'serialize_rdf_xml not implemented.')

  def serialize_null(self, doc, pretty=False, jsonvar=False):
    raise d1_common.exceptions.NotImplemented(0, 'Serialization method not implemented.')

    #== Deserialization methods ==================================================

  def deserialize(self, doc, content_type='application/json'):
    return self.deserialize_map[d1_common.util.get_content_type(content_type)](doc)

  def deserialize_xml(self, doc):
    self.identifier = d1_common.types.generated.dataoneTypes.CreateFromDocument(doc)
    return self.identifier

  def deserialize_json(self, doc):
    j = json.loads(doc)
    self.identifier = d1_common.types.generated.dataoneTypes.identifier(j['identifier'])
    return self.identifier

  def deserialize_csv(self, doc):
    io = StringIO.StringIO(doc)
    csv_reader = csv.reader(
      io, dialect=csv.excel,
      quotechar='"', quoting=csv.QUOTE_MINIMAL
    )

    for csv_line in csv_reader:
      self.identifier = d1_common.types.generated.dataoneTypes.identifier(csv_line[0])
      break
    return self.identifier

  def deserialize_rdf_xml(self, doc):
    raise d1_common.exceptions.NotImplemented(0, 'deserialize_rdf_xml not implemented.')

  def deserialize_null(self, doc):
    raise d1_common.exceptions.NotImplemented(
      0, 'Deserialization method not implemented.'
    )
