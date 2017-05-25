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

import json
import pprint
import unittest
import cStringIO as StringIO
import logging

import rdflib
import rdflib.compare

import d1_common.resource_map
import d1_common.util
import d1_test.util


class TestResourceMap(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.maxDiff = None

  def _norm_nt(self, nt_str):
    return sorted([sorted(v.split(' ')) for v in nt_str.split('\n')])

  def _norm_triples(self, triple_list):
    return sorted([sorted(v) for v in triple_list])

  def _norm_to_str(self, nt_str):
    return pprint.pformat(self._norm_nt(nt_str))

  def _assert_is_equal_nt(self, a_nt, b_nt):
    self.assertListEqual(self._norm_nt(a_nt), self._norm_nt(b_nt))

  def _create(self):
    return d1_common.resource_map.ResourceMap(
      'ore_pid', 'meta_pid', ['data_pid', 'data2_pid', 'data3_pid'], debug=False
    )

  def _check_nt(self, ore, filename):
    ore_nt = ore.serialize(doc_format='nt')
    if not d1_test.util.is_existing_file(filename):
      d1_test.util.write_test_file(filename, ore_nt)
      logging.warning(u'Wrote new test file: {}'.format(filename))
    expected_ore_nt = d1_test.util.read_test_file(filename)
    self._assert_is_equal_nt(ore_nt, expected_ore_nt)

  def _check_obj(self, obj, filename):
    got_json = json.dumps(obj, indent=2, sort_keys=True)
    if not d1_test.util.is_existing_file(filename):
      d1_test.util.write_test_file(filename, got_json)
      logging.warning(u'Wrote new test file: {}'.format(filename))
    expected_json = d1_test.util.read_test_file(filename)
    self.assertEquals(got_json, expected_json)

  def _sort_obj(self, obj):
    if isinstance(obj, dict):
      return self._sort_obj(obj.items())
    elif isinstance(obj, list):
      return sorted(obj)
    return obj

  def test_0010(self):
    """init(): Instantiate empty resource map
    """
    ore = d1_common.resource_map.ResourceMap()
    self.assertIsInstance(ore, d1_common.resource_map.ResourceMap)

  def test_0020(self):
    """init(): Instantiate resource map by ORE PID"""
    ore = d1_common.resource_map.ResourceMap('test_pid', ore_software_id='TEST')
    self._check_nt(ore, 'resource_map_pid.result')

  def test_0030(self):
    """serialize(): Instantiate resource map by pid, scimeta and scidata"""
    ore = self._create()
    self._check_nt(ore, 'resource_map_full.result')

  def test_0040(self):
    """getAggregation()"""
    ore = self._create()
    aggr = ore.getAggregation()
    self.assertIsInstance(aggr, rdflib.URIRef)
    self.assertEqual(
      str(aggr), 'https://cn.dataone.org/cn/v2/resolve/ore_pid/aggregation'
    )

  def test_0050(self):
    """getObjectByPid()"""
    ore = self._create()
    u = ore.getObjectByPid('ore_pid')
    self.assertIsInstance(u, rdflib.URIRef)
    self.assertEqual(str(u), 'https://cn.dataone.org/cn/v2/resolve/ore_pid')

  def test_0060(self):
    """addResource()"""
    ore = self._create()
    ore.addResource('resource1_pid')
    self._check_nt(ore, 'resource_map_add_resource.result')

  def test_0070(self):
    """setDocuments()"""
    ore = self._create()
    ore.addResource('resource1_pid')
    ore.addResource('resource2_pid')
    ore.setDocuments('resource1_pid', 'resource2_pid')
    self._check_nt(ore, 'resource_map_set_documents.result')

  def test_0080(self):
    """setDocumentedBy()"""
    ore = self._create()
    ore.addResource('resource1_pid')
    ore.addResource('resource2_pid')
    ore.setDocuments('resource1_pid', 'resource2_pid')
    self._check_nt(ore, 'resource_map_set_documented_by.result')

  def test_0090(self):
    """addMetadataDocument()"""
    ore = self._create()
    ore.addMetadataDocument('meta_pid')
    self._check_nt(ore, 'resource_map_add_metadata_document_by.result')

  def test_0100(self):
    """addDataDocuments()"""
    ore = self._create()
    ore.addDataDocuments(['more_data1_pid', 'more_data2_pid'], 'meta_pid')
    self._check_nt(ore, 'resource_map_add_data_documents_by.result')

  def test_0110(self):
    """getResourceMapPid()"""
    ore = self._create()
    resource_map_pid = ore.getResourceMapPid()
    self.assertIsInstance(resource_map_pid, str)
    self.assertEquals(resource_map_pid, 'ore_pid')

  def test_0120(self):
    """getAllTriples()"""
    ore = self._create()
    triple_list = ore.getAllTriples()
    sorted_triple_list = self._sort_obj(triple_list)
    self._check_obj(sorted_triple_list, 'resource_map_get_all_triples.result')

  def test_0130(self):
    """getAllPredicates()"""
    ore = self._create()
    predicate_list = ore.getAllPredicates()
    sorted_predicate_list = self._sort_obj(predicate_list)
    self._check_obj(
      sorted_predicate_list, 'resource_map_get_all_predicates.result'
    )

  def test_0140(self):
    """getSubjectObjectsByPredicate()"""
    ore = self._create()
    subobj_list = ore.getSubjectObjectsByPredicate(
      'http://www.openarchives.org/ore/terms/isAggregatedBy'
    )
    sorted_subobj_list = self._sort_obj(subobj_list)
    self._check_obj(
      sorted_subobj_list, 'resource_map_get_subject_objects_by_predicate.result'
    )

  def test_0150(self):
    """getAggregatedPids()"""
    ore = self._create()
    pid_list = ore.getAggregatedPids()
    sorted_pid_list = self._sort_obj(pid_list)
    self._check_obj(sorted_pid_list, 'resource_map_get_aggregated_pids.result')

  def test_0160(self):
    """getAggregatedScienceMetadataPids()"""
    ore = self._create()
    pid_list = ore.getAggregatedScienceMetadataPids()
    sorted_pid_list = self._sort_obj(pid_list)
    self._check_obj(
      sorted_pid_list,
      'resource_map_get_aggregated_science_metadata_pids.result'
    )

  def test_0170(self):
    """getAggregatedScienceDataPids()"""
    ore = self._create()
    pid_list = ore.getAggregatedScienceDataPids()
    sorted_pid_list = self._sort_obj(pid_list)
    self._check_obj(
      sorted_pid_list, 'resource_map_get_aggregated_science_data_pids.result'
    )

  def test_0180(self):
    """asGraphvizDot()"""
    ore = self._create()
    stream = StringIO.StringIO()
    ore.asGraphvizDot(stream)
    self.assertIn('node0 -> node1', stream.getvalue())
