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
import os

import pytest

import d1_scimeta.util
import d1_scimeta.validate

import d1_test.d1_test_case


class TestSciMetaValidate(d1_test.d1_test_case.D1TestCase):
    @pytest.mark.parametrize(
        "missing_invalid_format_id",
        ["http://www.icpsr.umich.edu/DDI", "unknown_format_id"],
    )
    def test_1000(self, missing_invalid_format_id):
        """SciMeta.assert_valid(): Missing schema raises SciMetaError with
        expected message."""
        xml_str = self.test_files.load_bin("xml/isotc211/ieda.xml")
        with pytest.raises(d1_scimeta.util.SciMetaError, match="Invalid formatId"):
            d1_scimeta.validate.assert_valid(missing_invalid_format_id, xml_str)

    def test_1020(self):
        """SciMeta.assert_valid(): onedcx does not validate as EML."""
        xml_str = self.test_files.load_bin("xml/scimeta_dc_1.xml")
        format_id = "eml://ecoinformatics.org/eml-2.1.1"
        with pytest.raises(
            d1_scimeta.util.SciMetaError, match="XML document does not validate"
        ):
            d1_scimeta.validate.assert_valid(format_id, xml_str)

    def test_1030(self):
        """SciMeta.assert_valid(): onedcx validates successfully as DataONE Dublin Core
        Extended."""
        xml_str = self.test_files.load_bin("xml/scimeta_dc_1.xml")
        format_id = "http://ns.dataone.org/metadata/schema/onedcx/v1.0"
        d1_scimeta.validate.assert_valid(format_id, xml_str)

    def test_1050(self):
        """SciMeta.assert_valid(): Valid EML 2.1.1."""
        xml_str = self.test_files.load_bin("xml/scimeta_eml_valid.xml")
        format_id = "eml://ecoinformatics.org/eml-2.1.1"
        d1_scimeta.validate.assert_valid(format_id, xml_str)

    def test_1060(self):
        """SciMeta.assert_valid(): Invalid EML 2.1.1: Unexpected element."""
        xml_str = self.test_files.load_bin("xml/scimeta_eml_invalid_1.xml")
        format_id = "eml://ecoinformatics.org/eml-2.1.1"
        with pytest.raises(d1_scimeta.util.SciMetaError, match="unexpectedElement"):
            d1_scimeta.validate.assert_valid(format_id, xml_str)

    def test_1070(self):
        """SciMeta.assert_valid(): Invalid EML 2.1.1: Missing child element."""
        xml_str = self.test_files.load_bin("xml/scimeta_eml_invalid_2.xml")
        format_id = "eml://ecoinformatics.org/eml-2.1.1"
        with pytest.raises(d1_scimeta.util.SciMetaError, match="Missing child element"):
            d1_scimeta.validate.assert_valid(format_id, xml_str)

    # ISO

    @pytest.mark.parametrize(
        "format_id",
        [
            "eml://ecoinformatics.org/eml-2.0.0",
            "eml://ecoinformatics.org/eml-2.0.1",
            "eml://ecoinformatics.org/eml-2.1.0",
            "eml://ecoinformatics.org/eml-2.1.1",
            # "FGDC-STD-001-1998",
            # "FGDC-STD-001.1-1999",
            "http://datacite.org/schema/kernel-3.0",
            "http://datacite.org/schema/kernel-3.1",
            "http://datadryad.org/profile/v3.1",
            "http://ns.dataone.org/metadata/schema/onedcx/v1.0",
            "http://purl.org/dryad/terms/",
            "http://purl.org/ornl/schema/mercury/terms/v1.0",
            # "http://rs.tdwg.org/dwc/xsd/simpledarwincore/",
        ],
    )
    def test_1080(self, format_id):
        """SciMeta.assert_valid(): ISO/TC 211 does not validate as other formatId."""
        xml_str = self.test_files.load_bin("xml/isotc211/noaa_ncei.xml")
        with pytest.raises(
            d1_scimeta.util.SciMetaError, match="XML document does not validate"
        ):
            d1_scimeta.validate.assert_valid(format_id, xml_str)

    @pytest.mark.parametrize(
        "xml_doc", ["boilerplate.xml", "ieda.xml", "noaa_ncei.xml", "nsidc.xml"]
    )
    def test_1090(self, xml_doc):
        """SciMeta.assert_valid(): Valid ISO/TC 211"""
        xml_str = self.test_files.load_xml_to_bytes(os.path.join("isotc211", xml_doc))
        d1_scimeta.validate.assert_valid("http://www.isotc211.org/2005/gmd", xml_str)
