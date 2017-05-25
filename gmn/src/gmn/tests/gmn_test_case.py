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

import datetime
import hashlib
import random
import string

import d1_client.mnclient
import d1_client.session
import d1_common.checksum
import d1_common.types
import d1_common.types.dataoneTypes_v2_0 as v2
import d1_common.util
import d1_common.xml
import django.test
import gmn.app.models
import gmn.tests.gmn_test_client
import requests

DEFAULT_ACCESS_RULE_LIST = [
  ([
    'subj1',
  ], ['read'],),
  (['subj2', 'subj3', 'subj4'], ['read', 'write'],),
  (['subj5', 'subj6', 'subj7', 'subj8'], ['read', 'changePermission'],),
  (['subj9', 'subj10', 'subj11', 'subj12'], ['changePermission'],),
]

HTTPBIN_SERVER_STR = 'http://httpbin.org'

GMN_TEST_SUBJECT_PUBLIC = 'public'
GMN_TEST_SUBJECT_TRUSTED = 'gmn_test_subject_trusted'


class D1TestCase(django.test.TestCase):
  def disable_server_cert_validation(self):
    requests.packages.urllib3.disable_warnings()
    d1_client.session.DEFAULT_VERIFY_TLS = False

  #
  # assert
  #

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

  def assert_sci_obj_size_matches_sysmeta(self, response, sysmeta_pyxb):
    self.assertEqual(sysmeta_pyxb.size, len(response.content))

  def assert_sci_obj_checksum_matches_sysmeta(self, response, sysmeta_pyxb):
    self.assertTrue(
      d1_common.checksum.
      is_checksum_correct_on_string(sysmeta_pyxb, response.content)
    )

  def assert_has_public_object_list(self, gmn_url):
    client = gmn.tests.gmn_test_client.GMNTestClient(gmn_url)
    self.assertTrue(
      client.get_setting('PUBLIC_OBJECT_LIST'),
      'This test requires that public access has been enabled for listObjects.',
    )

  def assert_checksums_equal(self, a_pyxb, b_pyxb):
    self.assertTrue(d1_common.checksum.are_checksums_equal(a_pyxb, b_pyxb))

  def assert_valid_chain(self, client, pid_chain_list, base_sid):
    pad_pid_chain_list = [None] + pid_chain_list + [None]
    for prev_pid, cur_pid, next_pid in zip(
        pad_pid_chain_list, pad_pid_chain_list[1:], pad_pid_chain_list[2:]
    ):
      obj_str, sysmeta_pyxb = self.get(client, cur_pid)
      self.assertEqual(self.get_pyxb_value(sysmeta_pyxb, 'obsoletes'), prev_pid)
      self.assertEqual(self.get_pyxb_value(sysmeta_pyxb, 'identifier'), cur_pid)
      self.assertEqual(
        self.get_pyxb_value(sysmeta_pyxb, 'obsoletedBy'), next_pid
      )
      if base_sid:
        self.assertEqual(
          self.get_pyxb_value(sysmeta_pyxb, 'seriesId'), base_sid
        )

  #
  # CRUD
  #

  def create(
      self, client, binding, pid, sid=None, submitter=None, rights_holder=None,
      access_rule_list=None, active_subject_list=None
  ):
    sci_obj_str, sysmeta_pyxb = self.generate_sciobj(
      binding, pid, sid=sid, submitter=submitter, rights_holder=rights_holder,
      access_rule_list=access_rule_list
    )
    client.create(
      pid, sci_obj_str, sysmeta_pyxb,
      vendorSpecific=self.include_subjects(active_subject_list)
    )
    return sci_obj_str, sysmeta_pyxb

  def update(
      self, client, binding, old_pid, new_pid, sid=None, submitter=None,
      rights_holder=None, access_rule_list=None, active_subject_list=None
  ):
    sci_obj_str, sysmeta_pyxb = self.generate_sciobj(
      binding, new_pid, sid=sid, submitter=submitter,
      rights_holder=rights_holder, access_rule_list=access_rule_list
    )
    client.update(
      old_pid, sci_obj_str, new_pid, sysmeta_pyxb,
      vendorSpecific=self.include_subjects(active_subject_list)
    )
    return sci_obj_str, sysmeta_pyxb

  def get(self, client, did, active_subject_list=None):
    sysmeta_pyxb = client.getSystemMetadata(
      did, vendorSpecific=self.include_subjects(active_subject_list)
    )
    response = client.get(
      did, vendorSpecific=self.include_subjects(active_subject_list)
    )
    self.assert_sci_obj_size_matches_sysmeta(response, sysmeta_pyxb)
    self.assert_sci_obj_checksum_matches_sysmeta(response, sysmeta_pyxb)
    return response.content, sysmeta_pyxb

  def convert_to_replica(self, pid):
    """Convert a local sciobj to a replica by adding a LocalReplica model to it
    """
    replica_info_model = gmn.app.models.replica_info(
      'completed', 'urn:node:testReplicaSource'
    )
    gmn.app.models.local_replica(pid, replica_info_model)

  def create_chain(self, client, binding, chain_len):
    """Create an obsolescence chain with a total of {chain_len} objects. If
    client is v2, assign a SID to the chain. Return the SID (None for v1)
    and a list of the PIDs in the chain. The first PID in the list is the
    tail and the last is the head.
    """
    base_pid = self.random_pid()
    base_sid = self.random_sid() if binding is v2 else None
    self.create(
      client, binding, base_pid, **{'sid': base_sid} if base_sid else {}
    )
    pid_chain_list = [base_pid]
    for i in range(chain_len - 1):
      update_pid = self.random_pid()
      self.update(
        client, binding, base_pid, update_pid, **{'sid': base_sid}
        if base_sid else {}
      )
      pid_chain_list.append(update_pid)
      base_pid = update_pid
    return base_sid, pid_chain_list

  #
  # SysMeta
  #

  def generate_sysmeta(
      self, binding, pid, sciobj_str, submitter, rights_holder, obsoletes=None,
      obsoleted_by=None, sid=None, access_rule_list=None
  ):
    now = datetime.datetime.now()
    sysmeta_pyxb = binding.systemMetadata()
    sysmeta_pyxb.serialVersion = 1
    sysmeta_pyxb.identifier = pid
    sysmeta_pyxb.seriesId = sid
    sysmeta_pyxb.formatId = 'application/octet-stream'
    sysmeta_pyxb.size = len(sciobj_str)
    sysmeta_pyxb.submitter = submitter
    sysmeta_pyxb.rightsHolder = rights_holder
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
    if access_rule_list is None:
      return None
    elif access_rule_list == 'default':
      access_rule_list = DEFAULT_ACCESS_RULE_LIST
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

  def generate_sciobj(
      self, binding, pid, submitter=None, rights_holder=None, obsoletes=None,
      obsoleted_by=None, sid=None, access_rule_list=None
  ):
    sciobj = 'Science Object Bytes for pid="{}"'.format(pid.encode('utf-8'))
    sysmeta_pyxb = self.generate_sysmeta(
      binding, pid, sciobj, submitter or GMN_TEST_SUBJECT_PUBLIC,
      rights_holder or GMN_TEST_SUBJECT_PUBLIC, obsoletes, obsoleted_by, sid,
      access_rule_list
    )
    return sciobj, sysmeta_pyxb

  def include_subjects(self, active_subject_list):
    if active_subject_list is None:
      return {}
    elif active_subject_list == 'trusted':
      active_subject_list = [GMN_TEST_SUBJECT_TRUSTED]
    elif isinstance(active_subject_list, basestring):
      active_subject_list = [active_subject_list]
    return {'VENDOR-INCLUDE-SUBJECTS': u'\t'.join(active_subject_list)}

  #
  # Misc
  #

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

  def get_pyxb_value(self, inst_pyxb, inst_attr):
    try:
      return getattr(inst_pyxb, inst_attr).value()
    except (ValueError, AttributeError):
      return None

  def object_list_to_pid_list(self, object_list_pyxb):
    return sorted([v.identifier.value() for v in object_list_pyxb.objectInfo])
