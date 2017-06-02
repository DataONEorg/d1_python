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
"""Test MNStorage.archive() for objects in revision chains"""

from __future__ import absolute_import

import responses

import gmn.tests.gmn_mock
import gmn.tests.gmn_test_case


@gmn.tests.gmn_mock.disable_auth_decorator
class TestArchiveRevision(gmn.tests.gmn_test_case.D1TestCase):
  @responses.activate
  def test_0010(self):
    """archive(): Archived flag correctly set and represented"""

    def test(client, binding, sid=None):
      base_sid, pid_chain_list = self.create_obj_chain(
        client, binding, chain_len=5, sid=sid
      )
      self.assert_valid_chain(client, pid_chain_list, base_sid)

      def assert_archived(client, binding, pid):
        unarchived_sysmeta_pyxb = client.getSystemMetadata(pid)
        self.assertFalse(unarchived_sysmeta_pyxb.archived)
        pid_archived = client.archive(pid)
        self.assertEqual(pid, pid_archived.value())
        archived_sysmeta_pyxb = client.getSystemMetadata(pid)
        self.assertTrue(archived_sysmeta_pyxb.archived)
        self.assert_eq_sysmeta_sid(
          unarchived_sysmeta_pyxb,
          archived_sysmeta_pyxb,
        )

      # Archive head
      assert_archived(client, binding, pid_chain_list[-1])
      # Archive tail
      assert_archived(client, binding, pid_chain_list[0])
      # Archive center
      assert_archived(client, binding, pid_chain_list[3])

    test(self.client_v1, self.v1)
    test(self.client_v2, self.v2)
