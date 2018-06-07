#!/usr/bin/env python
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

import mock
import responses

import d1_common.logging_context
import d1_common.type_conversions
import d1_common.types.exceptions
import d1_common.util

import d1_test.d1_test_case
import d1_test.mock_api.get_capabilities

import d1_client.d1client


class TesttUtil(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def test_1000(self, mn_client_v1_v2):
    """get_api_major_by_base_url(): Returns correct API major versions"""
    d1_test.mock_api.get_capabilities.add_callback(
      d1_test.d1_test_case.MOCK_MN_BASE_URL
    )

    node_pyxb = mn_client_v1_v2.getCapabilities()
    with mock.patch(
        'd1_client.mnclient.MemberNodeClient.getCapabilities',
        return_value=node_pyxb
    ):
      node_api_major = int(
        d1_common.type_conversions.
        get_version_tag_by_bindings(mn_client_v1_v2.bindings)[-1]
      )
      assert (
        d1_client.d1client.get_api_major_by_base_url(
          d1_test.d1_test_case.MOCK_MN_BASE_URL
        ) == node_api_major
      )
