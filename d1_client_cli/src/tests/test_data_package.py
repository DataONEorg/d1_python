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

#PID_SciMeta =  'knb-lter-gce.294.17'
#PID_SciData0 = 'knb-lter-gce.196.27'
#PID_SciData1 = 'knb-lter-gce.128.27'
#PID_SciData2 = None
PID_SciMeta = 'doi:10.5072/FK2/KNB/CHL.8.2'
PID_SciData0 = 'doi:10.5072/FK2/KNB/6000141086_2.7.1'
PID_SciData1 = 'doi:10.5072/FK2/KNB/6000141086_2.7.2'
PID_SciData2 = 'doi:10.5072/FK2/KNB/6000141086_2.8.1'
PID_List = (PID_SciMeta, PID_SciData0, PID_SciData1, PID_SciData2)

PKG_Pid = 'pkg-20120417T2031Z'
PKG_SciMeta = 'knb-lter-gce.234.17'
PKG_SciData0 = 'abp-20120409T2341Z'
PKG_SciData1 = 'abp-20120403T2021Z'
PKG_SciData2 = 'abp-20120406T2215Z'

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
    self.verify_pids_exist((PID_SciMeta, ))
    pkg = data_package.DataPackage("test_040")
    pkg.scimeta_add(self.sess, PID_SciMeta)
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
    self.verify_pids_exist(PID_List)
    now = datetime.datetime.now()
    pkg_pid = now.strftime('pkg_test_030_%Y%m%dT%H%MZ')
    pkg = data_package.DataPackage(pkg_pid)
    pkg.scimeta_add(self.sess, PID_SciMeta)
    pkg.scidata_add(self.sess, PID_SciData0)
    pkg.scidata_add(self.sess, PID_SciData1)
    pkg.scidata_add(self.sess, PID_SciData2)
    self.assertTrue(pkg.is_dirty(), 'Package is not marked as dirty.')
    serial = pkg._serialize(self.sess)
    self.assertNotEqual(None, serial, 'Couldn\'t serialize "%s".' % pkg_pid)
    #

  def test_031(self):
    '''Test 031: Add scimeta, scidata objects and serialize.'''
    pkg = data_package.DataPackage('pkg_test_031')
    pkg.scimeta_add(
      self.sess, 'sysmeta0',
      'files/knb-lter-gce.294.17.xml;format-id=eml://ecoinformatics.org/eml-2.1.0'
    )
    pkg.scidata_add(self.sess, 'sysdata1', 'files/small.csv;format-id=text/csv')
    pkg.scidata_add(self.sess, 'sysdata2', 'files/small.csv;format-id=text/csv')
    pkg.scidata_add(self.sess, 'sysdata3', 'files/small.csv;format-id=text/csv')
    serial = pkg._serialize(self.sess)
    self.assertNotEqual(None, serial, 'Couldn\'t serialize package "test_031"')

  def test_040(self):
    '''Test 040: Add scimeta, scidata objects and serialize.'''
    self.verify_pids_exist(PID_List)
    now = datetime.datetime.now()
    pkg_pid = now.strftime('test_040_%Y%m%dT%H%MZ')
    pkg = data_package.DataPackage(pkg_pid)
    pkg.scimeta_add(self.sess, PID_SciMeta)
    pkg.scidata_add(self.sess, PID_SciData0)
    pkg.scidata_add(self.sess, PID_SciData1)
    pkg.scidata_add(self.sess, PID_SciData2)
    self.assertTrue(pkg.is_dirty(), 'Package is not marked as dirty.')
    new_pid = pkg.save(self.sess)
    try:
      self.assertEqual(pkg_pid, new_pid, 'Couldn\'t save "test_040"')
      self.assertFalse(pkg.is_dirty(), 'Package is still marked as dirty.')
      new_sysmeta = cli_client.get_sysmeta_by_pid(self.sess, pkg_pid, True)
      self.assertNotEqual(None, new_sysmeta, 'Couldn\'t find new sysmeta')
    finally:
      mn_client = cli_client.CLIMNClient(self.sess)
      mn_client.archive(pkg_pid)

  def test_050(self):
    '''Test 050: parse package file.'''
    self.verify_pids_exist(('knb-lter-gce.128.27', ))
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
    self.verify_pids_exist((PKG_Pid, ))
    # pkg => (scimeta, (scidata, scidata, ...))
    tests = {PKG_Pid: (PKG_SciMeta, (PKG_SciData0, PKG_SciData1, PKG_SciData2)), }
    #
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

  def verify_pids_exist(self, pid_list):
    '''  Make sure all the pids in use for this test exist in DataONE. '''
    mn_client = cli_client.CLIMNClient(self.sess)
    for pid in pid_list:
      if pid:
        try:
          mn_client.getSystemMetadata(pid)
        except:
          self.fail('%s: no such pid in system.' % pid)


if __name__ == "__main__":
  #  sys.argv = ['', 'TESTDataPackage.test_021']
  unittest.main()
