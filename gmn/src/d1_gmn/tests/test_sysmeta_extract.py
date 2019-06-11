#!/usr/bin/env python

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
"""Test: Extract SciObj information from models."""
import io

import freezegun
import responses

import d1_gmn.app.sysmeta_extract
import d1_gmn.tests.gmn_test_case

import d1_test.d1_test_case


@d1_test.d1_test_case.reproducible_random_decorator("TestSciObjExtract")
@freezegun.freeze_time("1917-7-17")
class TestSciObjExtract(d1_gmn.tests.gmn_test_case.GMNTestCase):
    @responses.activate
    def test_1000(self, gmn_client_v2):
        """Extract single lookup based value, filtered to SID containing "bc"."""
        sciobj_list = d1_gmn.app.sysmeta_extract.extract_values(
            filter_arg_dict={"pid__chainmember_pid__chain__sid__did__contains": "bc"},
            field_list=["formatid"],
        )
        self.sample.assert_equals(sciobj_list, "single_lookup")

    @responses.activate
    def test_1010(self, gmn_client_v2):
        """Extract single generate based value, filtered to SID containing "cd"."""
        sciobj_list = d1_gmn.app.sysmeta_extract.extract_values(
            filter_arg_dict={"pid__chainmember_pid__chain__sid__did__contains": "cd"},
            field_list=["permissions"],
        )
        self.sample.assert_equals(sciobj_list, "single_generate")

    @responses.activate
    def test_1020(self, gmn_client_v2):
        """Extract all values to stream."""
        str_buf = io.StringIO()
        d1_gmn.app.sysmeta_extract.extract_values(out_stream=str_buf)
        self.sample.assert_equals(str_buf.getvalue(), "all_stream")
