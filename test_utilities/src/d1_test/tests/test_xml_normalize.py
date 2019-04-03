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
import pytest

import d1_test.d1_test_case
import d1_test.xml_normalize


class TestXmlNormalize(d1_test.d1_test_case.D1TestCase):
    @pytest.mark.parametrize(
        "xml_testfile",
        [
            'xml_normalize_1.xml',
            'xml_normalize_2.xml',
            'systemMetadata_v2_0.swizzled.xml',
            'node_list_gmn_valid_swizzled.xml',
        ],
    )
    def test_1000(self, xml_testfile):
        xml = self.test_files.load_xml_to_str(xml_testfile)
        json = d1_test.xml_normalize.get_normalized_xml_representation(xml)
        self.sample.assert_equals(json, xml_testfile)
