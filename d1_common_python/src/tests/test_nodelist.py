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
Module d1_common.tests.test_nodelist
====================================

Unit tests for serializaton and de-serialization of the NodeList type.

:Created: 2011-03-03
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import sys
import unittest
import xml.sax

# 3rd party.
import pyxb

# D1.
from d1_common import xmlrunner
import d1_common.types.generated.dataoneTypes as dataoneTypes

EG_NODELIST_GMN = """<?xml version="1.0" encoding="UTF-8"?>
<d1:nodeList xmlns:d1="http://ns.dataone.org/service/types/v1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://ns.dataone.org/service/types/v1 file:/home/roger/eclipse_workspace_d1/d1_common_python/src/d1_schemas/dataoneTypes.xsd">
    <node replicate="false" synchronize="false" type="mn" state="up">
        <identifier>identifier0</identifier>
        <name>name0</name>
        <description>description0</description>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <services>
            <service name="name1" version="version0" available="false">
                <restriction name="name2" rest="rest0">
                    <allowed>
                    </allowed>
                </restriction>
                <restriction name="name3" rest="rest1">
                    <allowed>
                    </allowed>
                </restriction>
            </service>
            <service name="name4" version="version1" available="false">
                <restriction name="name5" rest="rest2">
                    <allowed>
                    </allowed>
                </restriction>
                <restriction name="name6" rest="rest3">
                    <allowed>
                    </allowed>
                </restriction>
            </service>
        </services>
        <synchronization>
            <schedule hour="*" mday="*" min="*" mon="*" sec="*" wday="*" year="*"/>
            <lastHarvested>2006-05-04T18:13:51.0Z</lastHarvested>
            <lastCompleteHarvest>2006-05-04T18:13:51.0Z</lastCompleteHarvest>
        </synchronization>
        <ping success="false" lastSuccess="2006-05-04T18:13:51.0Z"/>
        <subject>subject0</subject>
        <subject>subject1</subject>
    </node>
    <node replicate="false" synchronize="false" type="mn" state="up">
        <identifier>identifier1</identifier>
        <name>name7</name>
        <description>description1</description>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <services>
            <service name="name8" version="version2" available="false">
                <restriction name="name9" rest="rest4">
                    <allowed>
                    </allowed>
                </restriction>
                <restriction name="name10" rest="rest5">
                    <allowed>
                    </allowed>
                </restriction>
            </service>
            <service name="name11" version="version3" available="false">
                <restriction name="name12" rest="rest6">
                    <allowed>
                    </allowed>
                </restriction>
                <restriction name="name13" rest="rest7">
                    <allowed>
                    </allowed>
                </restriction>
            </service>
        </services>
        <synchronization>
            <schedule hour="*" mday="*" min="*" mon="*" sec="*" wday="*" year="*"/>
            <lastHarvested>2006-05-04T18:13:51.0Z</lastHarvested>
            <lastCompleteHarvest>2006-05-04T18:13:51.0Z</lastCompleteHarvest>
        </synchronization>
        <ping success="false" lastSuccess="2006-05-04T18:13:51.0Z"/>
        <subject>subject2</subject>
        <subject>subject3</subject>
    </node>
</d1:nodeList>"""

# TODO.
EG_NODELIST_KNB = """"""

