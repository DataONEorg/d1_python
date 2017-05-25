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
"""Test MNStorage.delete()

MNStorage.delete(session, did) → Identifier
"""
from __future__ import absolute_import

import d1_client.mnclient_1_1
import d1_client.mnclient_2_0
import d1_common.types.dataoneTypes_v1_1 as v1
import d1_common.types.dataoneTypes_v2_0 as v2
import d1_common.types.exceptions
import d1_common.util
import d1_test.mock_api.django_client as mock_django_client
import django.test
import gmn.tests.gmn_test_case
import responses

BASE_URL = 'http://mock/mn'


@django.test.override_settings(DEBUG=True)
class TestDelete(gmn.tests.gmn_test_case.D1TestCase):
  # @classmethod
  # def setUpClass(cls):
  #   pass # d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    mock_django_client.add_callback(BASE_URL)
    self.client_v1 = d1_client.mnclient_1_1.MemberNodeClient_1_1(BASE_URL)
    self.client_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(BASE_URL)

  # delete(): Standalone

  def _test_0010(self, client, binding, local_sid=None):
    """delete(): Standalone object without SID"""
    local_pid = self.random_pid()
    self.create(client, binding, local_pid, local_sid)
    # Is retrievable
    self.client_v2.getSystemMetadata(local_pid)
    # Delete
    identifier_pyxb = client.delete(local_pid)
    self.assertEqual(identifier_pyxb.value(), local_pid)
    # Is no longer retrievable and raises 404
    self.assertRaises(
      d1_common.types.exceptions.NotFound, client.delete, local_pid
    )
    # PID can now be reused
    self.create(client, binding, local_pid)
    # Is again retrievable
    client.getSystemMetadata(local_pid)

  @responses.activate
  def test_0010_v1(self):
    """MNStorage.delete(): Standalone object without SID"""
    self._test_0010(self.client_v1, v1, local_sid=None)

  @responses.activate
  def test_0010_v2(self):
    """MNStorage.delete(): Standalone object without SID"""
    self._test_0010(self.client_v2, v2, local_sid=None)

  @responses.activate
  def test_0011_v1(self):
    """MNStorage.delete(): Standalone object with SID"""
    self._test_0010(self.client_v1, v1, local_sid=self.random_sid())

  @responses.activate
  def test_0011_v2(self):
    """MNStorage.delete(): Standalone object with SID"""
    self._test_0010(self.client_v2, v2, local_sid=self.random_sid())

  # delete(): Obsolescence chain

  @responses.activate
  def test_0020_v2(self):
    """MNStorage.delete(): Obsolescence chain without SID, delete head"""
    base_sid, pid_chain_list = self.create_chain(self.client_v2, v2, 10)
    self.assert_valid_chain(self.client_v2, pid_chain_list, base_sid)
