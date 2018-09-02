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
"""Context managers for working with the DataONE AccessPolicy type

Example:

with d1_common.wrap.access_policy.wrap(self.sysmeta_pyxb) as ap:
  ap.clear()
  ap.add_perm('subj1', 'read')

  print ap.get_subjects('changePermission')

Exiting the context manager scope causes the changes that were made to the
AccessPolicy to be written back to the wrapped SystemMetadata.

# An overview of the AccessPolicy

There can be multiple rules in a policy and each rule can contain multiple
subjects and permissions. So the same subject can be specified multiple times in
the same rules or in different rules, each time with a different set of
permissions. In such cases, the permissions are combined to determine the
effective permission for the subject.

The permissions supported by DataONE are 'read', 'write' and 'changePermission'.
'write' implicitly includes 'read', and 'changePermission' implicitly includes
'read' and 'write'. So, only a single permission needs to be assigned to a
subject in order to determine all permissions the subject has.

  read < write < changePermission

Implicit permissions are included. E.g., if the AccessPolicy specifies only
'write' for {subj_str}, perm_str='read' also returns True.

{perm_str} must be one of read, 'write', 'changePermission'.

E.g., the following two access policies are equivalent:

<accessPolicy>
  <allow>
    <subject>subj2</subject>
    <subject>subj1</subject>
    <perm>read</perm>
  </allow>
  <allow>
    <subject>subj4</subject>
    <perm>read</perm>
    <perm>changePermission</perm>
  </allow>
  <allow>
    <subject>subj2</subject>
    <subject>subj3</subject>
    <perm>read</perm>
    <perm>write</perm>
  </allow>
  <allow>
    <subject>subj5</subject>
    <perm>read</perm>
    <perm>write</perm>
  </allow>
</accessPolicy>

and

<accessPolicy>
  <allow>
    <subject>subj1</subject>
    <perm>read</perm>
  </allow>
  <allow>
    <subject>subj2</subject>
    <subject>subj3</subject>
    <subject>subj5</subject>
    <perm>write</perm>
  </allow>
  <allow>
    <subject>subj4</subject>
    <perm>changePermission</perm>
  </allow>
</accessPolicy>
"""

import copy
import inspect
import logging
import pprint
import sys

import contextlib2

import d1_common.const
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.xml

ORDERED_PERM_LIST = ['read', 'write', 'changePermission']

# ==============================================================================
"""
subj_dict maps each subj to the perms the the subj has specifically been given.
It holds perms just having been read for PyXB. Duplicates caused by the same
subj being given the same perm in multiple ways are filtered out.

  {
    'subj1': { 'read' },
    'subj2': { 'read', 'write' },
    'subj3': { 'read', 'write' },
    'subj4': { 'changePermission', 'read' },
    'subj5': { 'read', 'write' }
  }

perm_dict maps each perm that a subj has specifically been given, to the subj.
If the AccessPolicy contains multiple "allow" elements, and they each give
different perms to a subj, those show up as additional mappings. Duplicates
caused by the same subj being given the same perm in multiple ways are filtered
out. Calls such as `add_perm()` also cause extra mappings to be added here, as
long as they're not exact duplicates. Whenever this dict is used for generating
PyXB or making comparisons, it is first normalized to a norm_perm_list.

  {
    'read': { 'subj1', 'subj2' },
    'write': { 'subj3' },
    'changePermission': { 'subj2' },
  }

subj_highest_dict maps each subj to the highest perm the subj has. The dict has
the same number of keys as there are subj.

  {
    'subj1': 'write',
    'subj2': 'changePermission',
    'subj3': 'write',
  }

highest_perm_dict maps the highest perm a subj has, to the subj. The dict can
have at most 3 keys:

  {
    'changePermission': { 'subj2', 'subj3', 'subj5', 'subj6' },
    'read': { 'public' },
    'write': { 'subj1', 'subj4' }
  }

norm_perm_list is a minimal, ordered and hashable list of lists. The top level
has up to 3 lists, one for each perm that is in use. Each of the lists then has
a list of subj for which that perm is the highest perm. norm_perm_list is the
shortest way that the required permissions can be expressed, and is used for
comparing access policies and creating uniform PyXB objects:

  [
    ['read', ['public']],
    ['write', ['subj1', 'subj4']],
    ['changePermission', ['subj2', 'subj3', 'subj5', 'subj6']]
  ]

"""


@contextlib2.contextmanager
def wrap(access_pyxb, read_only=False):
  """Work with the AccessPolicy in a SystemMetadata PyXB object
  - When only a single AccessPolicy operation is needed, there's no need to use
  this context manager. Instead, use the generated context manager wrappers.
  """
  w = AccessPolicyWrapper(access_pyxb)
  yield w
  if not read_only:
    w.get_normalized_pyxb()


