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
"""Test MNRead.getChecksum()

MNRead.getChecksum(session, did[, checksumAlgorithm]) → Checksum
"""
from __future__ import absolute_import

import d1_client.mnclient_1_1
import d1_client.mnclient_2_0
import d1_common.checksum
import d1_common.types.dataoneTypes_v1_1 as v1
import d1_common.types.dataoneTypes_v2_0 as v2
import d1_common.util
import d1_test.mock_api.django_client as mock_django_client
import gmn.tests.gmn_test_case
import responses

BASE_URL = 'http://mock/mn'


class TestChecksum(gmn.tests.gmn_test_case.D1TestCase):
  # @classmethod
  # def setUpClass(cls):
  #   pass # d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    mock_django_client.add_callback(BASE_URL)
    self.client_v1 = d1_client.mnclient_1_1.MemberNodeClient_1_1(BASE_URL)
    self.client_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(BASE_URL)

  def _assert_matching_checksum(self, client, binding):
    local_pid = self.random_pid()
    sci_obj_str, sysmeta_pyxb = self.create(client, binding, local_pid)
    retrieved_checksum_pyxb = client.getChecksum(
      local_pid, vendorSpecific=self.
      include_subjects(gmn.tests.gmn_test_client.GMN_TEST_SUBJECT_TRUSTED)
    )
    self.assertIsInstance(retrieved_checksum_pyxb, binding.Checksum)
    created_checksum_pyxb = d1_common.checksum.create_checksum_object(
      sci_obj_str, retrieved_checksum_pyxb.algorithm
    )
    self.assert_checksums_equal(created_checksum_pyxb, retrieved_checksum_pyxb)

  @responses.activate
  def test_0010_v1(self):
    """MNRead.getChecksum()"""
    self._assert_matching_checksum(self.client_v1, v1)

  @responses.activate
  def test_0010_v2(self):
    """MNRead.getChecksum()"""
    self._assert_matching_checksum(self.client_v2, v2)
