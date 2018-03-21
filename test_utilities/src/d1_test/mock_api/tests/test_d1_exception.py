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

import d1_test.d1_test_case
import d1_test.mock_api.d1_exception
import d1_test.mock_api.util
import d1_test.sample


class TestMockD1Exception(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """trigger_by_status_code(): GET request returns DataONEException XML doc"""

    class FakeRequest:
      method = 'GET'

    exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_status_code(
      FakeRequest(), 413
    )
    d1_test.sample.assert_equals(
      exc_response_tup, 'trigger_by_status_code_regular'
    )

  def test_1010(self):
    """trigger_by_status_code(): HEAD request returns DataONEException headers"""

    class FakeRequest:
      method = 'HEAD'

    exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_status_code(
      FakeRequest(), 413
    )
    d1_test.sample.assert_equals(
      exc_response_tup, 'trigger_by_status_code_head'
    )

  def test_1020(self):
    """trigger_by_pid()"""

    class FakeRequest:
      method = 'GET'

    exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_pid(
      FakeRequest, 'trigger_413'
    )
    d1_test.sample.assert_equals(exc_response_tup, 'trigger_by_pid')
