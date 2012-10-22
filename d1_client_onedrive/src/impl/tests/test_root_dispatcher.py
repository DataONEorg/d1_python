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
''':mod:`test_root_resolver`
============================

:Synopsis:
 - Test the RootResolver class.
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
import solr_query_simulator
import root_dispatcher
import test_resolver


class TestRootDispatcher(unittest.TestCase):
  def setUp(self):
    self.r = root_dispatcher.RootDispatcher(solr_query_simulator.SolrQuerySimulator())
    # Monkey-patch the RootDispatcher.
    self.r.resolvers['TestResolver'] = test_resolver.Resolver()

  def test_100_resolve(self):
    d = self.r.resolve('relative/path')
    self.assertTrue('<non-existing directory>' in [f[0] for f in d])

  def test_110_resolve(self):
    d = self.r.resolve('/absolute/path/invalid')
    self.assertTrue('<non-existing directory>' in [f[0] for f in d])

  def test_120_resolve(self):
    d = self.r.resolve('/')
    self.assertFalse('<non-existing directory>' in [f[0] for f in d])
    self.assertTrue('FacetedSearch' in [f[0] for f in d])
    self.assertTrue('PreconfiguredSearch' in [f[0] for f in d])

  def test_130_resolve(self):
    d = self.r.resolve('/TestResolver')
    self.assertTrue('##/##' in [f[0] for f in d])

  def test_140_resolve(self):
    d = self.r.resolve('/TestResolver/')
    self.assertTrue('##/##' in [f[0] for f in d])

  def _test_150_resolve(self):
    d = self.r.resolve('/TestResolver/abc/def')
    print d
    self.assertTrue('/abc/def' in [f[0] for f in d])

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

  s = TestRootDispatcher
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
