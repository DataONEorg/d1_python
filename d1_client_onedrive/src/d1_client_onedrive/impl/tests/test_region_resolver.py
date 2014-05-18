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
''':mod:`test_resource_map_resolver`
====================================

:Synopsis:
 - Test the ResourceMapResolver class.
:Region:
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
import resolver.region
import command_echoer


class O():
  pass


class TestRegionResolver(unittest.TestCase):
  def setUp(self):
    options = O()
    options.base_url = 'https://localhost/'
    options.workspace_xml = './test_workspace.xml'
    options.max_error_path_cache_size = 1000
    options.max_solr_query_cache_size = 1000
    self._resolver = resolver.region.Resolver(options, command_echoer.CommandEchoer())

  def test_100_init(self):
    # Test class instantiation (done in setUp())
    pass

  def test_200_merge_empty(self):
    dst = {}
    src = {}
    self._resolver._merge_region_trees(dst, src, 'testpid')
    self.assertEqual(dst, {})

  def test_210_merge_simple_to_empty(self):
    dst = {}
    src = {'d1': {}, 'd2': {'d21': {}, 'd22': {'d31': {}}}}
    self._resolver._merge_region_trees(dst, src, 'testpid')
    self.assertEqual(dst, {'d2': {'d21': {'testpid': None}, 'd22': {'testpid': None, 'd31': {'testpid': None}}, 'testpid': None}, 'd1': {'testpid': None}})

  def test_220_merge_simple_to_simple(self):
    dst = {'f1': None, 'd1': {'f21': None}}
    src = {'d1': {}, 'd2': {}, 'd3': {'d31': {'d311': {}}, 'd32': {}}}
    self._resolver._merge_region_trees(dst, src, 'testpid')
    self.assertEqual(dst, {'f1': None, 'd2': {'testpid': None}, 'd3': {'d32': {'testpid': None}, 'testpid': None, 'd31': {'d311': {'testpid': None}, 'testpid': None}}, 'd1': {'f21': None, 'testpid': None}})

  def test_230_merge_complex_to_complex(self):
    dst = {'f1': None, 'd1': {'d11': {}, 'd12': {'f121': None}}, 'd2': {'d21': {}, 'd22': {'d31': {}}}}
    src = {'d1': {'f11': None}, 'd2': {}, 'd3': {'d31': {'d311': {'f3111': None}}, 'd32': {}}}
    self._resolver._merge_region_trees(dst, src, 'x')
    self.assertEqual(dst, {'f1': None, 'd2': {'d21': {}, 'x': None, 'd22': {'d31': {}}}, 'd3': {'x': None, 'd32': {'x': None}, 'd31': {'x': None, 'd311': {'x': None, 'f3111': {'x': None}}}}, 'd1': {'x': None, 'f11': {'x': None}, 'd11': {}, 'd12': {'f121': None}}})

  def test_240_merge_conflict_1(self):
    dst = {'x1': {}}
    src = {'x1': None}
    self._resolver._merge_region_trees(dst, src, 'x')
    self.assertEqual(dst, {'x1': {'x': None}})

  def test_250_merge_conflict_2(self):
    dst = {'x1': {'x': None}}
    src = {'x1': {'x': {}}}
    self._resolver._merge_region_trees(dst, src, 'x')
    self.assertEqual(dst, {'x1': {'x': {'x': None}}})

  def test_260_merge_build(self):
    dst = {}
    self._resolver._merge_region_trees(dst, {'d1': {}}, 'x')
    self._resolver._merge_region_trees(dst, {'d1': {}}, 'y')
    self.assertEqual(dst, {'d1': {'x': None, 'y': None}})

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
    '--test',
    action='store',
    default='',
    dest='test',
    readme='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestRegionResolver
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
