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
''':mod:`test_faceted_search_resolver`
======================================

:Synopsis:
 - Test the FacetedSearchResolver class.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
#import os
import pprint
import sys
import unittest

# D1.
sys.path.append('../fuse')
from directory import Directory, DirectoryItem
import solr_query_simulator
import faceted_search_resolver


class TestFacetedSearchResolver(unittest.TestCase):
  def setUp(self):
    self.i = faceted_search_resolver.Resolver(solr_query_simulator.SolrQuerySimulator())

  def test_100_resolve(self):
    d = self.i.resolve('/')
    self.assertEqual(len(d), 2 + 4 + 1000)
    self.assertTrue(DirectoryItem('@color', 5, True) in d)
    self.assertTrue(DirectoryItem('@shape', 5, True) in d)
    self.assertTrue(DirectoryItem('@texture', 5, True) in d)
    self.assertTrue(DirectoryItem('@weight', 5, True) in d)
    self.assertTrue(DirectoryItem('red-oval-smooth-medium', 123) in d)
    self.assertTrue(DirectoryItem('blue-square-smooth-medium', 123) in d)

  def test_110_resolve(self):
    d = self.i.resolve('/@shape')
    self.assertEqual(len(d), 2 + 5 + 1000)
    self.assertTrue(DirectoryItem('#square', 209, True) in d)
    self.assertTrue(DirectoryItem('#rectangle', 196, True) in d)
    self.assertTrue(DirectoryItem('#circle', 192, True) in d)
    self.assertTrue(DirectoryItem('#oval', 206, True) in d)
    self.assertTrue(DirectoryItem('#pentagon', 197, True) in d)
    self.assertTrue(DirectoryItem('red-oval-smooth-medium', 123) in d)
    self.assertTrue(DirectoryItem('blue-square-smooth-medium', 123) in d)

  def test_120_resolve(self):
    d = self.i.resolve('/@shape/#square/@color')
    self.assertEqual(len(d), 2 + 5 + 209)
    for o in d:
      self.assertTrue(
        'square' in o.name() or
        o.name() in ('.', '..', '#red', '#white', '#green', '#blue', '#yellow')
      )

  def test_130_resolve(self):
    d = self.i.resolve('/@shape/#square/@color/#red')
    self.assertEqual(len(d), 2 + 3 + 47)
    for o in d:
      self.assertTrue(
        o.name().startswith('red-square') or
        o.name() in ('.', '..', '@color', '@texture', '@weight')
      )

  def test_140_resolve(self):
    d = self.i.resolve('/red-square-soft-heavy')
    self.assertTrue('dummy1' in [n.name() for n in d])

  def test_150_resolve(self):
    d = self.i.resolve('/@shape/#square/@color/#red/red-square-soft-heavy/')
    self.assertTrue('dummy1' in [n.name() for n in d])

  def test_160_resolve(self):
    d = self.i.resolve('/@shape/#square/@color/#red/a/b/c')
    self.assertTrue('<non-existing directory>' in [n.name() for n in d])

  def test_170_resolve(self):
    d = self.i.resolve('/a/b')
    self.assertTrue('<non-existing directory>' in [n.name() for n in d])

  def test_180_resolve(self):
    d = self.i.resolve('/@color/#green/@shape/#square/@texture/#invalid')
    print d
    self.assertTrue('<non-existing directory>' in [n.name() for n in d])

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

  s = TestFacetedSearchResolver
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
