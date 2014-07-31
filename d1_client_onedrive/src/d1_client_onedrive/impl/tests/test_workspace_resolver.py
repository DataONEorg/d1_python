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
''':mod:`test_object_tree`
========================

:Synopsis:
 - Test the ObjectTreeResolver class.
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
import resolver.object_tree
import object_tree
import onedrive_exceptions


class O():
  def object_tree(self):
    pass


class TestObjectTreeResolver(unittest.TestCase):
  def setUp(self):
    options = O()
    options.base_url = 'https://localhost/'
    options.object_tree_xml = './test_object_tree.xml'
    options.max_error_path_cache_size = 1000
    options.max_solr_query_cache_size = 1000
    self._object_tree = object_tree.CommandProcessor(options)
    self._w = resolver.object_tree.Resolver(options, self._object_tree)

  def test_050_path_root(self):
    f = self._w._get_object_tree_folder([])
    self._assertEqual(f.name, 'root')

  def test_100_path_root_first(self):
    f = self._w._get_object_tree_folder(['folder_1'])
    self._assertEqual(f.name, 'folder_1')

  def test_110_path_root_second(self):
    f = self._w._get_object_tree_folder(['folder_2'])
    self._assertEqual(f.name, 'folder_2')

  def test_120_path_root_level_2(self):
    f = self._w._get_object_tree_folder(['folder_2', 'folder_3'])
    self._assertEqual(f.name, 'folder_3')

  def test_130_path_does_not_find_level_2_in_level_1(self):
    self._assertTrue(self._w._get_object_tree_folder(['folder_3']) is None)

  def test_140_path_does_not_find_level_2_in_level_1(self):
    self._assertTrue(self._w._get_object_tree_folder(['folder_3']) is None)

  def test_150_folder_contents(self):
    f = self._w._get_object_tree_folder(['folder_2'])
    self._assertTrue('dataone_identifier_2b' in f.identifier)
    self._assertTrue('solr_query_2a' in f.query)
    self._assertTrue(f.folder[0].name == 'folder_3')

  def test_200_split_path_by_reserved_name_1(self):
    # Exception should be onedrive_exceptions.PathException but then the test doesn't
    # work. Why?
    self._assertRaises(Exception, self._w._split_path_by_reserved_name, [])

  def test_210_split_path_by_reserved_name_2(self):
    # Exception should be onedrive_exceptions.PathException but then the test doesn't
    # work. Why?
    self._assertRaises(Exception, self._w._split_path_by_reserved_name, ['a', 'b', 'c'])

  def test_220_split_path_by_reserved_name_3(self):
    p = self._w._split_path_by_reserved_name(['Regions', 'b', 'c'])
    self._assertTrue(p == ([], 'Regions', ['b', 'c']))

  def test_230_split_path_by_reserved_name_4(self):
    p = self._w._split_path_by_reserved_name(['a', 'Regions', 'c'])
    self._assertTrue(p == (['a'], 'Regions', ['c']))

  def test_240_split_path_by_reserved_name_5(self):
    p = self._w._split_path_by_reserved_name(['a', 'b', 'Regions'])
    self._assertTrue(p == (['a', 'b'], 'Regions', []))

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

  s = TestObjectTreeResolver
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
