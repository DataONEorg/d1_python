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

import d1_common.xml

import d1_test.d1_test_case

XML_CORRECT = """<?xml version="1.0" ?>
<ns1:objectList count="5" start="0" total="100"
    xmlns:ns1="http://ns.dataone.org/service/types/v1">
    <objectInfo>
        <identifier>hdl:10255/dryad.1228/mets.xml</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">3f56de593b6ffc536253b799b429453e3673fc19</checksum>
        <dateSysMetadataModified>1970-01-19T04:53:32</dateSysMetadataModified>
        <size>3666</size>
    </objectInfo>
    <objectInfo>
        <identifier>hdl:10255/dryad.1073/mets.xml</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">aac6cca196fb6330d1013a10cce6a4604ca180d3</checksum>
        <dateSysMetadataModified>1970-02-06T18:11:22</dateSysMetadataModified>
        <size>3635</size>
    </objectInfo>
    <objectInfo>
        <identifier>AnserMatrix.htm</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="MD5">0e25cf59d7bd4d57154cc83e0aa32b34</checksum>
        <dateSysMetadataModified>1970-05-27T06:12:49</dateSysMetadataModified>
        <size>11048</size>
    </objectInfo>
</ns1:objectList>
"""

XML_CORRECT_SWAPPED_ATTRIBUTES = """<?xml version="1.0" ?>
<ns1:objectList total="100" start="0" count="5"
    xmlns:ns1="http://ns.dataone.org/service/types/v1">
    <objectInfo>
        <identifier>hdl:10255/dryad.1228/mets.xml</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">3f56de593b6ffc536253b799b429453e3673fc19</checksum>
        <dateSysMetadataModified>1970-01-19T04:53:32</dateSysMetadataModified>
        <size>3666</size>
    </objectInfo>
    <objectInfo>
        <identifier>hdl:10255/dryad.1073/mets.xml</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">aac6cca196fb6330d1013a10cce6a4604ca180d3</checksum>
        <dateSysMetadataModified>1970-02-06T18:11:22</dateSysMetadataModified>
        <size>3635</size>
    </objectInfo>
    <objectInfo>
        <identifier>AnserMatrix.htm</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="MD5">0e25cf59d7bd4d57154cc83e0aa32b34</checksum>
        <dateSysMetadataModified>1970-05-27T06:12:49</dateSysMetadataModified>
        <size>11048</size>
    </objectInfo>
</ns1:objectList>
"""

XML_MISSING_COUNT = """<?xml version="1.0" ?>
<ns1:objectList start="0" total="100"
    xmlns:ns1="http://ns.dataone.org/service/types/v1">
    <objectInfo>
        <identifier>hdl:10255/dryad.1228/mets.xml</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">3f56de593b6ffc536253b799b429453e3673fc19</checksum>
        <dateSysMetadataModified>1970-01-19T04:53:32</dateSysMetadataModified>
        <size>3666</size>
    </objectInfo>
    <objectInfo>
        <identifier>hdl:10255/dryad.1073/mets.xml</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">aac6cca196fb6330d1013a10cce6a4604ca180d3</checksum>
        <dateSysMetadataModified>1970-02-06T18:11:22</dateSysMetadataModified>
        <size>3635</size>
    </objectInfo>
    <objectInfo>
        <identifier>AnserMatrix.htm</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="MD5">0e25cf59d7bd4d57154cc83e0aa32b34</checksum>
        <dateSysMetadataModified>1970-05-27T06:12:49</dateSysMetadataModified>
        <size>11048</size>
    </objectInfo>
</ns1:objectList>
"""

XML_MISSING_ENTRY = """<?xml version="1.0" ?>
<ns1:objectList count="5" start="0" total="100"
    xmlns:ns1="http://ns.dataone.org/service/types/v1">
    <objectInfo>
        <identifier>hdl:10255/dryad.1228/mets.xml</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">3f56de593b6ffc536253b799b429453e3673fc19</checksum>
        <dateSysMetadataModified>1970-01-19T04:53:32</dateSysMetadataModified>
        <size>3666</size>
    </objectInfo>
    <objectInfo>
        <identifier>hdl:10255/dryad.1073/mets.xml</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">aac6cca196fb6330d1013a10cce6a4604ca180d3</checksum>
        <dateSysMetadataModified>1970-02-06T18:11:22</dateSysMetadataModified>
        <size>3635</size>
    </objectInfo>
</ns1:objectList>
"""

