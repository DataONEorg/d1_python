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
import datetime
import sys
import unittest

# D1 Client
sys.path.append('../d1_client_cli/')
try:
  import cli_client
  from const import VERBOSE_sect, VERBOSE_name, PRETTY_sect, PRETTY_name
  import data_package
  import session
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  raise

#===============================================================================


class TESTDataPackage(unittest.TestCase):
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
    '''Test 010: Basic create.'''
    pkg = data_package.DataPackage()
    self.assertNotEqual(None, pkg, 'data_package() is None')
    pkg = data_package.DataPackage("test_010")
    self.assertNotEqual(None, pkg, 'data_package(String) is None')

  def test_020(self):
    '''Test 020: Add a scimeta object.'''
    pkg = data_package.DataPackage("test_020")
    self.assertNotEqual(None, pkg, 'pkg is None')
    pkg.scimeta_add(
      self.sess, 'abp_knb-lter-gce.294.17',
      'files/knb-lter-gce.294.17.xml;format-id=eml://ecoinformatics.org/eml-2.1.0'
    )
    self.assertNotEqual(None, pkg.scimeta, 'scimeta is None')

  def test_021(self):
    '''Test 021: Get an existing science metadata object. '''
    pkg = data_package.DataPackage("test_040")
    pkg.scimeta_add(self.sess, 'knb-lter-gce.294.17')
    self.assertNotEqual(None, pkg.scimeta, 'scimeta is None')

  def test_022(self):
    '''Test 022: Add a scidata objects.'''
    pkg = data_package.DataPackage("test_021")
    self.assertNotEqual(None, pkg, 'pkg is None')
    pkg.scidata_add(self.sess, 'pkg_test_021a', 'files/small.csv;format-id=text/csv')
    pkg.scidata_add(self.sess, 'pkg_test_021b', 'files/small.csv;format-id=text/csv')
    pkg.scidata_add(self.sess, 'pkg_test_021c', 'files/small.csv;format-id=text/csv')
    self.assertNotEqual(None, pkg.scidata_dict, 'scidata_dict is None')
    self.assertEqual(3, len(pkg.scidata_dict), 'Wrong number of scidata objects.')
    self.assertNotEqual(
      None, pkg.scidata_get(
        'pkg_test_021a'
      ), 'Couldn\'t find pid "pkg_test_021a"'
    )
    self.assertNotEqual(
      None, pkg.scidata_get(
        'pkg_test_021b'
      ), 'Couldn\'t find pid "pkg_test_021b"'
    )
    self.assertNotEqual(
      None, pkg.scidata_get(
        'pkg_test_021c'
      ), 'Couldn\'t find pid "pkg_test_021c"'
    )
    self.assertEqual(None, pkg.scidata_get('pkg_test_021d'), 'Found pid "pkg_test_021d"')

  def test_030(self):
    '''Test 030: Add scimeta, scidata objects and serialize.'''
    now = datetime.datetime.now()
    pkg_pid = now.strftime('pkg_test_030_%Y%m%dT%H%MZ')
    pkg = data_package.DataPackage(pkg_pid)
    #    pkg.scimeta_add(self.sess, 'knb-lter-gce.294.17')
    #    pkg.scidata_add(self.sess, 'knb-lter-gce.196.27')
    #    pkg.scidata_add(self.sess, 'knb-lter-gce.128.27')
    pkg.scimeta_add(self.sess, 'doi:10.5072/FK2/KNB/CHL.8.2')
    pkg.scidata_add(self.sess, 'doi:10.5072/FK2/KNB/6000141086_2.7.1')
    pkg.scidata_add(self.sess, 'doi:10.5072/FK2/KNB/6000141086_2.7.2')
    pkg.scidata_add(self.sess, 'doi:10.5072/FK2/KNB/6000141086_2.8.1')
    self.assertTrue(pkg.is_dirty(), 'Package is not marked as dirty.')
    serial = pkg._serialize(self.sess)
    self.assertNotEqual(None, serial, 'Couldn\'t serialize "%s".' % pkg_pid)
    #
    # XML generator is non-deterministic.
    #    f = open('files/expected_dataPackage_test030.xml')
    #    expected = f.read()
    #    f.close()
    #    print 'Expected:\n', expected, '\n\nActual\n', serial
    #    self.assertEquals(expected, serial, 'Wrong output')

  def test_031(self):
    '''Test 031: Add scimeta, scidata objects and serialize.'''
    now = datetime.datetime.now()
    pid = {
      'pkg': now.strftime('pkg_test_031_%Y%m%dT%H%MZ'),
      'sm': now.strftime('knb-lter-gce.294.17_%Y%m%dT%H%MZ'),
      'sd1': now.strftime('pkg_test_031-scimeta1_%Y%m%dT%H%MZ'),
      'sd2': now.strftime('pkg_test_031-scimeta2_%Y%m%dT%H%MZ'),
      'sd3': now.strftime('pkg_test_031-scimeta3_%Y%m%dT%H%MZ'),
    }

    pkg = data_package.DataPackage(pid['pkg'])
    pkg.scimeta_add(
      self.sess, pid['sm'],
      'files/knb-lter-gce.294.17.xml;format-id=eml://ecoinformatics.org/eml-2.1.0'
    )
    pkg.scidata_add(self.sess, pid['sd1'], 'files/small.csv;format-id=text/csv')
    pkg.scidata_add(self.sess, pid['sd2'], 'files/small.csv;format-id=text/csv')
    pkg.scidata_add(self.sess, pid['sd3'], 'files/small.csv;format-id=text/csv')
    serial = pkg._serialize(self.sess)
    try:
      self.assertNotEqual(None, serial, 'Couldn\'t serialize package "test_031"')
    finally:
      mn_client = cli_client.CLIMNClient(self.sess)
      for k in pid.keys():
        try:
          mn_client.archive(pid[k]) # ignore errors.
        except:
          pass

  def test_040(self):
    '''Test 040: Add scimeta, scidata objects and serialize.'''
    now = datetime.datetime.now()
    pkg_pid = now.strftime('test_040_%Y%m%dT%H%MZ')
    pkg = data_package.DataPackage(pkg_pid)
    #    pkg.scimeta_add(self.sess, 'knb-lter-gce.294.17')
    #    pkg.scidata_add(self.sess, 'knb-lter-gce.196.27')
    #    pkg.scidata_add(self.sess, 'knb-lter-gce.128.27')
    pkg.scimeta_add(self.sess, 'doi:10.5072/FK2/KNB/CHL.8.2')
    pkg.scidata_add(self.sess, 'doi:10.5072/FK2/KNB/6000141086_2.7.1')
    pkg.scidata_add(self.sess, 'doi:10.5072/FK2/KNB/6000141086_2.7.2')
    pkg.scidata_add(self.sess, 'doi:10.5072/FK2/KNB/6000141086_2.8.1')
    self.assertTrue(pkg.is_dirty(), 'Package is not marked as dirty.')
    new_pid = pkg.save(self.sess)
    try:
      self.assertEqual(pkg_pid, new_pid, 'Couldn\'t save "test_040"')
      self.assertFalse(pkg.is_dirty(), 'Package is still marked as dirty.')
      new_sysmeta = cli_client.get_sysmeta_by_pid(self.sess, pkg_pid, True)
      self.assertNotEqual(None, new_sysmeta, 'Couldn\'t find new sysmeta')
