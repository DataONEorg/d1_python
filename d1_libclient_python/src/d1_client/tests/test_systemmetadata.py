#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2014 DataONE
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
'''Module d1_client.tests.systemmetadata.py
===========================================

Unit tests for SystemMetadata

:Created: 2012-10-25
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import sys
import unittest

# D1.
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare

# App.
sys.path.append('..')
import d1_client.systemmetadata
import testing_utilities
import testing_context


class TestSystemMetadata(TestCaseWithURLCompare):
  def setUp(self):
    self.sysmeta_doc = open(
      './d1_testdocs/BAYXXX_015ADCP015R00_20051215.50.9_SYSMETA.xml'
    ).read(
    )
    self.sysmeta = d1_client.systemmetadata.SystemMetadata(self.sysmeta_doc)

  def test_100_init(self):
    pass # Successful setup of the test means that the SystemMetadata object
    # initialized successfully.

  def test_200(self):
    self.assertEqual(self.sysmeta.pid, 'BAYXXX_015ADCP015R00_20051215.50.9')

  def test_210(self):
    self.assertEqual(self.sysmeta.objectFormat, None)

  def test_220(self):
    self.assertEqual(self.sysmeta.size, 34543)

  #  doc = self.generator.simple_generate_resource_map('abc', 'def', ['ghi', 'jkl'])
  #  # There are many possible variations in the resource map that doesn't change
  #  # the information, so only a few basic checks are performed on the returned
  #  # map in this test. A thorough test is performed below, after the parser
  #  # has been tested.
  #  self.assertTrue('http://www.openarchives.org/ore/terms/' in doc)
  #  self.assertTrue('https://cn.dataone.org/cn/object/ghi' in doc)
  #  self.assertTrue('<dcterms:identifier>def</dcterms:identifier>' in doc)
  #  self.assertTrue('<ore:describes rdf:resource="abc"/>' in doc)
  #
  #
  #def test_300_parser(self):
  #  doc = self.parser.get_identifiers_referenced_by_package(self.ore_doc)
  #  self.assertTrue('ghi' in doc)
  #  self.assertTrue('jkl' in doc)
  #  self.assertTrue('def' in doc)
  #
  #
  #def test_310_parser(self):
  #  doc = self.parser.get_triples_by_package(self.ore_doc)
  #  self.check_triples(doc)
  #
  #
  #def test_400_generator_and_parser_1(self):
  #  doc = self.generator.simple_generate_resource_map('abc', 'def', ['ghi', 'jkl'])
  #  triples = self.parser.get_triples_by_package(doc)
  #  self.check_triples(triples)
  #
  #
  #def check_triples(self, doc):
  #  self.assertTrue(('https://cn.dataone.org/cn/object/ghi', 'http://purl.org/spar/cito/isDocumentedBy', 'https://cn.dataone.org/cn/object/def') in doc)
  #  self.assertTrue(('https://cn.dataone.org/cn/object/ghi', 'http://purl.org/dc/terms/identifier', 'ghi') in doc)
  #  self.assertTrue(('https://cn.dataone.org/cn/object/jkl', 'http://purl.org/dc/terms/identifier', 'jkl') in doc)
  #  self.assertTrue(('https://cn.dataone.org/cn/object/jkl', 'http://purl.org/spar/cito/isDocumentedBy', 'https://cn.dataone.org/cn/object/def') in doc)
  #  self.assertTrue(('https://cn.dataone.org/cn/object/def', 'http://purl.org/dc/terms/identifier', 'def') in doc)
  #  self.assertTrue(('https://cn.dataone.org/cn/object/def', 'http://purl.org/spar/cito/documents', 'https://cn.dataone.org/cn/object/ghi') in doc)
  #  self.assertTrue(('https://cn.dataone.org/cn/object/def', 'http://purl.org/spar/cito/documents', 'https://cn.dataone.org/cn/object/jkl') in doc)
  #

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

  s = TestSystemMetadata
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
