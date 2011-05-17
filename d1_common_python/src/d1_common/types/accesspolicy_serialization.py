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
Module d1_common.types.accesspolicy_serialization
=================================================

Serializaton and deserialization of the DataONE AccessPolicy type.

:Created: 2011-05-12
:Author: DataONE (dahl)
:Dependencies:
  - python 2.6
'''

## Stdlib.
import logging
import sys
import json

# App.
try:
  import d1_common
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


class AccessPolicy(serialization_base.Serialization):
  def __init__(self):
    '''Serializaton and deserialization of the DataONE AccessPolicy type.
    '''
    serialization_base.Serialization.__init__(self)

    self.log = logging.getLogger('AccessPolicySerialization')

    self.pri = [
      d1_common.const.MIMETYPE_XML,
      d1_common.const.MIMETYPE_APP_XML,
      #d1_common.const.MIMETYPE_JSON,
      #d1_common.const.MIMETYPE_CSV,
      #d1_common.const.MIMETYPE_RDF,
      #d1_common.const.MIMETYPE_HTML,
      #d1_common.const.MIMETYPE_LOG,
    ]

    self.access_policy = d1_common.types.generated.dataoneTypes.accessPolicy()

  def serialize_xml(self, pretty=False, jsonvar=False):
    '''Serialize AccessPolicy to XML.
    '''
    return self.access_policy.toxml()

#===============================================================================

  def deserialize_xml(self, doc):
    '''Deserialize AccessPolicy from XML.
    '''
    self.access_policy = d1_common.types.generated.dataoneTypes.CreateFromDocument(doc)
    return self.access_policy
