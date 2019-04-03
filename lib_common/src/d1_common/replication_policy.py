# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
"""Utilities for handling the DataONE ReplicationPolicy type.

The Replication Policy is an optional section of the System Metadata which may be used
to enable or disable replication, set the desired number of replicas and specify remote
MNs to either prefer or block as replication targets.

Examples::

  ReplicationPolicy:

  <replicationPolicy replicationAllowed="true" numberReplicas="3">
    <!--Zero or more repetitions:-->
    <preferredMemberNode>node1</preferredMemberNode>
    <preferredMemberNode>node2</preferredMemberNode>
    <preferredMemberNode>node3</preferredMemberNode>
    <!--Zero or more repetitions:-->
    <blockedMemberNode>node4</blockedMemberNode>
    <blockedMemberNode>node5</blockedMemberNode>
  </replicationPolicy>

"""

import d1_common.types.dataoneTypes
import d1_common.xml


def has_replication_policy(sysmeta_pyxb):
    """Args: sysmeta_pyxb: SystemMetadata PyXB object.

    Returns:   bool: ``True`` if SystemMetadata includes the optional ReplicationPolicy
    section.

    """
    return bool(getattr(sysmeta_pyxb, 'replicationPolicy', False))


def sysmeta_add_preferred(sysmeta_pyxb, node_urn):
    """Add a remote Member Node to the list of preferred replication targets to this
    System Metadata object.

    Also remove the target MN from the list of blocked Member Nodes if present.

    If the target MN is already in the preferred list and not in the blocked list, this
    function is a no-op.

    Args:
      sysmeta_pyxb : SystemMetadata PyXB object.
        System Metadata in which to add the preferred replication target.

        If the System Metadata does not already have a Replication Policy, a default
        replication policy which enables replication is added and populated with the
        preferred replication target.

      node_urn : str
        Node URN of the remote MN that will be added. On the form
       ``urn:node:MyMemberNode``.

    """
    if not has_replication_policy(sysmeta_pyxb):
        sysmeta_set_default_rp(sysmeta_pyxb)
    rp_pyxb = sysmeta_pyxb.replicationPolicy
    _add_node(rp_pyxb, 'pref', node_urn)
    _remove_node(rp_pyxb, 'block', node_urn)


def sysmeta_add_blocked(sysmeta_pyxb, node_urn):
    """Add a remote Member Node to the list of blocked replication targets to this
    System Metadata object.

    The blocked node will not be considered a possible replication target for the
    associated System Metadata.

    Also remove the target MN from the list of preferred Member Nodes if present.

    If the target MN is already in the blocked list and not in the preferred list, this
    function is a no-op.

    Args:
      sysmeta_pyxb : SystemMetadata PyXB object.
        System Metadata in which to add the blocked replication target.

        If the System Metadata does not already have a Replication Policy, a default
        replication policy which enables replication is added and then populated with
        the blocked replication target.

      node_urn : str
        Node URN of the remote MN that will be added. On the form
        ``urn:node:MyMemberNode``.

    """
    if not has_replication_policy(sysmeta_pyxb):
        sysmeta_set_default_rp(sysmeta_pyxb)
    rp_pyxb = sysmeta_pyxb.replicationPolicy
    _add_node(rp_pyxb, 'block', node_urn)
    _remove_node(rp_pyxb, 'pref', node_urn)


def sysmeta_set_default_rp(sysmeta_pyxb):
    """Set a default, empty, Replication Policy.

    This will clear any existing Replication Policy in the System Metadata.

    The default Replication Policy disables replication and sets number of replicas to
    0.

    Args:
      sysmeta_pyxb : SystemMetadata PyXB object.
        System Metadata in which to set a default Replication Policy.

    """
    sysmeta_pyxb.replicationPolicy = dict_to_pyxb(
        {'allowed': False, 'num': 0, 'block': set(), 'pref': set()}
    )


# Direct ReplicationPolicy


def normalize(rp_pyxb):
    """Normalize a ReplicationPolicy PyXB type in place.

    The preferred and blocked lists are sorted alphabetically. As blocked nodes
    override preferred nodes, and any node present in both lists is removed from the
    preferred list.

    Args:
      rp_pyxb : ReplicationPolicy PyXB object
        The object will be normalized in place.

    """

    # noinspection PyMissingOrEmptyDocstring
    def sort(r, a):
        d1_common.xml.sort_value_list_pyxb(_get_attr_or_list(r, a))

    rp_pyxb.preferredMemberNode = set(_get_attr_or_list(rp_pyxb, 'pref')) - set(
        _get_attr_or_list(rp_pyxb, 'block')
    )
    sort(rp_pyxb, 'block')
    sort(rp_pyxb, 'pref')


def is_preferred(rp_pyxb, node_urn):
    """
  Args:
    rp_pyxb : ReplicationPolicy PyXB object
      The object will be normalized in place.

    node_urn : str
      Node URN of the remote MN for which to check preference.

  Returns:
    bool: ``True`` if ``node_urn`` is a preferred replica target.

    As blocked nodes override preferred nodes, return False if ``node_urn`` is in both
    lists.
  """
    return node_urn in _get_attr_or_list(
        rp_pyxb, 'pref'
    ) and node_urn not in _get_attr_or_list(rp_pyxb, 'block')


def is_blocked(rp_pyxb, node_urn):
    """
  Args:
    rp_pyxb : ReplicationPolicy PyXB object
      The object will be normalized in place.

    node_urn : str
      Node URN of the remote MN for which to check preference.

  Returns:
    bool: ``True`` if ``node_urn`` is a blocked replica target.

    As blocked nodes override preferred nodes, return True if ``node_urn`` is in both
    lists.
  """
    return node_urn in _get_attr_or_list(rp_pyxb, 'block')


