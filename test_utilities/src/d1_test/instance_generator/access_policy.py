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
"""Generate random AccessPolicy

Generates an AccessPolicy instance that is essentially random though conforms to
the following rules:

1. Subjects are selected at random from a set of 1000 values

2. If the subject contains the string "_group_" it is considered to be a group
of subjects rather than an individual

3. Access rules are assigned by the presence of the strings "_read_", "_write_",
"_execute_", and "_changePermission_".

This approach for construction allows verification of the rules through a
mechanism independent of the normal access policy evaluation process for testing
purposes.

For example, an <allow> clause that contains any subject with the string
"_read_" in it, should also contain the read permission entry.
"""

import random

import d1_common.types.dataoneTypes

import d1_test.d1_test_case
import d1_test.instance_generator.random_data

# Map between permission labels and permissions.
PERMISSIONS = {
  'read': d1_common.types.dataoneTypes.Permission.read,
  'write': d1_common.types.dataoneTypes.Permission.write,
  'changePermission': d1_common.types.dataoneTypes.Permission.changePermission,
}


def random_set_of_permissions():
  return random.sample(
    sorted(PERMISSIONS.keys()), random.randint(1, len(PERMISSIONS) - 1)
  )


def permission_labels_to_objects(permissions):
  permission_objects = []
  for permission in permissions:
    permission_objects.append(PERMISSIONS[permission])
  return permission_objects


def permissions_to_tag_string(permissions):
  return '_' + '_'.join(permissions) + '_'


def random_subject_with_permission_labels(permissions, group_chance=0.1):
  """Generate a random subject that is tagged with the provided permissions
  and has a certain chance of being tagged as group
  """
  subject_base = 'subj_{}'.format(
    d1_test.instance_generator.random_data.random_lower_ascii()
  )
  group = '_group' if random.random() <= group_chance else ''
  tags = permissions_to_tag_string(permissions)
  return subject_base + group + tags


def random_subject_list_with_permission_labels(
    permissions, min_len=1, max_len=100, group_chance=0.1
):
  subjects = []
  for i in range(random.randint(min_len, max_len)):
    subject = random_subject_with_permission_labels(permissions, group_chance)
    subjects.append(subject)
  return subjects


def random_subject_list(min_len=1, max_len=10, group_chance=0.1):
  return [
    'subj_{}{}'.format(
      d1_test.instance_generator.random_data.random_lower_ascii(),
      '_group' if random.random() <= group_chance else '',
    ) for _ in range(random.randint(min_len, max_len))
  ]


def generate(min_rules=1, max_rules=5, max_subjects=5):
  """Generate a random access policy document
  """
  n_rules = random.randint(min_rules, max_rules)
  if not n_rules:
    return None
  ap = d1_common.types.dataoneTypes.accessPolicy()
  rules = []
  for i in range(0, n_rules):
    ar = d1_common.types.dataoneTypes.accessRule()
    permissions = random_set_of_permissions()
    ar.subject = random_subject_list(max_len=max_subjects)
    ar.permission = permissions
    rules.append(ar)
  ap.allow = rules
  return ap


def generate_from_permission_list(client, permission_list):
  if permission_list is None:
    return None
  access_policy_pyxb = client.bindings.accessPolicy()
  for subject_list, action_list in permission_list:
    subject_list = d1_test.d1_test_case.D1TestCase.expand_subjects(subject_list)
    action_list = list(action_list)
    access_rule_pyxb = client.bindings.AccessRule()
    for subject_str in subject_list:
      access_rule_pyxb.subject.append(subject_str)
    for action_str in action_list:
      permission_pyxb = client.bindings.Permission(action_str)
      access_rule_pyxb.permission.append(permission_pyxb)
    access_policy_pyxb.append(access_rule_pyxb)
  return access_policy_pyxb
