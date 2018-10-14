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

import io as StringIO

import rdflib
import rdflib.compare

import d1_common.resource_map
import d1_common.util

import d1_test.d1_test_case

# d1_pyore Examples
# =================
#
# A. Create an OAI-ORE document from a list of PIDs
# -------------------------------------------------
#
# Given the text file pids.txt::
#
#   # Comment line, separate the # from text with a space.
#   # These are example values for pids2ore
#   # First row = identifier for resource map object
#   # Second row = identifier for metadata document
#   # Subsquent rows = identifiers for data
#   # Blank rows are ignored
#   # White space is stripped from start and end of rows.
#
#   PID_ORE_value
#   sci_meta_pid_value
#   data_pid_1
#   data_pid_2
#   data_pid_3
#
#
# Generate an OAI-ORE document by::
#
#   cat pids.txt | pids2ore
#
#
# The rdf-xml ORE document will be sent to stdout. Different formats (e.g. n3,
# turtle, json-ld) may be specified with the ``--format`` parameter.
#
# RDF-xml output from the above example:
#
# .. code:: xml
#
#   <rdf:RDF xmlns:cito="http://purl.org/spar/cito/"
#   xmlns:dcterms="http://purl.org/dc/terms/"
#   xmlns:ore="http://www.openarchives.org/ore/terms/"
#   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
#   xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" > <rdf:Description
#   rdf:about="https://cn.dataone.org/cn/v2/resolve/sci_meta_pid_value">
#   <ore:isAggregatedBy
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/PID_ORE_value#aggregation"/>
#   <dcterms:identifier>sci_meta_pid_value</dcterms:identifier> <cito:documents
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_3"/>
#   <cito:documents
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_2"/>
#   <cito:documents
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_1"/>
#   </rdf:Description> <rdf:Description
#   rdf:about="https://cn.dataone.org/cn/v2/resolve/PID_ORE_value"> <rdf:type
#   rdf:resource="http://www.openarchives.org/ore/terms/ResourceMap"/>
#   <ore:describes
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/PID_ORE_value#aggregation"/>
#   <dcterms:identifier>PID_ORE_value</dcterms:identifier>
#   <dcterms:creator>d1_pyore DataONE Python library</dcterms:creator>
#   </rdf:Description> <rdf:Description
#   rdf:about="https://cn.dataone.org/cn/v2/resolve/data_pid_1">
#   <dcterms:identifier>data_pid_1</dcterms:identifier> <ore:isAggregatedBy
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/PID_ORE_value#aggregation"/>
#   <cito:isDocumentedBy
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_1"/>
#   </rdf:Description> <rdf:Description
#   rdf:about="https://cn.dataone.org/cn/v2/resolve/PID_ORE_value#aggregation">
#   <ore:aggregates
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_1"/>
#   <ore:aggregates
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_2"/>
#   <ore:aggregates
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/sci_meta_pid_value"/>
#   <ore:aggregates
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_3"/> <rdf:type
#   rdf:resource="http://www.openarchives.org/ore/terms/Aggregation"/>
#   </rdf:Description> <rdf:Description
#   rdf:about="https://cn.dataone.org/cn/v2/resolve/data_pid_3">
#   <dcterms:identifier>data_pid_3</dcterms:identifier> <ore:isAggregatedBy
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/PID_ORE_value#aggregation"/>
#   <cito:isDocumentedBy
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_3"/>
#   </rdf:Description> <rdf:Description
#   rdf:about="https://cn.dataone.org/cn/v2/resolve/data_pid_2">
#   <dcterms:identifier>data_pid_2</dcterms:identifier> <ore:isAggregatedBy
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/PID_ORE_value#aggregation"/>
#   <cito:isDocumentedBy
#   rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_2"/>
#   </rdf:Description> <rdf:Description
#   rdf:about="http://www.openarchives.org/ore/terms/Aggregation">
#   <rdfs:isDefinedBy rdf:resource="http://www.openarchives.org/ore/terms/"/>
#   <rdfs:label>Aggregation</rdfs:label> </rdf:Description> </rdf:RDF>
#
#
# B. Text dump of an OAI-ORE document
# -----------------------------------
#
# Given the rdf-xml OAI-ORE document from above saved as "test.xml", parse and
# dump out the contents in slightly more intelligable plain text::
#
#   ore2txt test.xml
#
#   OAI-ORE Description
#
#   Resource Map Document PID: PID_ORE_value
#                          ID: https://cn.dataone.org/cn/v2/resolve/PID_ORE_value
#
#   Aggregations
#
#   1: https://cn.dataone.org/cn/v2/resolve/PID_ORE_value#aggregation
#      Contents:
#       1:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_1
#          pid: data_pid_1
#       2:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_3
#          pid: data_pid_3
#       3:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_2
#          pid: data_pid_2
#       4:  id: https://cn.dataone.org/cn/v2/resolve/sci_meta_pid_value
#          pid: sci_meta_pid_value
#
#   CITO:documents
#
#   The document:
#   1:  id: https://cn.dataone.org/cn/v2/resolve/sci_meta_pid_value   pid:
#   sci_meta_pid_value
#
#      describes:
#       1:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_1
#          pid: data_pid_1
#       2:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_2
#          pid: data_pid_2
#       3:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_3
#          pid: data_pid_3
#
#   CITO:isDocumentedBy
#
#   The data:
#   1:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_1
#      pid: data_pid_1
#
#      is described by:
#       1:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_1
#          pid: data_pid_1
#
#   The data:
#   2:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_3
#      pid: data_pid_3
#
#      is described by:
#       1:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_3
#          pid: data_pid_3
#
#   The data:
#   3:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_2
#      pid: data_pid_2
#
#      is described by:
#       1:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_2
#          pid: data_pid_2
#
#
# C. Create an ORE programmatically in Python
# -------------------------------------------
#
# .. code:: python
#
#   import d1_pyore
#
#   pkg = d1_pyore.ResourceMap()
#   pkg.oreInitialize("pid_for_ore")
#   pkg.addMetadataDocument("pid_for_metadata")
#   pkg.addDataDocuments(["data_pid_1", "data_pid_2"], "pid_for_metadata")
#   print pkg.serialize_to_display(format="json-ld", indent=2)
#
#
# .. code:: json
#
#   [
#     {
#       "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_1",
#       "http://purl.org/dc/terms/identifier": [
#         {
#           "@value": "data_pid_1"
#         }
#       ],
#       "http://purl.org/spar/cito/isDocumentedBy": [
#         {
#           "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_1"
#         }
#       ]
#     },
#     {
#       "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_2",
#       "http://purl.org/dc/terms/identifier": [
#         {
#           "@value": "data_pid_2"
#         }
#       ],
#       "http://purl.org/spar/cito/isDocumentedBy": [
#         {
#           "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_2"
#         }
#       ]
#     },
#     {
#       "@id": "https://cn.dataone.org/cn/v2/resolve/pid_for_metadata",
#       "http://purl.org/dc/terms/identifier": [
#         {
#           "@value": "pid_for_metadata"
#         }
#       ],
#       "http://purl.org/spar/cito/documents": [
#         {
#           "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_2"
#         },
#         {
#           "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_1"
#         }
#       ]
#     },
#     {
#       "@id": "https://cn.dataone.org/cn/v2/resolve/pid_for_ore",
#       "@type": [
#         "http://www.openarchives.org/ore/terms/ResourceMap"
#       ],
#       "http://purl.org/dc/terms/creator": [
#         {
#           "@value": "d1_pyore DataONE Python library"
#         }
#       ],
#       "http://purl.org/dc/terms/identifier": [
#         {
#           "@value": "pid_for_ore"
#         }
#       ],
#       "http://www.openarchives.org/ore/terms/describes": [
#         {
#           "@id": "https://cn.dataone.org/cn/v2/resolve/pid_for_ore#aggregation"
#         }
#       ]
#     },
#     {
#       "@id": "http://www.openarchives.org/ore/terms/Aggregation",
#       "http://www.w3.org/2000/01/rdf-schema#isDefinedBy": [
#         {
#           "@id": "http://www.openarchives.org/ore/terms/"
#         }
#       ],
#       "http://www.w3.org/2000/01/rdf-schema#label": [
#         {
#           "@value": "Aggregation"
#         }
#       ]
#     },
#     {
#       "@id": "https://cn.dataone.org/cn/v2/resolve/pid_for_ore#aggregation",
#       "@type": [
#         "http://www.openarchives.org/ore/terms/Aggregation"
#       ],
#       "http://www.openarchives.org/ore/terms/aggregates": [
#         {
#           "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_2"
#         },
#         {
#           "@id": "https://cn.dataone.org/cn/v2/resolve/pid_for_metadata"
#         },
#         {
#           "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_1"
#         }
#       ]
#     }
#   ]
#


