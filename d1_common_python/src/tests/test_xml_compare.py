#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
Module d1_common.tests.test_xml_compare
=======================================

Unit tests for XML document comparison utility.

:Created: 2011-03-03
:Author: DataONE (vieglais, dahl)
:Dependencies:
  - python 2.6
'''

import logging
import sys
import unittest
import StringIO

from d1_common import xmlrunner
import d1_common.xml_compare

xml_correct = """<?xml version="1.0" ?>
<ns1:objectList count="5" start="0" total="100"
    xmlns:ns1="http://dataone.org/service/types/0.5.1">
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

xml_correct_swapped_attributes = """<?xml version="1.0" ?>
<ns1:objectList total="100" start="0" count="5"
    xmlns:ns1="http://dataone.org/service/types/0.5.1">
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

xml_missing_count = """<?xml version="1.0" ?>
<ns1:objectList start="0" total="100"
    xmlns:ns1="http://dataone.org/service/types/0.5.1">
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

xml_missing_entry = """<?xml version="1.0" ?>
<ns1:objectList count="5" start="0" total="100"
    xmlns:ns1="http://dataone.org/service/types/0.5.1">
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

xml_wrong_order = """<?xml version="1.0" ?>
<ns1:objectList count="5" start="0" total="100"
    xmlns:ns1="http://dataone.org/service/types/0.5.1">
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

xml_missing_text = """<?xml version="1.0" ?>
<ns1:objectList count="5" start="0" total="100"
    xmlns:ns1="http://dataone.org/service/types/0.5.1">
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

xml_syntax_error = """<?xml version="1.0" ?>
<ns1:objectList count="5" start="0" total="100"
    xmlns:ns1="http://dataone.org/service/types/0.5.1">
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


class TestXMLCompare(unittest.TestCase):
  def test_correct_compare_with_itself(self):
    '''Compare xml_correct with itself and verify that compare passes.'''
    d1_common.xml_compare.compare(
      StringIO.StringIO(xml_correct), StringIO.StringIO(
        xml_correct
      )
    )

  def test_correct_swapped_attributes(self):
    '''Compare xml_correct with itself and verify that compare passes.'''
    d1_common.xml_compare.compare(
      StringIO.StringIO(xml_correct), StringIO.StringIO(
        xml_correct_swapped_attributes
      )
    )

  def test_error_missing_count(self):
    '''Verify that comparision fails when an attribute is missing.'''
    self.assertRaises(
      d1_common.xml_compare.CompareError, d1_common.xml_compare.compare,
      StringIO.StringIO(xml_correct), StringIO.StringIO(xml_missing_count)
    )

  def test_error_missing_entry(self):
    '''Verify that comparision fails when an element is missing.'''
    self.assertRaises(
      d1_common.xml_compare.CompareError, d1_common.xml_compare.compare,
      StringIO.StringIO(xml_correct), StringIO.StringIO(xml_missing_entry)
    )

  def test_error_wrong_order(self):
    '''Verify that comparision fails when to elements appear in the wrong order.'''
    self.assertRaises(
      d1_common.xml_compare.CompareError, d1_common.xml_compare.compare,
      StringIO.StringIO(xml_correct), StringIO.StringIO(xml_wrong_order)
    )

  def test_error_missing_text(self):
    '''Verify that comparision fails when an element is missing text.'''
    self.assertRaises(
      d1_common.xml_compare.CompareError, d1_common.xml_compare.compare,
      StringIO.StringIO(xml_correct), StringIO.StringIO(xml_missing_text)
    )

  def test_error_xml_syntax_error(self):
    '''Verify that comparision fails when the document is not well formed.'''
    self.assertRaises(
      d1_common.xml_compare.CompareError, d1_common.xml_compare.compare,
      StringIO.StringIO(xml_correct), StringIO.StringIO(xml_syntax_error)
    )

#===============================================================================
if __name__ == "__main__":
  argv = sys.argv
  if "--debug" in argv:
    logging.basicConfig(level=logging.DEBUG)
    argv.remove("--debug")
  if "--with-xunit" in argv:
    argv.remove("--with-xunit")
    unittest.main(argv=argv, testRunner=xmlrunner.XmlTestRunner(sys.stdout))
  else:
    unittest.main(argv=argv)
