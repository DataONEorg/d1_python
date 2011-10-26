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
'''Module gmn.tests.test_access_control
=======================================

Unit tests for GMN access control.

:Created: 2011-06-27
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import datetime
import hashlib
import random
import unittest2
import logging
#from d1_client import cnclient
#import d1_common.types.exceptions
import xml.parsers.expat

# MN API.
try:
  import d1_common.types.generated.dataoneTypes as dataoneTypes
  import d1_common.types.exceptions
  import d1_common.const
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/api-common-python/src/d1_common\n'
  )
  raise
try:
  import d1_client
  import d1_client.systemmetadata
  import d1_common.xml_compare
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/itk/d1-python/src/d1_client\n'
  )
  raise

# Test.
import test_context as context
import gmn_test_client


class TestAccessControl(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def gen_sysmeta(self, pid, size, md5, now, owner):
    sysmeta = dataoneTypes.systemMetadata()
    sysmeta.identifier = pid
    sysmeta.objectFormat = 'eml://ecoinformatics.org/eml-2.0.0'
    sysmeta.size = size
    sysmeta.submitter = owner
    sysmeta.rightsHolder = owner
    sysmeta.checksum = dataoneTypes.checksum(md5)
    sysmeta.checksum.algorithm = 'MD5'
    sysmeta.dateUploaded = now
    sysmeta.dateSysMetadataModified = now
    sysmeta.originMemberNode = 'MN1'
    sysmeta.authoritativeMemberNode = 'MN1'
    return sysmeta

  def gen_access_policy(self, access_rules):
    accessPolicy = dataoneTypes.accessPolicy()
    for access_rule in access_rules:
      accessRule = dataoneTypes.AccessRule()
      for subject in access_rule[0]:
        accessRule.subject.append(subject)
      for action in access_rule[1]:
        permission_obj = dataoneTypes.Permission(action)
        accessRule.permission.append(permission_obj)
      accessRule.resource.append('<dummy. field will be removed>')
      accessPolicy.append(accessRule)
    return accessPolicy

  def session(self, subject):
    return {'VENDOR_OVERRIDE_SESSION': subject}

  def test_010_prepare(self):
    context.gmn_url = 'http://0.0.0.0:8000/'
    context.test_pid = 'test_obj_1'
    context.test_owner_1 = 'test_owner_1'

    client = gmn_test_client.GMNTestClient(context.gmn_url)

    # Delete all permissions.
    client.delete_all_access_rules(headers=self.session(d1_common.const.SUBJECT_TRUSTED))

    # Delete the test object.
    client.test_delete_single_object(context.test_pid)

    # Verify that the test object no longer exists.
    self.assertRaises(xml.parsers.expat.ExpatError, client.describe, context.test_pid)

    # Create object containing random bytes.
    context.obj_str = "".join(chr(random.randrange(0, 255)) for i in xrange(1024))

    # Create sysmeta.
    context.sysmeta = self.gen_sysmeta(
      context.test_pid,
      1024,
      hashlib.md5(context.obj_str).hexdigest(),
      datetime.datetime.now(),
      owner=context.test_owner_1
    )

    # Create an access policy.
    context.access_policy = self.gen_access_policy(
      (
        (('test_perm_1', 'test_perm_2'), ('read', )),
        (('test_perm_3', 'test_perm_4'), ('write', 'changePermission')),
        (('test_perm_5', 'test_perm_6'), ('execute', )),
      )
    )

  def test_020_create(self):
    '''Create object with access policy.
    '''

    client = gmn_test_client.GMNTestClient(context.gmn_url)

    # Add the access policy to the SysMeta.
    context.sysmeta.accessPolicy = context.access_policy

    # POST the new object to MN.
    response = client.createResponse(
      pid=context.test_pid,
      obj=context.obj_str,
      sysmeta=context.sysmeta,
      vendorSpecific=self.session(context.test_owner_1)
    )

  def test_030_read_by_owner(self):
    '''Access is allowed for owner.
    '''
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    obj = client.get(context.test_pid, vendorSpecific=self.session(context.test_owner_1))
    self.assertEqual(context.obj_str, obj.read())

  def test_040_read_by_trusted(self):
    '''Access is allowed for SUBJECT_TRUSTED.
    '''
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    obj = client.get(
      context.test_pid,
      vendorSpecific=self.session(d1_common.const.SUBJECT_TRUSTED)
    )
    self.assertEqual(context.obj_str, obj.read())

  def test_050_read_by_permitted_subject_with_exact_rule(self):
    '''Access is allowed for subject with exact allow rule.
    '''
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    obj = client.get(context.test_pid, vendorSpecific=self.session('test_perm_2'))
    self.assertEqual(context.obj_str, obj.read())

  def test_060_read_by_permitted_subject_with_higher_level_rule_1(self):
    '''Access is allowed for subject with higher level access (1).
    '''
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    obj = client.get(context.test_pid, vendorSpecific=self.session('test_perm_3'))
    self.assertEqual(context.obj_str, obj.read())

  def test_070_read_by_permitted_subject_with_higher_level_rule_2(self):
    '''Access is allowed for subject with higher level access (2).
    '''
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    obj = client.get(context.test_pid, vendorSpecific=self.session('test_perm_5'))
    self.assertEqual(context.obj_str, obj.read())

  def test_080_read_by_public(self):
    '''Access is denied for SUBJECT_PUBLIC.
    '''
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    self.assertRaises(
      d1_common.types.exceptions.NotAuthorized,
      client.get,
      context.test_pid,
      vendorSpecific=self.session(d1_common.const.SUBJECT_PUBLIC)
    )

  def test_090_read_by_regular_subject(self):
    '''Access is denied for regular subject.
    '''
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    self.assertRaises(
      d1_common.types.exceptions.NotAuthorized,
      client.get,
      context.test_pid,
      vendorSpecific=self.session('other_subject')
    )

  def test_200_update_access_policy(self):
    '''Update access policy, denying access for old subjects and allowing
    access to new subjects.
    '''
    client = gmn_test_client.GMNTestClient(context.gmn_url)

    access_policy = self.gen_access_policy(
      (
        (('test_perm_7', 'test_perm_8'), ('changePermission', )),
      )
    )

    client.setAccessPolicy(
      context.test_pid,
      access_policy,
      vendorSpecific=self.session(context.test_owner_1)
    )

  def test_210_check_sysmeta_sync(self):
    '''Access policy is correctly reflected in SysMeta.
    '''
    client = gmn_test_client.GMNTestClient(context.gmn_url)

    sysmeta = client.getSystemMetadata(
      context.test_pid,
      vendorSpecific=self.session(context.test_owner_1)
    )

    self.assertEqual(sysmeta.accessPolicy.allow[0].subject[0].value(), 'test_perm_7')
    self.assertEqual(sysmeta.accessPolicy.allow[0].subject[1].value(), 'test_perm_8')
    self.assertEqual(sysmeta.accessPolicy.allow[0].permission[0], 'changePermission')

  def test_220_access_denied_for_previous_subjects(self):
    '''Access now denied for previous subjects.
    '''
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    for subject in (
      'test_perm_1', 'test_perm_2', 'test_perm_3', 'test_perm_4', 'test_perm_5',
      'test_perm_6'
    ):
      self.assertRaises(
        d1_common.types.exceptions.NotAuthorized,
        client.get,
        context.test_pid,
        vendorSpecific=self.session(subject)
      )

  def test_220_access_allowed_for_current_subjects(self):
    '''Access allowed for current subjects.
    '''
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    for subject in ('test_perm_7', 'test_perm_8'):
      obj = client.get(context.test_pid, vendorSpecific=self.session(subject))
      self.assertEqual(context.obj_str, obj.read())

  def test_300_is_authorized_denied(self):
    '''isAuthorized returns access denied for previous subjects.
    '''
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    for subject in (
      'test_perm_1', 'test_perm_2', 'test_perm_3', 'test_perm_4', 'test_perm_5',
      'test_perm_6'
    ):
      self.assertRaises(
        d1_common.types.exceptions.NotAuthorized,
        client.isAuthorized,
        context.test_pid,
        'read',
        vendorSpecific=self.session(subject)
      )

  def test_310_is_authorized_allowed(self):
    '''isAuthorized returns access allowed for current subjects.
    '''
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    for subject in ('test_perm_7', 'test_perm_8'):
      obj = client.isAuthorized(
        context.test_pid, 'read',
        vendorSpecific=self.session(subject)
      )

  def test_320_is_authorized_denied_higher(self):
    '''isAuthorized returns access denied for levels higher than allowed.
    '''
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    for subject in ('test_perm_7', 'test_perm_8'):
      self.assertRaises(
        d1_common.types.exceptions.NotAuthorized,
        client.isAuthorized,
        context.test_pid,
        'execute',
        vendorSpecific=self.session(subject)
      )


if __name__ == "__main__":
  import sys
  #from node_test_common import loadTestInfo, initMain
  #unittest.main(argv=sys.argv, verbosity=2)
  suite = unittest.TestLoader().loadTestsFromTestCase(TestAccessControl)
  unittest.TextTestRunner(verbosity=2).run(suite)
