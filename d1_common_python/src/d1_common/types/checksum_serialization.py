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
Module d1_common.types.checksum_serialization
=============================================

Implements serializaton and de-serialization for the the checksum type.
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


class Checksum(object):
  '''Implements serialization of DataONE Checksum
  '''

  def __init__(self, checksum):
    self.serialize_map = {
      'application/json': self.serialize_json,
      'text/csv': self.serialize_csv,
      'text/xml': self.serialize_xml,
      'application/xml': self.serialize_xml,
      'application/rdf+xml': self.serialize_null, #TODO: Not in current REST spec.
      'text/html': self.serialize_null, #TODO: Not in current REST spec.
      'text/log': self.serialize_null, #TODO: Not in current REST spec.
    }

    self.deserialize_map = {
      'application/json': self.deserialize_json,
      'text/csv': self.deserialize_csv,
      'text/xml': self.deserialize_xml,
      'application/xml': self.deserialize_xml,
      'application/rdf+xml': self.deserialize_null, #TODO: Not in current REST spec.
      'text/html': self.deserialize_null, #TODO: Not in current REST spec.
      'text/log': self.deserialize_null, #TODO: Not in current REST spec.
    }

    self.pri = [
      'application/json',
      'text/csv',
      'text/xml',
      'application/xml',
      #'application/rdf+xml',
      #'text/html',
      #'text/log',
    ]

    self.checksum = d1_common.types.generated.dataoneTypes.checksum(checksum)

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
    '''Serialize Checksum to XML.
    '''
    return self.checksum.toxml()

  def serialize_json(self, pretty=False, jsonvar=False):
    '''Serialize Checksum to JSON.
    '''
    return json.dumps({'checksum': self.checksum.value(), 'algorithm': self.checksum.algorithm})

  def serialize_csv(self, pretty=False, jsonvar=False):
    '''Serialize Checksum to CSV.
    '''
    io = StringIO.StringIO()
    csv_writer = csv.writer(
      io, dialect=csv.excel,
      quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    csv_writer.writerow([self.checksum.value(), self.checksum.algorithm])
    return io.getvalue()

  def serialize_null(self, doc, pretty=False, jsonvar=False):
    raise d1_common.exceptions.NotImplemented(0, 'Serialization method not implemented.')

    #== Deserialization methods ==================================================

  def deserialize(self, doc, content_type='application/json'):
    return self.deserialize_map[d1_common.util.get_content_type(content_type)](doc)

  def deserialize_xml(self, doc):
    self.checksum = d1_common.types.generated.dataoneTypes.CreateFromDocument(doc)
    return self.checksum

  def deserialize_json(self, doc):
    j = json.loads(doc)

    self.checksum = d1_common.types.generated.dataoneTypes.checksum(j['checksum'])
    self.checksum.algorithm = j['algorithm']

    return self.checksum

  def deserialize_csv(self, doc):
    io = StringIO.StringIO(doc)
    csv_reader = csv.reader(
      io, dialect=csv.excel,
      quotechar='"', quoting=csv.QUOTE_MINIMAL
    )

    for csv_line in csv_reader:
      self.checksum = d1_common.types.generated.dataoneTypes.checksum(csv_line[0])
      self.checksum.algorithm = csv_line[1]
      break

    return self.checksum

  def deserialize_null(self, doc):
    raise d1_common.exceptions.NotImplemented(
      0, 'Deserialization method not implemented.'
    )
