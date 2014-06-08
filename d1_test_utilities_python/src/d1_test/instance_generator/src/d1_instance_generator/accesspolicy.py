#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2011
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
Module d1_instance_generator.accesspolicy
=========================================

:Synopsis:
  Generates an AccessPolicy instance that is essentially random though conforms
  to the following rules:
  
  1. Subjects are selected at random from a set of 1000 values
  
  2. If the subject contains the string "_group_" it is considered to be a group
  of subjects rather than an individual
  
  3. Access rules are assigned by the presence of the strings "_read_",
  "_write_", "_execute_", and "_changePermission_".
  
  This approach for construction allows verification of the rules through a
  mechanism independent of the normal access policy evaluation process for
  testing purposes.
  
  For example, an <allow> clause that contains any subject with the string
  "_read_" in it, should also contain the read permission entry.
:Created: 2011-08-02
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import random

# D1.
from d1_common.types.generated import dataoneTypes

# App.
import random_data

# Map between permission labels and permissions.
PERMISSIONS = {
  u'read': dataoneTypes.Permission.read,
  u'write': dataoneTypes.Permission.write,
  u'changePermission': dataoneTypes.Permission.changePermission,
}


def random_set_of_permissions():
  return random.sample(PERMISSIONS.keys(), random.randint(1, len(PERMISSIONS) - 1))


def permission_labels_to_objects(permissions):
  permission_objects = []
  for permission in permissions:
    permission_objects.append(PERMISSIONS[permission])
  return permission_objects


def permissions_to_tag_string(permissions):
  return '_' + '_'.join(permissions) + '_'


def random_subject_with_permission_labels(permissions, group_chance=0.1):
  '''Generate a random subject that is tagged with the provided permissions
  and has a certain chance of being tagged as group
  '''
  subject_base = random_data.random_3_words()
  tags = permissions_to_tag_string(permissions)
  group = '_group_' if random.random() <= group_chance else ''
  return subject_base + group + tags


def random_subjects_with_permission_labels(permissions, min=1, max=100, group_chance=0.1):
  subjects = []
  for i in xrange(random.randint(min, max)):
    subject = random_subject_with_permission_labels(permissions, group_chance)
    subjects.append(subject)
  return subjects


def generate(min_rules=1, max_rules=5, max_subjects=5):
  '''Generate a random access policy document.
  '''
  ap = dataoneTypes.AccessPolicy()
  n_rules = random.randint(min_rules, max_rules)
  rules = []
  for i in xrange(0, n_rules):
    ar = dataoneTypes.AccessRule()
    permissions = random_set_of_permissions()
    ar.subject = random_subjects_with_permission_labels(permissions, max=max_subjects)
    ar.permission = permissions
    rules.append(ar)
  ap.allow = rules
  return ap
