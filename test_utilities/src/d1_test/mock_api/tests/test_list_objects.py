# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
import responses

import d1_common.types.exceptions

import d1_test.d1_test_case
import d1_test.mock_api.list_objects


class TestMockListObjects(d1_test.d1_test_case.D1TestCase):
    @responses.activate
    def test_1000(self, mn_client_v1_v2):
        """mock_api.listObjects() returns a DataONE ObjectList PyXB object."""
        d1_test.mock_api.list_objects.add_callback(
            d1_test.d1_test_case.MOCK_MN_BASE_URL
        )
        assert isinstance(
            mn_client_v1_v2.listObjects(), mn_client_v1_v2.pyxb_binding.ObjectList
        )

    @responses.activate
    def test_1010(self, mn_client_v1_v2):
        """mock_api.listObjects() returns a populated ObjectList."""
        d1_test.mock_api.list_objects.add_callback(
            d1_test.d1_test_case.MOCK_MN_BASE_URL
        )
        object_list = mn_client_v1_v2.listObjects()
        self.sample.assert_equals(object_list, 'populated')

    @responses.activate
    def test_1020(self, mn_client_v1_v2):
        """mock_api.listObjects(): Passing a trigger header triggers a
        DataONEException."""
        d1_test.mock_api.list_objects.add_callback(
            d1_test.d1_test_case.MOCK_MN_BASE_URL
        )
        with pytest.raises(d1_common.types.exceptions.ServiceFailure):
            mn_client_v1_v2.listObjects(vendorSpecific={'trigger': '500'})

    # TODO: More tests
