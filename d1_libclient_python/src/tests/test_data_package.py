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
'''Module d1_client.tests.data_package.py
=========================================

Unit tests for ResourceMapGenerator and ResourceMapParser.

:Created: 2012-10-25
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import os
import sys
import unittest

# D1.
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare

# App.
import d1_client.data_package
import testing_utilities
import testing_context


# Create absolute path from path that is relative to the module from which
# the function is called.
def make_absolute(p):
  return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)


class TestDataPackage(TestCaseWithURLCompare):
  def setUp(self):
    self.ore_doc = open(make_absolute('./d1_testdocs/oai_ore.xml')).read()
    self.generator = d1_client.data_package.ResourceMapGenerator()
    self.parser = d1_client.data_package.ResourceMapParser(self.ore_doc)

  def test_050(self):
    '''simple_generate_resource_map()'''
    doc = self.generator.simple_generate_resource_map(
      'MAP_PID', 'SCIMETA_PID', [
        'SCIDATA_PID_1', 'SCIDATA_PID_2'
      ]
    )
    # There are many possible variations in the resource map that doesn't change
    # the information, so only a few basic checks are performed on the returned
    # map in this test. A more thorough test is performed below, after the
    # parser has been tested.
    self.assertTrue('http://www.openarchives.org/ore/terms/' in doc)
    self.assertTrue('/resolve/SCIDATA_PID' in doc)
    self.assertTrue('<dcterms:identifier>SCIMETA_PID</dcterms:identifier>' in doc)

  def test_100(self):
    '''init()'''
    pass # Successful setup of the test means that the parser and generator
    # initialized successfully.

  def test_110(self):
    '''get_graphs()'''
    graph = self.parser.get_graphs()
    self.assertEqual(len(graph), 7)

  def test_120(self):
    '''get_aggregation()'''
    aggr = self.parser.get_aggregation()
    self.assertEqual(str(aggr), 'abc')

  def test_130(self):
    pid = self.parser.get_resource_map_pid()
    self.assertEqual(pid, 'https://cn.dataone.org/cn/resolve/abc')

  def test_140(self):
    '''get_all_triples()'''
    triples = self.parser.get_all_triples()
    self.check_triples(triples)

  def test_150(self):
    '''get_all_predicates()'''
    preds = self.parser.get_all_predicates()
    expected_preds = [
      'http://www.openarchives.org/ore/terms/aggregates',
      'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
      'http://www.w3.org/2001/01/rdf-schema#isDefinedBy',
      'http://www.w3.org/2001/01/rdf-schema#label',
      'http://purl.org/spar/cito/isDocumentedBy',
      'http://purl.org/dc/terms/identifier',
      'http://purl.org/spar/cito/documents',
    ]
    for p in preds:
      self.assertTrue(p in expected_preds)

  def test_160(self):
    '''get_identifiers_referenced_by_package()'''
    pids = self.parser.get_identifiers_referenced_by_package()
    self.assertEqual(len(pids), 3)
    self.assertTrue('def' in pids)
    self.assertTrue('ghi' in pids)
    self.assertTrue('jkl' in pids)

  def test_170(self):
    '''get_sci_meta_pids()'''
    pids = self.parser.get_sci_meta_pids()
    self.assertTrue('https://cn.dataone.org/cn/object/def' in pids)

  def test_180(self):
    '''get_sci_data_pids()'''
    pids = self.parser.get_sci_data_pids()
    self.assertTrue('https://cn.dataone.org/cn/object/ghi' in pids)
    self.assertTrue('https://cn.dataone.org/cn/object/jkl' in pids)

  def test_200(self):
    '''generator_and_parser_1'''
    # TODO: Ticket #4108.
    doc = self.generator.simple_generate_resource_map('abc', 'def', ['ghi', 'jkl'])
    #doc = open(make_absolute('./d1_testdocs/oai_ore.xml')).read()
    #print doc
    #return
    p = d1_client.data_package.ResourceMapParser(doc)
    triples = p.get_all_triples()
    #print triples

  def check_triples(self, doc):
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/object/ghi',
        'http://purl.org/spar/cito/isDocumentedBy', 'https://cn.dataone.org/cn/object/def'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/object/ghi', 'http://purl.org/dc/terms/identifier',
        'ghi'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/object/jkl', 'http://purl.org/dc/terms/identifier',
        'jkl'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/object/jkl',
        'http://purl.org/spar/cito/isDocumentedBy', 'https://cn.dataone.org/cn/object/def'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/object/def', 'http://purl.org/dc/terms/identifier',
        'def'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/object/def', 'http://purl.org/spar/cito/documents',
        'https://cn.dataone.org/cn/object/ghi'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/object/def', 'http://purl.org/spar/cito/documents',
        'https://cn.dataone.org/cn/object/jkl'
      ) in doc
    )

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

  s = TestDataPackage
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
