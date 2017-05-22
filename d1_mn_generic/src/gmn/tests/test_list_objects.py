# -*- coding: utf-8 -*-

from __future__ import absolute_import

import d1_client.mnclient_2_0
import d1_common.types.dataoneTypes_v2_0 as v2
import d1_test.mock_api.django_client as mock_django_client
import responses

import tests.d1_test_case

BASE_URL = 'http://mock/mn'


class TestListObjects(tests.d1_test_case.D1TestCase):
  def setUp(self):
    mock_django_client.add_callback(BASE_URL)
    self.d1_client = d1_client.mnclient_2_0.MemberNodeClient_2_0(BASE_URL)

  @responses.activate
  def test_0010(self):
    """listObjects(): replicaStatus filter"""
    # Create two objects, one local and one replica
    local_pid = self.random_pid()
    self.create(self.d1_client, v2, local_pid)
    replica_pid = self.random_pid()
    self.create(self.d1_client, v2, replica_pid)
    self.convert_to_replica(replica_pid)
    # No replicationStatus filter returns both objects
    object_list_pyxb = self.d1_client.listObjects()
    self.assertListEqual(
      self.object_list_to_pid_list(object_list_pyxb),
      sorted([replica_pid, local_pid]),
    )
    # replicationStatus=False returns only the local object
    object_list_pyxb = self.d1_client.listObjects(replicaStatus=False)
    self.assertListEqual(
      self.object_list_to_pid_list(object_list_pyxb),
      [local_pid]
    )
