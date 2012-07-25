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
:mod:`tier_3_mn_storage_create`
===============================

:Created: 2011-04-22
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Std.
import os
import sys

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes

import d1_instance_generator
import d1_instance_generator.random_data
import d1_instance_generator.systemmetadata
import d1_instance_generator.accesspolicy

# App.
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
sys.path.append(_here('../../../shared/'))
import settings
import subject_dn
import transaction

# Config

# The number of bytes in each science object.
N_SCI_OBJ_BYTES = 1024

# The number of subjects to allow access to each created test object.
N_ALLOW_ACCESS = 10


class Transaction(transaction.Transaction):
  def __init__(self):
    super(Transaction, self).__init__()

  def d1_mn_api_call(self):
    '''MNStorage.create()'''
    sci_obj = self.create_science_object()
    subjects = self.create_list_of_random_subjects(N_ALLOW_ACCESS)
    access_policy = self.create_access_policy(subjects)
    sys_meta = self.create_system_metadata(sci_obj, access_policy)
    client = self.create_client_for_subject(settings.SUBJECT_WITH_CREATE_PERMISSIONS)
    response = client.createResponse(sys_meta.identifier.value(), sci_obj, sys_meta)
    self.check_response(response)

  def create_science_object(self):
    return d1_instance_generator.random_data.random_bytes_flo(N_SCI_OBJ_BYTES)

  def create_system_metadata(self, sci_obj, access_policy):
    return d1_instance_generator.systemmetadata.generate_from_flo(
      sci_obj, {'accessPolicy': access_policy}
    )

  def create_access_policy(self, subjects):
    ap = dataoneTypes.AccessPolicy()
    ar = dataoneTypes.AccessRule()
    for subject in subjects:
      ar.subject.append(
        subject_dn.get_dataone_compliant_dn_serialization_by_subject(subject)
      )
      ar.permission = ['changePermission']
    ap.allow.append(ar)
    return ap


if __name__ == '__main__':
  t = Transaction()
  t.run()
  #import cProfile
  #cProfile.run('t.run()', 'profile')
