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
Module d1_client_cli.tests.test_session
=======================================

:Synopsis: Unit tests for session parameters.
:Created: 2011-11-10
:Author: DataONE (Dahl)
'''

# Stdlib.
import unittest
import logging
import sys

try:
  # D1.
  from d1_common.testcasewithurlcompare import TestCaseWithURLCompare 
  
  # App.
  sys.path.append('../d1_client_cli/')
  import cli_util
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  raise


#===============================================================================

class TESTCLIUtil(TestCaseWithURLCompare):
  def setUp(self):
    pass


  def test_010(self):
    '''Create a complex path from "string".'''
    complex_path = cli_util.create_complex_path("string")
    self.assertEquals("string", complex_path.path)
    self.assertEquals(None, complex_path.formatId)

  def test_011(self):
    '''Create a complex path from "string;format=text/csv".'''
    complex_path = cli_util.create_complex_path("string;format=text/csv")
    self.assertEquals("string", complex_path.path)
    self.assertEquals("text/csv", complex_path.formatId)

  def test_012(self):
    '''Create a complex path from ";format=text/csv".'''
    complex_path = cli_util.create_complex_path(";format=text/csv")
    self.assertEquals(None, complex_path.path)
    self.assertEquals("text/csv", complex_path.formatId)

  def test_013(self):
    '''Create a complex path from "".'''
    complex_path = cli_util.create_complex_path("")
    self.assertEquals(None, complex_path.path)
    self.assertEquals(None, complex_path.formatId)



if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
TESTCLIUtil
  unittest.main()
