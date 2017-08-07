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
from __future__ import print_function

import responses

import d1_test.d1_test_case
import d1_test.mock_api.get_capabilities as get_capabilities


class TestMockGetCapabilities(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def test_1000(self, mn_client_v1_v2):
    """mock_api.getCapabilities() returns a DataONE Node PyXB object"""
    get_capabilities.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
    node_pyxb = mn_client_v1_v2.getCapabilities()
    self.sample.assert_equals(
      node_pyxb, 'mock_get_capabilities', mn_client_v1_v2
    )
