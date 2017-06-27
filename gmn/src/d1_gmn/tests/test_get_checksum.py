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
"""

from __future__ import absolute_import

import StringIO

import pytest
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common.checksum
import d1_common.types
import d1_common.types.exceptions
import d1_common.util


class TestGetChecksum(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self, mn_client_v1_v2):
    """MNRead.getChecksum(): Matching checksums"""
    with d1_gmn.tests.gmn_mock.disable_auth():
      pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(self.client_v2)
      recv_checksum_pyxb = mn_client_v1_v2.getChecksum(pid)
      assert isinstance(recv_checksum_pyxb, mn_client_v1_v2.bindings.Checksum)
      send_checksum_pyxb = d1_common.checksum.create_checksum_object_from_string(
        sciobj_str, recv_checksum_pyxb.algorithm
      )
      self.assert_checksums_equal(send_checksum_pyxb, recv_checksum_pyxb)

  @responses.activate
  def test_1010(self, mn_client_v1_v2):
    """getChecksum(): Supported algorithms return matching checksum
    """

    def test(client, algorithm_str):
      pid, sid, sciobj_str, send_sysmeta_pyxb = (
        self.generate_sciobj_with_defaults(client)
      )
      send_checksum = d1_common.checksum.create_checksum_object_from_string(
        sciobj_str, algorithm_str
      )
      send_sysmeta_pyxb.checksum = send_checksum
      with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
        client.create(pid, StringIO.StringIO(sciobj_str), send_sysmeta_pyxb)
      recv_checksum = client.getChecksum(pid, algorithm_str)
      d1_common.checksum.are_checksums_equal(
        send_sysmeta_pyxb.checksum, recv_checksum
      )

    with d1_gmn.tests.gmn_mock.disable_auth():
      test(mn_client_v1_v2, 'MD5')
      test(mn_client_v1_v2, 'SHA-1')

  @responses.activate
  def test_1020(self, mn_client_v1_v2):
    """getChecksum(): Unsupported algorithm returns InvalidRequest exception"""

    with d1_gmn.tests.gmn_mock.disable_auth():
      pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(mn_client_v1_v2)
      with pytest.raises(d1_common.types.exceptions.InvalidRequest):
        mn_client_v1_v2.getChecksum(pid, 'INVALID_ALGORITHM')

  @responses.activate
  def test_1030(self, mn_client_v1_v2):
    """getChecksum(): Non-existing object raises NotFound exception"""

    with d1_gmn.tests.gmn_mock.disable_auth():
      with pytest.raises(d1_common.types.exceptions.NotFound):
        mn_client_v1_v2.getChecksum('INVALID_PID')
