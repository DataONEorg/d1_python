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

import d1_scimeta.xml_schema

import d1_test.d1_test_case


class TestSciMeta(d1_test.d1_test_case.D1TestCase):
    def test_1000(self):
        """SciMeta.validate(): Uninstalled schema raises SciMetaValidationError with
        expected message."""
        # xml_str = self.load_utf8_to_str('xml/scimeta_isotc211_1.xml')
        xml_str = self.test_files.load_bin('xml/scimeta_isotc211_1.xml')
        format_id = 'http://www.icpsr.umich.edu/DDI'
        with pytest.raises(
            d1_scimeta.xml_schema.SciMetaValidationError,
            match='Schema not installed for Science Metadata',
        ):
            d1_scimeta.xml_schema.validate(format_id, xml_str)

    def test_1010(self):
        """SciMeta.validate(): Unknown formatId raises SciMetaValidationError with
        expected message."""
        xml_str = self.test_files.load_bin('xml/scimeta_isotc211_1.xml')
        format_id = 'unknown_format_id'
        with pytest.raises(
            d1_scimeta.xml_schema.SciMetaValidationError,
            match='Invalid Science Metadata',
        ):
            d1_scimeta.xml_schema.validate(format_id, xml_str)

    def test_1020(self):
        """SciMeta.validate(): onedcx does not validate as EML."""
        xml_str = self.test_files.load_bin('xml/scimeta_dc_1.xml')
        format_id = 'eml://ecoinformatics.org/eml-2.1.1'
        with pytest.raises(
            d1_scimeta.xml_schema.SciMetaValidationError,
            match='No matching global declaration available for the validation root',
        ):
            d1_scimeta.xml_schema.validate(format_id, xml_str)

    def test_1030(self):
        """SciMeta.validate(): onedcx validates successfully as DataONE Dublin Core
        Extended."""
        xml_str = self.test_files.load_bin('xml/scimeta_dc_1.xml')
        format_id = 'http://ns.dataone.org/metadata/schema/onedcx/v1.0'
        d1_scimeta.xml_schema.validate(format_id, xml_str)

    def test_1040(self):
        """SciMeta.validate(): ISO/TC 211 does not validate as Dryad."""
        xml_str = self.test_files.load_bin('xml/scimeta_isotc211_1.xml')
        format_id = 'http://datadryad.org/profile/v3.1'
        with pytest.raises(
            d1_scimeta.xml_schema.SciMetaValidationError,
            match='No matching global declaration available for the validation root',
        ):
            d1_scimeta.xml_schema.validate(format_id, xml_str)

    def test_1050(self):
        """SciMeta.validate(): Valid EML 2.1.1."""
        xml_str = self.test_files.load_bin('xml/scimeta_eml_valid.xml')
        format_id = 'eml://ecoinformatics.org/eml-2.1.1'
        d1_scimeta.xml_schema.validate(format_id, xml_str)

    def test_1060(self):
        """SciMeta.validate(): Invalid EML 2.1.1: Unexpected element."""
        xml_str = self.test_files.load_bin('xml/scimeta_eml_invalid_1.xml')
        format_id = 'eml://ecoinformatics.org/eml-2.1.1'
        with pytest.raises(
            d1_scimeta.xml_schema.SciMetaValidationError, match='unexpectedElement'
        ):
            d1_scimeta.xml_schema.validate(format_id, xml_str)

    def test_1070(self):
        """SciMeta.validate(): Invalid EML 2.1.1: Missing child element."""
        xml_str = self.test_files.load_bin('xml/scimeta_eml_invalid_2.xml')
        format_id = 'eml://ecoinformatics.org/eml-2.1.1'
        with pytest.raises(
            d1_scimeta.xml_schema.SciMetaValidationError, match='Missing child element'
        ):
            d1_scimeta.xml_schema.validate(format_id, xml_str)