#      f = open("files/expected_dataPackage_test040.xml", "r")
#      expected = f.read()
#      f.close()
#      self.assertEqual(expected, pkg.resmap, "Wrong datapackage")
    finally:
      mn_client = cli_client.CLIMNClient(self.sess)
      mn_client.archive(pkg_pid)

  def test_050(self):
    '''Test 050: parse package file.'''
    pkg = data_package.DataPackage()
    result = pkg._parse_rdf_xml('files/test_050-rdf.xml')
    self.assertTrue(result, 'Couldn\'t parse "test_050-rdf.xml"')
    self.assertNotEqual(None, pkg.scimeta, 'No Science Metadata Object found')
    self.assertNotEqual(
      None, pkg.scidata_get(
        'knb-lter-gce.128.27'
      ), 'No Science Data Object "knb-lter-gce.128.27" found'
    )
    self.assertNotEqual(
      None, pkg.scidata_get(
        'knb-lter-gce.196.27'
      ), 'No Science Data Object "knb-lter-gce.196.27" found'
    )

  def test_051(self):
    '''Test 051: Load and parse a package.'''
    # pkg => (scimeta, (scidata, scidata, ...))
    tests = { 'pkg-20120417T2031Z': ('knb-lter-gce.234.17',
                ('abp-20120409T2341Z', 'abp-20120403T2021Z', 'abp-20120406T2215Z')),
             }
    for (pkg_name, pkg_contents) in tests.items():
      pkg = data_package.DataPackage(pkg_name)
      self.assertNotEqual(None, pkg.load(self.sess), 'Couldn\'t load "%s".' % pkg_name)
      self.assertNotEqual(None, pkg.scimeta, 'No Science Metadata Object found')
      self.assertEqual(
        pkg_contents[0], pkg.scimeta.pid, 'Wrong Science Metadata Object found'
      )
      for scidata_name in pkg_contents[1]:
        self.assertNotEqual(
          None, pkg.scidata_get(
            scidata_name
          ), 'No Science Data Object "%s" found' % scidata_name
        )

if __name__ == "__main__":
  sys.argv = ['', 'TESTDataPackage.test_031']
  unittest.main()
