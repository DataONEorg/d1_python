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

import d1_test.d1_test_case
import d1_test.instance_generator.access_policy as access_policy

#===============================================================================


@d1_test.d1_test_case.reproducible_random_decorator('TestAccessPolicy')
class TestAccessPolicy(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """select_random_set_of_permissions()"""
    permissions = access_policy.random_set_of_permissions()
    self.sample.assert_equals(
      permissions, 'inst_gen_select_random_set_of_permissions'
    )

  def test_1010(self):
    """permissions_to_tag_string()"""
    permissions = access_policy.random_set_of_permissions()
    s = access_policy.permissions_to_tag_string(permissions)
    self.sample.assert_equals(s, 'inst_gen_permissions_to_tag_string')

  def test_1020(self):
    """random_subject_with_permission_labels()"""
    permissions = access_policy.random_set_of_permissions()
    s = access_policy.random_subject_with_permission_labels(permissions)
    self.sample.assert_equals(
      s, 'inst_gen_random_subject_with_permission_labels'
    )

  def test_1030(self):
    """random_subjects_with_permission_labels()"""
    permissions = access_policy.random_set_of_permissions()
    subjects = access_policy.random_subject_list_with_permission_labels(
      permissions
    )
    self.sample.assert_equals(
      subjects, 'inst_gen_random_subjects_with_permission_labels'
    )

  def test_1040(self):
    """generate()"""
    access_policy_pyxb = access_policy.generate()
    self.sample.assert_equals(access_policy_pyxb, 'inst_gen_generate')

  def test_1050(self):
    """random_subject_list()"""
    subject_list = access_policy.random_subject_list()
    self.sample.assert_equals(subject_list, 'inst_gen_random_subject_list')