class TestResourceMap(d1_test.d1_test_case.D1TestCase):
  # def _norm_nt(self, nt_str):
  #   return sorted([sorted(v.split(' ')) for v in nt_str.split('\n')])

  # def _normalize_n_triples(self, nt_str):
  #   return '\n'.join(sorted(nt_str.splitlines()))

  # def _norm_triples(self, triple_list):
  #   return sorted([sorted(v) for v in triple_list])

  # def _norm_to_str(self, nt_str):
  #   return pprint.pformat(self._norm_nt(nt_str))

  # def _assert_are_equal_nt(self, a_nt, b_nt):
  #   assert self._norm_nt(a_nt) == self._norm_nt(b_nt)

  def _create(self):
    return d1_common.resource_map.ResourceMap(
      'ore_pid', 'meta_pid', ['data_pid', 'data2_pid', 'data3_pid'], debug=False
    )

  def _sort_obj(self, obj):
    if isinstance(obj, dict):
      return self._sort_obj(list(obj.items()))
    elif isinstance(obj, list):
      return sorted(obj)
    return obj

  def test_1000(self, mn_client_v2):
    """__init__(): Empty"""
    ore = d1_common.resource_map.ResourceMap()
    assert isinstance(ore, d1_common.resource_map.ResourceMap)

  def test_1010(self, mn_client_v2):
    """__init__(): Instantiate resource map by ORE PID"""
    ore = d1_common.resource_map.ResourceMap('test_pid', ore_software_id='TEST')
    self.sample.assert_equals(ore, 'init', mn_client_v2)

  def test_1020(self, mn_client_v2):
    """serialize_to_display(): Instantiate resource map by pid, scimeta and scidata"""
    ore = self._create()
    self.sample.assert_equals(ore, 'serialize', mn_client_v2)

  def test_1030(self, mn_client_v2):
    """getAggregation()"""
    ore = self._create()
    aggr = ore.getAggregation()
    assert isinstance(aggr, rdflib.URIRef)
    assert str(
      aggr
    ) == 'https://cn.dataone.org/cn/v2/resolve/ore_pid/aggregation'

  def test_1040(self, mn_client_v2):
    """getObjectByPid()"""
    ore = self._create()
    u = ore.getObjectByPid('ore_pid')
    assert isinstance(u, rdflib.URIRef)
    assert str(u) == 'https://cn.dataone.org/cn/v2/resolve/ore_pid'

  def test_1050(self, mn_client_v2):
    """addResource()"""
    ore = self._create()
    ore.addResource('resource1_pid')
    self.sample.assert_equals(ore, 'add_resource', mn_client_v2)

  def test_1060(self, mn_client_v2):
    """setDocuments()"""
    ore = self._create()
    ore.addResource('resource1_pid')
    ore.addResource('resource2_pid')
    ore.setDocuments('resource1_pid', 'resource2_pid')
    self.sample.assert_equals(ore, 'set_documents', mn_client_v2)

  def test_1070(self, mn_client_v2):
    """setDocumentedBy()"""
    ore = self._create()
    ore.addResource('resource1_pid')
    ore.addResource('resource2_pid')
    ore.setDocuments('resource1_pid', 'resource2_pid')
    self.sample.assert_equals(ore, 'set_documented_by', mn_client_v2)

  def test_1080(self, mn_client_v2):
    """addMetadataDocument()"""
    ore = self._create()
    ore.addMetadataDocument('meta_pid')
    self.sample.assert_equals(ore, 'add_metadata_document_by', mn_client_v2)

  def test_1090(self, mn_client_v2):
    """addDataDocuments()"""
    ore = self._create()
    ore.addDataDocuments(['more_data1_pid', 'more_data2_pid'], 'meta_pid')
    self.sample.assert_equals(ore, 'add_data_documents_by', mn_client_v2)

  def test_1100(self, mn_client_v2):
    """getResourceMapPid()"""
    ore = self._create()
    resource_map_pid = ore.getResourceMapPid()
    assert isinstance(resource_map_pid, str)
    assert resource_map_pid == 'ore_pid'

  def test_1110(self, mn_client_v2):
    """getAllTriples()"""
    ore = self._create()
    triple_list = ore.getAllTriples()
    sorted_triple_list = self._sort_obj(triple_list)
    self.sample.assert_equals(
      sorted_triple_list, 'get_all_triples', mn_client_v2
    )

  def test_1120(self, mn_client_v2):
    """getAllPredicates()"""
    ore = self._create()
    predicate_list = ore.getAllPredicates()
    sorted_predicate_list = self._sort_obj(predicate_list)
    self.sample.assert_equals(
      sorted_predicate_list, 'get_all_predicates', mn_client_v2
    )

  def test_1130(self, mn_client_v2):
    """getSubjectObjectsByPredicate()"""
    ore = self._create()
    subobj_list = ore.getSubjectObjectsByPredicate(
      'http://www.openarchives.org/ore/terms/isAggregatedBy'
    )
    sorted_subobj_list = self._sort_obj(subobj_list)
    self.sample.assert_equals(
      sorted_subobj_list, 'get_subject_objects_by_predicate', mn_client_v2
    )

  def test_1140(self, mn_client_v2):
    """getAggregatedPids()"""
    ore = self._create()
    pid_list = ore.getAggregatedPids()
    sorted_pid_list = self._sort_obj(pid_list)
    self.sample.assert_equals(
      sorted_pid_list, 'get_aggregated_pids', mn_client_v2
    )

  def test_1150(self, mn_client_v2):
    """getAggregatedScienceMetadataPids()"""
    ore = self._create()
    pid_list = ore.getAggregatedScienceMetadataPids()
    sorted_pid_list = self._sort_obj(pid_list)
    self.sample.assert_equals(
      sorted_pid_list, 'get_aggregated_science_metadata_pids', mn_client_v2
    )

  def test_1160(self, mn_client_v2):
    """getAggregatedScienceDataPids()"""
    ore = self._create()
    pid_list = ore.getAggregatedScienceDataPids()
    sorted_pid_list = self._sort_obj(pid_list)
    self.sample.assert_equals(
      sorted_pid_list, 'get_aggregated_science_data_pids', mn_client_v2
    )

  def test_1170(self, mn_client_v2):
    """asGraphvizDot()"""
    ore = self._create()
    stream = StringIO.StringIO()
    ore.asGraphvizDot(stream)
    self.sample.assert_equals(
      stream.getvalue(), 'as_graphviz_dot', mn_client_v2
    )
