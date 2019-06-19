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
"""Test MNRead.describe()"""
import freezegun
import pytest
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common.types.exceptions

import d1_test.d1_test_case
import d1_test.instance_generator.identifier


@d1_test.d1_test_case.reproducible_random_decorator("TestDescribe")
@freezegun.freeze_time("1945-03-01")
class TestDescribe(d1_gmn.tests.gmn_test_case.GMNTestCase):
    @responses.activate
    def test_1000(self, gmn_client_v1_v2):
        """MNStorage.describe(): Returns valid header for valid object."""

        with d1_gmn.tests.gmn_mock.disable_auth():
            pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
                gmn_client_v1_v2, sid=True
            )
            info_dict = gmn_client_v1_v2.describe(pid)
            assert "dataone-formatid" in info_dict
            assert "content-length" in info_dict
            assert "last-modified" in info_dict
            assert "dataone-checksum" in info_dict
            self.sample.assert_equals(info_dict, "valid_object", gmn_client_v1_v2)

    @responses.activate
    def test_1010(self, gmn_client_v1_v2):
        """MNStorage.describe(): Returns 404 for unknown object."""
        with d1_gmn.tests.gmn_mock.disable_auth():
            with pytest.raises(d1_common.types.exceptions.NotFound):
                gmn_client_v1_v2.describe(
                    d1_test.instance_generator.identifier.generate_pid()
                )

    @responses.activate
    def test_1020(self, gmn_client_v1_v2):
        """MNStorage.describe(): Returns the DataONE exception as headers."""
        with d1_gmn.tests.gmn_mock.disable_auth():
            response = gmn_client_v1_v2.describeResponse(
                d1_test.instance_generator.identifier.generate_pid()
            )
            self.sample.assert_equals(
                response.headers, "exception_header", gmn_client_v1_v2
            )

    @responses.activate
    def test_1030(self, gmn_client_v1_v2):
        """MNStorage.describe(): DataONE exception transferred in headers is detected
        and raised as DatONEException."""
        with d1_gmn.tests.gmn_mock.disable_auth():
            try:
                gmn_client_v1_v2.describe(
                    d1_test.instance_generator.identifier.generate_pid()
                )
            except d1_common.types.exceptions.NotFound as e:
                self.sample.assert_equals(
                    e.friendly_format(), "exception", gmn_client_v1_v2
                )
