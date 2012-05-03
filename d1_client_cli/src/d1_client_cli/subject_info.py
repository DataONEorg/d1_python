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
:mod:`subject_info`
===================

:Synopsis: Get list of equivalent subjects.
:Created: 2012-05-01
:Author: DataONE (Pippin)
'''

import access_control


def get_equivalent_subjects(subject_info):
  equiv_map_list = []
  if subject_info.person:
    for person in subject_info.person:
      _add_person(equiv_map_list, person)
  equiv_list_list = _flatten_dictionary(equiv_map_list)
  if subject_info.group:
    for group in subject_info.group:
      _add_group(equiv_list_list, group)
  return equiv_list_list


def _add_person(equiv_map_list, person):
  '''  Add a person to the equivalency list. '''
  personName = _normalize_subject(person.subject.value())
  inner_map = {personName: True}
  equivalent_identity_list = person.equivalentIdentity
  for equivalent_identity in equivalent_identity_list:
    inner_map[_normalize_subject(equivalent_identity.value())] = True
  equiv_map_list.append(inner_map)
  if person.isMemberOf:
    for group in person.isMemberOf:
      inner_map[_normalize_subject(group.value())] = True


def _add_group(equiv_list_list, group):
  ''' Add a group to the equivalency lists. '''
  groupName = _normalize_subject(group.subject.value())
  for member in group.hasMember:
    memberName = member.value()
    for equiv_list in equiv_list_list:
      try: # Because Python 2.6 doesn't have list.contains()
        equiv_list.index(memberName)
        try:
          equiv_list.index(groupName)
        except:
          equiv_list.append(groupName)
      except:
        pass
  return equiv_list_list


def _normalize_subject(subject):
  ''' Clean up white space, capitalize component keys, and set CN first. '''
  new_subject = []
  if subject.lower() == 'public':
    return 'public'
  for component in subject.split(','):
    carray = component.split('=', 2)
    carray[0] = carray[0].upper()
    carray[1] = ' '.join(carray[1].split())
    new_subject.append('='.join(carray))
  if new_subject[0].find("CN=") != 0:
    new_subject.reverse()
  return ','.join(new_subject)


def _flatten_dictionary(equiv_map_list):
  ''' "flatten" equivalancies and return a list of lists. '''
  # Go through each disctionary and see if any member is a member of some other.
  result_map_list = [equiv_map_list[0]]
  ndx = 1
  while ndx < len(equiv_map_list):
    test_equiv_map = equiv_map_list[ndx]
    found = False
    for result_map in result_map_list:
      if not found:
        for subj in test_equiv_map:
          if result_map.get(subj):
            _merge_maps(result_map, test_equiv_map)
            found = True
            break
    if not found:
      result_map_list.append(test_equiv_map)
    ndx += 1
  result_list_list = []
  for result_map in result_map_list:
    result_list = []
    for subj in result_map.keys():
      result_list.append(subj)
    result_list.sort()
    result_list_list.append(result_list)
  return result_list_list


def _merge_maps(result_map, merge_map):
  for m in merge_map:
    if not result_map.get(m):
      result_map[m] = True


def highest_authority(subject_info, access_policy):
  ''' Returns a list of (highest authority, subject matched, policy matched) '''
  subject_lists = get_equivalent_subjects(subject_info)
  access_map = _create_policy_maps(access_policy)
  return _highest_authority(subject_lists, access_map)


def _highest_authority(subject_lists, access_map):
  blank_policy = access_control.access_control()
  perm_list = list(blank_policy._get_valid_permissions())
  perm_list.reverse() # Permissions are listed lowest first.
  for permission in perm_list:
    permission_map = access_map.get(permission)
    if permission_map:
      if permission_map.get('public'):
        return permission
      for subject_list in subject_lists:
        for subject in subject_list:
          normalized = _normalize_subject(subject)
          if permission_map.get(normalized):
            return permission


def _create_policy_maps(access_policy):
  policy_map = {}
  for allow in access_policy.allow:
    subject_list = allow.subject
    for permission in allow.permission:
      subject_map = policy_map.get(permission)
      if not subject_map:
        subject_map = {}
        policy_map[permission] = subject_map
      for subject in subject_list:
        normalized = _normalize_subject(subject.value())
        subject_map[normalized] = True
        pass # foreach subject
      pass # foreach permission
    pass # foreach allow
  return policy_map