def are_equivalent_pyxb(a_pyxb, b_pyxb):
    """Check if two ReplicationPolicy objects are semantically equivalent.

    The ReplicationPolicy objects are normalized before comparison.

    Args:
      a_pyxb, b_pyxb : ReplicationPolicy PyXB objects to compare

    Returns:
      bool: ``True`` if the resulting policies for the two objects are semantically
      equivalent.

    """
    return pyxb_to_dict(a_pyxb) == pyxb_to_dict(b_pyxb)


def are_equivalent_xml(a_xml, b_xml):
    """Check if two ReplicationPolicy XML docs are semantically equivalent.

    The ReplicationPolicy XML docs are normalized before comparison.

    Args:
      a_xml, b_xml: ReplicationPolicy XML docs to compare

    Returns:
      bool: ``True`` if the resulting policies for the two objects are semantically
      equivalent.

    """
    return are_equivalent_pyxb(
        d1_common.xml.deserialize(a_xml), d1_common.xml.deserialize(b_xml)
    )


def add_preferred(rp_pyxb, node_urn):
    """Add a remote Member Node to the list of preferred replication targets.

    Also remove the target MN from the list of blocked Member Nodes if present.

    If the target MN is already in the preferred list and not in the blocked list, this
    function is a no-op.

    Args:
      rp_pyxb: SystemMetadata PyXB object.
        Replication Policy in which to add the preferred replication target.

      node_urn : str
        Node URN of the remote MN that will be added. On the form
        ``urn:node:MyMemberNode``.

    """
    _add_node(rp_pyxb, 'pref', node_urn)
    _remove_node(rp_pyxb, 'block', node_urn)


def add_blocked(rp_pyxb, node_urn):
    """Add a remote Member Node to the list of blocked replication targets.

    Also remove the target MN from the list of preferred Member Nodes if present.

    If the target MN is already in the blocked list and not in the preferred list, this
    function is a no-op.

    Args:
      rp_pyxb: SystemMetadata PyXB object.
        Replication Policy in which to add the blocked replication target.

      node_urn : str
        Node URN of the remote MN that will be added. On the form
        ``urn:node:MyMemberNode``.

    """
    _add_node(rp_pyxb, 'block', node_urn)
    _remove_node(rp_pyxb, 'pref', node_urn)


def pyxb_to_dict(rp_pyxb):
    """Convert ReplicationPolicy PyXB object to a normalized dict.

    Args:
      rp_pyxb: ReplicationPolicy to convert.

    Returns:
        dict : Replication Policy as normalized dict.

    Example::

      {
        'allowed': True,
        'num': 3,
        'blockedMemberNode': {'urn:node:NODE1', 'urn:node:NODE2', 'urn:node:NODE3'},
        'preferredMemberNode': {'urn:node:NODE4', 'urn:node:NODE5'},
      }

    """
    return {
        'allowed': bool(_get_attr_or_list(rp_pyxb, 'allowed')),
        'num': _get_as_int(rp_pyxb),
        'block': _get_as_set(rp_pyxb, 'block'),
        'pref': _get_as_set(rp_pyxb, 'pref'),
    }


def dict_to_pyxb(rp_dict):
    """Convert dict to ReplicationPolicy PyXB object.

    Args:
      rp_dict: Native Python structure representing a Replication Policy.

    Example::

      {
        'allowed': True,
        'num': 3,
        'blockedMemberNode': {'urn:node:NODE1', 'urn:node:NODE2', 'urn:node:NODE3'},
        'preferredMemberNode': {'urn:node:NODE4', 'urn:node:NODE5'},
      }

    Returns:
      ReplicationPolicy PyXB object.

    """
    rp_pyxb = d1_common.types.dataoneTypes.replicationPolicy()
    rp_pyxb.replicationAllowed = rp_dict['allowed']
    rp_pyxb.numberReplicas = rp_dict['num']
    rp_pyxb.blockedMemberNode = rp_dict['block']
    rp_pyxb.preferredMemberNode = rp_dict['pref']
    normalize(rp_pyxb)
    return rp_pyxb


def _add_node(rp_pyxb, attr, node_url):
    setattr(rp_pyxb, _map_dict_key(attr), _get_as_set(rp_pyxb, attr) | {node_url})
    _ensure_allow_rp(rp_pyxb)
    normalize(rp_pyxb)


def _remove_node(rp_pyxb, attr, node_url):
    setattr(rp_pyxb, _map_dict_key(attr), _get_as_set(rp_pyxb, attr) - {node_url})
    normalize(rp_pyxb)


def _ensure_allow_rp(rp_pyxb):
    """Ensure that RP allows replication."""
    if not rp_pyxb.replicationAllowed:
        rp_pyxb.replicationAllowed = True
    if not rp_pyxb.numberReplicas:
        rp_pyxb.numberReplicas = 3


def _get_attr_or_list(rp_pyxb, attr):
    return getattr(rp_pyxb, _map_dict_key(attr), [])


def _get_as_set(rp_pyxb, attr):
    return {x.value() for x in getattr(rp_pyxb, _map_dict_key(attr), [])}


def _get_as_int(rp_pyxb):
    return int(getattr(rp_pyxb, _map_dict_key('num'), 0))


def _map_dict_key(attr):
    return {
        'block': 'blockedMemberNode',
        'pref': 'preferredMemberNode',
        'allowed': 'replicationAllowed',
        'num': 'numberReplicas',
    }[attr]
