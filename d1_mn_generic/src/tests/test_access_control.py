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
'''Module gmn.tests.test_access_control
=======================================

Unit tests for GMN access control.

:Created: 2011-06-27
:Author: DataONE (Dahl)
'''

# Stdlib.
import datetime
import hashlib
import logging
import random
import sys
import unittest2
import xml.parsers.expat

# D1.
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

# from d1_client import cnclient
# import d1_common.types.exceptions

# App.
import test_context as context
import gmn_test_client


class options():
  def __init__(self):
    self.gmn_url = 'http://127.0.0.1:8000'
    self.obj_path = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_objects'
    self.wrapped = False
    self.obj_url = 'http://127.0.0.1:8000'


class TestAccessControl(unittest2.TestCase):
  def setUp(self):
    self.options = options()

  def tearDown(self):
    pass

  def session(self, subject):
    return {'VENDOR_INCLUDE_SUBJECTS': subject}

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

  def gen_access_policy(self, rules):
    access_policy = dataoneTypes.accessPolicy()
    for rule in rules:
      subjects = rule[0]
      actions = rule[1]
      access_rule = dataoneTypes.AccessRule()
      for subject in subjects:
        access_rule.subject.append(subject)
      for action in actions:
        permission = dataoneTypes.Permission(action)
        access_rule.permission.append(permission)
      access_policy.append(access_rule)
    return access_policy

  def _set_access_policy(self, pid, access_rules):
    access_policy = self.gen_access_policy(access_rules)
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    client.set_access_policy(pid, access_policy)

  def test_010(self):
    '''Delete all access policies'''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    client.delete_all_access_policies()

  def test_get_access_policy(self):
    pid = 'AnserMatrix.htm'
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    response = client.get_access_policy(pid)
    self.assertEqual(
      response,
      '''<?xml version="1.0" ?><accessPolicy><allow><subject>8920_skye_fondled</subject><subject>public</subject><subject>folding_5087</subject><permission>read</permission></allow></accessPolicy>'''
    )

  #  def _test(self):
  #    # Delete the test object.
  #    client.test_delete_single_object(context.pid)
  #
  #    # Verify that the test object no longer exists.
  #    self.assertRaises(xml.parsers.expat.ExpatError, client.describe, context.pid)
  #
  #    # Create object containing random bytes.
  #    context.obj_str = "".join(chr(random.randrange(0, 255)) for i in xrange(1024))
  #
  #    # Create sysmeta.
  #    context.sysmeta = self.gen_sysmeta(
  #      context.pid, 1024,
  #      hashlib.md5(context.obj_str).hexdigest(),
  #      datetime.datetime.now(),
  #      owner=context.test_owner_1)

  def test_020(self):
    '''Set access policy'''
    context.pid = 'AnserMatrix.htm'
    rules = (
      (('test_perm_1', 'test_perm_2'), ('read', )),
      (('test_perm_3', 'test_perm_4'), ('write', 'changePermission')),
    )
    self._set_access_policy(context.pid, rules)

  #  def ___test_020(self):
  #    '''Create object with access policy.
  #    '''
  #    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
  #
  #    # Add the access policy to the SysMeta.
  #    context.sysmeta.accessPolicy = context.access_policy
  #
  #    # POST the new object to MN.
  #    response = client.createResponse(pid=context.pid,
  #      obj=context.obj_str, sysmeta=context.sysmeta,
  #      vendorSpecific=self.session(context.test_owner_1))

  def test_030(self):
    '''Access is allowed for owner.'''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    obj = client.get(context.pid, vendorSpecific=self.session(context.test_owner_1))
    self.assertEqual(context.obj_str, obj.read())

  def ___test_040(self):
    '''Access is allowed for SUBJECT_TRUSTED.'''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    obj = client.get(
      context.pid,
      vendorSpecific=self.session(d1_common.const.SUBJECT_TRUSTED)
    )
    self.assertEqual(context.obj_str, obj.read())

  def ___test_050(self):
    '''Read access is allowed for subject with exact allow rule.'''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    obj = client.get(context.pid, vendorSpecific=self.session('test_perm_2'))
    self.assertEqual(context.obj_str, obj.read())

  def ___test_060(self):
    '''Read access is allowed for subject with higher level access (1).'''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    obj = client.get(context.pid, vendorSpecific=self.session('test_perm_3'))
    self.assertEqual(context.obj_str, obj.read())

  def ___test_070(self):
    '''Read access is allowed for subject with higher level access (2).'''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    obj = client.get(context.pid, vendorSpecific=self.session('test_perm_5'))
    self.assertEqual(context.obj_str, obj.read())

  def ___test_080(self):
    '''Read access is denied for SUBJECT_PUBLIC.'''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    self.assertRaises(
      d1_common.types.exceptions.NotAuthorized,
      client.get,
      context.pid,
      vendorSpecific=self.session(d1_common.const.SUBJECT_PUBLIC)
    )

  def ___test_090(self):
    '''Read access is denied for regular subject.
    '''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    self.assertRaises(
      d1_common.types.exceptions.NotAuthorized,
      client.get,
      context.pid,
      vendorSpecific=self.session('other_subject')
    )

  def ___test_200(self):
    '''Update access policy, denying access for old subjects and allowing
    access to new subjects.'''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)

    access_policy = self.gen_access_policy(
      (
        (('test_perm_7', 'test_perm_8'), ('changePermission', )),
      )
    )

    client.setAccessPolicy(
      context.pid,
      access_policy,
      vendorSpecific=self.session(context.test_owner_1)
    )

  def ___test_210(self):
    '''Access policy is correctly reflected in SysMeta.'''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)

    sysmeta = client.getSystemMetadata(
      context.pid, vendorSpecific=self.session(
        context.test_owner_1
      )
    )

    self.assertEqual(sysmeta.accessPolicy.allow[0].subject[0].value(), 'test_perm_7')
    self.assertEqual(sysmeta.accessPolicy.allow[0].subject[1].value(), 'test_perm_8')
    self.assertEqual(sysmeta.accessPolicy.allow[0].permission[0], 'changePermission')

  def ___test_220(self):
    '''Access now denied for previous subjects.'''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    for subject in (
      'test_perm_1', 'test_perm_2', 'test_perm_3', 'test_perm_4', 'test_perm_5',
      'test_perm_6'
    ):
      self.assertRaises(
        d1_common.types.exceptions.NotAuthorized,
        client.get,
        context.pid,
        vendorSpecific=self.session(subject)
      )

  def ___test_220(self):
    '''Access allowed for current subjects.'''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    for subject in ('test_perm_7', 'test_perm_8'):
      obj = client.get(context.pid, vendorSpecific=self.session(subject))
      self.assertEqual(context.obj_str, obj.read())

  def ___test_300(self):
    '''isAuthorized returns access denied for previous subjects.'''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    for subject in (
      'test_perm_1', 'test_perm_2', 'test_perm_3', 'test_perm_4', 'test_perm_5',
      'test_perm_6'
    ):
      self.assertRaises(
        d1_common.types.exceptions.NotAuthorized,
        client.isAuthorized,
        context.pid,
        'read',
        vendorSpecific=self.session(subject)
      )

  def ___test_310(self):
    '''isAuthorized returns access allowed for current subjects.
    '''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    for subject in ('test_perm_7', 'test_perm_8'):
      obj = client.isAuthorized(context.pid, 'read', vendorSpecific=self.session(subject))

  def ___test_320(self):
    '''isAuthorized returns access denied for levels higher than allowed.
    '''
    client = gmn_test_client.GMNTestClient(self.options.gmn_url)
    for subject in ('test_perm_7', 'test_perm_8'):
      self.assertRaises(
        d1_common.types.exceptions.NotAuthorized,
        client.isAuthorized,
        context.pid,
        'execute',
        vendorSpecific=self.session(subject)
      )

# ===============================================================================


def log_setup():
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  import optparse

  log_setup()

  # Command line options.
  parser = optparse.OptionParser()
  parser.add_option(
    '--gmn-url',
    dest='gmn_url',
    action='store',
    type='string',
    default='http://0.0.0.0:8000/'
  )
  parser.add_option('--debug', action='store_true', default=False, dest='debug')
  parser.add_option('--verbose', action='store_true', default=False, dest='verbose')
  parser.add_option(
    '--test', action='store',
    default='',
    dest='test',
    help='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if not options.verbose:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestAccessControl
  s.options = options

  if options.test != '':
    suite = unittest2.TestSuite(map(s, [options.test]))
    # suite.debug()
  else:
    suite = unittest2.TestLoader().loadTestsFromTestCase(s)

  #  if options.debug == True:
  #    unittest2.TextTestRunner(verbosity=2).debug(suite)
  #  else:
  unittest2.TextTestRunner(verbosity=2, failfast=True).run(suite)


if __name__ == '__main__':
  main()
