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

# 3rd party.
import foresite
import foresite.ore
import rdflib

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
    # The oai_ore.xml contains one resource map that describes one aggregation.
    # The pid for the resource map is "abc". The aggregation doesn't have a
    # a pid. Its subject is "...abc#aggregation". The aggregation lists the
    # aggregated resources, "def", "ghi" and "jkl". Entries for each of the
    # aggregated resources describe their relationships. "def" documents "ghi",
    # and "jkl". The reverse relationship, "isDocumentedBy" is recorded in
    # the "ghi" and "jkl" entries.
    self.ore_doc = open(make_absolute('./d1_testdocs/oai_ore.xml')).read()
    self.generator = d1_client.data_package.ResourceMapGenerator()
    self.parser = d1_client.data_package.ResourceMapParser(self.ore_doc)

  def test_100(self):
    '''simple_generate_resource_map()'''
    doc = self.generator.simple_generate_resource_map(
      'MAP_PID', 'SCIMETA_PID', ['SCIDATA_PID_1', 'SCIDATA_PID_2']
    )
    # There are many possible variations in the resource map that doesn't change
    # the information, so only a few basic checks are performed on the returned
    # map in this test. A more thorough test is performed below, after the
    # parser has been tested.
    self.assertTrue('http://www.openarchives.org/ore/terms/' in doc)
    self.assertTrue('/resolve/SCIDATA_PID' in doc)
    self.assertTrue('<dcterms:identifier>SCIMETA_PID</dcterms:identifier>' in doc)

  def test_110(self):
    '''init()'''
    pass # Successful setup of the test means that the parser and generator
    # initialized successfully.

  def test_120(self):
    '''get_resource_map()'''
    self.assertTrue(isinstance(self.parser.get_resource_map(), foresite.ore.ResourceMap))

  def test_130(self):
    '''get_resource_map_graph()'''
    self.assertTrue(isinstance(self.parser.get_resource_map_graph(), rdflib.graph.Graph))

  def test_140(self):
    '''get_aggregation()'''
    aggr = self.parser.get_aggregation()
    self.assertTrue(isinstance(aggr, foresite.ore.Aggregation))
    self.assertEqual(str(aggr), 'https://cn.dataone.org/cn/v1/resolve/abc#aggregation')

  def test_150(self):
    '''get_aggregation_graph()'''
    self.assertTrue(isinstance(self.parser.get_aggregation_graph(), rdflib.graph.Graph))

  def test_160(self):
    '''get_resource_map_pid()'''
    self.assertEqual(self.parser.get_resource_map_pid(), 'abc')

  def test_170(self):
    '''get_merged_graph()'''
    g = self.parser.get_merged_graph()
    self.assertTrue(isinstance(g, rdflib.graph.Graph))
    self.assertEqual(len(g), 20)

  def test_180(self):
    '''get_all_triples()'''
    triples = self.parser.get_all_triples()
    self.check_triples(triples)

  def test_190(self):
    '''get_all_predicates()'''
    preds = self.parser.get_all_predicates()
    expected_preds = [
      'http://purl.org/dc/terms/modified',
      'http://www.w3.org/2001/01/rdf-schema#isDefinedBy',
      'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
      'http://purl.org/spar/cito/documents', 'http://purl.org/dc/elements/1.1/format',
      'http://purl.org/spar/cito/isDocumentedBy',
      'http://www.openarchives.org/ore/terms/describes',
      'http://purl.org/dc/terms/created',
      'http://www.openarchives.org/ore/terms/aggregates',
      'http://purl.org/dc/terms/creator', 'http://www.w3.org/2001/01/rdf-schema#label',
      'http://purl.org/dc/terms/identifier'
    ]
    for p in preds:
      self.assertTrue(p in expected_preds)

  def test_195(self):
    '''get_subject_objects_by_predicate()'''
    subject_objects = self.parser.get_subject_objects_by_predicate('ore:aggregates')
    self.assertEqual(len(subject_objects), 3)

  def test_200(self):
    '''get_aggregated_pids()'''
    pids = self.parser.get_aggregated_pids()
    self.assertEqual(len(pids), 3)
    self.assertTrue('def' in pids)
    self.assertTrue('ghi' in pids)
    self.assertTrue('jkl' in pids)

  def test_210(self):
    '''get_aggregated_science_metadata_pids()'''
    pids = self.parser.get_aggregated_science_metadata_pids()
    self.assertEqual(len(pids), 1)
    self.assertTrue('def' in pids)

  def test_220(self):
    '''get_aggregated_science_data_pids()'''
    pids = self.parser.get_aggregated_science_data_pids()
    self.assertEqual(len(pids), 2)
    self.assertTrue('ghi' in pids)
    self.assertTrue('jkl' in pids)

  def test_230(self):
    '''generator_and_parser_1'''
    doc = self.generator.simple_generate_resource_map('abc', 'def', ['ghi', 'jkl'])
    p = d1_client.data_package.ResourceMapParser(doc)
    self.check_triples(p.get_all_triples())

  def check_triples(self, doc):
    # for created and modified, only subject and predicate are checked, as the
    # the datetimes are set to the current time.
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/abc',
        'http://www.openarchives.org/ore/terms/describes',
        'https://cn.dataone.org/cn/v1/resolve/abc#aggregation'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/abc',
        'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
        'http://www.openarchives.org/ore/terms/ResourceMap'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/abc', 'http://purl.org/dc/terms/modified'
      ) in [
        (
          d[0], d[1]
        ) for d in doc
      ]
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/abc',
        'http://purl.org/dc/elements/1.1/format', 'application/rdf+xml'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/abc', 'http://purl.org/dc/terms/identifier',
        'abc'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/abc', 'http://purl.org/dc/terms/creator',
        'http://foresite-toolkit.googlecode.com/#pythonAgent'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/abc', 'http://purl.org/dc/terms/created'
      ) in [
        (
          d[0], d[1]
        ) for d in doc
      ]
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/abc#aggregation',
        'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
        'http://www.openarchives.org/ore/terms/Aggregation'
      ) in doc
    )
    self.assertTrue(
      (
        'http://www.openarchives.org/ore/terms/Aggregation',
        'http://www.w3.org/2001/01/rdf-schema#isDefinedBy',
        'http://www.openarchives.org/ore/terms/'
      ) in doc
    )
    self.assertTrue(
      (
        'http://www.openarchives.org/ore/terms/Aggregation',
        'http://www.w3.org/2001/01/rdf-schema#label', 'Aggregation'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/abc#aggregation',
        'http://www.openarchives.org/ore/terms/aggregates',
        'https://cn.dataone.org/cn/v1/resolve/def'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/def', 'http://purl.org/spar/cito/documents',
        'https://cn.dataone.org/cn/v1/resolve/jkl'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/def', 'http://purl.org/spar/cito/documents',
        'https://cn.dataone.org/cn/v1/resolve/ghi'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/def', 'http://purl.org/dc/terms/identifier',
        'def'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/abc#aggregation',
        'http://www.openarchives.org/ore/terms/aggregates',
        'https://cn.dataone.org/cn/v1/resolve/jkl'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/jkl', 'http://purl.org/dc/terms/identifier',
        'jkl'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/jkl',
        'http://purl.org/spar/cito/isDocumentedBy',
        'https://cn.dataone.org/cn/v1/resolve/def'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/abc#aggregation',
        'http://www.openarchives.org/ore/terms/aggregates',
        'https://cn.dataone.org/cn/v1/resolve/ghi'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/ghi',
        'http://purl.org/spar/cito/isDocumentedBy',
        'https://cn.dataone.org/cn/v1/resolve/def'
      ) in doc
    )
    self.assertTrue(
      (
        'https://cn.dataone.org/cn/v1/resolve/ghi', 'http://purl.org/dc/terms/identifier',
        'ghi'
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
