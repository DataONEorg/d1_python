#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2011
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
Module d1_libclient.tests.all_tests
===================================

Run all Unit tests.

:Created: 2011-04-08
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''

import sys
import logging
import unittest
from d1_common import xmlrunner
# The DataONEBaseClient tests work, but I haven't looked into how to pass
# options from here to the class.
# from test_d1baseclient import TestDataONEBaseClient
from test_cnclient import TestCNClient
from test_d1baseclient import TestDataONEBaseClient
from test_d1client import TestDataONEClient
from test_data_package import TestDataPackage
from test_logrecorditerator import TestLogRecordIterator
from test_mnclient import TestMNClient
from test_object_format_info import TestObjectFormatInfo
from test_objectlistiterator import TestObjectListIterator
from test_solr_client import TestSolrClient
from test_systemmetadata import TestSystemMetadata

#=========================================================================


def main():
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


if __name__ == '__main__':
  # print 'Not implemented. See ticket #4109.'
  main()
