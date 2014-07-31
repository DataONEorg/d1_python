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
 - Test the ObjectTree class.
:Author: DataONE (Dahl)
'''

# Stdlib.
import datetime
import logging
#import os
import pprint
import pickle
import sys
import tempfile
import unittest

# D1.
sys.path.append('..')
import object_tree


class TestObjectTree(unittest.TestCase):
  def setUp(self):
    pass

  def test_100(self):
    '''Create ObjectTree with defaults'''
    a = object_tree.ObjectTree()

  def test_110(self):
    '''Create ObjectTree and unpickle default cache'''
    with object_tree.ObjectTree() as w:
      pass

  def test_120(self):
    '''Create ObjectTree, unpickle default cache and refresh with empty def'''
    with object_tree.ObjectTree(object_tree_def_path='object_tree_empty.xml') as w:
      w.refresh()

  def test_130(self):
    '''Create ObjectTree, unpickle default cache and refresh with single folder'''
    with object_tree.ObjectTree(
      object_tree_def_path='object_tree_single.xml',
      automatic_refresh=True
    ) as w:
      pass

  #def test_140(self):
  #  '''Create ObjectTree, unpickle default cache and refresh with all folders'''
  #  #with object_tree.ObjectTree(object_tree_def_path='object_tree_tiny_two_levels.xml') as w:
  #  with object_tree.ObjectTree(object_tree_def_path='object_tree_all.xml') as w:
  #    w.refresh()
  #    #pprint.pprint(w.get_cache())
  #
  #
  #def test_150(self):
  #  '''Retrieve folder'''
  #  with object_tree.ObjectTree(object_tree_def_path='object_tree_all.xml') as w:
  #    folder = w.get_folder([])
  #    pprint.pprint(folder)
  #    #self._print_folder_items(folder)
  #    #folder = w.get_folder(['folder_level_1'])
  #    #self._print_folder_items(folder)
  #

  def test_140(self):
    '''Create ObjectTree, unpickle default cache and refresh with all folders'''
    #with object_tree.ObjectTree(object_tree_def_path='object_tree_tiny_two_levels.xml') as w:
    with object_tree.ObjectTree(object_tree_def_path='object_tree_all.xml') as w:
      w.refresh()
      #pprint.pprint(w.get_cache())

  def test_150(self):
    '''Retrieve folder'''
    with object_tree.ObjectTree() as w:
      #folder = w.get_folder([])
      #pprint.pprint(folder, depth=3)
      #self._print_folder_items(folder)
      folder = w.get_folder(['folder_2'])
      self._print_folder(folder)

  def _print_folder(self, folder):
    print 'dirs:'
    for k, v in folder['dirs'].items():
      print k
    print 'items:'
    for k, v in folder['items'].items():
      print k

  def _test_1000(self):
    '''TODO: Test refresh on various non-emtpy cache.'''
    with tempfile.NamedTemporaryFile(delete=False) as f:
      pickle.dump([], f)
      f.close()
      with object_tree.ObjectTree(
        object_tree_cache_path=f.name,
        object_tree_def_path='object_tree_empty.xml'
      ) as w:
        w.refresh()
        self.assertEqual(w._object_tree, [])

#===============================================================================


def log_setup():
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(module)s %(message)s', '%Y-%m-%d %H:%M:%S'
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

  s = TestObjectTree
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
