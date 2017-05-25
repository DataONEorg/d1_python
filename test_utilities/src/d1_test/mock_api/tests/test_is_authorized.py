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

import unittest

import d1_client.mnclient_2_0
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.util
import d1_test.mock_api.is_authorized as mock_is_authorized
import d1_test.mock_api.tests.config as config
import responses


class TestMockIsAuthorized(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    pass # d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      base_url=config.MN_RESPONSES_BASE_URL
    )

  @responses.activate
  def test_0010(self):
    """mock_api.isAuthorized(): Returns 200 for 'authorized_pid"""
    mock_is_authorized.add_callback(config.MN_RESPONSES_BASE_URL)
    self.assertTrue(self.client.isAuthorized('authorized_pid', 'read'))

  @responses.activate
  def test_0020(self):
    """mock_api.isAuthorized(): Raises NotAuthorized for 'unauthorized_pid"""
    mock_is_authorized.add_callback(config.MN_RESPONSES_BASE_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotAuthorized, self.client.isAuthorized,
      'unauthorized_pid', 'read'
    )
