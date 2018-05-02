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
"""Test MNStorage.archive() for objects in revision chains
"""

import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case


class TestRevisionArchive(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self, gmn_client_v1_v2):
    """archive(): Archived flag correctly set and represented"""

    def assert_archived(client, pid):
      unarchived_sysmeta_pyxb = client.getSystemMetadata(pid)
      assert not unarchived_sysmeta_pyxb.archived
      pid_archived = client.archive(pid)
      assert pid == pid_archived.value()
      archived_sysmeta_pyxb = client.getSystemMetadata(pid)
      assert archived_sysmeta_pyxb.archived
      self.assert_eq_sysmeta_sid(
        unarchived_sysmeta_pyxb,
        archived_sysmeta_pyxb,
      )

    # archive() is supported on both CNs and MNs. Since this test creates a
    # revision chain, and create() is only supported on MNs, we use the MN
    # client to create the objects when testing both CN and MN archive().

    # mock_get_system_metadata.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)

    with d1_gmn.tests.gmn_mock.disable_auth():

      base_sid, pid_chain_list = self.create_revision_chain(
        self.client_v2, chain_len=5, sid=True, disable_auth=False
      )

      self.assert_valid_chain(self.client_v2, pid_chain_list, base_sid)

      # Archive head
      assert_archived(gmn_client_v1_v2, pid_chain_list[-1])
      # Archive tail
      assert_archived(gmn_client_v1_v2, pid_chain_list[0])
      # Archive center
      assert_archived(gmn_client_v1_v2, pid_chain_list[3])
