#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Test serialization and de-serialization of the ObjectList type
"""

# Stdlib
import unittest
import xml.sax

# 3rd party
import pyxb

# D1
from d1_common.types import dataoneTypes

# App
import util

EG_OBJECTLIST_GMN = """<?xml version="1.0" ?>
<ns1:objectList count="5" start="0" total="154933"
    xmlns:ns1="http://ns.dataone.org/service/types/v1">
    <objectInfo>
        <identifier>__invalid_test_object__81e0e944-bf2d-11e0-a5cd-8122f1474081</identifier>
        <formatId>CF-1.2</formatId>
        <!-- <objectFormat>
            <formatId>CF-1.2</formatId>
            <formatName>CF-1.2</formatName>
            <scienceMetadata>false</scienceMetadata>
        </objectFormat> -->
        <checksum algorithm="MD5">9d7d2447d5e1e37b647ad7c836f9a1b950f4d950</checksum>
        <dateSysMetadataModified>2011-08-05T06:38:19.532139</dateSysMetadataModified>
        <size>1772</size>
    </objectInfo>
    <objectInfo>
        <identifier>__invalid_test_object__81ef3846-bf2d-11e0-92e1-8122f1474081</identifier>
        <formatId>eml://ecoinformatics.org/eml-2.0.0</formatId>
        <!-- <objectFormat>
            <formatId>eml://ecoinformatics.org/eml-2.0.0</formatId>
            <formatName>eml://ecoinformatics.org/eml-2.0.0</formatName>
            <scienceMetadata>false</scienceMetadata>
        </objectFormat> -->
        <checksum algorithm="MD5">37f32730fcfb5f32be3c213c0918750b2c867704</checksum>
        <dateSysMetadataModified>2011-08-05T06:38:19.582158</dateSysMetadataModified>
        <size>1889</size>
    </objectInfo>
    <objectInfo>
        <identifier>__invalid_test_object__81e412b8-bf2d-11e0-abbc-8122f1474081</identifier>
        <formatId>text/plain</formatId>
        <!-- <objectFormat>
            <formatId>text/plain</formatId>
            <formatName>text/plain</formatName>
            <scienceMetadata>false</scienceMetadata>
        </objectFormat> -->
        <checksum algorithm="MD5">2368785aa1a11e4ea4e6ef7cde9ff744f0e0194b</checksum>
        <dateSysMetadataModified>2011-08-05T06:38:19.599811</dateSysMetadataModified>
        <size>1363</size>
    </objectInfo>
    <objectInfo>
        <identifier>__invalid_test_object__81f9356c-bf2d-11e0-8cb7-8122f1474081</identifier>
        <formatId>FGDC-STD-001.1-1999</formatId>
        <!-- <objectFormat>
            <formatId>FGDC-STD-001.1-1999</formatId>
            <formatName>FGDC-STD-001.1-1999</formatName>
            <scienceMetadata>false</scienceMetadata>
        </objectFormat> -->
        <checksum algorithm="MD5">dcb5e13466d55b430e5bfc08917c3fb62764a6fc</checksum>
        <dateSysMetadataModified>2011-08-05T06:38:19.623681</dateSysMetadataModified>
        <size>550</size>
    </objectInfo>
    <objectInfo>
        <identifier>__invalid_test_object__81fb4226-bf2d-11e0-8b16-8122f1474081</identifier>
        <formatId>http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2</formatId>
        <!-- <objectFormat>
            <formatId>http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2</formatId>
            <formatName>http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2</formatName>
            <scienceMetadata>false</scienceMetadata>
        </objectFormat> -->
        <checksum algorithm="MD5">df6f8379c36acb5be04d01b2997672a7bbb5652b</checksum>
        <dateSysMetadataModified>2011-08-05T06:38:19.632426</dateSysMetadataModified>
        <size>794</size>
    </objectInfo>
