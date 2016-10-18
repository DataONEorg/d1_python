#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
''':mod:`test_root`
============================

:Synopsis:
 - Test the RootResolver class.
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
sys.path.append('../..')
import command_echoer
import impl.resolver.root as root
import command_echoer
from object_tree_test_sample import object_tree

options = {}


class O():
  pass


class TestRootResolver(unittest.TestCase):
  def setUp(self):
    options = O()
    options.base_url = 'https://localhost/'
    options.object_tree_xml = './test_object_tree.xml'
    options.max_error_path_cache_size = 1000
    options.max_solr_query_cache_size = 1000
    options.region_tree_max_cache_items = 1000
    options.region_tree_cache_path = './region_tree_cache'
    options.ignore_special = []
    self._r = root.RootResolver(options, object_tree)

  def test_050_instantiate(self):
    pass

  # To enable these tests, the test object_tree class must be expanded to match
  # a real one more closely.

  #def test_100_get_directory(self):
  #  d = self._r.get_directory('relative/path')
  #  self._assertTrue('<non-existing directory>' in [f[0] for f in d])
  #
  #
  #def test_110_resolve(self):
  #  d = self._r.get_directory('/absolute/path/invalid')
  #  self._assertTrue('<non-existing directory>' in [f[0] for f in d])
  #
  #
  #def test_120_resolve(self):
  #  d = self._r.get_directory('/')
  #  self._assertFalse('<non-existing directory>' in [f[0] for f in d])
  #  self._assertTrue('FacetedSearch' in [f[0] for f in d])
  #  self._assertTrue('PreconfiguredSearch' in [f[0] for f in d])
  #
  #
  #def test_130_resolve(self):
  #  d = self._r.get_directory('/TestResolver')
  #  self._assertTrue('##/##' in [f[0] for f in d])
  #
  #
  #def test_140_resolve(self):
  #  d = self._r.get_directory('/TestResolver/')
  #  self._assertTrue('##/##' in [f[0] for f in d])
  #
  #
  #def _test_150_resolve(self):
  #  d = self._r.get_directory('/TestResolver/abc/def')
  #  self._assertTrue('/abc/def' in [f[0] for f in d])

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

  s = TestRootResolver
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
