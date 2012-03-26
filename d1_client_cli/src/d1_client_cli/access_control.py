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
:mod:`access_control`
=====================

:Synopsis: Create and manipulate access control objects.
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


class access_control():
  def __init__(self):
    self.allow = {}
    self.public = False

  def __str__(self):
    return self._pretty_format()

  def _get_valid_permissions(self):
    return ('read', 'write', 'changePermission', 'execute', 'replicate')

  def _clear(self):
    self.allow.clear()
    self.public = False

  def _list_to_pyxb(self):
    if not self.allow:
      return None
    access_policy = dataoneTypes.accessPolicy()
    for subject in sorted(self.allow.keys()):
      access_rule = dataoneTypes.AccessRule()
      access_rule.subject.append(subject)
      permission = dataoneTypes.Permission(self.allow[subject])
      access_rule.permission.append(permission)
      access_policy.append(access_rule)
    return access_policy

  def _add_public_subject(self, access_policy):
    if access_policy is None:
      access_policy = dataoneTypes.accessPolicy()
    access_rule = dataoneTypes.AccessRule()
    access_rule.subject.append(d1_common.const.SUBJECT_PUBLIC)
    permission = dataoneTypes.Permission('read')
    access_rule.permission.append(permission)
    access_policy.append(access_rule)
    return access_policy

  def _add_allowed_subject(self, subject, permission):
    self.allow[subject] = permission

  def _pretty_format(self):
    lines = []
    format_str = '  {0: <30s}{1}'
    #    if not len(lines):
    #      lines.append(format_str.format('submitter', 'full access'))
    if self.public:
      lines.append(format_str.format('public', 'read'))
    for subject in sorted(self.allow.keys()):
      lines.append(format_str.format(subject, self.allow[subject]))
    return 'access:\n' + '\n'.join(lines)

  # ============================================================================

  def to_pyxb(self):
    access_policy = self._list_to_pyxb()
    if self.public:
      access_policy = self._add_public_subject(access_policy)
    return access_policy

  def to_xml(self):
    return self.to_pyxb().toxml()

  def from_xml(self, xml):
    access_policy = dataoneTypes.CreateFromDocument(xml)
    for access_rule in access_policy.allow:
      subject = access_rule.subject[0].value()
      permission = access_rule.permission[0]
      self._add_allowed_subject(subject, permission)

  def clear(self):
    self._clear()

  def add_allowed_subject(self, subject, permission):
    if permission is None:
      permission = 'read'
    if permission not in self._get_valid_permissions():
      msg = 'Invalid permission: {0}. Must be one of: {1}'\
        .format(permission, ', '.join(self._get_valid_permissions()))
      raise cli_exceptions.InvalidArguments(msg)
    self._add_allowed_subject(subject, permission)

  def remove_allowed_subject(self, subject):
    try:
      del self.allow[subject]
    except KeyError:
      raise cli_exceptions.InvalidArguments('Subject not in access control list: {0}'\
        .format(subject))

  def allow_public(self, allow):
    self.public = allow

  def remove_all_allowed_subjects(self):
    self.clear()
    self.allow_public(False)
