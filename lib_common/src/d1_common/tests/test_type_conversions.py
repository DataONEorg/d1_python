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

import d1_common.type_conversions

import d1_test.d1_test_case


class TestTypeConversions(d1_test.d1_test_case.D1TestCase):
    def test_1000(self):
        """is_v1()"""
        systemMetadata_v1_0_str = self.test_files.load_xml_to_str(
            'systemMetadata_v1_0.xml'
        )
        assert d1_common.type_conversions.str_is_v1(systemMetadata_v1_0_str)
        assert not d1_common.type_conversions.str_is_v2(systemMetadata_v1_0_str)

    def test_1010(self):
        """is_v2()"""
        systemMetadata_v2_0_str = self.test_files.load_xml_to_str(
            'systemMetadata_v2_0.xml'
        )
        assert d1_common.type_conversions.str_is_v2(systemMetadata_v2_0_str)
        assert not d1_common.type_conversions.str_is_v1(systemMetadata_v2_0_str)

    def test_1020(self):
        """v1 XML string to PyXB conversion and type check."""
        systemMetadata_v1_0_str = self.test_files.load_xml_to_str(
            'systemMetadata_v1_0.xml'
        )
        systemMetadata_v1_0_pyxb = d1_common.type_conversions.str_to_pyxb(
            systemMetadata_v1_0_str
        )
        assert d1_common.type_conversions.pyxb_is_v1(systemMetadata_v1_0_pyxb)

    def test_1030(self):
        """v2 XML string to PyXB conversion and type check."""
        systemMetadata_v2_0_str = self.test_files.load_xml_to_str(
            'systemMetadata_v2_0.xml'
        )
        systemMetadata_v2_0_pyxb = d1_common.type_conversions.str_to_pyxb(
            systemMetadata_v2_0_str
        )
        assert d1_common.type_conversions.pyxb_is_v2(systemMetadata_v2_0_pyxb)
        assert not d1_common.type_conversions.pyxb_is_v1(systemMetadata_v2_0_pyxb)

    def test_1040(self):
        """LogEntry v1 to v2."""
        logEntry_v1_0_str = self.test_files.load_xml_to_str('logEntry_v1_0.xml')
        logEntry_v2_str = d1_common.type_conversions.str_to_v2_str(logEntry_v1_0_str)
        assert d1_common.type_conversions.str_is_v2(logEntry_v2_str)
        assert not d1_common.type_conversions.str_is_v1(logEntry_v2_str)

    def test_1050(self):
        """LogEntry v2 to v1."""
        logEntry_v2_0_str = self.test_files.load_xml_to_str('logEntry_v2_0.xml')
        logEntry_v1_str = d1_common.type_conversions.str_to_v1_str(logEntry_v2_0_str)
        assert d1_common.type_conversions.str_is_v1(logEntry_v1_str)
        assert not d1_common.type_conversions.str_is_v2(logEntry_v1_str)

    def test_1060(self):
        """Log v2 to v1."""
        log_v2_0_str = self.test_files.load_xml_to_str('log_v2_0.xml')
        log_v1_str = d1_common.type_conversions.str_to_v1_str(log_v2_0_str)
        assert d1_common.type_conversions.str_is_v1(log_v1_str)
        assert not d1_common.type_conversions.str_is_v2(log_v1_str)

    def test_1070(self):
        """Node v2 to v1."""
        node_v2_0_str = self.test_files.load_xml_to_str('node_v2_0.xml')
        node_v1_str = d1_common.type_conversions.str_to_v1_str(node_v2_0_str)
        assert d1_common.type_conversions.str_is_v1(node_v1_str)
        assert not d1_common.type_conversions.str_is_v2(node_v1_str)

    def test_1080(self):
        """NodeList v2 to v1."""
        node_list_v2_0_str = self.test_files.load_xml_to_str('nodeList_v2_0.xml')
        node_list_v1_str = d1_common.type_conversions.str_to_v1_str(node_list_v2_0_str)
        assert d1_common.type_conversions.str_is_v1(node_list_v1_str)
        assert not d1_common.type_conversions.str_is_v2(node_list_v1_str)

    def test_1090(self):
        """SystemMetadata v2 to v1."""
        systemMetadata_v2_0_str = self.test_files.load_xml_to_str(
            'systemMetadata_v2_0.xml'
        )
        systemMetadata_v1_str = d1_common.type_conversions.str_to_v1_str(
            systemMetadata_v2_0_str
        )
        assert d1_common.type_conversions.str_is_v1(systemMetadata_v1_str)
        assert not d1_common.type_conversions.str_is_v2(systemMetadata_v1_str)
