#!/usr/bin/env python
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
"""Create and manipulate replication policies.
"""

import d1_cli.impl.cli_exceptions
import d1_cli.impl.cli_util

import d1_common.const


class ReplicationPolicy():
  def __init__(self):
    self._member_nodes = {}
    self.replication_allowed = True
    self.number_of_replicas = d1_common.const.DEFAULT_NUMBER_OF_REPLICAS

  def __str__(self):
    return self._pretty_format()

  def clear(self):
    self.__init__()

  def get_preferred(self):
    return [
      k for k in sorted(self._member_nodes.keys()) if self._member_nodes[k]
    ]

  def get_blocked(self):
    return [
      k for k in sorted(self._member_nodes.keys()) if not self._member_nodes[k]
    ]

  def add_preferred(self, mns):
    for mn in mns:
      self._add_preferred(mn)

  def repremove(self, mns):
    for mn in mns:
      self._remove_policy(mn)

  def add_blocked(self, mns):
    for mn in mns:
      self._add_blocked(mn)

  def set_replication_allowed(self, replication_allowed):
    self.replication_allowed = replication_allowed
    if not replication_allowed:
      self.number_of_replicas = 0
    elif self.number_of_replicas == 0:
      self.number_of_replicas = d1_common.const.DEFAULT_NUMBER_OF_REPLICAS
      d1_cli.impl.cli_util.print_info(
        'Changed number of replicas to %d.' % self.number_of_replicas
      )

  def get_replication_allowed(self):
    return self.replication_allowed

  def get_number_of_replicas(self):
    return self.number_of_replicas

  def set_number_of_replicas(self, number_of_replicas):
    if not number_of_replicas:
      self.replication_allowed = False
    else:
      try:
        int(number_of_replicas)
      except ValueError:
        raise d1_cli.impl.cli_exceptions.InvalidArguments(
          '"Invalid number: {}'.format(number_of_replicas)
        )
    self.number_of_replicas = int(number_of_replicas)

  def print_replication_policy(self):
    d1_cli.impl.cli_util.print_info(self._pretty_format())

  #
  # Private.
  #

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

    lines.append(
      format_str.format('number of replicas', self.number_of_replicas)
    )
    lines.append(
      format_str.format('replication allowed', self.replication_allowed)
    )
    return 'replication:\n' + '\n'.join(lines)

  def _set_policy(self, mn, preferred):
    self._member_nodes[mn] = preferred

  def _remove_policy(self, mn):
    try:
      del self._member_nodes[mn]
    except KeyError:
      raise d1_cli.impl.cli_exceptions.InvalidArguments(
        'Replication policy not set for MN: {}'.format(mn)
      )

  def _add_preferred(self, mn):
    if self._is_blocked(mn):
      d1_cli.impl.cli_util.print_warn(
        'The Member Node, "{}", was changed from blocked to preferred'.
        format(mn)
      )
    self._set_policy(mn, True)

  def _add_blocked(self, mn):
    if self._is_preferred(mn):
      d1_cli.impl.cli_util.print_warn(
        'The Member Node, "{}", was changed from preferred to blocked'.
        format(mn)
      )
    self._set_policy(mn, False)

  def _is_preferred(self, mn):
    return mn in self._member_nodes and self._member_nodes[mn]

  def _is_blocked(self, mn):
    return mn in self._member_nodes and not self._member_nodes[mn]
