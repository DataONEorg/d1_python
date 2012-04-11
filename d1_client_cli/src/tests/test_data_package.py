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
Module d1_client_cli.tests.test_data_package
============================================

:Synopsis: Unit tests for data_package.
:Created: 2012-04-10
:Author: DataONE (Pippin)
'''

# Stdlib
import sys
import unittest

# D1 Client
sys.path.append('../d1_client_cli/')
from const import *
import data_package
import session


class TestDataPackage(unittest.TestCase):
  def setUp(self):
    self.sess = session.session()
    self.sess.load(suppress_error=True)
    self.sess.set(VERBOSE_sect, VERBOSE_name, False)
    self.sess.set(PRETTY_sect, PRETTY_name, False)
    pass

  def tearDown(self):
    pass

  def testName(self):
    pass

  def test_010(self):
    '''Basic create.'''
    pkg = data_package.DataPackage()
    self.assertNotEqual(None, pkg, 'data_package() is None')
    pkg = data_package.DataPackage("test_010")
    self.assertNotEqual(None, pkg, 'data_package(String) is None')

  def test_020(self):
    '''Add a scimeta object.'''
    pkg = data_package.DataPackage("test_020")
    self.assertNotEqual(None, pkg, 'pkg is None')
    pkg.scimeta_add(
      self.sess, 'abp_knb-lter-gce.294.17',
      'files/knb-lter-gce.294.17.xml;format-id=eml://ecoinformatics.org/eml-2.1.0'
    )
    self.assertNotEqual(None, pkg.scimeta, 'scimeta is None')

  def test_021(self):
    ''' Get an existing science metadata object. '''
    pkg = data_package.DataPackage("test_040")
    pkg.scimeta_add(self.sess, 'knb-lter-gce.294.17')
    self.assertNotEqual(None, pkg.scimeta, 'scimeta is None')

  def test_022(self):
    '''Add a scidata objects.'''
    pkg = data_package.DataPackage("test_021")
    self.assertNotEqual(None, pkg, 'pkg is None')
    pkg.scidata_add(self.sess, 'abp_test_021a', 'files/small.csv;format-id=text/csv')
    pkg.scidata_add(self.sess, 'abp_test_021b', 'files/small.csv;format-id=text/csv')
    pkg.scidata_add(self.sess, 'abp_test_021c', 'files/small.csv;format-id=text/csv')
    self.assertNotEqual(None, pkg.scidata_dict, 'scidata_dict is None')
    self.assertEqual(3, len(pkg.scidata_dict), 'Wrong number of scidata objects.')
    self.assertNotEqual(
      None, pkg.scidata_get(
        'abp_test_021a'
      ), 'Couldn\'t find pid "abp_test_021a"'
    )
    self.assertNotEqual(
      None, pkg.scidata_get(
        'abp_test_021b'
      ), 'Couldn\'t find pid "abp_test_021b"'
    )
    self.assertNotEqual(
      None, pkg.scidata_get(
        'abp_test_021c'
      ), 'Couldn\'t find pid "abp_test_021c"'
    )
    self.assertEqual(None, pkg.scidata_get('abp_test_021d'), 'Found pid "abp_test_021d"')

  def test_030(self):
    '''Add scimeta, scidata objects and serialize.'''
    pkg = data_package.DataPackage("test_030")
    pkg.scimeta_add(self.sess, 'knb-lter-gce.294.17')
    pkg.scidata_add(self.sess, 'knb-lter-gce.196.27')
    pkg.scidata_add(self.sess, 'knb-lter-gce.128.27')
    serial = pkg._serialize()
    self.assertNotEqual(None, serial, 'Couldn\'t serialize package "test_030"')

  def test_031(self):
    '''Add scimeta, scidata objects and serialize.'''
    pkg = data_package.DataPackage("test_030")
    pkg.scimeta_add(
      self.sess, 'abp_knb-lter-gce.294.17',
      'files/knb-lter-gce.294.17.xml;format-id=eml://ecoinformatics.org/eml-2.1.0'
    )
    pkg.scidata_add(self.sess, 'abp_test_021a', 'files/small.csv;format-id=text/csv')
    pkg.scidata_add(self.sess, 'abp_test_021b', 'files/small.csv;format-id=text/csv')
    pkg.scidata_add(self.sess, 'abp_test_021c', 'files/small.csv;format-id=text/csv')
    serial = pkg._serialize()
    self.assertNotEqual(None, serial, 'Couldn\'t serialize package "test_031"')


if __name__ == "__main__":
  #import sys;sys.argv = ['', 'Test.testName']
  unittest.main()
