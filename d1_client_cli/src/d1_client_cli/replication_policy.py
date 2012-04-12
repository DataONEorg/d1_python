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
:mod:`replication_policy`
=========================

:Synopsis: Create and manipulate replication policies.
:Created: 2011-11-20
:Author: DataONE (Dahl)
'''

# Stdlib.
import sys

# D1.
try:
  import d1_common.const
  import d1_common.types.generated.dataoneTypes as dataoneTypes
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install DataONE_Common\n')
  raise

# App.
from print_level import * #@UnusedWildImport
import cli_exceptions


class replication_policy():
  def __init__(self):
    self.member_nodes = {}
    self.replication_allowed = True
    self.number_of_replicas = d1_common.const.DEFAULT_NUMBER_OF_REPLICAS

  def __str__(self):
    return self._pretty_format()

  def _list_to_pyxb(self):
    access_policy = dataoneTypes.replicationPolicy()
    for preferred in self.get_preferred():
      node_reference = dataoneTypes.NodeReference(preferred)
      access_policy.preferredMemberNode.append(node_reference)
    for blocked in self.get_blocked():
      node_reference = dataoneTypes.NodeReference(blocked)
      access_policy.blockedMemberNode.append(node_reference)
    access_policy.replicationAllowed = self.get_replication_allowed()
    access_policy.numberReplicas = self.get_number_of_replicas()
    return access_policy

  def _pretty_format(self):
    lines = []
    format_str = '  {0: <30s}{1}'

    preferred_nodes = None
    if self.get_preferred():
      preferred_nodes = '"' + '", "'.join(self.get_preferred()) + '"'
    else:
      preferred_nodes = 'none'
    lines.append(format_str.format('preferred member nodes', preferred_nodes))
    blocked_nodes = None
    if self.get_blocked():
      blocked_nodes = '"' + '", "'.join(self.get_blocked()) + '"'
    else:
      blocked_nodes = 'none'
    lines.append(format_str.format('blocked member nodes', blocked_nodes))

    lines.append(format_str.format('number of replicas', self.number_of_replicas))
    lines.append(format_str.format('replication allowed', self.replication_allowed))
    return 'replication:\n' + '\n'.join(lines)

  def _set_policy(self, mn, preferred):
    self.member_nodes[mn] = preferred

  def _add_policy(self, mn, preferred):
    if mn in self.member_nodes:
      msg = 'MN, "{}", is already included in a replication policy. To change '
      'from preferred to blocked or vice versa, please remove MN from policy '
      'and add again.'
      raise cli_exceptions.InvalidArguments(msg)
    self._set_policy(mn, preferred)

  def _remove_policy(self, mn):
    try:
      del self.member_nodes[mn]
    except KeyError:
      raise cli_exceptions.InvalidArguments(
        'Replication policy not set for MN: {0}'.format(mn)
      )

  def _add_preferred(self, mn):
    self._add_policy(mn, True)

  def _add_blocked(self, mn):
    self._add_policy(mn, False)

  # ============================================================================

  def clear(self):
    self.__init__()

  def get_preferred(self):
    return [k for k in sorted(self.member_nodes.keys()) if self.member_nodes[k]]

  def get_blocked(self):
    return [k for k in sorted(self.member_nodes.keys()) if not self.member_nodes[k]]

  def add_preferred(self, mn):
    self._add_preferred(mn)

  def remove(self, mn):
    self._remove_policy(mn)

  def add_blocked(self, mn):
    self._add_blocked(mn)

  def set_replication_allowed(self, replication_allowed):
    self.replication_allowed = replication_allowed
    if not replication_allowed:
      self.number_of_replicas = 0
    elif self.number_of_replicas == 0:
      self.number_of_replicas = d1_common.const.DEFAULT_NUMBER_OF_REPLICAS
      print_info('Changed number of replicas to %d.' % self.number_of_replicas)

  def get_replication_allowed(self):
    return self.replication_allowed

  def get_number_of_replicas(self):
    return self.number_of_replicas

  def set_number_of_replicas(self, number_of_replicas):
    if not number_of_replicas:
      self.replication_allowed = False
    else:
      try:
        float(number_of_replicas)
      except ValueError:
        print_error('"%s" is not a valid number.' % number_of_replicas)
        return

    self.number_of_replicas = int(number_of_replicas)

  def print_replication_policy(self):
    print_info(self._pretty_format())

  def to_pyxb(self):
    replication_policy = self._list_to_pyxb()
    return replication_policy

  def to_xml(self):
    replication_policy = self._list_to_pyxb()
    return replication_policy.toxml()
