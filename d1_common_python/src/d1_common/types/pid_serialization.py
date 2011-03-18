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
Module d1_common.types.pid_serialization
========================================

Serializaton and deserialization of the DataONE PID type.

:Created: 2010-12-02
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
  import d1_common
  import d1_common.types.exceptions
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
import serialization_base


class Identifier(serialization_base.Serialization):
  '''Implements serialization of DataONE Identifier
  '''

  def __init__(self, pid='<dummy>'):
    '''Serializaton and deserialization of the DataONE PID type.
    '''
    serialization_base.Serialization.__init__(self)

    self.log = logging.getLogger('PIDSerialization')

    self.pri = [
      d1_common.const.MIMETYPE_XML,
      d1_common.const.MIMETYPE_APP_XML,
      d1_common.const.MIMETYPE_JSON,
      d1_common.const.MIMETYPE_CSV,
      d1_common.const.MIMETYPE_RDF,
      #d1_common.const.MIMETYPE_HTML,
      #d1_common.const.MIMETYPE_LOG,
    ]

    self.pid = d1_common.types.generated.dataoneTypes.identifier(pid)

  def serialize_xml(self, pretty=False, jsonvar=False):
    '''Serialize Identifier to XML.
    '''
    return self.pid.toxml()

  def serialize_json(self, pretty=False, jsonvar=False):
    '''Serialize Identifier to JSON.
    '''
    return json.dumps({'pid': self.pid.value()})

  def serialize_csv(self, pretty=False, jsonvar=False):
    '''Serialize Identifier to CSV.
    '''
    io = StringIO.StringIO()
    csv_writer = csv.writer(
      io, dialect=csv.excel,
      quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    csv_writer.writerow([self.pid.value()])
    return io.getvalue()

  #============================================================================

  def deserialize_xml(self, doc):
    '''Deserialize Identifier from XML.
    '''
    self.pid = d1_common.types.generated.dataoneTypes.CreateFromDocument(doc)
    return self.pid

  def deserialize_json(self, doc):
    '''Deserialize Identifier from JSON.
    '''
    j = json.loads(doc)
    self.pid = d1_common.types.generated.dataoneTypes.Identifier(j['pid'])
    return self.pid

  def deserialize_csv(self, doc):
    '''Deserialize Identifier from CSV.
    '''
    io = StringIO.StringIO(doc)
    csv_reader = csv.reader(
      io, dialect=csv.excel,
      quotechar='"', quoting=csv.QUOTE_MINIMAL
    )

    for csv_line in csv_reader:
      self.pid = d1_common.types.generated.dataoneTypes.Identifier(csv_line[0])
      break

    return self.pid
