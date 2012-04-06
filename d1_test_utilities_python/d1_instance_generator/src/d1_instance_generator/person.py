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
Module d1_instance_generator.person
===================================

:Synopsis: Generate random Person objects.
:Created: 2011-12-08
:Author: DataONE (Dahl)
'''

# Stdlib.
import random

# D1.
from d1_common.types.generated import dataoneTypes

# App.
import dates
import random_data
import subject


def generate():
  person = dataoneTypes.Person()
  person.subject = subject.generate()
  for i in range(random.randint(1, 3)):
    person.givenName.append('givenName_' + random_data.random_word())
  person.familyName = 'familyName_' + random_data.random_word()
  for i in range(random.randint(1, 3)):
    person.email.append(random_data.random_email())
  for i in range(random.randint(1, 3)):
    person.isMemberOf.append('isMemberOf_' + random_data.random_word())
  for i in range(random.randint(1, 3)):
    person.equivalentIdentity.append('equivalentIdentity_' + random_data.random_word())
  person.verified = random_data.random_bool()
  return person
