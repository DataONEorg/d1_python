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

import StringIO
import datetime
import hashlib
import random
import string
import subprocess
import tempfile

import d1_client.mnclient
import d1_client.session
import d1_common.checksum
import d1_common.types
import d1_common.xml
import django.test
import requests

import tests.gmn_test_client

DEFAULT_ACCESS_RULE_LIST = [
  ([
    'subj1',
  ], ['read'],),
  (['subj2', 'subj3', 'subj4'], ['read', 'write'],),
  (['subj5', 'subj6', 'subj7', 'subj8'], ['read', 'changePermission'],),
  (['subj9', 'subj10', 'subj11', 'subj12'], ['changePermission'],),
]

HTTPBIN_SERVER_STR = 'http://httpbin.org'


class D1TestCase(django.test.TestCase):
  def disable_server_cert_validation(self):
    requests.packages.urllib3.disable_warnings()
    d1_client.session.DEFAULT_VERIFY_TLS = False

  def assert_object_list_slice(self, object_list, start, count, total):
    self.assertEqual(object_list.start, start)
    self.assertEqual(object_list.count, count)
    self.assertEqual(object_list.total, total)
    # Check that the actual number of objects matches the count
    # provided in the slice.
    self.assertEqual(len(object_list.objectInfo), count)

  def assert_log_slice(self, log, start, count, total):
    self.assertEqual(log.start, start)
    self.assertEqual(log.count, count)
    self.assertEqual(log.total, total)
    # Check that the actual number of log records matches the count
    # provided in the slice.
    self.assertEqual(len(log.logEntry), count)

  def assert_response_headers(self, response):
    """Required response headers are present.
    """
    self.assertIn('last-modified', response.headers)
    self.assertIn('content-length', response.headers)
    self.assertIn('content-type', response.headers)

  def assert_valid_date(self, date_str):
    self.assertTrue(datetime.datetime(*map(int, date_str.split('-'))))

  def find_valid_pid(self, client):
    """Find the PID of an object that exists on the server.
    """
    # Verify that there's at least one object on server.
    object_list = client.listObjects(
      vendorSpecific=self.
      include_subjects(tests.gmn_test_client.GMN_TEST_SUBJECT_TRUSTED)
    )
    self.assertTrue(object_list.count > 0, 'No objects to perform test on')
    # Get the first PID listed. The list is in random order.
    return object_list.objectInfo[0].identifier.value()

  def generate_sysmeta(
      self, binding, pid, sciobj_str, owner, obsoletes=None, obsoleted_by=None,
      sid=None, access_rule_list=None
  ):
    now = datetime.datetime.now()
    sysmeta_pyxb = binding.systemMetadata()
    sysmeta_pyxb.serialVersion = 1
    sysmeta_pyxb.identifier = pid
    sysmeta_pyxb.seriesId = sid
    sysmeta_pyxb.formatId = 'application/octet-stream'
    sysmeta_pyxb.size = len(sciobj_str)
    sysmeta_pyxb.submitter = owner
    sysmeta_pyxb.rightsHolder = owner
    sysmeta_pyxb.checksum = d1_common.types.dataoneTypes.checksum(
      hashlib.md5(sciobj_str).hexdigest()
    )
    sysmeta_pyxb.checksum.algorithm = 'MD5'
    sysmeta_pyxb.dateUploaded = now
    sysmeta_pyxb.dateSysMetadataModified = now
    sysmeta_pyxb.originMemberNode = 'MN1'
    sysmeta_pyxb.authoritativeMemberNode = 'MN1'
    sysmeta_pyxb.obsoletes = obsoletes
    sysmeta_pyxb.obsoletedBy = obsoleted_by
    sysmeta_pyxb.accessPolicy = self.generate_access_policy(
      binding, access_rule_list
    )
    sysmeta_pyxb.replicationPolicy = self.create_replication_policy_pyxb(
      binding
    )
    return sysmeta_pyxb

  def generate_access_policy(self, binding, access_rule_list=None):
    access_rule_list = access_rule_list or DEFAULT_ACCESS_RULE_LIST
    access_policy = binding.accessPolicy()
    for subject_list, permission_list in access_rule_list:
      access_rule_pyxb = binding.AccessRule()
      for subject_str in subject_list:
        access_rule_pyxb.subject.append(subject_str)
      for permission_str in permission_list:
        permission_pyxb = binding.Permission(permission_str)
        access_rule_pyxb.permission.append(permission_pyxb)
      access_policy.append(access_rule_pyxb)
    return access_policy

  def create_replication_policy_pyxb(
      self,
      binding,
      preferred_node_list=None,
      blocked_node_list=None,
      is_replication_allowed=True,
      num_replicas=None,
  ):
    if preferred_node_list is None:
      preferred_node_list = [
        self.random_tag('preferred_node') for _ in range(5)
      ]
    if blocked_node_list is None:
      blocked_node_list = [self.random_tag('blocked_node') for _ in range(5)]
    rep_pyxb = binding.ReplicationPolicy()
    rep_pyxb.preferredMemberNode = preferred_node_list
    rep_pyxb.blockedMemberNode = blocked_node_list
    rep_pyxb.replicationAllowed = is_replication_allowed
    rep_pyxb.numberReplicas = num_replicas or random.randint(10, 100)
    return rep_pyxb

  def generate_test_object(
      self, binding, pid, obsoletes=None, obsoleted_by=None, sid=None,
      access_rule_list=None
  ):
    sciobj = 'Science Object Bytes for pid="{}"'.format(pid.encode('utf-8'))
    sysmeta_pyxb = self.generate_sysmeta(
      binding, pid, sciobj, tests.gmn_test_client.GMN_TEST_SUBJECT_PUBLIC,
      obsoletes, obsoleted_by, sid, access_rule_list
    )
    return sciobj, sysmeta_pyxb

  def include_subjects(self, subjects):
    if isinstance(subjects, basestring):
      subjects = [subjects]
    return {'VENDOR-INCLUDE-SUBJECTS': u'\t'.join(subjects)}

  def has_public_object_list(self, gmn_url):
    client = tests.gmn_test_client.GMNTestClient(gmn_url)
    return client.get_setting('PUBLIC_OBJECT_LIST')

  def now_str(self):
    return datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

  def random_str(self, num_chars=10):
    return ''.join([
      random.choice(string.ascii_lowercase) for _ in range(num_chars)
    ])

  def random_id(self):
    return '{}_{}'.format(self.random_str(), self.now_str())

  def random_pid(self):
    return 'PID_{}'.format(self.random_id())

  def random_sid(self):
    return 'SID_{}'.format(self.random_id())

  def random_tag(self, tag_str):
    return '{}_{}'.format(tag_str, self.random_str())

  def create(
      self, client, binding, pid, sid=None, obsoletes=None, obsoleted_by=None,
      access_rule_list=None
  ):
    sci_obj_str, sysmeta_pyxb = self.generate_test_object(
      binding, pid, obsoletes, obsoleted_by, sid, access_rule_list
    )
    client.create(
      pid,
      sci_obj_str,
      sysmeta_pyxb,
      vendorSpecific=self.
      include_subjects(tests.gmn_test_client.GMN_TEST_SUBJECT_TRUSTED),
    )
    return sci_obj_str, sysmeta_pyxb

  def update(
      self, client, binding, old_pid, new_pid, sid=None, obsoletes=None,
      obsoleted_by=None
  ):
    sci_obj_str, sysmeta_pyxb = self.generate_test_object(
      binding, new_pid, obsoletes, obsoleted_by, sid
    )
    client.update(
      old_pid,
      sci_obj_str,
      new_pid,
      sysmeta_pyxb,
      vendorSpecific=self.
      include_subjects(tests.gmn_test_client.GMN_TEST_SUBJECT_TRUSTED),
    )
    return sci_obj_str, sysmeta_pyxb

  def get(self, client, did):
    sysmeta_pyxb = client.getSystemMetadata(
      did, vendorSpecific=self.
      include_subjects(tests.gmn_test_client.GMN_TEST_SUBJECT_TRUSTED)
    )
    response = client.get(
      did, vendorSpecific=self.
      include_subjects(tests.gmn_test_client.GMN_TEST_SUBJECT_TRUSTED)
    )
    self.assert_sci_obj_size_matches_sysmeta(response, sysmeta_pyxb)
    self.assert_sci_obj_checksum_matches_sysmeta(response, sysmeta_pyxb)
    return response.content, sysmeta_pyxb

  def assert_sci_obj_size_matches_sysmeta(self, response, sysmeta_pyxb):
    self.assertEqual(sysmeta_pyxb.size, len(response.content))

  def get_checksum_calculator(self, sysmeta_pyxb):
    return d1_common.checksum.get_checksum_calculator_by_dataone_designator(
      sysmeta_pyxb.checksum.algorithm
    )

  def calculate_object_checksum(self, response, checksum_calculator):
    checksum_calculator.update(response.content)
    return checksum_calculator.hexdigest()

  def create_checksum_object_from_string(self, sciobj_str, checksum_pyxb=None):
    return (
      d1_common.checksum.create_checksum_object_from_stream(
        StringIO.StringIO(sciobj_str), checksum_pyxb.algorithm
        if checksum_pyxb else 'SHA-1'
      )
    )

  def assert_sci_obj_checksum_matches_sysmeta(self, sciobj_str, sysmeta_pyxb):
    self.assertTrue(
      d1_common.checksum.checksums_are_equal(
        self.create_checksum_object_from_string(
          sciobj_str, sysmeta_pyxb.checksum
        ), sysmeta_pyxb.checksum
      )
    )

  def pyxb_to_pretty_xml(self, obj_pyxb):
    xml_str = obj_pyxb.toxml().encode('utf-8')
    return d1_common.xml.pretty_xml(xml_str)

  def restore_sysmeta_mn_controlled_fields(
      self, sysmeta_a_pyxb, sysmeta_b_pyxb
  ):
    """Copy values that the MN overwrites from sysmeta_b to sysmeta_a so that
    the sysmeta used in create() can be compared with sysmeta retrieved in
    get().
    """
    sysmeta_a_pyxb.archived = sysmeta_b_pyxb.archived
    sysmeta_b_pyxb.dateSysMetadataModified = sysmeta_a_pyxb.dateSysMetadataModified
    sysmeta_b_pyxb.originMemberNode = sysmeta_a_pyxb.originMemberNode
    sysmeta_b_pyxb.authoritativeMemberNode = sysmeta_a_pyxb.authoritativeMemberNode
    sysmeta_b_pyxb.dateUploaded = sysmeta_a_pyxb.dateUploaded

  def get_checksum_test(self, client, binding, pid, checksum, algorithm):
    checksum_obj = client.getChecksum(
      pid, checksumAlgorithm=algorithm, vendorSpecific=self.
      include_subjects(tests.gmn_test_client.GMN_TEST_SUBJECT_TRUSTED)
    )
    self.assertIsInstance(checksum_obj, binding.Checksum)
    self.assertEqual(checksum, checksum_obj.value())
    self.assertEqual(algorithm, checksum_obj.algorithm)

  def kdiff_pyxb(self, a_pyxb, b_pyxb):
    with tempfile.NamedTemporaryFile() as a_f:
      with tempfile.NamedTemporaryFile() as b_f:
        a_f.write(d1_common.xml.pretty_pyxb(a_pyxb))
        b_f.write(d1_common.xml.pretty_pyxb(b_pyxb))
        a_f.seek(0)
        b_f.seek(0)
        subprocess.call(['kdiff3', a_f.name, b_f.name])