@contextlib2.contextmanager
def wrap_sysmeta_pyxb(sysmeta_pyxb, read_only=False):
  """Work with the AccessPolicy in a SystemMetadata PyXB object
  - When only a single AccessPolicy operation is needed, there's no need to use
  this context manager. Instead, use the generated context manager wrappers.
  - There is no clean way in Python to make a context manager that allows client
  code to replace the object that is passed out of the manager. The AccessPolicy
  schema does not allow the AccessPolicy element to be empty. However, the
  SystemMetadata schema specifies the AccessPolicy as optional. By wrapping the
  SystemMetadata instead of the AccessPolicy when working with AccessPolicy that
  is within SystemMetadata, the wrapper can handle the situation of empty
  AccessPolicy by instead dropping the AccessPolicy from the SystemMetadata.
  """
  w = AccessPolicyWrapper(sysmeta_pyxb.accessPolicy)
  yield w
  if not read_only:
    sysmeta_pyxb.accessPolicy = w.get_normalized_pyxb()


# ==============================================================================


class AccessPolicyWrapper(object):
  def __init__(self, access_pyxb):
    self._access_pyxb = access_pyxb
    self._perm_dict = self._perm_dict_from_pyxb(access_pyxb)
    self._orig_perm_dict = self._perm_dict.copy()

  def update(self):
    """Update the wrapped AccessPolicy PyXB object with normalized and minimal
    rules representing current state
    """
    self._access_pyxb.allow = self.get_normalized_pyxb().allow

  # Examine current state

  def get_normalized_pyxb(self):
    """Return current state of the wrapper as a minimal, ordered, AccessPolicy
    PyXB object
    - The returned PyXB object contains the minimal rules required for correctly
    representing the perms.
    """
    return self._pyxb_from_perm_dict(self._perm_dict)

  def get_normalized_perm_list(self):
    """Return a minimal, ordered, hashable list of subjects and permissions that
    represents the current state of the wrapper"""
    return self._norm_perm_list_from_perm_dict(self._perm_dict)

  def get_highest_perm_str(self, subj_str):
    """Return the highest permission for {subj_str} or None if {subj_str} does
    not have any permissions """
    pres_perm_set = self._present_perm_set_for_subj(self._perm_dict, subj_str)
    return (
      None
      if not pres_perm_set else self._highest_perm_from_iter(pres_perm_set)
    )

  def get_effective_perm_list(self, subj_str):
    """Return list of permissions up to and including the highest permission for
    {subj_str}, ordered lower to higher, or empty list if {subj_str} does not
    have any permissions
    - E.g.: If 'write' is highest permission for {subj_str}, return ['read',
    'write']. """
    highest_perm_str = self.get_highest_perm_str(subj_str)
    if highest_perm_str is None:
      return []
    return self._equal_or_lower_perm_list(highest_perm_str)

  def get_subjects_with_equal_or_higher_perm(self, perm_str):
    """Return set of subj that have perm equal or higher than {perm_str}
    - {perm_str}='read' will return all subjects. """
    self._assert_valid_permission(perm_str)
    return {
      s
      for p in self._equal_or_higher_perm(perm_str)
      for s in self._perm_dict.get(p, set())
    }

  def dump(self):
    """Dump the current state to debug level log"""
    logging.debug('AccessPolicy:')
    list(
      map(
        logging.debug, [
          '  {}'.format(s)
          for s in pprint.pformat(self.get_normalized_perm_list()).splitlines()
        ]
      )
    )

  # Check current state

  def is_public(self):
    """Return True if AccessPolicy allows public read"""
    return self.subj_has_perm(d1_common.const.SUBJECT_PUBLIC, 'read')

  def is_private(self):
    """Return True if AccessPolicy does not grant access to any subjects"""
    return not self.get_subjects_with_equal_or_higher_perm('read')

  def is_empty(self):
    """Return True if AccessPolicy does not grant access to any subjects"""
    return self.is_private()

  def are_equivalent_pyxb(self, access_pyxb):
    """Return True if the AccessPolicy PyXB object in {access_pyxb} grants the
    exact same permissions as this one.
    - Differences in how the permissions are represented in the XML docs are
    handled by transforming to normalized lists before comparison."""
    return (
      self.get_normalized_perm_list() == get_normalized_perm_list(access_pyxb)
    )

  def are_equivalent_xml(self, access_xml):
    """Return True if the AccessPolicy XML doc in {access_xml} grants the exact same
    permissions as this one.
    - Differences in how the permissions are represented in the XML docs are
    handled by transforming to normalized lists before comparison."""
    return self.are_equivalent_pyxb(d1_common.xml.deserialize(access_xml))

  def subj_has_perm(self, subj_str, perm_str):
    """Return True if {subj_str} has perm equal to or higher than {perm_str} """
    self._assert_valid_permission(perm_str)
    return perm_str in self.get_effective_perm_list(subj_str)

  # Update state

  def clear(self):
    """Remove AccessPolicy
    - Only the rightsHolder set in the SystemMetadata will be able to access the
    object unless new perms are now added"""
    self._perm_dict = {}

  def add_public_read(self):
    """Add read perm for public"""
    self.add_perm(d1_common.const.SUBJECT_PUBLIC, 'read')

  def add_authenticated_read(self):
    """Add read perm for all authenticated subj
    - Public read is removed if present. """
    self.remove_perm(d1_common.const.SUBJECT_PUBLIC, 'read')
    self.add_perm(d1_common.const.SUBJECT_AUTHENTICATED, 'read')

  def add_verified_read(self):
    """Add read perm for all verified subj
    - Public read is removed if present. """
    self.remove_perm(d1_common.const.SUBJECT_PUBLIC, 'read')
    self.add_perm(d1_common.const.SUBJECT_VERIFIED, 'read')

  def add_perm(self, subj_str, perm_str):
    """Add {perm_str} permission for {subj_str} """
    self._assert_valid_permission(perm_str)
    self._perm_dict.setdefault(perm_str, set()).add(subj_str)

  def remove_perm(self, subj_str, perm_str):
    """Remove {perm_str} and higher permissions for {subj_str} """
    self._assert_valid_permission(perm_str)
    for perm_str in self._equal_or_higher_perm(perm_str):
      self._perm_dict.setdefault(perm_str, set()).discard(subj_str)

  def remove_subj(self, subj_str):
    """Remove all permissions for {subj_str}
    - {subj_str} may still have access to the obj, e.g., if the obj has public
    access or {subj_str} is is in a group or has an equivalent subj that has
    access. """
    for subj_set in list(self._perm_dict.values()):
      subj_set -= {subj_str}

  #
  # Private
  #

  def _perm_dict_from_pyxb(self, access_pyxb):
    """Return dict representation of AccessPolicy PyXB obj"""
    subj_dict = self._subj_dict_from_pyxb(access_pyxb)
    return self._perm_dict_from_subj_dict(subj_dict)

  def _perm_dict_from_subj_dict(self, subj_dict):
    """Return dict where keys and values of {subj_dict} have been flipped
    around"""
    perm_dict = {}
    for subj_str, perm_set in list(subj_dict.items()):
      for perm_str in perm_set:
        perm_dict.setdefault(perm_str, set()).add(subj_str)
    return perm_dict

  def _pyxb_from_perm_dict(self, perm_dict):
    """Return an AccessPolicy PyXB representation of {perm_dict}
    - If {norm_perm_list} is empty, None is returned. The schema does not allow
    AccessPolicy to be empty, but in SystemMetadata, it can be left out
    altogether. So returning None instead of an empty AccessPolicy allows the
    result to be inserted directly into a SystemMetadata PyXB object. """
    norm_perm_list = self._norm_perm_list_from_perm_dict(perm_dict)
    return self._pyxb_from_norm_perm_list(norm_perm_list)

  def _pyxb_from_norm_perm_list(self, norm_perm_list):
    """Return an AccessPolicy PyXB representation of {norm_perm_list} """
    # Using accessPolicy() instead of AccessPolicy() and accessRule() instead of
    # AccessRule() gives PyXB the type information required for using this as a
    # root element.
    access_pyxb = d1_common.types.dataoneTypes.accessPolicy()
    for perm_str, subj_list in norm_perm_list:
      rule_pyxb = d1_common.types.dataoneTypes.accessRule()
      rule_pyxb.permission.append(perm_str)
      for subj_str in subj_list:
        rule_pyxb.subject.append(subj_str)
      access_pyxb.allow.append(rule_pyxb)
    if len(access_pyxb.allow):
      return access_pyxb

  def _subj_dict_from_pyxb(self, access_pyxb):
    """Return a dict representation of {access_pyxb}, which is an AccessPolicy PyXB
    object. This also remove any duplicate subjects and permissions in the PyXB
    object. """
    subj_dict = {}
    for allow_pyxb in access_pyxb.allow:
      perm_set = set()
      for perm_pyxb in allow_pyxb.permission:
        perm_set.add(perm_pyxb)
      for subj_pyxb in allow_pyxb.subject:
        subj_dict.setdefault(subj_pyxb.value(), set()).update(perm_set)
    return subj_dict

  def _highest_perm_dict_from_perm_dict(self, perm_dict):
    """Return a perm_dict where only the highest permission for each subject
    is included"""
    highest_perm_dict = copy.copy(perm_dict)
    for ordered_str in reversed(ORDERED_PERM_LIST):
      for lower_perm in self._lower_perm_list(ordered_str):
        highest_perm_dict.setdefault(lower_perm, set())
        highest_perm_dict[lower_perm] -= perm_dict.get(ordered_str, set())
    return highest_perm_dict

  def _norm_perm_list_from_perm_dict(self, perm_dict):
    """Return a minimal, ordered, hashable list of subjects and permissions"""
    high_perm_dict = self._highest_perm_dict_from_perm_dict(perm_dict)
    return [[k, list(sorted(high_perm_dict[k]))]
            for k in ORDERED_PERM_LIST if high_perm_dict.get(k, False)]

  def _effective_perm_list_from_iter(self, perm_iter):
    """Return list of effective permissions for for highest permission
    in {perm_iter}, ordered lower to higher, or None if {perm_iter} is empty
    """
    highest_perm_str = self._highest_perm_from_iter(perm_iter)
    return (
      self._equal_or_lower_perm_list(highest_perm_str)
      if highest_perm_str is not None else None
    )

  def _present_perm_set_for_subj(self, perm_dict, subj_str):
    """Return a set containing only the permissions that are present in the
    {perm_dict} for {subj_str}
    """
    return {p for p, s in list(perm_dict.items()) if subj_str in s}

  def _highest_perm_from_iter(self, perm_iter):
    """Return the highest perm present in {perm_iter} or None if {perm_iter}
    is empty"""
    perm_set = set(perm_iter)
    for perm_str in reversed(ORDERED_PERM_LIST):
      if perm_str in perm_set:
        return perm_str

  def _ordered_idx_from_perm(self, perm_str):
    """Return the ordered index of {perm_str} or None if {perm_str} is not a
    valid permission"""
    for i, ordered_str in enumerate(ORDERED_PERM_LIST):
      if perm_str == ordered_str:
        return i

  def _lower_perm_list(self, perm_str):
    """Return a list containing the 0, 1 or 2 permissions that are lower than
    {perm_str}, ordered lower to higher"""
    return ORDERED_PERM_LIST[:self._ordered_idx_from_perm(perm_str)]

  def _equal_or_lower_perm_list(self, perm_str):
    """Return a list containing the 1, 2 or 3 permissions that are equal or
    lower than {perm_str}, ordered lower to higher"""
    return ORDERED_PERM_LIST[:self._ordered_idx_from_perm(perm_str) + 1]

  def _equal_or_higher_perm(self, perm_str):
    """Return a list containing the 0, 1 or 2 permissions that are equal or
    higher than than {perm_str}, ordered lower to higher"""
    return ORDERED_PERM_LIST[self._ordered_idx_from_perm(perm_str):]

  def _has_access_policy(self, sysmeta_pyxb):
    """Return True if there is an AccessPolicy in the SystemMetadata"""
    return bool(getattr(sysmeta_pyxb, 'accessPolicy', False))

  def _assert_valid_permission(self, perm_str):
    """Raise D1 exception if {perm_str} is not a valid permission"""
    if perm_str not in ORDERED_PERM_LIST:
      raise d1_common.types.exceptions.InvalidRequest(
        0, 'Permission must be one of {}. perm_str="{}"'.format(
          ', '.join(ORDERED_PERM_LIST), perm_str
        )
      )


