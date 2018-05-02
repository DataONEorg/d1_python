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
"""Test MNStorage.delete() for objects in revision chains

When an object in a revision chains is deleted, GMN repairs the chain by
connecting any objects on either side of the deleted object with each other
"""

import pytest
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common


class TestDeleteRevision(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def assert_delete(self, client, pid, sid, pid_chain_list):
    with d1_gmn.tests.gmn_mock.disable_auth():
      # Is retrievable
      recv_sciobj_bytes, recv_sysmeta_pyxb = self.get_obj(client, pid)
      self.assert_sysmeta_pid_and_sid(recv_sysmeta_pyxb, pid, sid)
      # Delete
      identifier_pyxb = client.delete(pid)
      assert identifier_pyxb.value() == pid
      # Is no longer retrievable so new delete() raises 404
      with pytest.raises(d1_common.types.exceptions.NotFound):
        client.delete(pid)
      # New chain is valid and matches the expected chain
      pid_chain_list.remove(pid)
      self.assert_valid_chain(client, pid_chain_list, sid)
      # PID can now be reused
      self.create_obj(client, pid, sid)
      # Is again retrievable
      reused_sysmeta_pyxb = self.client_v2.getSystemMetadata(pid)
      self.assert_sysmeta_pid_and_sid(reused_sysmeta_pyxb, pid, sid)

  @responses.activate
  def test_1000(self, gmn_client_v1_v2):
    """MNStorage.delete(): Deleted flag correctly set and represented"""
    sid, pid_chain_list = self.create_revision_chain(
      gmn_client_v1_v2,
      chain_len=5,
    )
    self.assert_valid_chain(gmn_client_v1_v2, pid_chain_list, sid)
    # Delete head
    self.assert_delete(
      gmn_client_v1_v2, pid_chain_list[-1], sid, pid_chain_list
    )
    # Delete tail
    self.assert_delete(gmn_client_v1_v2, pid_chain_list[0], sid, pid_chain_list)
    # Delete center
    self.assert_delete(gmn_client_v1_v2, pid_chain_list[2], sid, pid_chain_list)
