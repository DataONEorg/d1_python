#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
Module d1_instance_generator.tests.test_access_policy
=====================================================

:Synopsis: Unit tests for random access policy generator.
:Created: 2011-12-05
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import os
import sys
import unittest
import uuid
import StringIO

# D1.
import d1_common.types.generated.dataoneTypes_v1 as dataoneTypes_v1
import d1_common.const
import d1_common.testcasewithurlcompare
import d1_common.types.exceptions
import d1_common.xmlrunner

# App.
sys.path.append('../generator/')
import accesspolicy

#===============================================================================


class TestAccessPolicy(d1_common.testcasewithurlcompare.TestCaseWithURLCompare):
  def setUp(self):
    pass

  def test_010(self):
    '''select_random_set_of_permissions()'''
    for i in range(10):
      permissions = accesspolicy.random_set_of_permissions()
      self.assertTrue(accesspolicy.permission_labels_to_objects(permissions))

  def test_020(self):
    '''permissions_to_tag_string()'''
    for i in range(10):
      permissions = accesspolicy.random_set_of_permissions()
      s = accesspolicy.permissions_to_tag_string(permissions)
      self.assertTrue(isinstance(s, unicode))

  def test_030(self):
    '''random_subject_with_permission_labels()'''
    for i in range(10):
      permissions = accesspolicy.random_set_of_permissions()
      subject = accesspolicy.random_subject_with_permission_labels(permissions)

  def test_040(self):
    '''random_subjects_with_permission_labels()'''
    for i in range(100):
      permissions = accesspolicy.random_set_of_permissions()
      subjects = accesspolicy.random_subjects_with_permission_labels(permissions)
      self.assertTrue(isinstance(subjects, list))

  def test_050(self):
    '''generate()'''
    for i in range(10):
      access_policy = accesspolicy.generate()
      self.assertTrue(isinstance(access_policy, dataoneTypes_v1.AccessPolicy))
      self.assertTrue(access_policy.toxml())


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
