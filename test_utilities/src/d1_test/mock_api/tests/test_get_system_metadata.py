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

import freezegun
import pytest
import responses

import d1_common.const
import d1_common.date_time
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.util
import d1_common.xml

import d1_test.d1_test_case
import d1_test.mock_api.get_system_metadata as mock_sysmeta


@d1_test.d1_test_case.reproducible_random_decorator('TestMockSystemMetadata')
@freezegun.freeze_time('1977-01-27')
class TestMockSystemMetadata(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def test_1000(self, mn_client_v1_v2):
    """mock_api.getSystemMetadata() returns a System Metadata PyXB object"""
    mock_sysmeta.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    assert isinstance(
      mn_client_v1_v2.getSystemMetadata('test_pid'),
      mn_client_v1_v2.bindings.SystemMetadata
    )

  @responses.activate
  def test_1010(self, mn_client_v1_v2):
    """mock_api.getSystemMetadata(): Passing a trigger header triggers a DataONEException"""
    mock_sysmeta.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    with pytest.raises(d1_common.types.exceptions.NotFound):
      mn_client_v1_v2.getSystemMetadata(
        'test_pid', vendorSpecific={'trigger': '404'}
      )

  @responses.activate
  def test_1020(self, mn_client_v1_v2):
    """mock_api.getSystemMetadata() returns expected SysMeta values"""
    mock_sysmeta.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    sysmeta_pyxb = mn_client_v1_v2.getSystemMetadata('test_pid')
    self.sample.assert_equals(
      sysmeta_pyxb, 'mock_get_system_metadata', mn_client_v1_v2
    )
