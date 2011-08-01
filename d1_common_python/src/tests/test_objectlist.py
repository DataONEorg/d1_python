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
Module d1_common.tests.test_objectlist
======================================

Unit tests for serializaton and de-serialization of the ObjectList type.

:Created: 2010-07-21
:Author: DataONE (vieglais, dahl)
:Dependencies:
  - python 2.6
'''

import logging
import sys
import unittest

import d1_common
from d1_common import xmlrunner
import d1_common.types.objectlist_serialization

EG_OBJECTLIST_GMN = """<?xml version="1.0" ?>
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
    <objectInfo>
        <identifier>anterior1.jpg</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="MD5">5b415607e35c1d367bad0ab3bce6ac25</checksum>
        <dateSysMetadataModified>1970-09-20T00:33:17</dateSysMetadataModified>
        <size>717851</size>
    </objectInfo>
    <objectInfo>
        <identifier>hdl:10255/dryad.109/mets.xml</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="SHA-1">efe0869971f40987d77188cd5694cd49d5204cea</checksum>
        <dateSysMetadataModified>1970-09-27T13:11:16</dateSysMetadataModified>
        <size>3132</size>
    </objectInfo>
</ns1:objectList>"""

EG_OBJECTLIST_KNB = """<?xml version="1.0" encoding="UTF-8"?>
<d1:objectList xmlns:d1="http://ns.dataone.org/service/types/v1" count="5" start="0"
    total="673">
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
        <identifier>knb:testid:201019123134366</identifier>
        <objectFormat>text/csv</objectFormat>
        <checksum algorithm="MD5"
            >4d6537f48d2967725bfcc7a9f0d5094ce4088e0975fcd3f1a361f15f46e49f83</checksum>
        <dateSysMetadataModified>2010-07-11T13:09:55.924Z</dateSysMetadataModified>
        <size>12</size>
    </objectInfo>
    <objectInfo>
        <identifier>test.201018115165054</identifier>
        <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
        <checksum algorithm="MD5">9CF71CAAEBE5B24B122F2ACF9EB8C1C3</checksum>
        <dateSysMetadataModified>2010-07-01T05:16:50.127Z</dateSysMetadataModified>
        <size>86</size>
    </objectInfo>
</d1:objectList>
"""

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
  def _test_deserialize(self, doc, shouldfail=False):
    serializer = d1_common.types.objectlist_serialization.ObjectList()
    olist = serializer.deserialize(doc, content_type=d1_common.const.MIMETYPE_XML)
    oinfo = olist.objectInfo
    if shouldfail:
      self.assertNotEqual(len(oinfo), olist.count)
    else:
      self.assertEqual(len(oinfo), olist.count)

  def test_deserialize_xml_gmn(self):
    self._test_deserialize(EG_OBJECTLIST_GMN)

  def test_deserialize_xml_knb(self):
    self._test_deserialize(EG_OBJECTLIST_KNB)

  def test_deserialize_xml_bad(self):
    self._test_deserialize(EG_BAD_OBJECTLIST, shouldfail=True)

#RDF Serialization is not implemented yet
#  def test_serialize_rdf(self):
#    serializer = d1_common.types.objectlist_serialization.ObjectList()
#    olist = serializer.deserialize(EG_OBJECTLIST_GMN, content_type=d1_common.const.MIMETYPE_XML)
#    #olist.deserialize(content_type=d1_common.const.MIMETYPE_XML)
#    #olist = serializer.deserialize(EG_OBJECTLIST_GMN, content_type="text/xml")
#    #serialize_rdf_xml
#    l2 = d1_common.types.objectlist_serialization.ObjectList()
#    l2.object_list = olist
#    l2.serialize(accept=d1_common.const.MIMETYPE_RDF)
#    #oinfo = olist.objectInfo
#    #if shouldfail:
#    #  self.assertNotEqual(len(oinfo), olist.count)
#    #else:
#    #  self.assertEqual(len(oinfo), olist.count)

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