# ==============================================================================

# Stubs to keep IDEs and code validation tools happy. The actual methods are
# generated below.


def update():
  pass


def get_normalized_pyxb(access_pyxb):
  pass


def get_normalized_perm_list(access_pyxb):
  pass


def get_highest_perm_str(subj_str):
  pass


def get_effective_perm_list(subj_str):
  pass


def get_subjects_with_equal_or_higher_perm(perm_str):
  pass


def dump():
  pass


def is_public(access_pyxb):
  pass


def is_private(access_pyxb):
  pass


def is_empty(access_pyxb):
  pass


def are_equivalent_pyxb(access_pyxb):
  pass


def are_equivalent_xml(access_xml):
  pass


def subj_has_perm(subj_str, perm_str):
  pass


def clear(access_pyxb):
  pass


def add_public_read(access_pyxb):
  pass


def add_authenticated_read(access_pyxb):
  pass


def add_verified_read(access_pyxb):
  pass


def add_perm(subj_str, perm_str):
  pass


def remove_perm(subj_str, perm_str):
  pass


def remove_subj(subj_str):
  pass


# ==============================================================================

# Generate module level wrappers for the public class methods


def mk_func(func_name):
  """This function wrapping func is required because of something, something,
  mumble, closures"""

  def func(access_pyxb, *args, **kwargs):
    return getattr(AccessPolicyWrapper(access_pyxb), func_name)(*args, **kwargs)

  func.__name__ = func_name
  return func


for method in inspect.getmembers(AccessPolicyWrapper):
  method_name, method_obj = method
  if not method_name.startswith('_'):
    setattr(sys.modules[__name__], method_name, mk_func(method_name))
