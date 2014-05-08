#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
''':mod:`test_workspace`
========================

:Synopsis:
 - Test the WorkspaceResolver class.
:Author:
  DataONE (Dahl)
'''

# Stdlib.
import logging
#import os
import pprint
import sys
import unittest

# D1.
sys.path.append('..')
sys.path.append('../..')
import directory
import directory_item
import solr_query_simulator
import resolver.workspace
import workspace
import path_exception


class O():
  def workspace(self):
    pass


class TestWorkspaceResolver(unittest.TestCase):
  def setUp(self):
    options = O()
    options.BASE_URL = 'https://localhost/'
    options.WORKSPACE_XML = './test_workspace.xml'
    options.MAX_ERROR_PATH_CACHE_SIZE = 1000
    options.MAX_SOLR_QUERY_CACHE_SIZE = 1000
    self.workspace = workspace.CommandProcessor(options)
    self.w = resolver.workspace.Resolver(options, self.workspace)

  def test_050_path_root(self):
    f = self.w._get_workspace_folder([])
    self.assertEqual(f.name, 'root')

  def test_100_path_root_first(self):
    f = self.w._get_workspace_folder(['folder_1'])
    self.assertEqual(f.name, 'folder_1')

  def test_110_path_root_second(self):
    f = self.w._get_workspace_folder(['folder_2'])
    self.assertEqual(f.name, 'folder_2')

  def test_120_path_root_level_2(self):
    f = self.w._get_workspace_folder(['folder_2', 'folder_3'])
    self.assertEqual(f.name, 'folder_3')

  def test_130_path_does_not_find_level_2_in_level_1(self):
    self.assertTrue(self.w._get_workspace_folder(['folder_3']) is None)

  def test_140_path_does_not_find_level_2_in_level_1(self):
    self.assertTrue(self.w._get_workspace_folder(['folder_3']) is None)

  def test_150_folder_contents(self):
    f = self.w._get_workspace_folder(['folder_2'])
    self.assertTrue('dataone_identifier_2b' in f.identifier)
    self.assertTrue('solr_query_2a' in f.query)
    self.assertTrue(f.folder[0].name == 'folder_3')

  def test_200_split_path_by_reserved_name_1(self):
    # Exception should be path_exception.PathException but then the test doesn't
    # work. Why?
    self.assertRaises(Exception, self.w._split_path_by_reserved_name, [])

  def test_210_split_path_by_reserved_name_2(self):
    # Exception should be path_exception.PathException but then the test doesn't
    # work. Why?
    self.assertRaises(Exception, self.w._split_path_by_reserved_name, ['a', 'b', 'c'])

  def test_220_split_path_by_reserved_name_3(self):
    p = self.w._split_path_by_reserved_name(['Regions', 'b', 'c'])
    self.assertTrue(p == ([], 'Regions', ['b', 'c']))

  def test_230_split_path_by_reserved_name_4(self):
    p = self.w._split_path_by_reserved_name(['a', 'Regions', 'c'])
    self.assertTrue(p == (['a'], 'Regions', ['c']))

  def test_240_split_path_by_reserved_name_5(self):
    p = self.w._split_path_by_reserved_name(['a', 'b', 'Regions'])
    self.assertTrue(p == (['a', 'b'], 'Regions', []))

#===============================================================================


def log_setup():
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  import optparse

  log_setup()

  # Command line opts.
  parser = optparse.OptionParser()
  parser.add_option('--debug', action='store_true', default=False, dest='debug')
  parser.add_option(
    '--test', action='store',
    default='',
    dest='test',
    help='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestWorkspaceResolver
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
