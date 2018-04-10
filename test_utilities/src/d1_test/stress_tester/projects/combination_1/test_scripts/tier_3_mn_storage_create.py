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
"""
:mod:`tier_3_mn_storage_create`
===============================

:Created: 2011-04-22
:Author: DataONE (Dahl)
"""

import random
import string

import settings
import transaction

import d1_common.types.dataoneTypes as dataoneTypes

from d1_test.instance_generator import random_data
from d1_test.instance_generator import system_metadata

# Config

# The number of bytes in each science object.
N_SCI_OBJ_BYTES = 1024

# The number of subjects to allow access to each created test object.
N_SUBJECTS = 10

# Chance, in percent, that an object is created with public access.
PUBLIC_ACCESS_PERCENT = 25.0


class Transaction(transaction.Transaction):
  def __init__(self):
    super().__init__()

  def d1_mn_api_call(self):
    """MNStorage.create()"""
    sci_obj = self.create_science_object()
    subjects = self.get_random_subjects(PUBLIC_ACCESS_PERCENT, N_SUBJECTS)
    access_policy = self.create_access_policy(subjects)
    sys_meta = self.create_system_metadata(sci_obj, access_policy)
    client = self.create_client_for_subject(
      settings.SUBJECT_WITH_CREATE_PERMISSIONS
    )
    response = client.createResponse(
      sys_meta.identifier.value(), sci_obj, sys_meta
    )
    self.check_response(response)

  def create_science_object(self):
    return random_data.random_bytes_file(N_SCI_OBJ_BYTES)

  def create_system_metadata(self, sci_obj, access_policy):
    return system_metadata.generate_from_file(
      sci_obj, {
        'identifier': self.generate_random_ascii_pid(),
        'accessPolicy': access_policy,
        'rightsHolder': self.select_random_subject(),
      }
    )

  def create_access_policy(self, subjects):
    ap = dataoneTypes.AccessPolicy()
    ar = dataoneTypes.AccessRule()
    ar.subject = subjects
    ar.permission = ['changePermission']
    ap.allow.append(ar)
    return ap

  def generate_random_ascii_pid(self):
    return ''.join(
      random.
      choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
      for x in range(10)
    )


if __name__ == '__main__':
  t = Transaction()
  t.run()
  #import cProfile
  #cProfile.run('t.run()', 'profile')
