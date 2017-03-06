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
"""Utilities for handling the DataONE AccessPolicy type

Note:

There can be multiple rules in a policy and each rule can contain multiple
subjects and permissions. So the same subject can be specified multiple times in
the same rules or in different rules, each time with a different set of
permissions. In such cases, the permissions are combined to determine the
effective permission for the subject.

The permissions supported by DataONE are 'read', 'write' and 'changePermission'.
'write' implicitly includes 'read', and 'changePermission' implicitly includes
'read' and 'write'. So, only a single permission needs to be assigned to a
subject in order to determine all permissions the subject has.

E.g., the following two access policies are equivalent:

<accessPolicy>
  <allow>
    <subject>subj2</subject>
    <subject>subj1</subject>
    <permission>read</permission>
  </allow>
  <allow>
    <subject>subj4</subject>
    <permission>read</permission>
    <permission>changePermission</permission>
  </allow>
  <allow>
    <subject>subj2</subject>
    <subject>subj3</subject>
    <permission>read</permission>
    <permission>write</permission>
  </allow>
  <allow>
    <subject>subj5</subject>
    <permission>read</permission>
    <permission>write</permission>
  </allow>
</accessPolicy>

and

<accessPolicy>
  <allow>
    <subject>subj1</subject>
    <permission>read</permission>
  </allow>
  <allow>
    <subject>subj2</subject>
    <subject>subj3</subject>
    <subject>subj5</subject>
    <permission>write</permission>
  </allow>
  <allow>
    <subject>subj4</subject>
    <permission>changePermission</permission>
  </allow>
</accessPolicy>
"""

# D1
import d1_common.xml
import d1_common.types.dataoneTypes

ORDERED_PERMISSION_LIST = ['read', 'write', 'changePermission']


def normalize(access_policy_pyxb):
  normalized_permission_list = get_normalized_permission_list(
    access_policy_pyxb
  )
  grouped_permission_dict = _get_grouped_permission_dict(
    normalized_permission_list
  )
  return get_access_policy_pyxb(grouped_permission_dict)


def get_normalized_permission_list(access_policy_pyxb):
  """Returns the briefest possible representation of a set of permissions for
  subjects in alphabetical order. E.g.:
  [
    ('subj1', 'read'),
    ('subj2', 'write'),
  ]
  """
  return [(s, get_normalized_permission_from_iter(p))
          for s, p in
          sorted(get_effective_permission_dict(access_policy_pyxb).items())]


def get_effective_permission_list(access_policy_pyxb, subject_str):
  """Returns a list of permissions for {subject}. E.g., ['read', 'write'].
  Handles implicit permissions. E.g., if {access_policy} specifies only
  'write', returns ['read', 'write']. If {subject} is not in {access_policy},
  returns [].
  """
  return get_effective_permission_dict(access_policy_pyxb)[subject_str]


def get_effective_permission_dict(access_policy_pyxb):
  """Like get_effective_permission(), but returns a dict of subjects to
  permissions. E.g.:
  {
    'subj2': ['read'],
    'subj1': ['read', 'write'],
  }
  """
  return {
    s: get_effective_permission_list_from_iter(p)
    for s, p in _get_unique_permissions_dict(access_policy_pyxb).items()
  }


def get_access_policy_pyxb(grouped_permission_dict):
  """Returns AccessPolicy PyXB representation of {grouped_permission_dict}.
  Returns None if {grouped_permission_dict} is empty. The schema does not allow
  AccessPolicy to be empty, but in System Metadata, it can be left out
  altogether. So returning None instead of an empty AccessPolicy allows the
  result to be inserted directly into a SystemMetadata PyXB object.

  Example input:

  {
    'read': ['subj2'],
    'write': ['subj1', 'subj3'],
  }
  """
  # Using accessPolicy() instead of AccessPolicy() and accessRule() instead of
  # AccessRule() gives PyXB the type information required for using this as a
  # root element.
  access_policy_pyxb = d1_common.types.dataoneTypes.accessPolicy()
  for perm_str in ORDERED_PERMISSION_LIST:
    if perm_str in grouped_permission_dict:
      rule_pyxb = d1_common.types.dataoneTypes.accessRule()
      rule_pyxb.permission.append(perm_str)
      for subj_str in grouped_permission_dict[perm_str]:
        rule_pyxb.subject.append(subj_str)
      access_policy_pyxb.allow.append(rule_pyxb)
  if len(access_policy_pyxb.allow):
    return access_policy_pyxb


def is_subject_allowed(access_policy_pyxb, subject_str, permission_str):
  """Returns True if {subject} has {permission}, else False. Handles implicit
  permissions. E.g., if {access_policy} specifies only 'write' for {subject},
  and {permission} is 'read', returns True.
  """
  return permission_str in get_effective_permission_list(
    access_policy_pyxb, subject_str
  )


def get_effective_permission_list_from_iter(permission_iterable):
  """Given an iterable of permissions, return effective permission list. E.g.,
  ['write', 'changePermission'] returns ['read', 'write', 'changePermission'].
  Returns None if the iterable is empty.
  """
  for i in range(2, -1, -1):
    if ORDERED_PERMISSION_LIST[i] in permission_iterable:
      return ORDERED_PERMISSION_LIST[:i + 1]


def get_normalized_permission_from_iter(permission_iterable):
  """Given an iterable of permissions, returns the single permission that
  explicitly and implicitly specifies the permissions in the iterable. E.g.,
  ['write', 'changePermission'] returns 'changePermission'. Returns None if
  the iterable is empty.
  """
  perm_idx = None
  for perm_str in permission_iterable:
    perm_idx = max(perm_idx, ORDERED_PERMISSION_LIST.index(perm_str))
  if perm_idx is not None:
    return ORDERED_PERMISSION_LIST[perm_idx]


def is_equivalent_pyxb(a_pyxb, b_pyxb):
  return get_normalized_permission_list(a_pyxb) \
    == get_normalized_permission_list(b_pyxb)


def is_equivalent_xml(a_xml, b_xml):
  return is_equivalent_pyxb(
    d1_common.xml.deserialize(a_xml),
    d1_common.xml.deserialize(b_xml),
  )


#
# Private
#


def _get_grouped_permission_dict(normalized_permission_list):
  """Arranges {normalized_permission_list} into a dict suitable as a base
  for building the briefest possible representation in an AccessPolicy PyXB
  object.
  [
    ('subj1', 'write'),
    ('subj2', 'read'),
    ('subj3', 'write'),
  ] ->
  {
    'read': ['subj2'],
    'write': ['subj1', 'subj3'],
  }
  """
  perm_group_dict = {}
  for subj_str, perm_str in normalized_permission_list:
    perm_group_dict.setdefault(perm_str, set()).add(subj_str)
  return {
    perm_str: sorted(subj_set) for perm_str, subj_set in perm_group_dict.items()
  }


def _get_unique_permissions_dict(access_policy_pyxb):
  """Returns a dict of subjects to permission sets. Translates the PyXB obj
  to a dict and removes duplicate subjects and permissions.
  """
  perm_dict = {}
  for allow_pyxb in access_policy_pyxb.allow:
    perm_set = set()
    for permission_pyxb in allow_pyxb.permission:
      perm_set.add(permission_pyxb)
    for subject_pyxb in allow_pyxb.subject:
      perm_dict.setdefault(subject_pyxb.value(), set()).update(perm_set)
  return perm_dict
