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
"""Module d1_client.tests.data_package.py
=========================================

Unit tests for ResourceMapGenerator and ResourceMapParser.

:Created: 2012-10-25
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

# Stdlib
import unittest

# 3rd party
import rdflib
import foresite

# D1
import d1_common.test_case_with_url_compare
import d1_common.util
import d1_client.data_package

# TODO: Update tests for new OAI-ORE library

# # 3rd party
# import foresite
# import foresite.utils
# import rdflib
# import rdflib.namespace
# import rdflib.term
# import rdflib.plugin
# import rdflib.graph
#
# # App
# sys.path.append(os.pardir)
# import d1_client.data_package
# import util
# import shared_context
#
# rdflib.plugin.register(
#   'sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor'
# )
# rdflib.plugin.register(
#   'sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult'
# )
#
# ALLOWABLE_PACKAGE_SERIALIZATIONS = (
#   'xml', 'pretty-xml', 'n3', 'rdfa', 'json', 'pretty-json', 'turtle', 'nt',
#   'trix'
# )
# RDFXML_FORMATID = 'http://www.openarchives.org/ore/terms'
# CITO_NS = 'http://purl.org/spar/cito/'
# D1_API_RESOLVE_REST_PATH = 'v1/resolve/'


@unittest.skip("TODO: Update tests for new OAI-ORE library")
class TestDataPackage(
    d1_common.test_case_with_url_compare.TestCaseWithURLCompare
):
  def setUp(self):
    # The example_oai_ore.xml contains one resource map that describes one
    # aggregation. The pid for the resource map is "abc". The aggregation
    # doesn't have a a pid. Its subject is "...abc#aggregation". The aggregation
    # lists the aggregated resources, "def", "ghi" and "jkl". Entries for each
    # of the aggregated resources describe their relationships. "def" documents
    # "ghi", and "jkl". The reverse relationship, "isDocumentedBy" is recorded
    # in the "ghi" and "jkl" entries.
    self.ore_doc = open(d1_common.util.abs_path('./expected_oai_ore.xml')).read()
    self.generator = d1_client.data_package.ResourceMapGenerator()
    self.parser = d1_client.data_package.ResourceMapParser(self.ore_doc)

  def test_100(self):
    """init()"""
    pass # Successful setup of the test means that the parser and generator
    # initialized successfully.

    #
    # Generator.
    #

  def test_200(self):
    """simple_generate_resource_map()"""
    doc = self.generator.simple_generate_resource_map(
      'MAP_PID', 'SCIMETA_PID', ['SCIDATA_PID_1', 'SCIDATA_PID_2']
    )
    # There are many possible variations in the resource map that doesn't change
    # the information, so only a few basic checks are performed on the returned
    # map in this test. A more thorough test is performed below, after the
    # parser has been tested.
    self.assertTrue('http://www.openarchives.org/ore/terms/' in doc)
    self.assertTrue('/resolve/SCIDATA_PID' in doc)
    self.assertTrue(
      '<dcterms:identifier>SCIMETA_PID</dcterms:identifier>' in doc
    )

  def test_210(self):
    """generate_system_metadata_for_resource_map()"""
    sys_meta = self.generator.generate_system_metadata_for_resource_map(
      'test_pid', 'test_object', 'rights_holder'
    )
    self.assertEqual(
      sys_meta.checksum.value(), 'fc20ab0360ba35c4e29401c286d995b761a3cfc0'
    )
    self.assertEqual(sys_meta.checksum.algorithm, 'SHA-1')

  #
  # Parser.
  #

  def test_300(self):
    """get_resource_map()"""
    self.assertIsInstance(
      self.parser.get_resource_map(), foresite.ore.ResourceMap
    )

  def test_310(self):
    """get_resource_map_graph()"""
    self.assertIsInstance(
      self.parser.get_resource_map_graph(), rdflib.graph.Graph
    )

  def test_320(self):
    """get_aggregation()"""
    aggr = self.parser.get_aggregation()
    self.assertIsInstance(aggr, foresite.ore.Aggregation)
    self.assertEqual(
      str(aggr), 'https://cn.dataone.org/cn/v1/resolve/abc#aggregation'
    )

  def test_330(self):
    """get_aggregation_graph()"""
    self.assertIsInstance(
      self.parser.get_aggregation_graph(), rdflib.graph.Graph
    )

  def test_340(self):
    """get_resource_map_pid()"""
    self.assertEqual(self.parser.get_resource_map_pid(), 'abc')

  def test_350(self):
    """get_merged_graph()"""
    g = self.parser.get_merged_graph()
    self.assertIsInstance(g, rdflib.graph.Graph)
    self.assertEqual(len(g), 20)

  def test_360(self):
    """get_all_triples()"""
    triples = self.parser.get_all_triples()
    self.check_triples(triples)

  def test_370(self):
    """get_all_predicates()"""
    preds = self.parser.get_all_predicates()
    expected_preds = [
      'http://purl.org/dc/terms/modified',
      'http://www.w3.org/2001/01/rdf-schema#isDefinedBy',
      'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
      'http://purl.org/spar/cito/documents',
      'http://purl.org/dc/elements/1.1/format',
      'http://purl.org/spar/cito/isDocumentedBy',
      'http://www.openarchives.org/ore/terms/describes',
      'http://purl.org/dc/terms/created',
      'http://www.openarchives.org/ore/terms/aggregates',
      'http://purl.org/dc/terms/creator',
      'http://www.w3.org/2001/01/rdf-schema#label',
      'http://purl.org/dc/terms/identifier'
    ]
    for p in preds:
      self.assertTrue(p in expected_preds)

  def test_380(self):
    """get_subject_objects_by_predicate()"""
    subject_objects = self.parser.get_subject_objects_by_predicate(
      'ore:aggregates'
    )
    self.assertEqual(len(subject_objects), 3)

  def test_390(self):
    """get_aggregated_pids()"""
    pids = self.parser.get_aggregated_pids()
    self.assertEqual(len(pids), 3)
    self.assertTrue('def' in pids)
    self.assertTrue('ghi' in pids)
    self.assertTrue('jkl' in pids)

  def test_400(self):
    """get_aggregated_science_metadata_pids()"""
    pids = self.parser.get_aggregated_science_metadata_pids()
    self.assertEqual(len(pids), 1)
    self.assertTrue('def' in pids)

  def test_410(self):
    """get_aggregated_science_data_pids()"""
    pids = self.parser.get_aggregated_science_data_pids()
    self.assertEqual(len(pids), 2)
    self.assertTrue('ghi' in pids)
    self.assertTrue('jkl' in pids)

  def test_420(self):
    """generator_and_parser_1"""
    doc = self.generator.simple_generate_resource_map(
      'abc', 'def', ['ghi', 'jkl']
    )
    p = d1_client.data_package.ResourceMapParser(doc)
    self.check_triples(p.get_all_triples())

  def check_triples(self, doc):
    # for created and modified, only subject and predicate are checked, as the
    # the datetimes are set to the current time.
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/abc',
      'http://www.openarchives.org/ore/terms/describes',
      'https://cn.dataone.org/cn/v1/resolve/abc#aggregation'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/abc',
      'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
      'http://www.openarchives.org/ore/terms/ResourceMap'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/abc',
      'http://purl.org/dc/terms/modified'
    ) in [(d[0], d[1]) for d in doc])
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/abc',
      'http://purl.org/dc/elements/1.1/format', 'application/rdf+xml'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/abc',
      'http://purl.org/dc/terms/identifier', 'abc'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/abc',
      'http://purl.org/dc/terms/creator',
      'http://foresite-toolkit.googlecode.com/#pythonAgent'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/abc',
      'http://purl.org/dc/terms/created'
    ) in [(d[0], d[1]) for d in doc])
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/abc#aggregation',
      'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
      'http://www.openarchives.org/ore/terms/Aggregation'
    ) in doc)
    self.assertTrue((
      'http://www.openarchives.org/ore/terms/Aggregation',
      'http://www.w3.org/2001/01/rdf-schema#isDefinedBy',
      'http://www.openarchives.org/ore/terms/'
    ) in doc)
    self.assertTrue((
      'http://www.openarchives.org/ore/terms/Aggregation',
      'http://www.w3.org/2001/01/rdf-schema#label', 'Aggregation'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/abc#aggregation',
      'http://www.openarchives.org/ore/terms/aggregates',
      'https://cn.dataone.org/cn/v1/resolve/def'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/def',
      'http://purl.org/spar/cito/documents',
      'https://cn.dataone.org/cn/v1/resolve/jkl'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/def',
      'http://purl.org/spar/cito/documents',
      'https://cn.dataone.org/cn/v1/resolve/ghi'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/def',
      'http://purl.org/dc/terms/identifier', 'def'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/abc#aggregation',
      'http://www.openarchives.org/ore/terms/aggregates',
      'https://cn.dataone.org/cn/v1/resolve/jkl'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/jkl',
      'http://purl.org/dc/terms/identifier', 'jkl'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/jkl',
      'http://purl.org/spar/cito/isDocumentedBy',
      'https://cn.dataone.org/cn/v1/resolve/def'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/abc#aggregation',
      'http://www.openarchives.org/ore/terms/aggregates',
      'https://cn.dataone.org/cn/v1/resolve/ghi'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/ghi',
      'http://purl.org/spar/cito/isDocumentedBy',
      'https://cn.dataone.org/cn/v1/resolve/def'
    ) in doc)
    self.assertTrue((
      'https://cn.dataone.org/cn/v1/resolve/ghi',
      'http://purl.org/dc/terms/identifier', 'ghi'
    ) in doc)
