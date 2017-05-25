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

import logging
import unittest

import d1_common.types.dataoneTypes_v1 as dataoneTypes_v1
import d1_test.instance_generator.access_policy as access_policy

#===============================================================================


class TestAccessPolicy(unittest.TestCase):
  def setUp(self):
    pass

  def test_0010(self):
    """select_random_set_of_permissions()"""
    for i in range(10):
      permissions = access_policy.random_set_of_permissions()
      self.assertTrue(access_policy.permission_labels_to_objects(permissions))

  def test_0020(self):
    """permissions_to_tag_string()"""
    for i in range(10):
      permissions = access_policy.random_set_of_permissions()
      s = access_policy.permissions_to_tag_string(permissions)
      self.assertIsInstance(s, unicode)

  def test_0030(self):
    """random_subject_with_permission_labels()"""
    for i in range(10):
      permissions = access_policy.random_set_of_permissions()
      access_policy.random_subject_with_permission_labels(permissions)

  def test_0040(self):
    """random_subjects_with_permission_labels()"""
    for i in range(100):
      permissions = access_policy.random_set_of_permissions()
      subjects = access_policy.random_subjects_with_permission_labels(
        permissions
      )
      self.assertIsInstance(subjects, list)

  def test_0050(self):
    """generate()"""
    for i in range(10):
      access_policy_pyxb = access_policy.generate()
      self.assertIsInstance(access_policy_pyxb, dataoneTypes_v1.AccessPolicy)
      self.assertTrue(access_policy_pyxb.toxml())


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
