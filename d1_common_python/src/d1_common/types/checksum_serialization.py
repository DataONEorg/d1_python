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

Serializaton and deserialization of the DataONE Checksum type.

:Created: 2010-12-22
:Author: DataONE (dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import StringIO
import csv
import logging
import sys
import json

# App.
try:
  import d1_common.types.generated.dataoneTypes
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo easy_install pyxb\n')
  raise
import serialization_base


class Checksum(serialization_base.Serialization):
  '''Serializaton and deserialization of the DataONE Checksum type.
  '''

  def __init__(self, checksum):
    serialization_base.Serialization.__init__(self)

    self.log = logging.getLogger('ChecksumSerialization')

    self.pri = [
      d1_common.const.MIMETYPE_XML,
      d1_common.const.MIMETYPE_APP_XML,
      d1_common.const.MIMETYPE_JSON,
      d1_common.const.MIMETYPE_CSV,
      #d1_common.const.MIMETYPE_RDF,
      #d1_common.const.MIMETYPE_HTML,
      #d1_common.const.MIMETYPE_LOG,
    ]

    self.checksum = d1_common.types.generated.dataoneTypes.checksum(checksum)

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

    #============================================================================

  def deserialize_xml(self, doc):
    self.checksum = d1_common.types.generated.dataoneTypes.CreateFromDocument(doc)
    return self.checksum

  def deserialize_json(self, doc):
    '''Deserialize Checksum from JSON.
    '''
    j = json.loads(doc)

    self.checksum = d1_common.types.generated.dataoneTypes.checksum(j['checksum'])
    self.checksum.algorithm = j['algorithm']

    return self.checksum

  def deserialize_csv(self, doc):
    '''Deserialize Checksum from CSV.
    '''
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