# Wrong version.
EG_BAD_NODELIST_1 = """<?xml version="1.0" encoding="UTF-8"?>
<d1:nodeList xmlns:d1="http://ns.dataone.org/service/types/v2"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://ns.dataone.org/service/types/v1 file:/home/roger/eclipse_workspace_d1/d1_common_python/src/d1_schemas/dataoneTypes.xsd">
    <node replicate="false" synchronize="false" type="mn" state="up">
        <identifier>identifier0</identifier>
        <name>name0</name>
        <description>description0</description>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <services>
            <service name="name1" version="version0" available="false">
                <restriction name="name2" rest="rest0">
                    <allowed>
                    </allowed>
                </restriction>
                <restriction name="name3" rest="rest1">
                    <allowed>
                    </allowed>
                </restriction>
            </service>
            <service name="name4" version="version1" available="false">
                <restriction name="name5" rest="rest2">
                    <allowed>
                    </allowed>
                </restriction>
                <restriction name="name6" rest="rest3">
                    <allowed>
                    </allowed>
                </restriction>
            </service>
        </services>
        <synchronization>
            <schedule hour="*" mday="*" min="*" mon="*" sec="*" wday="*" year="*"/>
            <lastHarvested>2006-05-04T18:13:51.0Z</lastHarvested>
            <lastCompleteHarvest>2006-05-04T18:13:51.0Z</lastCompleteHarvest>
        </synchronization>
        <ping success="false" lastSuccess="2006-05-04T18:13:51.0Z"/>
        <subject>subject0</subject>
        <subject>subject1</subject>
    </node>
    <node replicate="false" synchronize="false" type="mn" state="up">
        <identifier>identifier1</identifier>
        <name>name7</name>
        <description>description1</description>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <services>
            <service name="name8" version="version2" available="false">
                <restriction name="name9" rest="rest4">
                    <allowed>
                    </allowed>
                </restriction>
                <restriction name="name10" rest="rest5">
                    <allowed>
                    </allowed>
                </restriction>
            </service>
            <service name="name11" version="version3" available="false">
                <restriction name="name12" rest="rest6">
                    <allowed>
                    </allowed>
                </restriction>
                <restriction name="name13" rest="rest7">
                    <allowed>
                    </allowed>
                </restriction>
            </service>
        </services>
        <synchronization>
            <schedule hour="*" mday="*" min="*" mon="*" sec="*" wday="*" year="*"/>
            <lastHarvested>2006-05-04T18:13:51.0Z</lastHarvested>
            <lastCompleteHarvest>2006-05-04T18:13:51.0Z</lastCompleteHarvest>
        </synchronization>
        <ping success="false" lastSuccess="2006-05-04T18:13:51.0Z"/>
        <subject>subject2</subject>
        <subject>subject3</subject>
    </node>
</d1:nodeList>"""

# Missing nodeList/node/service/name.
EG_BAD_NODELIST_2 = """<?xml version="1.0" encoding="UTF-8"?>
<d1:nodeList xmlns:d1="http://ns.dataone.org/service/types/v1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://ns.dataone.org/service/types/v1 file:/home/roger/eclipse_workspace_d1/d1_common_python/src/d1_schemas/dataoneTypes.xsd">
    <node replicate="false" synchronize="false" type="mn" state="up">
        <identifier>identifier0</identifier>
        <name>name0</name>
        <description>description0</description>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <services>
            <service version="version0" available="false">
                <restriction name="name2" rest="rest0">
                    <allowed>
                    </allowed>
                </restriction>
                <restriction name="name3" rest="rest1">
                    <allowed>
                    </allowed>
                </restriction>
            </service>
            <service name="name4" version="version1" available="false">
                <restriction name="name5" rest="rest2">
                    <allowed>
                    </allowed>
                </restriction>
                <restriction name="name6" rest="rest3">
                    <allowed>
                    </allowed>
                </restriction>
            </service>
        </services>
        <synchronization>
            <schedule hour="*" mday="*" min="*" mon="*" sec="*" wday="*" year="*"/>
            <lastHarvested>2006-05-04T18:13:51.0Z</lastHarvested>
            <lastCompleteHarvest>2006-05-04T18:13:51.0Z</lastCompleteHarvest>
        </synchronization>
        <ping success="false" lastSuccess="2006-05-04T18:13:51.0Z"/>
        <subject>subject0</subject>
        <subject>subject1</subject>
    </node>"""


class TestNodeList(unittest.TestCase):
  def deserialize_and_check(self, doc, shouldfail=False):
    try:
      obj = dataoneTypes.CreateFromDocument(doc)
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if shouldfail:
        return
      else:
        raise

  def test_serialization_gmn(self):
    '''Deserialize: XML -> NodeList (GMN)'''
    self.deserialize_and_check(EG_NODELIST_GMN)

  def test_serialization_knb(self):
    '''Deserialize: XML -> NodeList (KNB)'''
    #self.deserialize_and_check(EG_NODELIST_KNB)

  def test_serialization_bad_1(self):
    '''Deserialize: XML -> NodeList (bad 1)'''
    self.deserialize_and_check(EG_BAD_NODELIST_1, shouldfail=True)

  def test_serialization_bad_2(self):
    '''Deserialize: XML -> NodeList (bad 2)'''
    self.deserialize_and_check(EG_BAD_NODELIST_2, shouldfail=True)

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
