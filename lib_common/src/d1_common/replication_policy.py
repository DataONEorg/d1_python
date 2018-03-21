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
"""Utilities for handling the DataONE NodeReplicationPolicy type

Example rp_pyxb:

<replicationPolicy replicationAllowed="true" numberReplicas="3">
  <!--Zero or more repetitions:-->
  <preferredMemberNode>node1</preferredMemberNode>
  <preferredMemberNode>node2</preferredMemberNode>
  <preferredMemberNode>node3</preferredMemberNode>
  <!--Zero or more repetitions:-->
  <blockedMemberNode>node4</blockedMemberNode>
  <blockedMemberNode>node5</blockedMemberNode>
</replicationPolicy>

Example rp_dict:

{
  'allowed': True,
  'num': 3,
  'blockedMemberNode': {'urn:node:NODE1', 'urn:node:NODE2', 'urn:node:NODE3'},
  'preferredMemberNode': {'urn:node:NODE4', 'urn:node:NODE5'},
}

"""

import d1_common.types.dataoneTypes
import d1_common.xml

# Via SysMeta


def has_replication_policy(sysmeta_pyxb):
  return bool(getattr(sysmeta_pyxb, 'replicationPolicy', False))


def sysmeta_add_preferred(sysmeta_pyxb, node_urn):
  """Add to preferred if not already there. Remove from blocked if there
  """
  if not has_replication_policy(sysmeta_pyxb):
    sysmeta_set_default_rp(sysmeta_pyxb)
  rp_pyxb = sysmeta_pyxb.replicationPolicy
  add_node(rp_pyxb, 'pref', node_urn)
  del_node(rp_pyxb, 'block', node_urn)


def sysmeta_add_blocked(sysmeta_pyxb, node_urn):
  """Add to blocked if not already there. Remove from preferred if there
  """
  if not has_replication_policy(sysmeta_pyxb):
    sysmeta_set_default_rp(sysmeta_pyxb)
  rp_pyxb = sysmeta_pyxb.replicationPolicy
  add_node(rp_pyxb, 'block', node_urn)
  del_node(rp_pyxb, 'pref', node_urn)


def sysmeta_set_default_rp(sysmeta_pyxb):
  """Set a default, empty, replicationPolicy. Overwrite any existing rp."""
  sysmeta_pyxb.replicationPolicy = dict_to_pyxb({
    'allowed': False,
    'num': 0,
    'block': set(),
    'pref': set()
  })


# Direct ReplicationPolicy


def normalize(rp_pyxb):
  """Normalize a ReplicationPolicy PyXB type in place

  Blocked overrides preferred, so if a {node_urn} is in both, it is removed
  from preferred.
  """

  def sort(r, a):
    d1_common.xml.sort_value_list_pyxb(get(r, a))

  rp_pyxb.preferredMemberNode = (
    set(get(rp_pyxb, 'pref')) - set(get(rp_pyxb, 'block'))
  )
  sort(rp_pyxb, 'block')
  sort(rp_pyxb, 'pref')


def is_preferred(rp_pyxb, node_urn):
  """Return True if {node_urn} is a preferred replica target

  Blocked overrides preferred, so if a {node_urn} is in both, return False.
  """
  return (
    node_urn in get(rp_pyxb, 'pref') and node_urn not in get(rp_pyxb, 'block')
  )


def is_blocked(rp_pyxb, node_urn):
  """Return True if {node_urn} is a blocked replica target

  Blocked overrides preferred, so if a {node_urn} is in both, return False.
  """
  return node_urn in get(rp_pyxb, 'block')


def are_equivalent_pyxb(a_pyxb, b_pyxb):
  return pyxb_to_dict(a_pyxb) == pyxb_to_dict(b_pyxb)


def are_equivalent_xml(a_xml, b_xml):
  return are_equivalent_pyxb(
    d1_common.xml.deserialize(a_xml),
    d1_common.xml.deserialize(b_xml),
  )


def add_preferred(rp_pyxb, node_urn):
  """Add to preferred if not already there. Remove from blocked if there
  """
  add_node(rp_pyxb, 'pref', node_urn)
  del_node(rp_pyxb, 'block', node_urn)


def add_blocked(rp_pyxb, node_urn):
  """Add to blocked if not already there. Remove from preferred if there
  """
  add_node(rp_pyxb, 'block', node_urn)
  del_node(rp_pyxb, 'pref', node_urn)


def add_node(rp_pyxb, attr, node_url):
  setattr(rp_pyxb, exp(attr), get_vals(rp_pyxb, attr) | {node_url})
  ensure_allow_rp(rp_pyxb)
  normalize(rp_pyxb)


def del_blocked(rp_pyxb, node_url):
  del_node(rp_pyxb, 'block', node_url)


def del_preferred(rp_pyxb, node_url):
  del_node(rp_pyxb, 'pref', node_url)


def del_node(rp_pyxb, attr, node_url):
  setattr(rp_pyxb, exp(attr), get_vals(rp_pyxb, attr) - {node_url})
  normalize(rp_pyxb)


def pyxb_to_dict(rp_pyxb):
  """Returns dict representation of ReplicationPolicy PyXB.
  """
  return {
    'allowed': bool(get(rp_pyxb, 'allowed')),
    'num': get_n_rep(rp_pyxb),
    'block': get_vals(rp_pyxb, 'block'),
    'pref': get_vals(rp_pyxb, 'pref'),
  }


def dict_to_pyxb(rp_dict):
  rp_pyxb = d1_common.types.dataoneTypes.replicationPolicy()
  rp_pyxb.replicationAllowed = rp_dict['allowed']
  rp_pyxb.numberReplicas = rp_dict['num']
  rp_pyxb.blockedMemberNode = rp_dict['block']
  rp_pyxb.preferredMemberNode = rp_dict['pref']
  normalize(rp_pyxb)
  return rp_pyxb


def ensure_allow_rp(rp_pyxb):
  """Ensure that RP allows replication"""
  if not rp_pyxb.replicationAllowed:
    rp_pyxb.replicationAllowed = True
  if not rp_pyxb.numberReplicas:
    rp_pyxb.numberReplicas = 3


def get(rp_pyxb, attr):
  return getattr(rp_pyxb, exp(attr), [])


def get_vals(rp_pyxb, attr):
  return {x.value() for x in getattr(rp_pyxb, exp(attr), [])}


def get_n_rep(rp_pyxb):
  return int(getattr(rp_pyxb, exp('num'), 0))


def exp(attr):
  return {
    'block': 'blockedMemberNode',
    'pref': 'preferredMemberNode',
    'allowed': 'replicationAllowed',
    'num': 'numberReplicas',
  }[attr]
