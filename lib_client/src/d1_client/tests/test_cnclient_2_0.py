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

from __future__ import absolute_import

import d1_test.d1_test_case
import d1_test.mock_api.catch_all

import d1_client.cnclient_2_0


class TestCNClient_2_0(d1_test.d1_test_case.D1TestCase):
  def test_1000(self, cn_client_v2):
    """__init__()"""
    assert isinstance(
      cn_client_v2, d1_client.cnclient_2_0.CoordinatingNodeClient_2_0
    )

  @d1_test.mock_api.catch_all.activate
  def test_1010(self, cn_client_v2):
    """delete(): Generates expected REST call"""
    d1_test.mock_api.catch_all.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
    received_echo_dict = cn_client_v2.delete('valid_pid')
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'delete', cn_client_v2
    )
