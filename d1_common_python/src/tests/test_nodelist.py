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
:Author: DataONE (vieglais, dahl)
:Dependencies:
  - python 2.6
'''

import logging
import sys
import unittest

from d1_common import xmlrunner
from d1_common.types import nodelist_serialization

EG_NODELIST_GMN = """<?xml version="1.0" encoding="UTF-8"?>
<d1:nodeList xmlns:d1="http://ns.dataone.org/service/types/v1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://ns.dataone.org/service/types/v1">
    <node replicate="false" synchronize="false" type="mn">
        <identifier>identifier0</identifier>
        <name>name0</name>
        <description>description0</description>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <services>
            <service version="version0" available="false">
                <name>name1</name>
                <restriction name="name2" rest="rest0">
                    <allowed>
                    </allowed>
                </restriction>
                <restriction name="name3" rest="rest1">
                    <allowed>
                    </allowed>
                </restriction>
            </service>
            <service version="version1" available="false">
                <name>name4</name>
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
        <health state="up">
            <ping success="false" lastSuccess="2006-05-04T18:13:51.0Z"/>
            <status success="false" dateChecked="2006-05-04T18:13:51.0Z"/>
        </health>
    </node>
    <node replicate="false" synchronize="false" type="mn">
        <identifier>identifier1</identifier>
        <name>name7</name>
        <description>description1</description>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <services>
            <service version="version2" available="false">
                <name>name8</name>
                <restriction name="name9" rest="rest4">
                    <allowed>
                    </allowed>
                </restriction>
                <restriction name="name10" rest="rest5">
                    <allowed>
                    </allowed>
                </restriction>
            </service>
            <service version="version3" available="false">
                <name>name11</name>
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
        <health state="up">
            <ping success="false" lastSuccess="2006-05-04T18:13:51.0Z"/>
            <status success="false" dateChecked="2006-05-04T18:13:51.0Z"/>
        </health>
    </node>
</d1:nodeList>
"""

# TODO.
EG_NODELIST_KNB = """"""

EG_BAD_NODELIST_1 = """<?xml version="1.0" ?>
<ns1:nodeList xmlns:ns1="http://ns.dataone.org/service/types/v1">

  <node replicate="true" synchronize="true" type="mn">
    <identifier>gmn_test</identifier>
    <name>2796</name>
    <description>'GMN'</description>
    <INVALIDbaseURL>http://localhost:8000</baseURL>

    <services>
      <service available="true" version="'0.5'">
        <name>"GMN test"</name>
        <method implemented="true" name="session" rest="session/"/>
        <method implemented="true" name="object_collection" rest="object"/>
        <method implemented="true" name="get_object" rest="object/"/>
        <method implemented="true" name="get_meta" rest="meta/"/>
        <method implemented="true" name="log_collection" rest="log"/>

        <method implemented="true" name="health_ping" rest="health/ping"/>
        <method implemented="true" name="health_status" rest="health/status"/>
        <method implemented="true" name="monitor_object" rest="monitor/object"/>
        <method implemented="true" name="monitor_event" rest="monitor/event"/>
        <method implemented="true" name="node" rest="node"/>
      </service>
    </services>
  </node>

  <node replicate="true" synchronize="true" type="mn">
    <identifier>gmn_test_2</identifier>
    <name>gmn_test_2</name>
    <description>'GMN test 2'</description>
    <baseURL>http://192.168.1.122/mn</baseURL>
    <services>
      <service available="true" version="'0.5'">

        <name>"GMN test"</name>
        <method implemented="true" name="session" rest="session/"/>
        <method implemented="true" name="object_collection" rest="object"/>
        <method implemented="true" name="get_object" rest="object/"/>
        <method implemented="true" name="get_meta" rest="meta/"/>
        <method implemented="true" name="log_collection" rest="log"/>
        <method implemented="true" name="health_ping" rest="health/ping"/>
        <method implemented="true" name="health_status" rest="health/status"/>

        <method implemented="true" name="monitor_object" rest="monitor/object"/>
        <method implemented="true" name="monitor_event" rest="monitor/event"/>
        <method implemented="true" name="node" rest="node"/>
      </service>
    </services>
  </node>
</ns1:nodeList>"""

# Missing nodeList/node/service/name.
EG_BAD_NODELIST_2 = """<?xml version="1.0" ?>
<ns1:nodeList xmlns:ns1="http://ns.dataone.org/service/types/v1">

  <node replicate="true" synchronize="true" type="mn">
    <identifier>gmn_test</identifier>
    <name>2796</name>
    <description>'GMN'</description>
    <baseURL>http://localhost:8000</baseURL>

    <services>
      <service available="true" version="'0.5'">
        <name>"GMN test"</name>
        <method implemented="true" name="session" rest="session/"/>
        <method implemented="true" name="object_collection" rest="object"/>
        <method implemented="true" name="get_object" rest="object/"/>
        <method implemented="true" name="get_meta" rest="meta/"/>
        <method implemented="true" name="log_collection" rest="log"/>

        <method implemented="true" name="health_ping" rest="health/ping"/>
        <method implemented="true" name="health_status" rest="health/status"/>
        <method implemented="true" name="monitor_object" rest="monitor/object"/>
        <method implemented="true" name="monitor_event" rest="monitor/event"/>
        <method implemented="true" name="node" rest="node"/>
      </service>
    </services>
  </node>

  <node replicate="true" synchronize="true" type="mn">
    <identifier>gmn_test_2</identifier>
    <name>gmn_test_2</name>
    <description>'GMN test 2'</description>
    <baseURL>http://192.168.1.122/mn</baseURL>
    <services>
      <service available="true" version="'0.5'">

        <method implemented="true" name="session" rest="session/"/>
        <method implemented="true" name="object_collection" rest="object"/>
        <method implemented="true" name="get_object" rest="object/"/>
        <method implemented="true" name="get_meta" rest="meta/"/>
        <method implemented="true" name="log_collection" rest="log"/>
        <method implemented="true" name="health_ping" rest="health/ping"/>
        <method implemented="true" name="health_status" rest="health/status"/>

        <method implemented="true" name="monitor_object" rest="monitor/object"/>
        <method implemented="true" name="monitor_event" rest="monitor/event"/>
        <method implemented="true" name="node" rest="node"/>
      </service>
    </services>
  </node>
</ns1:nodeList>"""


class TestNodeList(unittest.TestCase):
  def test_serialization(self):
    loader = nodelist_serialization.NodeList()

    def doctest(doc, shouldfail=False):
      try:
        checksum = loader.deserialize(doc, content_type="text/xml")
      except:
        if shouldfail:
          pass
        else:
          raise

    doctest(EG_NODELIST_GMN)
    #doctest(EG_NODELIST_KNB)
    doctest(EG_BAD_NODELIST_1, shouldfail=True)
    doctest(EG_BAD_NODELIST_2, shouldfail=True)

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
