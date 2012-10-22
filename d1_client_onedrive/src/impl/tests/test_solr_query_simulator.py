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
''':mod:`test_solr_query_simulator`
===================================

:Synopsis:
 - Test the Solr simulator.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
#import os
import sys
import unittest

# D1.
sys.path.append('../fuse')
import solr_query_simulator


class TestSolrQuerySimulator(unittest.TestCase):
  def setUp(self):
    self.s = solr_query_simulator.SolrQuerySimulator()

  def test_100_count_total(self):
    self.assertEqual(self.s.count_total(), 1000)

  def test_200_is_valid_facet_name(self):
    self.assertFalse(self.s.is_valid_facet_name('invalid'))

  def test_201_is_valid_facet_name(self):
    self.assertTrue(self.s.is_valid_facet_name('shape'))

  def test_250_object_matches_facet(self):
    obj = ('blue-square-smooth-heavy', 'blue', 'square', 'smooth', 'heavy')
    self.assertTrue(self.s.object_matches_facet(obj, ('color', 'blue')))

  def test_251_object_matches_facet(self):
    obj = ('blue-square-smooth-heavy', 'blue', 'square', 'smooth', 'heavy')
    self.assertFalse(self.s.object_matches_facet(obj, ('shape', 'circle')))

  def test_300_search_and(self):
    # color: red
    objects = self.s.search_and((('color', 'red'), ))
    self.assertEqual(len(objects), 207)
    for obj in objects:
      self.assertTrue(obj[0].startswith('red'))

  def test_301_search_and(self):
    # color: red and shape: square
    objects = self.s.search_and((('color', 'red'), ('shape', 'square')))
    self.assertEqual(len(objects), 48)
    for obj in objects:
      self.assertTrue(
        obj[0].startswith('red-square') or obj[0].startswith('red-pentagon') or
        obj[0].startswith('blue-square') or obj[0].startswith('blue-pentagon')
      )

  def test_302_search_or(self):
    # color: red
    objects = self.s.search_or((('color', 'red'), ))
    self.assertEqual(len(objects), 207)
    for obj in objects:
      self.assertTrue(obj[0].startswith('red'))

  def test_303_search_or(self):
    # color: red and shape: square
    objects = self.s.search_or((('color', 'red'), ('shape', 'square')))
    self.assertEqual(len(objects), 368)
    for obj in objects:
      self.assertTrue('red' in obj[0] or 'square' in obj[0])

  def test_400_unapplied_facet_names(self):
    f = self.s.unapplied_facet_names((('color', 'red'), ('shape', 'square')))
    self.assertEqual(len(f), 2)
    self.assertFalse('color' in f)
    self.assertFalse('shape' in f)
    self.assertTrue('weight' in f)
    self.assertTrue('texture' in f)

  def test_500_values_for_facet(self):
    f = self.s.facet_values_for_facet_name('color')
    self.assertTrue('white' in f)
    self.assertTrue('yellow' in f)
    self.assertFalse('square' in f)

  def test_600_count_matches_for_facet(self):
    objects = self.s.all_objects()
    self.assertEqual(self.s.count_matches_for_facet(objects, ('color', 'red')), 207)
    self.assertEqual(self.s.count_matches_for_facet(objects, ('weight', 'heavy')), 209)

  def test_700_count_matches_for_unapplied_facets(self):
    objects = self.s.all_objects()
    s = self.s.count_matches_for_unapplied_facets(objects, (('color', 'red'), ))
    self.assertTrue((196, ('shape', 'rectangle')) in s)
    self.assertTrue((197, ('shape', 'pentagon')) in s)
    self.assertTrue((223, ('texture', 'rough')) in s)
    self.assertFalse((215, ('weight', 'heavy')) in s)
    self.assertFalse((215, ('weight', 'medium')) in s)

  def test_800_unapplied_facet_names_with_value_counts(self):
    s = self.s.unapplied_facet_names_with_value_counts((('color', 'red'), ))
    self.assertTrue(('weight', 5) in s)
    self.assertTrue('texture' in [f[0] for f in s])
    self.assertFalse('color' in [f[0] for f in s])

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

  s = TestSolrQuerySimulator
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