XML_WRONG_ORDER = """<?xml version="1.0" ?>
<ns1:objectList count="5" start="0" total="100"
    xmlns:ns1="http://ns.dataone.org/service/types/v1">
    <objectInfo>
        <identifier>hdl:10255/dryad.1228/mets.xml</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">3f56de593b6ffc536253b799b429453e3673fc19</checksum>
        <dateSysMetadataModified>1970-01-19T04:53:32</dateSysMetadataModified>
        <size>3666</size>
    </objectInfo>
    <objectInfo>
        <identifier>AnserMatrix.htm</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="MD5">0e25cf59d7bd4d57154cc83e0aa32b34</checksum>
        <dateSysMetadataModified>1970-05-27T06:12:49</dateSysMetadataModified>
        <size>11048</size>
    </objectInfo>
    <objectInfo>
        <identifier>hdl:10255/dryad.1073/mets.xml</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">aac6cca196fb6330d1013a10cce6a4604ca180d3</checksum>
        <dateSysMetadataModified>1970-02-06T18:11:22</dateSysMetadataModified>
        <size>3635</size>
    </objectInfo>
</ns1:objectList>
"""

XML_MISSING_TEXT = """<?xml version="1.0" ?>
<ns1:objectList count="5" start="0" total="100"
    xmlns:ns1="http://ns.dataone.org/service/types/v1">
    <objectInfo>
        <identifier></identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">3f56de593b6ffc536253b799b429453e3673fc19</checksum>
        <dateSysMetadataModified>1970-01-19T04:53:32</dateSysMetadataModified>
        <size>3666</size>
    </objectInfo>
    <objectInfo>
        <identifier>AnserMatrix.htm</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="MD5">0e25cf59d7bd4d57154cc83e0aa32b34</checksum>
        <dateSysMetadataModified>1970-05-27T06:12:49</dateSysMetadataModified>
        <size>11048</size>
    </objectInfo>
    <objectInfo>
        <identifier>hdl:10255/dryad.1073/mets.xml</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">aac6cca196fb6330d1013a10cce6a4604ca180d3</checksum>
        <dateSysMetadataModified>1970-02-06T18:11:22</dateSysMetadataModified>
        <size>3635</size>
    </objectInfo>
</ns1:objectList>
"""

XML_SYNTAX_ERROR = """<?xml version="1.0" ?>
<ns1:objectList count="5" start="0" total="100"
    xmlns:ns1="http://ns.dataone.org/service/types/v1">
    <objectInfo>
        <identifier></identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">3f56de593b6ffc536253b799b429453e3673fc19</checksum>
        <dateSysMetadataModified>1970-01-19T04:53:32</dateSysMetadataModified>
        <size>3666</size>
    </objectInfo>
    <objectInfo>
        <identifier>AnserMatrix.htm</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="MD5">0e25cf59d7bd4d57154cc83e0aa32b34</checksum>
        <dateSysMetadataModified>1970-05-27T06:12:49</dateSysMetadataModified>
        <size>11048</size>
    </objectInfo>
    <objectInfo>
        <identifier>hdl:10255/dryad.1073/mets.xml</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">aac6cca196fb6330d1013a10cce6a4604ca180d3</checksum>
        <dateSysMetadataModified>1970-02-06T18:11:22</dateSysMetadataModified>
        <size>3635</size>
    </objectInfo>
</ns1:objectList>
"""

# TODO: Add tests for remaining functions in xml.py.


class TestXml(d1_test.d1_test_case.D1TestCase):
  def test_0010(self):
    """Compare xml_correct with itself and verify that compare passes"""
    assert d1_common.xml.is_equivalent(XML_CORRECT, XML_CORRECT)

  def test_0020(self):
    """Compare xml_correct with itself and verify that compare passes"""
    assert d1_common.xml.is_equivalent(
      XML_CORRECT, XML_CORRECT_SWAPPED_ATTRIBUTES
    )

  def test_0030(self):
    """Verify that comparison fails when an attribute is missing"""
    assert not d1_common.xml.is_equivalent(XML_CORRECT, XML_MISSING_COUNT)

  def test_0040(self):
    """Verify that comparison fails when an element is missing"""
    assert not d1_common.xml.is_equivalent(XML_CORRECT, XML_MISSING_ENTRY)

  def test_0050(self):
    """Verify that comparison fails when to elements appear in the wrong order"""
    assert not d1_common.xml.is_equivalent(XML_CORRECT, XML_WRONG_ORDER)

  def test_0060(self):
    """Verify that comparison fails when an element is missing text"""
    assert not d1_common.xml.is_equivalent(XML_CORRECT, XML_MISSING_TEXT)

  def test_0070(self):
    """Verify that comparison fails when the document is not well formed"""
    assert not d1_common.xml.is_equivalent(XML_CORRECT, XML_SYNTAX_ERROR)
