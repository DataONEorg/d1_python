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
"""Test access control.
"""

from __future__ import absolute_import

import unittest

import d1_client.mnclient_1_1
import d1_client.mnclient_2_0
#import d1_common.types.dataoneTypes_v1_1 as v1
import d1_common.types.dataoneTypes_v2_0 as v2
import d1_common.const
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.xml
import d1_test.mock_api.django_client as mock_django_client
import gmn.tests.gmn_test_case
import gmn.tests.gmn_test_client
import responses

BASE_URL = 'http://mock/mn'
SCIOBJ_PATH = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_objects'
PROXIED = False
SCIOBJ_URL = 'http://127.0.0.1:8000'


class TestAccessControl(gmn.tests.gmn_test_case.D1TestCase):
  # @classmethod
  # def setUpClass(cls):
  #   pass # d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    mock_django_client.add_callback(BASE_URL)
    self.client_v1 = d1_client.mnclient_1_1.MemberNodeClient_1_1(BASE_URL)
    self.client_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(BASE_URL)
    self.test_client = gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)

  def tearDown(self):
    pass

  @responses.activate
  def test_0010(self):
    """Delete all access policies"""
    client = gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)
    client.delete_all_access_policies()

  @responses.activate
  def test_0040(self):
    """Access is not allowed for submitter"""
    # access_policy = self.gen_access_policy([
    #   ('test_perm_7', 'changePermission'),
    #   ('test_perm_8', 'changePermission'),
    # ])
    # access_policy = self.gen_access_policy([
    #   ('test_perm_7', 'changePermission'),
    #   ('test_perm_8', 'changePermission'),
    # ])

    pid = self.random_pid()
    sid = self.random_sid()

    sciobj, sysmeta_pyxb = self.create(
      self.client_v2,
      v2,
      pid,
      sid,
      submitter='test_submitter',
      rights_holder='test_rights_holder',
      access_rule_list=None,
    )
    print d1_common.xml.pretty_pyxb(sysmeta_pyxb)

    sciobj_str, sysmeta_pyxb = self.get(self.client_v2, pid)

    # client.setAccessPolicy(
    #   pid, access_policy, vendorSpecific=self.session(test_owner_1)
    # )
    #
    # obj = self.test_client.get(pid, vendorSpecific=self.session(test_owner_1))
    # self.assertEqual(obj_str, obj.read())

  @unittest.skip('TODO')
  def test_0050(self):
    """Access is allowed for SUBJECT_TRUSTED."""
    # client =gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)
    # obj = client.get(
    #   pid, vendorSpecific=self.session(d1_common.const.SUBJECT_TRUSTED)
    # )
    # self.assertEqual(obj_str, obj.read())

  @unittest.skip('TODO')
  def test_0060(self):
    """Read access is allowed for subject with exact allow rule."""
    # client =gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)
    # obj = client.get(pid, vendorSpecific=self.session('test_perm_2'))
    # self.assertEqual(obj_str, obj.read())

  @unittest.skip('TODO')
  def test_0070(self):
    """Read access is allowed for subject with higher level access (1)."""
    # client =gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)
    # obj = client.get(pid, vendorSpecific=self.session('test_perm_3'))
    # self.assertEqual(obj_str, obj.read())

  @unittest.skip('TODO')
  def test_0080(self):
    """Read access is allowed for subject with higher level access (2)."""
    # client =gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)
    # obj = client.get(pid, vendorSpecific=self.session('test_perm_5'))
    # self.assertEqual(obj_str, obj.read())

  @unittest.skip('TODO')
  def test_0090(self):
    """Read access is denied for SUBJECT_PUBLIC."""
    # client =gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)
    # self.assertRaises(
    #   d1_common.types.exceptions.NotAuthorized, client.get, pid,
    #   vendorSpecific=self.session(d1_common.const.SUBJECT_PUBLIC)
    # )

  @unittest.skip('TODO')
  def test_0100(self):
    """Read access is denied for regular subject.
    """
    # client =gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)
    # self.assertRaises(
    #   d1_common.types.exceptions.NotAuthorized, client.get, pid,
    #   vendorSpecific=self.session('other_subject')
    # )

  @unittest.skip('TODO')
  def test_0110(self):
    """Update access policy, denying access for old subjects and allowing
    access to new subjects."""
    # client =gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)
    #
    # access_policy = self.gen_access_policy(((('test_perm_7', 'test_perm_8'),
    #                                          ('changePermission',)),))
    #
    # client.setAccessPolicy(
    #   pid, access_policy, vendorSpecific=self.session(test_owner_1)
    # )

  @unittest.skip('TODO')
  def test_0120(self):
    """Access policy is correctly reflected in SysMeta."""
    # client =gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)
    #
    # sysmeta_pyxb = client.getSystemMetadata(
    #   pid, vendorSpecific=self.session(test_owner_1)
    # )
    #
    # self.assertEqual(
    #   sysmeta_pyxb.accessPolicy.allow[0].subject[0].value(), 'test_perm_7'
    # )
    # self.assertEqual(
    #   sysmeta_pyxb.accessPolicy.allow[0].subject[1].value(), 'test_perm_8'
    # )
    # self.assertEqual(
    #   sysmeta_pyxb.accessPolicy.allow[0].permission[0], 'changePermission'
    # )

  @unittest.skip('TODO')
  def test_0130(self):
    """Access now denied for previous subjects."""
    # client =gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)
    # for subject in (
    #     'test_perm_1', 'test_perm_2', 'test_perm_3', 'test_perm_4',
    #     'test_perm_5', 'test_perm_6'
    # ):
    #   self.assertRaises(
    #     d1_common.types.exceptions.NotAuthorized, client.get, pid,
    #     vendorSpecific=self.session(subject)
    #   )

  @unittest.skip('TODO')
  def test_0140(self):
    """Access allowed for current subjects."""
    # client =gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)
    # for subject in ('test_perm_7', 'test_perm_8'):
    #   obj = client.get(pid, vendorSpecific=self.session(subject))
    #   self.assertEqual(obj_str, obj.read())

  @unittest.skip('TODO')
  def test_0150(self):
    """isAuthorized returns access denied for previous subjects."""
    # client =gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)
    # for subject in (
    #     'test_perm_1', 'test_perm_2', 'test_perm_3', 'test_perm_4',
    #     'test_perm_5', 'test_perm_6'
    # ):
    #   self.assertRaises(
    #     d1_common.types.exceptions.NotAuthorized, client.isAuthorized, pid,
    #     'read', vendorSpecific=self.session(subject)
    #   )

  @unittest.skip('TODO')
  def test_0160(self):
    """isAuthorized returns access allowed for current subjects.
    """
    # client =gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)
    # for subject in ('test_perm_7', 'test_perm_8'):
    #   obj = client.isAuthorized(
    #     pid, 'read', vendorSpecific=self.session(subject)
    #   )

  @unittest.skip('TODO')
  def test_0170(self):
    """isAuthorized returns access denied for levels higher than allowed.
    """
    # client =gmn.tests.gmn_test_client.GMNTestClient(BASE_URL)
    # for subject in ('test_perm_7', 'test_perm_8'):
    #   self.assertRaises(
    #     d1_common.types.exceptions.NotAuthorized, client.isAuthorized, pid,
    #     'execute', vendorSpecific=self.session(subject)
    #   )
