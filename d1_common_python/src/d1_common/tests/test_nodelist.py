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
"""Test serialization and de-serialization of the NodeList
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

# flake8: noqa: E501

EG_NODELIST_GMN = """<?xml version="1.0" encoding="UTF-8"?>
<d1:nodeList xmlns:d1="http://ns.dataone.org/service/types/v1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://ns.dataone.org/service/types/v1 file:/home/dahl/eclipse_workspace_d1/d1_common_python/src/d1_schemas/dataoneTypes.xsd">
    <node replicate="false" synchronize="false" type="mn" state="up">
        <identifier>identifier0</identifier>
        <name>name0</name>
        <description>description0</description>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <services>
            <service name="name1" version="version0" available="false">
                <restriction methodName="methodName0">
                    <subject>subject0</subject>
                    <subject>subject1</subject>
                </restriction>
                <restriction methodName="methodName1">
                    <subject>subject2</subject>
                    <subject>subject3</subject>
                </restriction>
            </service>
            <service name="name2" version="version1" available="false">
                <restriction methodName="methodName2">
                    <subject>subject4</subject>
                    <subject>subject5</subject>
                </restriction>
                <restriction methodName="methodName3">
                    <subject>subject6</subject>
                    <subject>subject7</subject>
                </restriction>
            </service>
        </services>
        <synchronization>
            <schedule hour="*" mday="*" min="*" mon="*" sec="1" wday="*" year="*"/>
            <lastHarvested>2006-05-04T18:13:51.0Z</lastHarvested>
            <lastCompleteHarvest>2006-05-04T18:13:51.0Z</lastCompleteHarvest>
        </synchronization>
        <ping success="false" lastSuccess="2006-05-04T18:13:51.0Z"/>
        <subject>subject8</subject>
        <subject>subject9</subject>
        <contactSubject>contactSubject0</contactSubject>
        <contactSubject>contactSubject1</contactSubject>
    </node>
    <node replicate="false" synchronize="false" type="mn" state="up">
        <identifier>identifier1</identifier>
        <name>name3</name>
        <description>description1</description>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <services>
            <service name="name4" version="version2" available="false">
                <restriction methodName="methodName4">
                    <subject>subject10</subject>
                    <subject>subject11</subject>
                </restriction>
                <restriction methodName="methodName5">
                    <subject>subject12</subject>
                    <subject>subject13</subject>
                </restriction>
            </service>
            <service name="name5" version="version3" available="false">
                <restriction methodName="methodName6">
                    <subject>subject14</subject>
                    <subject>subject15</subject>
                </restriction>
                <restriction methodName="methodName7">
                    <subject>subject16</subject>
                    <subject>subject17</subject>
                </restriction>
            </service>
        </services>
        <synchronization>
            <schedule hour="*" mday="*" min="*" mon="*" sec="1" wday="*" year="*"/>
            <lastHarvested>2006-05-04T18:13:51.0Z</lastHarvested>
            <lastCompleteHarvest>2006-05-04T18:13:51.0Z</lastCompleteHarvest>
        </synchronization>
        <ping success="false" lastSuccess="2006-05-04T18:13:51.0Z"/>
        <subject>subject18</subject>
        <subject>subject19</subject>
        <contactSubject>contactSubject2</contactSubject>
        <contactSubject>contactSubject3</contactSubject>
    </node>
</d1:nodeList>
"""

# TODO.
EG_NODELIST_KNB = """"""

# Missing version.
EG_BAD_NODELIST_1 = """<?xml version="1.0" encoding="UTF-8"?>
<d1:nodeList xmlns:d1="http://ns.dataone.org/service/types/v1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://ns.dataone.org/service/types/v1 file:/home/dahl/eclipse_workspace_d1/d1_common_python/src/d1_schemas/dataoneTypes.xsd">
    <node replicate="false" synchronize="false" type="mn" state="up">
        <identifier>identifier0</identifier>
        <name>name0</name>
        <description>description0</description>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <services>
            <service name="name1" available="false">
                <restriction methodName="methodName0">
                    <subject>subject0</subject>
                    <subject>subject1</subject>
                </restriction>
                <restriction methodName="methodName1">
                    <subject>subject2</subject>
                    <subject>subject3</subject>
                </restriction>
            </service>
            <service name="name2" version="version1" available="false">
                <restriction methodName="methodName2">
                    <subject>subject4</subject>
                    <subject>subject5</subject>
                </restriction>
                <restriction methodName="methodName3">
                    <subject>subject6</subject>
                    <subject>subject7</subject>
                </restriction>
            </service>
        </services>
        <synchronization>
            <schedule hour="*" mday="*" min="*" mon="*" sec="1" wday="*" year="*"/>
            <lastHarvested>2006-05-04T18:13:51.0Z</lastHarvested>
            <lastCompleteHarvest>2006-05-04T18:13:51.0Z</lastCompleteHarvest>
        </synchronization>
        <ping success="false" lastSuccess="2006-05-04T18:13:51.0Z"/>
        <subject>subject8</subject>
        <subject>subject9</subject>
        <contactSubject>contactSubject0</contactSubject>
        <contactSubject>contactSubject1</contactSubject>
    </node>
    <node replicate="false" synchronize="false" type="mn" state="up">
        <identifier>identifier1</identifier>
        <name>name3</name>
        <description>description1</description>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <services>
            <service name="name4" version="version2" available="false">
                <restriction methodName="methodName4">
                    <subject>subject10</subject>
                    <subject>subject11</subject>
                </restriction>
                <restriction methodName="methodName5">
                    <subject>subject12</subject>
                    <subject>subject13</subject>
                </restriction>
            </service>
            <service name="name5" version="version3" available="false">
                <restriction methodName="methodName6">
                    <subject>subject14</subject>
                    <subject>subject15</subject>
                </restriction>
                <restriction methodName="methodName7">
                    <subject>subject16</subject>
                    <subject>subject17</subject>
                </restriction>
            </service>
        </services>
        <synchronization>
            <schedule hour="*" mday="*" min="*" mon="*" sec="1" wday="*" year="*"/>
            <lastHarvested>2006-05-04T18:13:51.0Z</lastHarvested>
            <lastCompleteHarvest>2006-05-04T18:13:51.0Z</lastCompleteHarvest>
        </synchronization>
        <ping success="false" lastSuccess="2006-05-04T18:13:51.0Z"/>
        <subject>subject18</subject>
        <subject>subject19</subject>
        <contactSubject>contactSubject2</contactSubject>
        <contactSubject>contactSubject3</contactSubject>
    </node>
