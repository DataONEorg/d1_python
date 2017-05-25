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
"""Test MNRead.listObjects()

MNRead.listObjects(session[, fromDate][, toDate][, formatId][, replicaStatus]
[, start=0][, count=1000]) → ObjectList
"""

from __future__ import absolute_import

import d1_client.mnclient_1_1
import d1_client.mnclient_2_0
import d1_common.types.dataoneTypes_v2_0 as v2
import d1_common.types.exceptions
import d1_common.util
import d1_test.mock_api.django_client as mock_django_client
import responses

import gmn.tests.gmn_test_case

BASE_URL = 'http://mock/mn'


class TestListObjects(gmn.tests.gmn_test_case.D1TestCase):
  def __init__(self, *args, **kwargs):
    super(TestListObjects, self).__init__(*args, **kwargs)
    d1_common.util.log_setup(is_debug=True)
    self.client_v1 = None
    self.client_v2 = None

  def setUp(self):
    mock_django_client.add_callback(BASE_URL)
    self.client_v1 = d1_client.mnclient_1_1.MemberNodeClient_1_1(BASE_URL)
    self.client_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(BASE_URL)

  @responses.activate
  def test_0010(self):
    """MNRead.listObjects(): replicaStatus filter"""
    # Create two objects, one local and one replica
    local_pid = self.random_pid()
    self.create(self.client_v2, v2, local_pid)
    replica_pid = self.random_pid()
    self.create(self.client_v2, v2, replica_pid)
    self.convert_to_replica(replica_pid)
    # No replicationStatus filter returns both objects
    object_list_pyxb = self.client_v2.listObjects()
    self.assertListEqual(
      self.object_list_to_pid_list(object_list_pyxb),
      sorted([replica_pid, local_pid]),
    )
    # replicationStatus=False returns only the local object
    object_list_pyxb = self.client_v2.listObjects(replicaStatus=False)
    self.assertListEqual(
      self.object_list_to_pid_list(object_list_pyxb),
      [local_pid]
    )
