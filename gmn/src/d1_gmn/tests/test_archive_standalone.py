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
"""Test MNStorage.archive() for standalone objects
"""

import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case


class TestArchiveStandalone(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def _assert_archived_flag_set(self, client):
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(client)
    assert not sysmeta_pyxb.archived
    pid_archived = client.archive(pid)
    assert pid == pid_archived.value()
    archived_sysmeta_pyxb = client.getSystemMetadata(pid)
    assert archived_sysmeta_pyxb.archived

  @responses.activate
  @d1_gmn.tests.gmn_mock.disable_auth()
  def test_1000(self):
    """MNStorage.archive(): Archived flag is set in sysmeta"""
    self._assert_archived_flag_set(self.client_v1)

  @responses.activate
  @d1_gmn.tests.gmn_mock.disable_auth()
  def test_1010(self):
    """MNStorage.archive(): Archived flag is set in sysmeta"""
    self._assert_archived_flag_set(self.client_v2)
