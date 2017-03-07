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

# Stdlib.
import unittest

# Django
import django.test

# D1.
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.const
import d1_common.xml

# App.
import tests.gmn_test_client

GMN_URL = 'http://127.0.0.1:8000'
SCIOBJ_PATH = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_objects'
PROXIED = False
SCIOBJ_URL = 'http://127.0.0.1:8000'


class TestAccessControl(django.test.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def _gen_sysmeta(self, pid, size, md5, now, owner):
    sysmeta_pyxb = d1_common.types.dataoneTypes.systemMetadata()
    sysmeta_pyxb.identifier = pid
    sysmeta_pyxb.objectFormat = 'eml://ecoinformatics.org/eml-2.0.0'
    sysmeta_pyxb.size = size
    sysmeta_pyxb.submitter = owner
    sysmeta_pyxb.rightsHolder = owner
    sysmeta_pyxb.checksum = d1_common.types.dataoneTypes.checksum(md5)
    sysmeta_pyxb.checksum.algorithm = 'MD5'
    sysmeta_pyxb.dateUploaded = now
    sysmeta_pyxb.dateSysMetadataModified = now
    sysmeta_pyxb.originMemberNode = 'MN1'
    sysmeta_pyxb.authoritativeMemberNode = 'MN1'
    return sysmeta_pyxb

  def gen_access_policy(self, rules):
    access_policy = d1_common.types.dataoneTypes.accessPolicy()
    for rule in rules:
      subjects = rule[0]
      actions = rule[1]
      access_rule = d1_common.types.dataoneTypes.AccessRule()
      for subject in subjects:
        access_rule.subject.append(subject)
      for action in actions:
        permission = d1_common.types.dataoneTypes.Permission(action)
        access_rule.permission.append(permission)
      access_policy.append(access_rule)
    return access_policy

  def _set_access_policy(self, pid, access_rules):
    access_policy = self.gen_access_policy(access_rules)
    client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    client.set_access_policy(pid, access_policy)

  @unittest.skip('TODO')
  def test_010(self):
    """Delete all access policies"""
    client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    client.delete_all_access_policies()

  @unittest.skip('TODO')
  def test_get_access_policy(self):
    pid = 'AnserMatrix.htm'
    client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    response = client.get_access_policy(pid)
    self.assertEqual(
      response, '<?xml version="1.0" ?><accessPolicy><allow>'
      '<subject>8920_skye_fondled</subject><subject>public</subject>'
      '<subject>folding_5087</subject>'
      '<permission>read</permission></allow></accessPolicy>'
    )

  @unittest.skip('TODO')
  def test_020(self):
    """Set access policy"""
    pid = 'AnserMatrix.htm'
    rules = ((('test_perm_1', 'test_perm_2'), ('read',)),
             (('test_perm_3', 'test_perm_4'), ('write', 'changePermission')),)
    self._set_access_policy(pid, rules)

  #  @unittest.skip('TODO')
  #  def test_020(self):
  #    """Create object with access policy.
  #    """
  #    client = gmn_test_client.GMNTestClient(GMN_URL)
  #
  #    # Add the access policy to the SysMeta.
  #    sysmeta_pyxb.accessPolicy = access_policy
  #
  #    # POST the new object to MN.
  #    response = client.createResponse(pid=pid,
  #      obj=obj_str, sysmeta_pyxb=sysmeta_pyxb,
  #      vendorSpecific=self.session(test_owner_1))

  @unittest.skip('TODO')
  def test_030(self):
    """Access is allowed for owner."""
    # client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    # obj = client.get(pid, vendorSpecific=self.session(test_owner_1))
    # self.assertEqual(obj_str, obj.read())

  @unittest.skip('TODO')
  def test_040(self):
    """Access is allowed for SUBJECT_TRUSTED."""
    # client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    # obj = client.get(
    #   pid, vendorSpecific=self.session(d1_common.const.SUBJECT_TRUSTED)
    # )
    # self.assertEqual(obj_str, obj.read())

  @unittest.skip('TODO')
  def test_050(self):
    """Read access is allowed for subject with exact allow rule."""
    # client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    # obj = client.get(pid, vendorSpecific=self.session('test_perm_2'))
    # self.assertEqual(obj_str, obj.read())

  @unittest.skip('TODO')
  def test_060(self):
    """Read access is allowed for subject with higher level access (1)."""
    # client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    # obj = client.get(pid, vendorSpecific=self.session('test_perm_3'))
    # self.assertEqual(obj_str, obj.read())

  @unittest.skip('TODO')
  def test_070(self):
    """Read access is allowed for subject with higher level access (2)."""
    # client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    # obj = client.get(pid, vendorSpecific=self.session('test_perm_5'))
    # self.assertEqual(obj_str, obj.read())

  @unittest.skip('TODO')
  def test_080(self):
    """Read access is denied for SUBJECT_PUBLIC."""
    # client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    # self.assertRaises(
    #   d1_common.types.exceptions.NotAuthorized, client.get, pid,
    #   vendorSpecific=self.session(d1_common.const.SUBJECT_PUBLIC)
    # )

  @unittest.skip('TODO')
  def test_090(self):
    """Read access is denied for regular subject.
    """
    # client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    # self.assertRaises(
    #   d1_common.types.exceptions.NotAuthorized, client.get, pid,
    #   vendorSpecific=self.session('other_subject')
    # )

  @unittest.skip('TODO')
  def test_200(self):
    """Update access policy, denying access for old subjects and allowing
    access to new subjects."""
    # client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    #
    # access_policy = self.gen_access_policy(((('test_perm_7', 'test_perm_8'),
    #                                          ('changePermission',)),))
    #
    # client.setAccessPolicy(
    #   pid, access_policy, vendorSpecific=self.session(test_owner_1)
    # )

  @unittest.skip('TODO')
  def test_210(self):
    """Access policy is correctly reflected in SysMeta."""
    # client = tests.gmn_test_client.GMNTestClient(GMN_URL)
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
  def test_220(self):
    """Access now denied for previous subjects."""
    # client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    # for subject in (
    #     'test_perm_1', 'test_perm_2', 'test_perm_3', 'test_perm_4',
    #     'test_perm_5', 'test_perm_6'
    # ):
    #   self.assertRaises(
    #     d1_common.types.exceptions.NotAuthorized, client.get, pid,
    #     vendorSpecific=self.session(subject)
    #   )

  @unittest.skip('TODO')
  def test_230(self):
    """Access allowed for current subjects."""
    # client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    # for subject in ('test_perm_7', 'test_perm_8'):
    #   obj = client.get(pid, vendorSpecific=self.session(subject))
    #   self.assertEqual(obj_str, obj.read())

  @unittest.skip('TODO')
  def test_300(self):
    """isAuthorized returns access denied for previous subjects."""
    # client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    # for subject in (
    #     'test_perm_1', 'test_perm_2', 'test_perm_3', 'test_perm_4',
    #     'test_perm_5', 'test_perm_6'
    # ):
    #   self.assertRaises(
    #     d1_common.types.exceptions.NotAuthorized, client.isAuthorized, pid,
    #     'read', vendorSpecific=self.session(subject)
    #   )

  @unittest.skip('TODO')
  def test_310(self):
    """isAuthorized returns access allowed for current subjects.
    """
    # client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    # for subject in ('test_perm_7', 'test_perm_8'):
    #   obj = client.isAuthorized(
    #     pid, 'read', vendorSpecific=self.session(subject)
    #   )

  @unittest.skip('TODO')
  def test_320(self):
    """isAuthorized returns access denied for levels higher than allowed.
    """
    # client = tests.gmn_test_client.GMNTestClient(GMN_URL)
    # for subject in ('test_perm_7', 'test_perm_8'):
    #   self.assertRaises(
    #     d1_common.types.exceptions.NotAuthorized, client.isAuthorized, pid,
    #     'execute', vendorSpecific=self.session(subject)
    #   )