</ns1:objectList>
"""

#EG_OBJECTLIST_KNB="""<?xml version="1.0" encoding="UTF-8"?>
#<d1:objectList xmlns:d1="http://ns.dataone.org/service/types/v1" count="5" start="0"
#    total="673">
#    <objectInfo>
#        <identifier>knb:testid:201020217324403 </identifier>
#        <objectFormat>eml://ecoinformatics.org/eml-2.1.0</objectFormat>
#        <checksum algorithm="MD5"
#            >4d6537f48d2967725bfcc7a9f0d5094ce4088e0975fcd3f1a361f15f46e49f83</checksum>
#        <dateSysMetadataModified>2010-07-22T06:58:32.097Z</dateSysMetadataModified>
#        <size>12</size>
#    </objectInfo>
#    <objectInfo>
#        <identifier>test.2010181122146255</identifier>
#        <objectFormat>eml://ecoinformatics.org/eml-2.1.0</objectFormat>
#        <checksum algorithm="MD5">9CF71CAAEBE5B24B122F2ACF9EB8C1C3</checksum>
#        <dateSysMetadataModified>2010-07-01T02:21:46.633Z</dateSysMetadataModified>
#        <size>86</size>
#    </objectInfo>
#    <objectInfo>
#        <identifier>test.2010181153417114</identifier>
#        <objectFormat>eml://ecoinformatics.org/eml-2.1.0</objectFormat>
#        <checksum algorithm="MD5">9CF71CAAEBE5B24B122F2ACF9EB8C1C3</checksum>
#        <dateSysMetadataModified>2010-07-01T05:34:17.179Z</dateSysMetadataModified>
#        <size>86</size>
#    </objectInfo>
#    <objectInfo>
#        <identifier>knb:testid:201019123134366</identifier>
#        <objectFormat>text/csv</objectFormat>
#        <checksum algorithm="MD5"
#            >4d6537f48d2967725bfcc7a9f0d5094ce4088e0975fcd3f1a361f15f46e49f83</checksum>
#        <dateSysMetadataModified>2010-07-11T13:09:55.924Z</dateSysMetadataModified>
#        <size>12</size>
#    </objectInfo>
#    <objectInfo>
#        <identifier>test.201018115165054</identifier>
#        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
#        <checksum algorithm="MD5">9CF71CAAEBE5B24B122F2ACF9EB8C1C3</checksum>
#        <dateSysMetadataModified>2010-07-01T05:16:50.127Z</dateSysMetadataModified>
#        <size>86</size>
#    </objectInfo>
#</d1:objectList>
#"""

EG_BAD_OBJECTLIST = """<?xml version="1.0" encoding="UTF-8"?>
<d1:objectList xmlns:d1="http://ns.dataone.org/service/types/v1" count="5" start="0"
    total="0">
    <objectInfo>
        <identifier>knb:testid:201020217324403 </identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.1.0</objectFormat>
        <checksum algorithm="MD5"
            >4d6537f48d2967725bfcc7a9f0d5094ce4088e0975fcd3f1a361f15f46e49f83</checksum>
        <dateSysMetadataModified>2010-07-22T06:58:32.097Z</dateSysMetadataModified>
        <size>12</size>
    </objectInfo>
    <objectInfo>
        <identifier>test.2010181122146255</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.1.0</objectFormat>
        <checksum algorithm="MD5">9CF71CAAEBE5B24B122F2ACF9EB8C1C3</checksum>
        <dateSysMetadataModified>2010-07-01T02:21:46.633Z</dateSysMetadataModified>
        <size>86</size>
    </objectInfo>
    <objectInfo>
        <identifier>test.2010181153417114</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.1.0</objectFormat>
        <checksum algorithm="MD5">9CF71CAAEBE5B24B122F2ACF9EB8C1C3</checksum>
        <dateSysMetadataModified>2010-07-01T05:34:17.179Z</dateSysMetadataModified>
        <size>86</size>
    </objectInfo>
    <objectInfo>
        <identifier>test.201018115165054</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="MD5">9CF71CAAEBE5B24B122F2ACF9EB8C1C3</checksum>
        <dateSysMetadataModified>2010-07-01T05:16:50.127Z</dateSysMetadataModified>
        <size>86</size>
    </objectInfo>
</d1:objectList>"""


class TestObjectList(unittest.TestCase):
  def deserialize_and_check(self, doc, shouldfail=False):
    try:
      dataoneTypes.CreateFromDocument(doc)
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if shouldfail:
        return
      else:
        raise

  def test_deserialize_xml_gmn(self):
    util.deserialize_and_check(EG_OBJECTLIST_GMN)

#  def test_deserialize_xml_knb(self):
#    util.deserialize_and_check(EG_OBJECTLIST_KNB)

  def test_deserialize_xml_bad(self):
    util.deserialize_and_check(EG_BAD_OBJECTLIST, shouldfail=True)

  def test_serialization_gmn(self):
    """Deserialize: XML -> ObjectList (GMN)"""
    util.deserialize_and_check(EG_OBJECTLIST_GMN)

  def test_serialization_knb(self):
    """Deserialize: XML -> ObjectList (KNB)"""
    #util.deserialize_and_check(EG_OBJECTLIST_KNB)

  def test_serialization_bad(self):
    """Deserialize: XML -> ObjectList (bad)"""
    util.deserialize_and_check(EG_BAD_OBJECTLIST, shouldfail=True)
