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
"""Test conversions of System Metadata between PyXB and database
"""

from __future__ import absolute_import

# Stdlib
import datetime

# Django
import django.test

# App
import app.models
import app.sysmeta
import app.sysmeta_replica
import app.sysmeta_util
import tests.util


class TestSysMeta(django.test.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def _create_sci_obj_base(self):
    sciobj_model = app.models.ScienceObject()
    sciobj_model.checksum_algorithm = app.models.checksum_algorithm('SHA-1')
    sciobj_model.format = app.models.format('test')
    sciobj_model.is_archived = False
    sciobj_model.modified_timestamp = datetime.datetime.now()
    sciobj_model.uploaded_timestamp = datetime.datetime.now()
    sciobj_model.pid = app.sysmeta_util.create_id_model('test')
    sciobj_model.serial_version = 1
    sciobj_model.size = 1

    sciobj_model.submitter = app.models.subject('test_submitter')
    sciobj_model.rights_holder = app.models.subject('rightsHolder0')
    sciobj_model.origin_member_node = app.models.node('test_origin_mn')
    sciobj_model.authoritative_member_node = app.models.node('test_auth_mn')

    sciobj_model.save()
    return sciobj_model

  def _compare_base_pyxb(self, a_pyxb, b_pyxb):
    element_list = [
      'serialVersion',
      'identifier',
      'formatId',
      'size',
      'checksum', # algorithm
      'submitter',
      'rightsHolder',
      'obsoletes',
      'obsoletedBy',
      'archived',
      'dateUploaded',
      'dateSysMetadataModified',
      'originMemberNode',
      'authoritativeMemberNode',
    ]
    for element_str in element_list:
      a_el = getattr(a_pyxb, element_str)
      b_el = getattr(b_pyxb, element_str)
      if hasattr(a_el, 'value'):
        self.assertEqual(a_el.value(), b_el.value())
      else:
        self.assertEqual(a_el, b_el)

  # Base

  def test_050(self):
    orig_sysmeta_pyxb = tests.util.read_test_xml('sysmeta_v2_0_sample.xml')
    sciobj_model = app.models.ScienceObject()
    sciobj_model.pid = app.sysmeta_util.create_id_model(
      orig_sysmeta_pyxb.identifier.value()
    )
    app.sysmeta._base_pyxb_to_model(
      sciobj_model,
      orig_sysmeta_pyxb,
      url='file://test',
    )
    gen_sciobj_pyxb = app.sysmeta._base_model_to_pyxb(sciobj_model)
    self._compare_base_pyxb(orig_sysmeta_pyxb, gen_sciobj_pyxb)

  # Access Policy

  # <accessPolicy>
  #         <allow>
  #                 <subject>subject0</subject>
  #                 <subject>subject1</subject>
  #                 <permission>read</permission>
  #                 <permission>changePermission</permission>
  #         </allow>
  #         <allow>
  #                 <subject>subject2</subject>
  #                 <subject>subject3</subject>
  #                 <permission>write</permission>
  #         </allow>
  # </accessPolicy>

  def test_100(self):
    orig_sysmeta_pyxb = tests.util.read_test_xml('sysmeta_v2_0_sample.xml')
    sciobj_model = self._create_sci_obj_base()
    app.sysmeta._access_policy_pyxb_to_model(sciobj_model, orig_sysmeta_pyxb)
    gen_access_policy_pyxb = app.sysmeta._access_policy_model_to_pyxb(
      sciobj_model
    )
    self.assertEqual(len(gen_access_policy_pyxb.allow), 4)
    for allow_pyxb in gen_access_policy_pyxb.allow:
      self.assertIn(allow_pyxb.permission[0], ['changePermission', 'write'])
      self.assertEqual(len(allow_pyxb.subject), 1)
      for subject in allow_pyxb.subject:
        if allow_pyxb.permission[0] == 'changePermission':
          self.assertIn(subject.value(), ['subject0', 'subject1'])
        if allow_pyxb.permission[0] == 'write':
          self.assertIn(subject.value(), ['subject2', 'subject3'])

  # Replication Policy

  # <replicationPolicy xmlns="" replicationAllowed="true" numberReplicas="42">
  #     <preferredMemberNode>preferredMemberNode0</preferredMemberNode>
  #     <preferredMemberNode>preferredMemberNode1</preferredMemberNode>
  #     <blockedMemberNode>blockedMemberNode0</blockedMemberNode>
  #     <blockedMemberNode>blockedMemberNode1</blockedMemberNode>
  # </replicationPolicy>

  def test_200(self):
    orig_sysmeta_pyxb = tests.util.read_test_xml('sysmeta_v2_0_sample.xml')
    sciobj_model = self._create_sci_obj_base()
    app.sysmeta._replication_policy_pyxb_to_model(
      sciobj_model, orig_sysmeta_pyxb
    )
    gen_replication_policy_pyxb = app.sysmeta._replication_policy_model_to_pyxb(
      sciobj_model
    )
    self.assertEqual(len(gen_replication_policy_pyxb.blockedMemberNode), 2)
    for blocked_member_node in gen_replication_policy_pyxb.blockedMemberNode:
      self.assertIn(
        blocked_member_node.value(),
        ['blockedMemberNode0', 'blockedMemberNode1']
      )
    self.assertEqual(len(gen_replication_policy_pyxb.preferredMemberNode), 2)
    for preferred_member_node in gen_replication_policy_pyxb.preferredMemberNode:
      self.assertIn(
        preferred_member_node.value(),
        ['preferredMemberNode0', 'preferredMemberNode1']
      )

  # Replica

  # <replica xmlns="">
  #     <replicaMemberNode>replicaMemberNode0</replicaMemberNode>
  #     <replicationStatus>queued</replicationStatus>
  #     <replicaVerified>2006-05-04T18:13:51.0</replicaVerified>
  # </replica>
  # <replica xmlns="">
  #     <replicaMemberNode>replicaMemberNode1</replicaMemberNode>
  #     <replicationStatus>queued</replicationStatus>
  #     <replicaVerified>2007-05-04T18:13:51.0</replicaVerified>
  # </replica>

  def test_300(self):
    orig_sysmeta_pyxb = tests.util.read_test_xml('sysmeta_v2_0_sample.xml')
    sciobj_model = self._create_sci_obj_base()
    app.sysmeta_replica.replica_pyxb_to_model(sciobj_model, orig_sysmeta_pyxb)
    gen_replica_pyxb_list = app.sysmeta_replica.replica_model_to_pyxb(
      sciobj_model
    )
    self.assertEqual(len(gen_replica_pyxb_list), 2)
    for replica_pyxb in gen_replica_pyxb_list:
      self.assertIn(
        replica_pyxb.replicaMemberNode.value(),
        ['replicaMemberNode0', 'replicaMemberNode1'],
      )
      if replica_pyxb.replicaMemberNode.value() == 'replicaMemberNode0':
        self.assertEqual(
          replica_pyxb.replicationStatus,
          'queued',
        )
        self.assertEqual(
          replica_pyxb.replicaVerified,
          datetime.datetime(2006, 5, 4, 18, 13, 51),
        )
      if replica_pyxb.replicaMemberNode.value() == 'replicaMemberNode1':
        self.assertEqual(
          replica_pyxb.replicationStatus,
          'completed',
        )
        self.assertEqual(
          replica_pyxb.replicaVerified,
          datetime.datetime(2007, 5, 4, 18, 13, 51),
        )