</d1:nodeList>
"""

# Missing nodeList/node/service/name.
EG_BAD_NODELIST_2 = """<?xml version="1.0" encoding="UTF-8"?>
<d1:nodeList xmlns:d1="http://ns.dataone.org/service/types/v1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://ns.dataone.org/service/types/v1 file:/home/dahl/eclipse_workspace_d1/d1_common_python/src/d1_schemas/dataoneTypes.xsd">
    <node replicate="false" synchronize="false" type="mn" state="up">
        <identifier>identifier0</identifier>
        <name>name0</name>
        <description>description0</description>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <services>
            <service version="version0" available="false">
                <restriction methodName="methodName0">
                    <subject>subject0</subject>
                    <subject>subject1</subject>
                </restriction>
                <restriction methodName="methodName1">
                    <subject>subject2</subject>
                    <subject>subject3</subject>
                </restriction>
            </service>
            <service name="name2" version="version1" available="false">
                <restriction methodName="methodName2">
                    <subject>subject4</subject>
                    <subject>subject5</subject>
                </restriction>
                <restriction methodName="methodName3">
                    <subject>subject6</subject>
                    <subject>subject7</subject>
                </restriction>
            </service>
        </services>
        <synchronization>
            <schedule hour="*" mday="*" min="*" mon="*" sec="1" wday="*" year="*"/>
            <lastHarvested>2006-05-04T18:13:51.0Z</lastHarvested>
            <lastCompleteHarvest>2006-05-04T18:13:51.0Z</lastCompleteHarvest>
        </synchronization>
        <ping success="false" lastSuccess="2006-05-04T18:13:51.0Z"/>
        <subject>subject8</subject>
        <subject>subject9</subject>
        <contactSubject>contactSubject0</contactSubject>
        <contactSubject>contactSubject1</contactSubject>
    </node>
    <node replicate="false" synchronize="false" type="mn" state="up">
        <identifier>identifier1</identifier>
        <name>name3</name>
        <description>description1</description>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <services>
            <service name="name4" version="version2" available="false">
                <restriction methodName="methodName4">
                    <subject>subject10</subject>
                    <subject>subject11</subject>
                </restriction>
                <restriction methodName="methodName5">
                    <subject>subject12</subject>
                    <subject>subject13</subject>
                </restriction>
            </service>
            <service name="name5" version="version3" available="false">
                <restriction methodName="methodName6">
                    <subject>subject14</subject>
                    <subject>subject15</subject>
                </restriction>
                <restriction methodName="methodName7">
                    <subject>subject16</subject>
                    <subject>subject17</subject>
                </restriction>
            </service>
        </services>
        <synchronization>
            <schedule hour="*" mday="*" min="*" mon="*" sec="1" wday="*" year="*"/>
            <lastHarvested>2006-05-04T18:13:51.0Z</lastHarvested>
            <lastCompleteHarvest>2006-05-04T18:13:51.0Z</lastCompleteHarvest>
        </synchronization>
        <ping success="false" lastSuccess="2006-05-04T18:13:51.0Z"/>
        <subject>subject18</subject>
        <subject>subject19</subject>
        <contactSubject>contactSubject2</contactSubject>
        <contactSubject>contactSubject3</contactSubject>
    </node>
</d1:nodeList>
"""


class TestNodeList(unittest.TestCase):
  def deserialize_and_check(self, doc, shouldfail=False):
    try:
      dataoneTypes.CreateFromDocument(doc)
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if shouldfail:
        return
      else:
        raise
    if shouldfail:
      raise Exception('Did not receive expected exception')

  def test_serialization_gmn(self):
    """Deserialize: XML -> NodeList (GMN)"""
    util.deserialize_and_check(EG_NODELIST_GMN)

  def test_serialization_knb(self):
    """Deserialize: XML -> NodeList (KNB)"""
    #util.deserialize_and_check(EG_NODELIST_KNB)

  def test_serialization_bad_1(self):
    """Deserialize: XML -> NodeList (bad 1)"""
    util.deserialize_and_check(EG_BAD_NODELIST_1, shouldfail=True)

  def test_serialization_bad_2(self):
    """Deserialize: XML -> NodeList (bad 2)"""
    util.deserialize_and_check(EG_BAD_NODELIST_2, shouldfail=True)
