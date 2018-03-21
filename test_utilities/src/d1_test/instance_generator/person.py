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
"""Generate random Person
"""

import random

import d1_common.types.dataoneTypes_v1

import d1_test.instance_generator.random_data
import d1_test.instance_generator.subject


def generate():
  person = d1_common.types.dataoneTypes_v1.person()
  person.subject = d1_test.instance_generator.subject.generate()
  for i in range(random.randint(1, 3)):
    person.givenName.append(
      'givenName_' + d1_test.instance_generator.random_data.random_lower_ascii()
    )
  person.familyName = 'familyName_' + d1_test.instance_generator.random_data.random_lower_ascii(
  )
  for i in range(random.randint(1, 3)):
    person.email.append(d1_test.instance_generator.random_data.random_email())
  for i in range(random.randint(1, 3)):
    person.isMemberOf.append(
      'isMemberOf_' + d1_test.instance_generator.random_data.random_lower_ascii()
    )
  for i in range(random.randint(1, 3)):
    person.equivalentIdentity.append(
      'equivalentIdentity_' +
      d1_test.instance_generator.random_data.random_lower_ascii()
    )
  person.verified = d1_test.instance_generator.random_data.random_bool()
  return person
