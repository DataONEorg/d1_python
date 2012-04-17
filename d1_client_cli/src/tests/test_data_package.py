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
try:
  from const import VERBOSE_sect, VERBOSE_name, PRETTY_sect, PRETTY_name
  import cli_client
  import data_package
  import session
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  raise

#===============================================================================


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

#  def test_010(self):
#    '''Test 010: Basic create.'''
#    pkg = data_package.DataPackage()
#    self.assertNotEqual(None, pkg, 'data_package() is None')
#    pkg = data_package.DataPackage("test_010")
#    self.assertNotEqual(None, pkg, 'data_package(String) is None')
#
#  def test_020(self):
#    '''Test 020: Add a scimeta object.'''
#    pkg = data_package.DataPackage("test_020")
#    self.assertNotEqual(None, pkg, 'pkg is None')
#    pkg.scimeta_add(self.sess, 'abp_knb-lter-gce.294.17', 'files/knb-lter-gce.294.17.xml;format-id=eml://ecoinformatics.org/eml-2.1.0')
#    self.assertNotEqual(None, pkg.scimeta, 'scimeta is None')
#    
#  def test_021(self):
#    '''Test 021: Get an existing science metadata object. '''
#    pkg = data_package.DataPackage("test_040")
#    pkg.scimeta_add(self.sess, 'knb-lter-gce.294.17')
#    self.assertNotEqual(None, pkg.scimeta, 'scimeta is None')
#
#  def test_022(self):
#    '''Test 022: Add a scidata objects.'''
#    pkg = data_package.DataPackage("test_021")
#    self.assertNotEqual(None, pkg, 'pkg is None')
#    pkg.scidata_add(self.sess, 'pkg_test_021a', 'files/small.csv;format-id=text/csv')
#    pkg.scidata_add(self.sess, 'pkg_test_021b', 'files/small.csv;format-id=text/csv')
#    pkg.scidata_add(self.sess, 'pkg_test_021c', 'files/small.csv;format-id=text/csv')
#    self.assertNotEqual(None, pkg.scidata_dict, 'scidata_dict is None')
#    self.assertEqual(3, len(pkg.scidata_dict), 'Wrong number of scidata objects.')
#    self.assertNotEqual(None, pkg.scidata_get('pkg_test_021a'), 'Couldn\'t find pid "pkg_test_021a"')
#    self.assertNotEqual(None, pkg.scidata_get('pkg_test_021b'), 'Couldn\'t find pid "pkg_test_021b"')
#    self.assertNotEqual(None, pkg.scidata_get('pkg_test_021c'), 'Couldn\'t find pid "pkg_test_021c"')
#    self.assertEqual(None, pkg.scidata_get('pkg_test_021d'), 'Found pid "pkg_test_021d"')
#
#  def test_030(self):
#    '''Test 030: Add scimeta, scidata objects and serialize.'''
#    now = datetime.datetime.now()
#    pkg_pid = now.strftime('pkg_test_030_%Y%m%dT%H%MZ')
#    pkg = data_package.DataPackage(pkg_pid)
#    pkg.scimeta_add(self.sess, 'knb-lter-gce.294.17')
#    pkg.scidata_add(self.sess, 'knb-lter-gce.196.27')
#    pkg.scidata_add(self.sess, 'knb-lter-gce.128.27')
#    serial = pkg._serialize(self.sess)
#    self.assertNotEqual(None, serial, 'Couldn\'t serialize "%s".' % pkg_pid)
#    
#  def test_031(self):
#    '''Test 031: Add scimeta, scidata objects and serialize.'''
#    now = datetime.datetime.now()
#    pkg_pid = now.strftime('pkg_test_031_%Y%m%dT%H%MZ') 
#    pkg = data_package.DataPackage(pkg_pid)
#    pkg.scimeta_add(self.sess, 'abp_knb-lter-gce.294.17', 'files/knb-lter-gce.294.17.xml;format-id=eml://ecoinformatics.org/eml-2.1.0')
#    pkg.scidata_add(self.sess, 'pkg_test_021a', 'files/small.csv;format-id=text/csv')
#    pkg.scidata_add(self.sess, 'pkg_test_021b', 'files/small.csv;format-id=text/csv')
#    pkg.scidata_add(self.sess, 'pkg_test_021c', 'files/small.csv;format-id=text/csv')
#    serial = pkg._serialize(self.sess)
#    self.assertNotEqual(None, serial, 'Couldn\'t serialize package "test_031"')
# 
#  def test_040(self):
#    '''Test 040: Add scimeta, scidata objects and serialize.'''
#    now = datetime.datetime.now()
#    pkg_pid = now.strftime('test_040_%Y%m%dT%H%MZ') 
#    pkg = data_package.DataPackage(pkg_pid)
#    pkg.scimeta_add(self.sess, 'knb-lter-gce.294.17')
#    pkg.scidata_add(self.sess, 'knb-lter-gce.196.27')
#    pkg.scidata_add(self.sess, 'knb-lter-gce.128.27')
#    new_pid = pkg.save(self.sess)
#    self.assertEqual(pkg_pid, new_pid, 'Couldn\'t save "test_040"')
#    
#  def test_050(self):
#    '''Test 050: parse package file.'''
#    f = open('files/test_050-rdf.xml')
#    rdf_xml = f.read()
#    f.close()
#    pkg = data_package.DataPackage()
#    result = pkg._parse_rdf_xml(rdf_xml)
#    self.assertNotEqual(None, result, 'Couldn\'t parse "test_050-rdf.xml"')
#    self.assertNotEqual(None, result.scimeta, 'No Science Metadata Object found')
#    self.assertNotEqual(None, result.scidata_get('knb-lter-gce.128.27'),
#                         'No Science Data Object "knb-lter-gce.128.27" found')
#    self.assertNotEqual(None, result.scidata_get('knb-lter-gce.196.27'),
#                         'No Science Data Object "knb-lter-gce.196.27" found')

  def test_060(self):
    '''Test 060: Load a package.'''
    load_pkg = data_package.DataPackage('pkg-20120417T2031Z')
    load_pkg.load(self.sess)

if __name__ == "__main__":
  #import sys;sys.argv = ['', 'Test.testName']
  unittest.main()
