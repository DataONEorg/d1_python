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
'''Module d1_client_cli.tests.test_system_metadata
=================================================

Unit tests for system_metadata.

:Created: 2011-11-10
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import unittest
import logging
import sys

# D1.
import d1_common.const
import d1_common.testcasewithurlcompare
import d1_common.types.exceptions
import d1_common.xmlrunner

# App.
sys.path.append('../d1_client_cli/')
import system_metadata
import cli_exceptions

#===============================================================================


class TESTCLISystemMetadata(d1_common.testcasewithurlcompare.TestCaseWithURLCompare):
  def setUp(self):
    pass

  def _get_sysmeta_dict(self):
    return {
      'object_format': ('TEST_OBJECT_FORMAT', str),
      'submitter': ('TEST_SUBMITTER', str),
      'rightsholder': ('TEST_RIGHTSHOLDER', str),
      'origin_member_node': ('TEST_ORIGIN_MEMBER_NODE', str),
      'authoritative_member_node': ('TEST_AUTHORITATIVE_MEMBER_NODE', str),
      'pid': ('TEST_PID', str),
      'checksum': ('TEST_CHECKSUM', str),
      'algorithm': ('TEST_ALGORITHM', str),
      'size': (123, int),
    }

  def test_010(self):
    '''The system_metadata object can be instantiated'''
    s = system_metadata.system_metadata(self._get_sysmeta_dict())

  def test_020(self):
    '''Representation on system metadata with missing value raises MissingSysmetaParameters'''
    t = self._get_sysmeta_dict()
    t['size'] = (None, int)
    s = system_metadata.system_metadata(t)
    self.assertRaises(system_metadata.MissingSysmetaParameters, s.__repr__)

  def test_030(self):
    '''Representation on valid system metadata returns XML'''
    s = system_metadata.system_metadata(self._get_sysmeta_dict())
    self.assertEqual(repr(s)[:19], '<?xml version="1.0"')

  def test_100(self):
    '''str() returns formatted string representation'''
    s = system_metadata.system_metadata(self._get_sysmeta_dict())
    self.assertEquals(str(s)[:13], '    algorithm')


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
