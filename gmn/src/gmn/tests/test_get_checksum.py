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
"""Test MNRead.getChecksum()"""
from __future__ import absolute_import

import StringIO

import responses

import d1_common.util
import d1_common.types
import d1_common.checksum
import d1_common.types.exceptions

import gmn.tests.gmn_mock
import gmn.tests.gmn_test_case


@gmn.tests.gmn_mock.disable_auth_decorator
class TestGetChecksum(gmn.tests.gmn_test_case.D1TestCase):
  @responses.activate
  def test_1010(self):
    """MNRead.getChecksum(): Matching checksums"""

    def test(client, binding):
      pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(
        self.client_v2, self.v2
      )
      recv_checksum_pyxb = client.getChecksum(pid)
      self.assertIsInstance(recv_checksum_pyxb, binding.Checksum)
      send_checksum_pyxb = d1_common.checksum.create_checksum_object(
        sciobj_str, recv_checksum_pyxb.algorithm
      )
      self.assert_checksums_equal(send_checksum_pyxb, recv_checksum_pyxb)

    test(self.client_v1, self.v1)
    test(self.client_v2, self.v2)

  @responses.activate
  def test_1020(self):
    """getChecksum(): Supported algorithms return matching checksum"""

    def test(client, binding, algorithm_str):
      pid, sid, sciobj_str, send_sysmeta_pyxb = (
        self.generate_sciobj_with_defaults(binding)
      )
      send_checksum = d1_common.checksum.create_checksum_object_from_string(
        sciobj_str, algorithm_str
      )
      send_sysmeta_pyxb.checksum = send_checksum
      client.create(pid, StringIO.StringIO(sciobj_str), send_sysmeta_pyxb)
      recv_checksum = client.getChecksum(pid, algorithm_str)
      d1_common.checksum.are_checksums_equal(
        send_sysmeta_pyxb.checksum, recv_checksum
      )

    test(self.client_v1, self.v1, 'MD5')
    test(self.client_v1, self.v1, 'SHA-1')
    test(self.client_v2, self.v2, 'MD5')
    test(self.client_v2, self.v2, 'SHA-1')

  @responses.activate
  def test_1040(self):
    """getChecksum(): Unsupported algorithm returns InvalidRequest exception"""

    def test(client, binding):
      pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(client, binding)
      with self.assertRaises(d1_common.types.exceptions.InvalidRequest):
        client.getChecksum(pid, 'INVALID_ALGORITHM')

    test(self.client_v1, self.v1)
    test(self.client_v2, self.v2)

  @responses.activate
  def test_1050(self):
    """getChecksum(): Non-existing object raises NotFound exception"""

    def test(client, binding):
      with self.assertRaises(d1_common.types.exceptions.NotFound):
        client.getChecksum('INVALID_PID')

    test(self.client_v1, self.v1)
    test(self.client_v2, self.v2)
