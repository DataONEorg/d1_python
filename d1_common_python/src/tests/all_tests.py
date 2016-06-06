#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2014 DataONE
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
Module d1_common.tests.all_tests
================================

Run all Unit tests.

:Created: 2011-03-09
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import sys
import logging
import unittest

# D1.
from d1_common import xmlrunner

# App.
from test_accesspolicy import TestAccessPolicy
from test_checksum import TestChecksum
from test_date_time import TestDateTime
from test_exceptions import TestExceptions
from test_logrecords import TestObjectList
from test_nodelist import TestNodeList
from test_objectlist import TestObjectList
from test_objectlocationlist import TestObjectLocationList
from test_pid import TestPID
from test_restclient import TestRESTClient
from test_systemmetadata import TestSystemMetadata
from test_testcasewithurlcompare import Test_URLCompare
from test_url import TestUrl
from test_utils import TestUtils
from test_xml_compare import TestXMLCompare

#===============================================================================

if __name__ == "__main__":
  from d1_common import svnrevision
  argv = sys.argv
  if "--debug" in argv:
    logging.basicConfig(level=logging.DEBUG)
    argv.remove("--debug")
  if "--with-xunit" in argv:
    argv.remove("--with-xunit")
    unittest.main(argv=argv, testRunner=xmlrunner.XmlTestRunner(sys.stdout))
  else:
    unittest.main(argv=argv)
