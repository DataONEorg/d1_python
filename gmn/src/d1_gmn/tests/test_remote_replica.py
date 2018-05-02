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
"""Test storage of information about remote replicas, as received in the
<replica> sections of SysMeta:

<replica>
  <replicaMemberNode>mn_ah</replicaMemberNode>
  <replicationStatus>requested</replicationStatus>
  <replicaVerified>2017-01-15T00:26:32.145777Z</replicaVerified>
</replica>

[...]
"""

import responses

import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_test_client

import d1_common
import d1_common.const
import d1_common.date_time
import d1_common.system_metadata
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.xml

import d1_test.sample


class TestRemoteReplica(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def _add_replica(self, sysmeta_pyxb, node_str, status_str, verified_dt):
    replica_pyxb = d1_common.types.dataoneTypes.Replica()
    replica_pyxb.replicaMemberNode = node_str
    replica_pyxb.replicationStatus = status_str
    replica_pyxb.replicaVerified = d1_common.date_time.dt_from_iso8601_str(
      verified_dt
    )
    sysmeta_pyxb.replica.append(replica_pyxb)

  def _add_regular_replica_sections(self, sysmeta_pyxb):
    self._add_replica(
      sysmeta_pyxb, 'node1', 'queued', '2013-05-21T19:02:49-06:00'
    )
    self._add_replica(
      sysmeta_pyxb, 'node2', 'failed', '2014-05-21T19:02:49-06:00'
    )
    self._add_replica(
      sysmeta_pyxb, 'node3', 'completed', '2015-05-21T19:02:49-06:00'
    )

  # TODO: Many sysmeta tests could handily be refactored to this
  def _assert_sysmeta_round_trip(self, client, sysmeta_pyxb):
    send_sciobj_bytes, send_sysmeta_pyxb = self.create_obj_by_sysmeta(
      client, sysmeta_pyxb
    )
    recv_sciobj_bytes, recv_sysmeta_pyxb = self.get_obj(
      client, d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
    )
    assert send_sciobj_bytes == recv_sciobj_bytes
    assert d1_common.system_metadata.are_equivalent_pyxb(
      send_sysmeta_pyxb, recv_sysmeta_pyxb
    )

  @responses.activate
  def test_1000(self, gmn_client_v2):
    """Regular replica sections correctly represented"""
    sysmeta_pyxb = d1_test.sample.load_xml_to_pyxb(
      'systemMetadata_v2_0_remote_replica_base.xml'
    )
    sysmeta_pyxb.identifier = 'remote_rep_pid_1'
    self._add_regular_replica_sections(sysmeta_pyxb)
    self._assert_sysmeta_round_trip(gmn_client_v2, sysmeta_pyxb)

  @responses.activate
  def test_1010(self, gmn_client_v2):
    """Replica information is stored per PID
    - Two different PIDs can hold different replica info for the same replica
    nodes
    """
    # Create obj with replica info for node1 and node2 on pid_1
    sysmeta_1_pyxb = d1_test.sample.load_xml_to_pyxb(
      'systemMetadata_v2_0_remote_replica_base.xml'
    )
    sysmeta_1_pyxb.identifier = 'remote_rep_pid_1'
    sysmeta_1_pyxb.seriesId = None
    self._add_replica(
      sysmeta_1_pyxb, 'node1', 'queued', '2013-05-21T19:02:49-06:00'
    )
    self._add_replica(
      sysmeta_1_pyxb, 'node2', 'failed', '2014-05-21T19:02:49-06:00'
    )
    send_sciobj_1_str, send_sysmeta_1_pyxb = self.create_obj_by_sysmeta(
      gmn_client_v2, sysmeta_1_pyxb
    )

    # Create obj with different replica info for node1 and node2 on pid_2
    sysmeta_2_pyxb = d1_test.sample.load_xml_to_pyxb(
      'systemMetadata_v2_0_remote_replica_base.xml'
    )
    sysmeta_2_pyxb.identifier = 'remote_rep_pid_2'
    sysmeta_2_pyxb.seriesId = None
    self._add_replica(
      sysmeta_2_pyxb, 'node1', 'completed', '2113-05-21T19:02:49-06:00'
    )
    self._add_replica(
      sysmeta_2_pyxb, 'node2', 'invalidated', '2114-05-21T19:02:49-06:00'
    )
    send_sciobj_2_str, send_sysmeta_2_pyxb = self.create_obj_by_sysmeta(
      gmn_client_v2, sysmeta_2_pyxb
    )
    # Check that pid_1 retains initial replica info for node1 and node2
    recv_sciobj_1_str, recv_sysmeta_1_pyxb = self.get_obj(
      gmn_client_v2, d1_common.xml.get_req_val(sysmeta_1_pyxb.identifier)
    )
    self.dump(recv_sysmeta_1_pyxb)
    assert send_sciobj_1_str == recv_sciobj_1_str
    assert d1_common.system_metadata.are_equivalent_pyxb(
      send_sysmeta_1_pyxb, recv_sysmeta_1_pyxb
    )
    # Check that pid_2 retains initial replica info for node1 and node2
    recv_sciobj_2_str, recv_sysmeta_2_pyxb = self.get_obj(
      gmn_client_v2, d1_common.xml.get_req_val(sysmeta_2_pyxb.identifier)
    )
    self.dump(recv_sysmeta_2_pyxb)
    assert send_sciobj_2_str == recv_sciobj_2_str
    assert d1_common.system_metadata.are_equivalent_pyxb(
      send_sysmeta_2_pyxb, recv_sysmeta_2_pyxb
    )
