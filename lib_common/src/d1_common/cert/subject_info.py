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
"""Extract a set of subjects from a DataONE SubjectInfo structure

Subjects are extracted from the SubjectInfo using the following algorithm:

- Start with empty set of subjects
- Perform recursive search with detection of circular dependencies, starting
  with Subject.
  - If subject is not in set of subjects:
    - Add subject to set of subjects.
    - Search for Person with subject.
      - If Person is found:
        - If the Person has the verified flag:
          - Add "verifiedUser"
        - Iterate over isMemberOf and equivalentIdentity:
          - Recursively add those subjects.
    - Search for Group with Subject.
      - If Group is found:
        - Iterate over hasMember:
          - Recursively add those subjects.
"""

import d1_common.const
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.xml


def extract_subjects(subject_info_xml, primary_str):
  """Extract a set of equivalent and group membership subjects from SubjectInfo

  {primary_str} is a DataONE subject, typically a DataONE compliant
  serialization of the DN of the DataONE X.509 v3 certificate extension from
  which the SubjectInfo was extracted.
  """
  subject_info_pyxb = _deserialize_subject_info(subject_info_xml)
  return _get_subject_info_sets(subject_info_pyxb, primary_str)


def _deserialize_subject_info(subject_info_xml):
  try:
    return d1_common.xml.deserialize(subject_info_xml)
  except ValueError as e:
    raise d1_common.types.exceptions.InvalidToken(
      0, 'Could not deserialize SubjectInfo. subject_info="{}", error="{}"'
      .format(subject_info_xml, str(e))
    )


def _get_subject_info_sets(subject_info_pyxb, primary_str):
  equivalent_set = set()
  _add_subject(equivalent_set, subject_info_pyxb, primary_str)
  return equivalent_set


def _add_subject(equivalent_set, subject_info_pyxb, subject_str):
  if subject_str in equivalent_set:
    return
  equivalent_set.add(subject_str)
  _add_person_subject(equivalent_set, subject_info_pyxb, subject_str)
  _add_group_subject(equivalent_set, subject_info_pyxb, subject_str)


# Person


def _add_person_subject(equivalent_set, subject_info_pyxb, subject_str):
  person_pyxb = _find_person_by_subject(subject_info_pyxb, subject_str)
  if not person_pyxb:
    return
  _if_person_is_verified_add_symbolic_subject(equivalent_set, person_pyxb)
  _add_person_is_member_of(equivalent_set, subject_info_pyxb, person_pyxb)
  _add_person_equivalent_subjects(
    equivalent_set, subject_info_pyxb, person_pyxb
  )


def _find_person_by_subject(subject_info_pyxb, subject_str):
  for person_pyxb in subject_info_pyxb.person:
    if person_pyxb.subject.value() == subject_str:
      return person_pyxb


def _add_person_is_member_of(equivalent_set, subject_info_pyxb, person_pyxb):
  for is_member_of in person_pyxb.isMemberOf:
    _add_subject(equivalent_set, subject_info_pyxb, is_member_of.value())


def _add_person_equivalent_subjects(
    equivalent_set, subject_info_pyxb, person_pyxb
):
  for equivalent_pyxb in person_pyxb.equivalentIdentity:
    _add_subject(equivalent_set, subject_info_pyxb, equivalent_pyxb.value())


def _if_person_is_verified_add_symbolic_subject(equivalent_set, person_pyxb):
  if person_pyxb.verified:
    equivalent_set.add(d1_common.const.SUBJECT_VERIFIED)


# Group


def _add_group_subject(equivalent_set, subject_info_pyxb, subject_str):
  group_pyxb = _find_group_by_subject(subject_info_pyxb, subject_str)
  if group_pyxb:
    _add_members(equivalent_set, subject_info_pyxb, group_pyxb)


def _find_group_by_subject(subject_info_pyxb, subject_str):
  for group_pyxb in subject_info_pyxb.group:
    if group_pyxb.subject.value() == subject_str:
      return group_pyxb


def _add_members(equivalent_set, subject_info_pyxb, group_pyxb):
  for member_pyxb in group_pyxb.hasMember:
    _add_subject(equivalent_set, subject_info_pyxb, member_pyxb.value())
