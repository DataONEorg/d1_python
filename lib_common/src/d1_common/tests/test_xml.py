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

import d1_common.xml

import d1_test.d1_test_case

# TODO: Add tests for remaining functions in xml.py.


class TestXml(d1_test.d1_test_case.D1TestCase):
    def test_1000(self):
        """are_equivalent(): True for identical docs."""
        valid_xml = self.test_files.load_xml_to_str('test_xml_valid_xml.xml')
        assert d1_common.xml.are_equivalent(valid_xml, valid_xml)

    def test_1010(self):
        """are_equivalent(): True for docs identical except for swapped attributes."""
        valid_xml = self.test_files.load_xml_to_str('test_xml_valid_xml.xml')
        valid_swapped_attr_xml = self.test_files.load_utf8_to_str(
            'xml/test_xml_valid_swapped_attr_xml.xml'
        )
        assert d1_common.xml.are_equivalent(valid_xml, valid_swapped_attr_xml)

    def test_1020(self):
        """are_equivalent(): False when an attribute is missing."""
        valid_xml = self.test_files.load_xml_to_str('test_xml_valid_xml.xml')
        missing_count_xml = self.test_files.load_utf8_to_str(
            'xml/test_xml_missing_count_xml.xml'
        )
        assert not d1_common.xml.are_equivalent(valid_xml, missing_count_xml)

    def test_1030(self):
        """are_equivalent(): False when an element is missing."""
        valid_xml = self.test_files.load_xml_to_str('test_xml_valid_xml.xml')
        missing_entry_xml = self.test_files.load_utf8_to_str(
            'xml/test_xml_missing_entry_xml.xml'
        )
        assert not d1_common.xml.are_equivalent(valid_xml, missing_entry_xml)

    def test_1040(self):
        """are_equivalent(): False when elements are in wrong order."""
        valid_xml = self.test_files.load_xml_to_str('test_xml_valid_xml.xml')
        wrong_order_xml = self.test_files.load_xml_to_str(
            'test_xml_wrong_order_xml.xml'
        )
        assert not d1_common.xml.are_equivalent(valid_xml, wrong_order_xml)

    def test_1050(self):
        """are_equivalent(): False when an element is missing text."""
        valid_xml = self.test_files.load_xml_to_str('test_xml_valid_xml.xml')
        missing_text_xml = self.test_files.load_xml_to_str(
            'test_xml_missing_text_xml.xml'
        )
        assert not d1_common.xml.are_equivalent(valid_xml, missing_text_xml)

    def test_1060(self):
        """are_equivalent(): False when the document is not well formed."""
        valid_xml = self.test_files.load_xml_to_str('test_xml_valid_xml.xml')
        syntax_error_xml = self.test_files.load_xml_to_str(
            'test_xml_syntax_error_xml.xml'
        )
        assert not d1_common.xml.are_equivalent(valid_xml, syntax_error_xml)
