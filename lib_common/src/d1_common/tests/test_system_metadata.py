#!/usr/bin/env python

import io

import freezegun
import pyxb

import pytest

import d1_common.system_metadata
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
import d1_test.test_files


class TestSystemMetadata(d1_test.d1_test_case.D1TestCase):
    sm_pyxb = d1_test.test_files.load_xml_to_pyxb("systemMetadata_v2_0.xml")

    def test_1000(self):
        """PyXB performs schema validation on sysmeta object and raises
        pyxb.PyXBException on invalid XML doc."""
        with pytest.raises(pyxb.PyXBException):
            self.test_files.load_xml_to_pyxb("systemMetadata_v1_0.invalid.xml")

    def test_1010(self):
        """are_equivalent() Returns False for modified sysmeta."""
        modified_pyxb = self.test_files.load_xml_to_pyxb("systemMetadata_v2_0.xml")
        modified_pyxb.identifier = "modifiedIdentifier"
        assert not d1_common.system_metadata.are_equivalent_pyxb(
            self.sm_pyxb, modified_pyxb, ignore_filename=True
        )

    def test_1020(self):
        """are_equivalent() Returns True for duplicated sysmeta."""
        assert d1_common.system_metadata.are_equivalent_pyxb(
            self.sm_pyxb, self.sm_pyxb, ignore_filename=True
        )

    def test_1030(self):
        """are_equivalent() Returns True for sysmeta where elements that can occur in
        any order without changing the meaning of the doc have been shuffled around."""
        swizzled_pyxb = self.test_files.load_xml_to_pyxb(
            "systemMetadata_v2_0.swizzled.xml"
        )
        assert d1_common.system_metadata.are_equivalent_pyxb(
            self.sm_pyxb, swizzled_pyxb, ignore_filename=True
        )

    def test_1040(self):
        """update_elements(): Elements are copied from src to dst."""
        dst_pyxb = self.test_files.load_xml_to_pyxb("sysmeta_variation_1.xml")
        src_pyxb = self.test_files.load_xml_to_pyxb("sysmeta_variation_2.xml")
        d1_common.system_metadata.update_elements(
            dst_pyxb, src_pyxb, ["identifier", "accessPolicy", "size", "checksum"]
        )
        # orig_pyxb = self.test_files.load_xml_to_pyxb('sysmeta_variation_1.xml')
        # logging.debug(self.sample.get_sxs_diff(orig_pyxb, dst_pyxb))
        self.sample.assert_equals(dst_pyxb, "update_elements_copy")

    def test_1050(self):
        """update_elements(): Passing invalid element raies ValueError."""
        dst_pyxb = self.test_files.load_xml_to_pyxb("sysmeta_variation_1.xml")
        src_pyxb = self.test_files.load_xml_to_pyxb("sysmeta_variation_2.xml")
        with pytest.raises(ValueError) as exc_info:
            d1_common.system_metadata.update_elements(
                dst_pyxb,
                src_pyxb,
                [
                    "identifier",
                    "accessPolicy",
                    "invalid1",
                    "size",
                    "checksum",
                    "invalid2",
                ],
            )
        self.sample.assert_equals(str(exc_info.exconly()), "update_elements_invalid")


    @freezegun.freeze_time('2000-01-01')
    def test_2000(self):
        """generate_system_metadata_pyxb(): Basic"""
        sysmeta_pyxb = d1_common.system_metadata.generate_system_metadata_pyxb(
            'pid', 'format_id', io.BytesIO(b'body'), 'submitter', 'rights_holder', 'aurn:mn:urn',
            is_private=True
        )
        s = d1_common.xml.serialize_to_xml_str(sysmeta_pyxb, pretty=True)
        self.sample.assert_equals(s, "gen_sysmeta_basic")

    @freezegun.freeze_time('2000-01-01')
    def test_2010(self):
        """generate_system_metadata_pyxb(): With AccessPolicy"""
        sysmeta_pyxb = d1_common.system_metadata.generate_system_metadata_pyxb(
            'pid', 'format_id', io.BytesIO(b'body'), 'submitter', 'rights_holder', 'aurn:mn:urn',
            is_private=False, access_list=(('subj1', 'read'), ('subj2', 'write'), ('subj3', 'changePermission'))
        )
        s = d1_common.xml.serialize_to_xml_str(sysmeta_pyxb, pretty=True)
        self.sample.assert_equals(s, "gen_sysmeta_access")

    @freezegun.freeze_time('2000-01-01')
    def test_2020(self):
        """generate_system_metadata_pyxb(): With ReplicationPolicy"""
        sysmeta_pyxb = d1_common.system_metadata.generate_system_metadata_pyxb(
            'pid', 'format_id', io.BytesIO(b'body'), 'submitter', 'rights_holder', 'aurn:mn:urn',
            is_replication_allowed=True, prefered_mn_list=('pref_mn1', 'pref_mn2', 'pref_mn3'),
            blocked_mn_list=('block_mn1', 'block_mn2', 'block_mn3'),

        )
        s = d1_common.xml.serialize_to_xml_str(sysmeta_pyxb, pretty=True)
        self.sample.assert_equals(s, "gen_sysmeta_replication")

    @freezegun.freeze_time('2000-01-01')
    def test_2030(self):
        """generate_system_metadata_pyxb(): With SID and obsolescence"""
        sysmeta_pyxb = d1_common.system_metadata.generate_system_metadata_pyxb(
            'pid', 'format_id', io.BytesIO(b'body'), 'submitter',
            'rights_holder', 'aurn:mn:urn',
            sid='series_id', obsoleted_by_pid='obsoleted_by_pid', obsoletes_pid='obsoletes_pid',
            is_archived=True,

        )
        s = d1_common.xml.serialize_to_xml_str(sysmeta_pyxb, pretty=True)
        self.sample.assert_equals(s, "gen_sysmeta_obsolescence")

    @freezegun.freeze_time('2000-01-01')
    def test_2035(self):
        """generate_system_metadata_pyxb(): With MediaType, assert on media_name"""
        with pytest.raises(AssertionError):
            d1_common.system_metadata.generate_system_metadata_pyxb(
            'pid', 'format_id', io.BytesIO(b'body'), 'submitter',
            'rights_holder', 'aurn:mn:urn',
            media_property_list=(('prop1','val1'),)

        )

    @freezegun.freeze_time('2000-01-01')
    def test_2040(self):
        """generate_system_metadata_pyxb(): With MediaType"""
        sysmeta_pyxb = d1_common.system_metadata.generate_system_metadata_pyxb(
            'pid', 'format_id', io.BytesIO(b'body'), 'submitter',
            'rights_holder', 'aurn:mn:urn',
            media_name='media_name', media_property_list=(('prop1','val1'),('prop2','val2'),('prop3','val3'),)

        )
        s = d1_common.xml.serialize_to_xml_str(sysmeta_pyxb, pretty=True)
        self.sample.assert_equals(s, "gen_sysmeta_media")
