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


def get_equivalent_subjects(subject_info):
  equiv_map_list = []
  for person in subject_info.person:
    subject = _normalize_subject(person.subject.value())
    inner_map = {subject: True}
    equivalent_identity_list = person.equivalentIdentity
    for equivalent_identity in equivalent_identity_list:
      inner_map[_normalize_subject(equivalent_identity.value())] = True
    equiv_map_list.append(inner_map)
  return _flatten_dictionary(equiv_map_list)


def _normalize_subject(subject):
  ''' Clean up white space, capitalize component keys, and set CN first. '''
  new_subject = []
  for component in subject.split(','):
    carray = component.split('=', 2)
    carray[0] = carray[0].upper()
    carray[1] = ' '.join(carray[1].split())
    new_subject.append('='.join(carray))
  if new_subject[0].find("CN=") != 0:
    new_subject.reverse()
  return ','.join(new_subject)


def _flatten_dictionary(equiv_map_list):
  ''' "flatten" equivalancies. '''
  # Go through each disctionary and see if any member is a member of some other.
  result_map_list = [equiv_map_list[0]]
  ndx = 1
  while ndx < len(equiv_map_list):
    equiv_map = equiv_map_list[ndx]
    for result_map in result_map_list:
      for subj in equiv_map:
        if result_map.get(subj):
          _merge_maps(result_map, equiv_map)
          found = True
          break
      if not found:
        result_map_list.append(equiv_map)
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
