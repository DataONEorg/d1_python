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
"""Test serialization and de-serialization of the LogRecords type.
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

EG_LOG_GMN = """<?xml version="1.0" ?>
<ns1:log count="5" start="0" total="453" xmlns:ns1="http://ns.dataone.org/service/types/v1">
<logEntry><entryId>453</entryId><identifier>hdl:10255/dryad.1228/mets.xml</identifier><ipAddress>127.0.0.1</ipAddress><userAgent>Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.04 (lucid) Firefox/3.6.13</userAgent><subject>127.0.0.1</subject><event>read</event><dateLogged>2011-02-20T19:01:19.171071</dateLogged><nodeIdentifier>urn:node:dryad_mn</nodeIdentifier></logEntry>
<logEntry><entryId>368</entryId><identifier>hdl:10255/dryad.1227/mets.xml</identifier><ipAddress>17.18.19.20</ipAddress><userAgent>Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0</userAgent><subject>17.18.19.20</subject><event>replicate</event><dateLogged>1999-12-19T16:03:22</dateLogged><nodeIdentifier>urn:node:dryad_mn</nodeIdentifier></logEntry>
<logEntry><entryId>408</entryId><identifier>hdl:10255/dryad.174/mets.xml</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0</userAgent><subject>21.22.23.24</subject><event>update</event><dateLogged>1999-11-17T04:15:23</dateLogged><nodeIdentifier>urn:node:dryad_mn</nodeIdentifier></logEntry>
<logEntry><entryId>9</entryId><identifier>12Cpaup.txt</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>Mozi,lla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)</userAgent><subject>21.22.23.24</subject><event>read</event><dateLogged>1999-10-05T01:34:37</dateLogged><nodeIdentifier>urn:node:dryad_mn</nodeIdentifier></logEntry>
<logEntry><entryId>29</entryId><identifier>15Jmatrix4.txt</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>msnbot-Products/1.0 (+http://search.msn.com/msnbot.htm)</userAgent><subject>21.22.23.24</subject><event>replicate</event><dateLogged>1999-09-17T01:59:18</dateLogged><nodeIdentifier>urn:node:dryad_mn</nodeIdentifier></logEntry>
</ns1:log>"""

# TODO.
EG_LOG_KNB = """<?xml version="1.0" ?>
<ns1:log count="5" start="0" total="453" xmlns:ns1="http://ns.dataone.org/service/types/v1">
<logEntry><entryId>453</entryId><identifier>hdl:10255/dryad.1228/mets.xml</identifier><ipAddress>127.0.0.1</ipAddress><userAgent>Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.04 (lucid) Firefox/3.6.13</userAgent><subject>127.0.0.1</subject><event>read</event><dateLogged>2011-02-20T19:01:19.171071</dateLogged><nodeIdentifier>urn:node:dryad_mn</nodeIdentifier></logEntry>
<logEntry><entryId>368</entryId><identifier>hdl:10255/dryad.1227/mets.xml</identifier><ipAddress>17.18.19.20</ipAddress><userAgent>Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0</userAgent><subject>17.18.19.20</subject><event>replicate</event><dateLogged>1999-12-19T16:03:22</dateLogged><nodeIdentifier>urn:node:dryad_mn</nodeIdentifier></logEntry>
<logEntry><entryId>408</entryId><identifier>hdl:10255/dryad.174/mets.xml</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0</userAgent><subject>21.22.23.24</subject><event>update</event><dateLogged>1999-11-17T04:15:23</dateLogged><nodeIdentifier>urn:node:dryad_mn</nodeIdentifier></logEntry>
<logEntry><entryId>9</entryId><identifier>12Cpaup.txt</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>Mozi,lla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)</userAgent><subject>21.22.23.24</subject><event>read</event><dateLogged>1999-10-05T01:34:37</dateLogged><nodeIdentifier>urn:node:dryad_mn</nodeIdentifier></logEntry>
<logEntry><entryId>29</entryId><identifier>15Jmatrix4.txt</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>msnbot-Products/1.0 (+http://search.msn.com/msnbot.htm)</userAgent><subject>21.22.23.24</subject><event>replicate</event><dateLogged>1999-09-17T01:59:18</dateLogged><nodeIdentifier>urn:node:dryad_mn</nodeIdentifier></logEntry>
</ns1:log>"""

EG_BAD_LOG_1 = """<?xml version="1.0" ?>
<ns1:log count="5" start="0" total="453" xmlns:ns1="http://ns.dataone.org/service/types/v1">
<logEntry><entryId>453</entryId><identifier>hdl:10255/dryad.1228/mets.xml</identifier><ipAddress>127.0.0.1</ipAddress><userAgent>Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.04 (lucid) Firefox/3.6.13</userAgent><subject>127.0.0.1</subject><event>read</event><dateLogged>2011-02-20T19:01:19.171071</dateLogged><nodeIdentifier>dryad_mn</nodeIdentifier></logEntry>
<logEntry><entryId>368</entryId><identifier>hdl:10255/dryad.1227/mets.xml</identifier><ipAddress>17.18.19.20</ipAddress><userAgent>Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0</userAgent><subject>17.18.19.20</subject><event>replicate</event><dateLogged>1999-12-19T16:03:22</dateLogged><nodeIdentifier>dryad_mn</nodeIdentifier></logEntry>
<logINVALIDEntry><entryId>408</entryId><identifier>hdl:10255/dryad.174/mets.xml</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0</userAgent><subject>21.22.23.24</subject><event>update</event><dateLogged>1999-11-17T04:15:23</dateLogged><nodeIdentifier>dryad_mn</nodeIdentifier></logEntry>
<logEntry><entryId>9</entryId><identifier>12Cpaup.txt</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>Mozi,lla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)</userAgent><subject>21.22.23.24</subject><event>read</event><dateLogged>1999-10-05T01:34:37</dateLogged><nodeIdentifier>dryad_mn</nodeIdentifier></logEntry>
<logEntry><entryId>29</entryId><identifier>15Jmatrix4.txt</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>msnbot-Products/1.0 (+http://search.msn.com/msnbot.htm)</userAgent><subject>21.22.23.24</subject><event>replicate</event><dateLogged>1999-09-17T01:59:18</dateLogged><nodeIdentifier>dryad_mn</nodeIdentifier></logEntry>
</ns1:log>"""

EG_BAD_LOG_2 = """<?xml version="1.0" ?>
<ns1:log count="5" start="0" total="453" xmlns:ns1="http://ns.dataone.org/service/types/v1">
<logEntry><entryId>453</entryId><identifier>hdl:10255/dryad.1228/mets.xml</identifier><ipAddress>127.0.0.1</ipAddress><userAgent>Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.04 (lucid) Firefox/3.6.13</userAgent><subject>127.0.0.1</subject><event>read</event><dateLogged>2011-02-20T19:01:19.171071</dateLogged><memberNode>dryad_mn</memberNode></logEntry>
<logEntry><entryId>368</entryId><identifier>hdl:10255/dryad.1227/mets.xml</identifier><ipAddress>17.18.19.20</ipAddress><userAgent>Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0</userAgent><subject>17.18.19.20</subject><event>replicate</event><dateLogged>1999-12-19T16:03:22</dateLogged><memberNode>dryad_mn</memberNode></logEntry>
<logEntry><identifier>hdl:10255/dryad.174/mets.xml</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0</userAgent><subject>21.22.23.24</subject><event>update</event><dateLogged>1999-11-17T04:15:23</dateLogged><memberNode>dryad_mn</memberNode></logEntry>
<logEntry><entryId>9</entryId><identifier>12Cpaup.txt</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>Mozi,lla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)</userAgent><subject>21.22.23.24</subject><event>read</event><dateLogged>1999-10-05T01:34:37</dateLogged><memberNode>dryad_mn</memberNode></logEntry>
<logEntry><entryId>29</entryId><identifier>15Jmatrix4.txt</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>msnbot-Products/1.0 (+http://search.msn.com/msnbot.htm)</userAgent><subject>21.22.23.24</subject><event>replicate</event><dateLogged>1999-09-17T01:59:18</dateLogged><memberNode>dryad_mn</memberNode></logEntry>
</ns1:log>"""

EG_BAD_LOG_3 = """<?xml version="1.0" ?>
<ns1:log count="5" start="0" total="453" xmlns:ns1="http://ns.dataone.org/service/types/v1">
<logEntry><entryId>453</entryId><identifier>hdl:10255/dryad.1228/mets.xml</identifier><ipAddress>127.0.0.1</ipAddress><userAgent>Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.04 (lucid) Firefox/3.6.13</userAgent><subject>127.0.0.1</subject><event>INVALID</event><dateLogged>2011-02-20T19:01:19.171071</dateLogged><memberNode>dryad_mn</memberNode></logEntry>
<logEntry><entryId>368</entryId><identifier>hdl:10255/dryad.1227/mets.xml</identifier><ipAddress>17.18.19.20</ipAddress><userAgent>Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0</userAgent><subject>17.18.19.20</subject><event>replicate</event><dateLogged>1999-12-19T16:03:22</dateLogged><memberNode>dryad_mn</memberNode></logEntry>
<logEntry><entryId>408</entryId><identifier>hdl:10255/dryad.174/mets.xml</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0</userAgent><subject>21.22.23.24</subject><event>update</event><dateLogged>1999-11-17T04:15:23</dateLogged><memberNode>dryad_mn</memberNode></logEntry>
<logEntry><entryId>9</entryId><identifier>12Cpaup.txt</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>Mozi,lla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)</userAgent><subject>21.22.23.24</subject><event>read</event><dateLogged>1999-10-05T01:34:37</dateLogged><memberNode>dryad_mn</memberNode></logEntry>
<logEntry><entryId>29</entryId><identifier>15Jmatrix4.txt</identifier><ipAddress>21.22.23.24</ipAddress><userAgent>msnbot-Products/1.0 (+http://search.msn.com/msnbot.htm)</userAgent><subject>21.22.23.24</subject><event>replicate</event><dateLogged>1999-09-17T01:59:18</dateLogged><memberNode>dryad_mn</memberNode></logEntry>
</ns1:log>"""


class TestObjectList(unittest.TestCase):
  def deserialize_and_check(self, doc, shouldfail=False):
    try:
      dataoneTypes.CreateFromDocument(doc)
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if shouldfail:
        return
      else:
        raise

  def test_serialization_gmn(self):
    """Deserialize: XML -> Log (GMN)"""
    try:
      util.deserialize_and_check(EG_LOG_GMN)
    except Exception as e:
      print e

  def test_serialization_knb(self):
    """Deserialize: XML -> Log (KNB)"""
    self.deserialize_and_check(EG_LOG_KNB)

  def test_serialization_bad_1(self):
    """Deserialize: XML -> Log (bad 1)"""
    util.deserialize_and_check(EG_BAD_LOG_1, shouldfail=True)

  def test_serialization_bad_2(self):
    """Deserialize: XML -> Log (bad 2)"""
    util.deserialize_and_check(EG_BAD_LOG_2, shouldfail=True)

  def test_serialization_bad_3(self):
    """Deserialize: XML -> Log (bad 3)"""
    util.deserialize_and_check(EG_BAD_LOG_3, shouldfail=True)
