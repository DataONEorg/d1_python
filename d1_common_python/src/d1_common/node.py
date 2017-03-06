# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Utilities for handling the DataONE Node and NodeList types
"""


def pyxb_to_dict(node_list_pyxb):
  """Return a dict representation of {node_list_pyxb}, keyed on
  the Node identifier (urn:node:*). E.g.:
  {
    u'urn:node:ARCTIC': {
      'base_url': u'https://arcticdata.io/metacat/d1/mn',
      'description': u'The US National Science Foundation...',
      'name': u'Arctic Data Center',
      'ping': None,
      'replicate': 0,
      'state': u'up',
      'synchronize': 1,
      'type': u'mn'
    },
    u'urn:node:BCODMO': {
      'base_url': u'https://www.bco-dmo.org/d1/mn',
      'description': u'Biological and Chemical Oceanography Data...',
      'name': u'Biological and Chemical Oceanography Data...',
      'ping': None,
      'replicate': 0,
      'state': u'up',
      'synchronize': 1,
      'type': u'mn'
    },
  }
  """
  f_dict = {}
  for f_pyxb in sorted(node_list_pyxb.node, key=lambda x: x.identifier.value()):
    f_dict[f_pyxb.identifier.value()] = {
      'name': f_pyxb.name,
      'description': f_pyxb.description,
      'base_url': f_pyxb.baseURL,
      'ping': f_pyxb.ping,
      'replicate': f_pyxb.replicate,
      'synchronize': f_pyxb.synchronize,
      'type': f_pyxb.type,
      'state': f_pyxb.state,
    }
    # TODO:
    # f_pyxb.services
    # f_pyxb.synchronization
    # f_pyxb.subject
    # f_pyxb.contactSubject
    # f_pyxb.nodeReplicationPolicy,

  return f_dict
