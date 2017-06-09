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
"""Pretty print an operation.
"""

from __future__ import absolute_import

import d1_cli.impl.cli_util as cli_util

LEVEL_INDENT = 2
TAB = 30


class OperationFormatter(object):
  """Print an operation according to the template. The template contains all
  parameters that can be in any of the operations and determines the relative
  position of each parameter that is present in the operation.
  """

  def __init__(self):
    self._template = (
      u'comment', u'operation', (u'CLI', u'verbose', u'editor',),
      (u'Target Nodes', u'cn-url', u'mn-url'),
      (u'Authentication', u'anonymous', u'cert-file',
       u'key-file',), (u'Slicing', u'start', u'count',), (
         u'Searching', u'query', u'query-type', u'from-date', u'to-date',
         u'search-format-id',
       ), (
         u'Parameters', u'identifier', u'identifier-new', u'identifier-old',
         u'identifier-package', u'identifier-science-meta',
         u'identifier-science-data', u'science-file',
         (u'Misc', u'format-id',
          u'algorithm',), (u'Reference Nodes', u'authoritative-mn',),
         (u'Subjects', u'rights-holder',), (u'Access Control', u'allow',), (
           u'Replication', u'replication-allowed', u'number-of-replicas',
           u'blocked-nodes', u'preferred-nodes',
         ),
       ),
    )

  def print_operation(self, operation):
    #pprint.pprint(operation)
    for line in self._format_operation(operation, self._template, 0):
      cli_util.print_info(line)

  def _format_operation(self, operation, template, indent):
    lines = []
    for v in template:
      if isinstance(v, basestring):
        lines.extend(self._format_value(operation, v, indent))
      else:
        lines_section = self._format_operation(
          operation, v[1:], indent + LEVEL_INDENT
        )
        if len(lines_section):
          lines.append(' ' * indent + v[0] + ':')
          lines.extend(lines_section)
    return lines

  def _format_value(self, operation, key, indent):
    """A value that exists in the operation but has value None is displayed.
    A value that does not exist in the operation is left out entirely.
    The value name in the operation must match the value name in the template,
    but the location does not have to match.
    """
    v = self._find_value(operation, key)
    if v == 'NOT_FOUND':
      return []
    if not isinstance(v, list):
      v = [v]
    if not len(v):
      v = [None]
    key = key + ':'
    lines = []
    for s in v:
      # Access control rules are stored in tuples.
      if isinstance(s, tuple):
        s = '{}: {}'.format(*s)
      lines.append(
        '{}{}{}{}'.
        format(' ' * indent, key, ' ' * (TAB - indent - len(key) - 1), s)
      )
      key = ''
    return lines

  def _find_value(self, operation, key):
    for k in operation.keys():
      if k == key:
        return operation[k]
      if isinstance(operation[k], dict):
        r = self._find_value(operation[k], key)
        if r != 'NOT_FOUND':
          return r
    return 'NOT_FOUND'
