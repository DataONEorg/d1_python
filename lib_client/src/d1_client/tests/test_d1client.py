#!/usr/bin/env python

import io

import freezegun
import pytest
import responses

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
import d1_common.types.exceptions

import d1_client.d1client

import d1_test.d1_test_case
import d1_test.mock_api.create
import d1_test.mock_api.get_capabilities


@freezegun.freeze_time("1988-05-01")
class TestDataONEClient(d1_test.d1_test_case.D1TestCase):
    @responses.activate
    def test_1010(self):
        """create_sysmeta()"""
        d1_test.mock_api.get_capabilities.add_callback(
            d1_test.d1_test_case.MOCK_MN_BASE_URL
        )
        d1_test.mock_api.create.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
        client = d1_client.d1client.DataONEClient(
            d1_test.d1_test_case.MOCK_MN_BASE_URL,
            cert_pem_path=self.test_files.get_abs_test_file_path(
                "cert/cert_with_simple_subject_info.pem"
            ),
        )
        sciobj_stream = io.BytesIO(b"test")
        sysmeta_pyxb = client.create_sysmeta(
            "pid", "eml://ecoinformatics.org/eml-2.0.0", sciobj_stream
        )
        self.sample.assert_equals(sysmeta_pyxb, "create_sysmeta")

    @responses.activate
    def test_1015(self):
        """create_sciobj(): Assert on unknown formatId"""
        client = d1_client.d1client.DataONEClient()
        with pytest.raises(
            d1_common.types.exceptions.InvalidSystemMetadata, match="Unknown formatId"
        ):
            sciobj_stream = io.BytesIO(b"test")
            client.create_sciobj("pid", "unknown_format_id", sciobj_stream)

    @responses.activate
    def test_1020(self):
        """create_sciobj(): Unknown formatId"""
        d1_test.mock_api.get_capabilities.add_callback(
            d1_test.d1_test_case.MOCK_MN_BASE_URL
        )
        d1_test.mock_api.create.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
        client = d1_client.d1client.DataONEClient(
            d1_test.d1_test_case.MOCK_MN_BASE_URL,
            cert_pem_path=self.test_files.get_abs_test_file_path(
                "cert/cert_with_simple_subject_info.pem"
            ),
        )
        sciobj_stream = io.BytesIO(b"test")
        client.create_sciobj("pid", "eml://ecoinformatics.org/eml-2.0.0", sciobj_stream)
