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
'''
:mod:`subject_info`
===================

:Synopsis: Get list of equivalent subjects.
:Created: 2012-05-01
:Author: DataONE (Pippin)
'''
'''  List of permissions, in increasing order. '''
ALLOWED_PERMISSIONS = ('changePermission', 'write', 'read')

#-- PUBLIC -----------------------------------------------------------------------------#


def get_equivalent_subjects(primary_subject, subject_info):
  ''' Find the equivalent identities of the primary subject inside
     a d1:SubjectInfo structure.
  '''
  equiv_list_of_sets = _create_identity_sets(subject_info)
  merged_list_of_sets = _merge_identity_sets(equiv_list_of_sets)
  return _find_primary_identity(primary_subject, merged_list_of_sets)


def highest_authority(primary_subject, subject_info, access_policy):
  ''' Returns a list of (highest authority, subject matched, policy matched) '''
  equiv_list_of_sets = _create_identity_sets(subject_info)
  merged_list_of_sets = _merge_identity_sets(equiv_list_of_sets)
  primary_identity_list = _find_primary_identity(primary_subject, merged_list_of_sets)
  equiv_set = _add_groups(primary_identity_list, subject_info)
  access_map = _create_policy_maps(access_policy)
  return _highest_authority(equiv_set, access_map)

#-- PRIVATE ----------------------------------------------------------------------------#


def _create_identity_sets(subject_info):
  ''' Convert a d1:SubjectInfo structure into a list of sets, with each
      set representing a person.
  '''
  equiv_list_of_sets = []
  for person in subject_info.person:
    equiv_set = set()
    subject = _normalize_subject(person.subject.value())
    equiv_set.add(subject)
    for equivalentIdentity in person.equivalentIdentity:
      subject = _normalize_subject(equivalentIdentity.value())
      equiv_set.add(subject)
    equiv_list_of_sets.append(equiv_set)
  return equiv_list_of_sets


def _merge_identity_sets(equiv_list_sets):
  ''' Merge overlapping sets (people) and get rid of empty sets.
  '''
  result_list_sets = []
  if equiv_list_sets:
    # Make sure there are no intersections.
    num_sets = len(equiv_list_sets)
    for i in range(num_sets):
      for j in range(num_sets):
        if i != j and len(equiv_list_sets[i]) > 0 and len(equiv_list_sets[j]) > 0:
          if not equiv_list_sets[i].isdisjoint(equiv_list_sets[j]):
            equiv_list_sets[i] = equiv_list_sets[i].union(equiv_list_sets[j])
            equiv_list_sets[j].clear()
    # At this point, there may be empty sets.
    for equiv_set in equiv_list_sets:
      if len(equiv_set) > 0:
        result_list_sets.append(equiv_set)
  # And it's done.
  return result_list_sets


def _find_primary_identity(primary_subject, equiv_list_sets):
  ''' Find the set with the primary identity.  Return it as a sorted list.
  '''
  for equiv_set in equiv_list_sets:
    if primary_subject in equiv_set:
      result = list(equiv_set)
      result.sort()
      return result
  return []


def _normalize_subject(subject):
  ''' Normalize the subject by:
      * Capitalizing attribute names
      * Reverse order if CA attribute is not first.
          (Note, this may not fix the order, but it will try)
  '''
  new_subject = []
  if subject.lower() == 'public':
    return 'public'
  for component in subject.split(','):
    carray = component.split('=', 2)
    carray[0] = carray[0].upper()
    # *** Do not remove internal whitespace.  It is unknown if it is part of the value.
    #carray[1] = ' '.join(carray[1].split())
    new_subject.append('='.join(carray))
  if new_subject[0].find("CN=") != 0:
    new_subject.reverse()
  return ','.join(new_subject)


def _add_groups(equiv_list, subject_info):
  ''' Add groups to the identities and return a set. '''
  equiv_set = set(equiv_list)
  for person in subject_info.person:
    person_name = person.subject.value()
    if person_name in equiv_set:
      for group in person.isMemberOf:
        equiv_set.add(group.value())
  for group in subject_info.group:
    group_subject = group.subject.value()
    for member in group.hasMember:
      member_value = member.value()
      if member_value in equiv_set:
        equiv_set.add(group_subject)
  return equiv_set


def _create_policy_maps(access_policy):
  policy_map = {}
  for allow in access_policy.allow:
    subject_list = allow.subject
    for permission in allow.permission:
      subject_set = policy_map.get(permission)
      if not subject_set:
        subject_set = set()
        policy_map[permission] = subject_set
      for subject in subject_list:
        normalized = _normalize_subject(subject.value())
        subject_set.add(normalized)
        pass # foreach subject
      pass # foreach permission
    pass # foreach allow
  return policy_map


def _highest_authority(subject_set, access_map):
  ''' Return the highest level of authorization.
  '''
  for permission in ALLOWED_PERMISSIONS:
    permission_set = access_map.get(permission)
    if permission_set:
      if 'public' in permission_set:
        return permission
      for subject in subject_set:
        normalized = _normalize_subject(subject)
        if normalized in permission_set:
          return permission
