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

import pytest

import d1_common.const
import d1_common.date_time
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.util

import d1_test.d1_test_case
import d1_test.mock_api.catch_all as mock_catch_all


class TestMockCatchAll(d1_test.d1_test_case.D1TestCase):
  @mock_catch_all.activate
  def test_1000(self, cn_client_v2):
    """mock_api.catch_all: Returns a dict correctly echoing the request"""
    mock_catch_all.add_callback(d1_test.d1_test_case.MOCK_CN_BASE_URL)
    echo_dict = cn_client_v2.getFormat('valid_format_id')
    mock_catch_all.assert_expected_echo(echo_dict, 'catch_all', cn_client_v2)

  @mock_catch_all.activate
  def test_1010(self, cn_client_v2):
    """mock_api.catch_all(): Passing a trigger header triggers a DataONEException"""
    mock_catch_all.add_callback(d1_test.d1_test_case.MOCK_CN_BASE_URL)
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v2.getFormat(
        'valid_format_id', vendorSpecific={'trigger': '404'}
      )
