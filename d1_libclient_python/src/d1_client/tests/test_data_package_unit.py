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
'''Module d1_client.tests.test_mnclient
=======================================

:Synopsis: Unit tests for mnclient.
:Created: 2011-01-20
:Author: DataONE (Flynn)
'''

# TODO: Update tests for new OAI-ORE library

# # Stdlib.
# import os
# import sys
# import mock
#
# # 3rd party.
# import foresite
# import foresite.ore
# import rdflib
#
# # App.
# sys.path.append(os.pardir)
#
# # D1.
# import d1_common.testcasewithurlcompare
# import d1_common.types.exceptions
# import d1_common.types.dataoneTypes as dataoneTypes
# import d1_test.instance_generator.accesspolicy
# import d1_test.instance_generator.identifier
# import d1_test.instance_generator.person
# import d1_test.instance_generator.random_data
# import d1_test.instance_generator.replicationpolicy
# import d1_test.instance_generator.subject
# import d1_test.instance_generator.systemmetadata
#
# # App.
# import d1_client.data_package as data_package
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
#
#
# class foresite(object):
#   def __init__(self, doc=None):
#     self.AggregatedResource = 'update'
#     self._dcterms = _dcterms()
#     self._cito = _cito()
#     self.RdfLibParser = RdfLibParser(doc)
#     self.parse = parse(doc)
#
#   def add_resource(self, meta_res):
#     return
#
#   def set_aggregation(self, aggr):
#     return 'sysmeta'
#
#   def ReMDocument(self, fdata, rdf_xml_doc):
#     self.format = 'xml'
#
#
# class RdfLibParser(foresite):
#   def __init__(self, foresite_doc):
#     super(RdfLibParser, self).__init__()
#     return
#
#
# class parse(foresite):
#   def __init__(self, foresite_doc):
#     super(parse, self).__init__()
#     return
#
#
# class _dcterms(foresite):
#   def __init__(self):
#     super(_dcterms, self).__init__()
#     self.identifier = 'id'
#
#
# class _cito(foresite):
#   def __init__(self):
#     super(_cito, self).__init__()
#     self.isDocumentedBy = 'docBy'
#     self.documents = 'docs'
#
#
# class resourcemap(object):
#   def __init__(self):
#     # type: () -> object
#     pass
#
#   def register_serialization(self, arg):
#     pass
#
#   def get_serialization(self, arg):
#     self.data = data()
#
#
# class data():
#   def __init__(self):
#     self.data = 'test_data'
#
#
# class sysmeta():
#   def __init__(self, pid, format_id, size, rights_holder, checksum, modified):
#     self.identifier = pid
#     self.formatId = format_id
#     self.size = size
#     self.rightsHolder = rights_holder
#     self.checksum = checksum
#     self.dateUploaded = modified
#     self.dateSysMetadataModified = modified
#     self.accessPolicy = accessPolicy()
#
#
# class accessPolicy():
#   def __init__(self):
#     pass
#
#
# class dataonetypes(object):
#   def __init__(self):
#     self.subject = subject()
#     self.permission = permission()
#     self.return_vals = []
#
#   def AccessRule(self):
#     return self.subject
#
#   def accessPolicy(self):
#     return []
#
#   def Permission(self, arg1):
#     return []
#
#   def append(self, arg1):
#     return self.return_vals.append(arg1)
#
#
# class subject(dataonetypes):
#   def __init__(self):
#     super(subject, self).__init__()
#     self.return_vals = []
#
#
# class permission(dataonetypes):
#   def __init__(self):
#     super(permission, self).__init__()
#     self.return_vals = []
#
#
# # Create absolute path from path that is relative to the module from which
# # the function is called.
# def make_absolute(p):
#   return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)
#
#
# # noinspection PyUnresolvedReferences
# class TestResourceMapGenerator(
#   d1_common.testcasewithurlcompare.TestCaseWithURLCompare
# ):
#   def setUp(self):
#     #self.baseurl = 'https://localhost/mn/'
#     #         self.baseurl = 'http://127.0.0.1:8000'
#     self.ore_doc = open(make_absolute('./expected_oai_ore.xml')).read()
#     self.generator = data_package.ResourceMapGenerator()
# #         self.parser = data_package.ResourceMapParser()
#
#   def tearDown(self):
#     pass
#
#   #=========================================================================
#   #
#   #=========================================================================
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_serialize_resource_map'
#   )
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_generate_resource_map'
#   )
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_aggregation_uri_from_pid'
#   )
#   def test_simple_generate_resource_map(
#     self, mock_aggregate, mock_generate, mock_serialize
#   ):
#     resource_map_pid = '_bogus_pid_459837453495884543459873'
#     science_metadata_pid = '_bogus_pid_845434598734598374534958'
#     science_data_pids = '_bogus_pid_983745349845434598734558'
#     mock_serialize.return_value = 'test'
#     response = self.generator.simple_generate_resource_map(
#       resource_map_pid, science_metadata_pid, science_data_pids
#     )
#     self.assertEqual('test', response)
#
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_serialize_resource_map'
#   )
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_generate_resource_map'
#   )
#   def test_simple_generate_resource_map_assert_called_aggregation_uri_from_pid(
#     self, mock_generate, mock_serialize
#   ):
#     with mock.patch.object(
#       data_package.ResourceMapGenerator, '_aggregation_uri_from_pid'
#     ) as mocked_method:
#       resource_map_pid = '_bogus_pid_459837453495884543459873'
#       science_metadata_pid = '_bogus_pid_845434598734598374534958'
#       science_data_pids = '_bogus_pid_983745349845434598734558'
#       self.generator.simple_generate_resource_map(
#         resource_map_pid, science_metadata_pid, science_data_pids
#       )
#       mocked_method.assert_called_with(resource_map_pid)
#
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_serialize_resource_map'
#   )
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_aggregation_uri_from_pid'
#   )
#   def test_simple_generate_resource_map_assert_called_generate_resource_map(
#     self, mock_aggregate, mock_serialize
#   ):
#     with mock.patch.object(
#       data_package.ResourceMapGenerator, '_generate_resource_map'
#     ) as mocked_method:
#       resource_map_pid = '_bogus_pid_459837453495884543459873'
#       science_metadata_pid = '_bogus_pid_845434598734598374534958'
#       science_data_pids = '_bogus_pid_983745349845434598734558'
#       relations = {science_metadata_pid: science_data_pids}
#       mock_aggregate.return_value = 'test'
#       self.generator.simple_generate_resource_map(
#         resource_map_pid, science_metadata_pid, science_data_pids
#       )
#       mocked_method.assert_called_with('test', resource_map_pid, relations)
#
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_aggregation_uri_from_pid'
#   )
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_generate_resource_map'
#   )
#   def test_simple_generate_resource_map_assert_called_serialize_resource_map(
#     self, mock_generate, mock_aggregate
#   ):
#     with mock.patch.object(
#       data_package.ResourceMapGenerator, '_serialize_resource_map'
#     ) as mocked_method:
#       resource_map_pid = '_bogus_pid_459837453495884543459873'
#       science_metadata_pid = '_bogus_pid_845434598734598374534958'
#       science_data_pids = '_bogus_pid_983745349845434598734558'
#       mock_generate.return_value = 'test'
#       self.generator.simple_generate_resource_map(
#         resource_map_pid, science_metadata_pid, science_data_pids
#       )
#       mocked_method.assert_called_with('test')
#
#   @mock.patch.object(data_package.ResourceMapGenerator, '_generate_sys_meta')
#   @mock.patch.object(d1_common.checksum, 'create_checksum_object')
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_serialize_resource_map'
#   )
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_generate_resource_map'
#   )
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_aggregation_uri_from_pid'
#   )
#   def test_generate_system_metadata_for_resource_map(
#     self, mock_aggregate, mock_generate, mock_serialize, mock_checksum,
#     mock_sysmeta
#   ):
#     resource_map_pid = '_bogus_pid_459837453495884543459873'
#     mock_checksum.return_value = 'test1'
#     mock_sysmeta.return_value = 'sysmeta'
#     response = self.generator.generate_system_metadata_for_resource_map(
#       resource_map_pid, 'test', 'user'
#     )
#     self.assertEqual('sysmeta', response)
#
#   @mock.patch.object(d1_common.checksum, 'create_checksum_object')
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_serialize_resource_map'
#   )
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_generate_resource_map'
#   )
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_aggregation_uri_from_pid'
#   )
#   def test_generate_system_metadata_for_resource_map_assert_called_generate_sys_meta(
#     self, mock_aggregate, mock_generate, mock_serialize, mock_checksum
#   ):
#     with mock.patch.object(
#       data_package.ResourceMapGenerator, '_generate_sys_meta'
#     ) as mocked_method:
#       resource_map_pid = '_bogus_pid_459837453495884543459873'
#       mock_generate.return_value = 'test'
#       mock_checksum.return_value = 'test1'
#       self.generator.generate_system_metadata_for_resource_map(
#         resource_map_pid, 'test', 'user'
#       )
#       mocked_method.assert_called_with(
#         '_bogus_pid_459837453495884543459873',
#         'http://www.openarchives.org/ore/terms', 4, 'test1', 'user'
#       )
#
#   @mock.patch.object(data_package.ResourceMapGenerator, '_generate_sys_meta')
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_serialize_resource_map'
#   )
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_generate_resource_map'
#   )
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_aggregation_uri_from_pid'
#   )
#   def test_generate_system_metadata_for_resource_map_assert_called_create_checksum_object(
#     self, mock_aggregate, mock_generate, mock_serialize, mock_checksum
#   ):
#     with mock.patch.object(
#       d1_common.checksum, 'create_checksum_object'
#     ) as mocked_method:
#       resource_map_pid = '_bogus_pid_459837453495884543459873'
#       mock_generate.return_value = 'test'
#       mock_checksum.return_value = 'test1'
#       self.generator.generate_system_metadata_for_resource_map(
#         resource_map_pid, 'test', 'user'
#       )
#       mocked_method.assert_called_with(
#         'test', d1_common.const.DEFAULT_CHECKSUM_ALGORITHM
#       )
#
#   @mock.patch('data_package.foresite.ResourceMap')
#   @mock.patch('data_package.foresite.AggregatedResource')
#   @mock.patch('data_package.foresite.utils')
#   @mock.patch('data_package.foresite.Aggregation')
#   @mock.patch.object(rdflib.namespace, 'Namespace')
#   @mock.patch('data_package.foresite.utils.Namespace')
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_resolvable_uri_from_pid'
#   )
#   def test_generate_resource_map(
#     self, mock_resolve, mock_foresite, mock_namespace, mock_aggregation,
#     mock_utils, mock_resource, mock_map
#   ):
#     relations = {'SCIMETA_PID': ['SCIDATA_PID_1', 'SCIDATA_PID_2']}
#     mock_namespace.return_value = 'test'
#     mock_resolve.return_value = 'test12'
#     mock_aggregation.return_value = foresite()
#     mock_resource.return_value = foresite()
#     mock_map.return_value = foresite()
#     response = self.generator._generate_resource_map(
#       'aggregation_id', 'resource_map_id', relations
#     )
#     self.assertEqual('sysmeta', response.set_aggregation(''))
#
#   @mock.patch('data_package.foresite.ResourceMap')
#   @mock.patch('data_package.foresite.AggregatedResource')
#   @mock.patch('data_package.foresite.utils')
#   @mock.patch('data_package.foresite.Aggregation')
#   @mock.patch.object(rdflib.namespace, 'Namespace')
#   @mock.patch('data_package.foresite.utils.Namespace')
#   def test_generate_resource_map_assert_called_resolvable_uri_from_pid(
#     self, mock_foresite, mock_namespace, mock_aggregation, mock_utils,
#     mock_resource, mock_map
#   ):
#     with mock.patch.object(
#       data_package.ResourceMapGenerator, '_resolvable_uri_from_pid'
#     ) as mocked_method:
#       relations = {'SCIMETA_PID': ['SCIDATA_PID_1', 'SCIDATA_PID_2']}
#       mock_namespace.return_value = 'test'
#       mock_aggregation.return_value = foresite()
#       mock_resource.return_value = foresite()
#       mock_map.return_value = foresite()
#       self.generator._generate_resource_map(
#         'aggregation_id', 'resource_map_id', relations
#       )
#       mocked_method.assert_called_with('resource_map_id')
#
#   @mock.patch('data_package.foresite.ResourceMap')
#   @mock.patch('data_package.foresite.AggregatedResource')
#   @mock.patch('data_package.foresite.utils')
#   @mock.patch('data_package.foresite.Aggregation')
#   @mock.patch.object(rdflib.namespace, 'Namespace')
#   @mock.patch('data_package.foresite.utils.Namespace')
#   def test_generate_resource_map_assert_number_calls_resolvable_uri_from_pid(
#     self, mock_foresite, mock_namespace, mock_aggregation, mock_utils,
#     mock_resource, mock_map
#   ):
#     with mock.patch.object(
#       data_package.ResourceMapGenerator, '_resolvable_uri_from_pid'
#     ) as mocked_method:
#       relations = {'SCIMETA_PID': ['SCIDATA_PID_1', 'SCIDATA_PID_2']}
#       mock_namespace.return_value = 'test'
#       mock_aggregation.return_value = foresite()
#       mock_resource.return_value = foresite()
#       mock_map.return_value = foresite()
#       self.generator._generate_resource_map(
#         'aggregation_id', 'resource_map_id', relations
#       )
#       self.assertEqual(mocked_method.call_count, 4)
#
#   @mock.patch('data_package.foresite.ResourceMap')
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_generate_resource_map'
#   )
#   @mock.patch('data_package.foresite.RdfLibSerializer')
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_assert_is_valid_serialization_format'
#   )
#   def test_serialize_resource_map(
#     self, mock_assert, mock_foresite, mock_generate, mock_map
#   ):
#     mock_foresite.return_value = foresite()
#     mock_assert.return_value = foresite()
#     mock_generate.return_value = foresite()
#     mock_map.get_serialization().data.return_value = 'data'
#     response = self.generator._serialize_resource_map(mock_map)
#     self.assertEqual('data', response.return_value)
#
#   @mock.patch('data_package.foresite.ResourceMap')
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, '_generate_resource_map'
#   )
#   @mock.patch('data_package.foresite.RdfLibSerializer')
#   def test_serialize_resource_map_assert_called_assert_is_valid_serialization_format(
#     self, mock_foresite, mock_generate, mock_map
#   ):
#     with mock.patch.object(
#       data_package.ResourceMapGenerator, '_assert_is_valid_serialization_format'
#     ) as mocked_method:
#       mock_foresite.return_value = foresite()
#       mock_generate.return_value = foresite()
#       mock_map.get_serialization().data.return_value = 'data'
#       self.generator._serialize_resource_map(mock_map)
#       mocked_method.assert_called_with('xml')
#
#   def test_resolvable_uri_from_pid_assert_called_URIRef(self):
#     with mock.patch.object(rdflib.term, 'URIRef') as mocked_method:
#       self.generator._resolvable_uri_from_pid(
#         '_bogus_pid_459837453495884543459873'
#       )
#       called_with = 'https://cn.dataone.org/cn/v1/resolve/_bogus_pid_459837453495884543459873'
#       mocked_method.assert_called_with(called_with.strip(""))
#
#   def test_aggregation_uri_from_pid_assert_called_URIRef(self):
#     with mock.patch.object(rdflib.term, 'URIRef') as mocked_method:
#       self.generator._aggregation_uri_from_pid(
#         '_bogus_pid_459837453495884543459873'
#       )
#       called_with = 'https://cn.dataone.org/cn/v1/resolve/_bogus_pid_459837453495884543459873#aggregation'
#       mocked_method.assert_called_with(called_with.strip(""))
#
#   def test_append_slash(self):
#     output = self.generator._append_slash('https://cn.dataone.org/cn')
#     self.assertEqual('https://cn.dataone.org/cn/', output)
#
#   def test_append_slash_no_append(self):
#     output = self.generator._append_slash('https://cn.dataone.org/cn/')
#     self.assertEqual('https://cn.dataone.org/cn/', output)
#
#   @mock.patch.object(
#     data_package.ResourceMapGenerator, 'generate_public_access_policy'
#   )
#   @mock.patch('d1_common.types.dataoneTypes.systemMetadata')
#   def test_generate_sys_meta(self, mock_types, mock_generate):
#     #         mock_time.return_value = '2015-03-06 12:56:54.323738'
#     with mock.patch('data_package.datetime.datetime') as mock_datetime:
#       mock_datetime.now.return_value = '2015-03-06 12:56:54.323738'
#       mock_types.return_value = sysmeta(
#         'SYSPID', '1234', 100, 'user', 'test', '2015-03-06 12:56:54.323738'
#       )
#       output = self.generator._generate_sys_meta(
#         '_bogus_pid_459837453495884543459873',
#         'http://www.openarchives.org/ore/terms', 10, 'checksum', 'rights_holder'
#       )
#       self.assertEqual(output.identifier, '_bogus_pid_459837453495884543459873')
#       self.assertEqual(output.formatId, 'http://www.openarchives.org/ore/terms')
#       self.assertEqual(output.size, 10)
#       self.assertEqual(output.rightsHolder, 'rights_holder')
#       self.assertEqual(output.checksum, 'checksum')
#       self.assertEqual(str(output.dateUploaded), mock_datetime.now.return_value)
#       self.assertEqual(
#         str(output.dateSysMetadataModified), mock_datetime.now.return_value
#       )
#
#   @mock.patch('d1_common.types.dataoneTypes.systemMetadata')
#   def test_generate_sys_meta_assert_called_generate_public_access_policy(
#     self, mock_types
#   ):
#     with mock.patch.object(
#       data_package.ResourceMapGenerator, 'generate_public_access_policy'
#     ) as mocked_method:
#       mock_types.return_value = sysmeta(
#         'SYSPID', '1234', 100, 'user', 'test', '2015-03-06 12:56:54.323738'
#       )
#       self.generator._generate_sys_meta(
#         '_bogus_pid_459837453495884543459873',
#         'http://www.openarchives.org/ore/terms', 10, 'checksum', 'rights_holder'
#       )
#       mocked_method.assert_called_with()
#
#   @mock.patch('d1_common.types.dataoneTypes.AccessRule')
#   @mock.patch('d1_common.types.dataoneTypes.accessPolicy')
#   def test_generate_public_access_policy(self, mock_policy, mock_rule):
#     mock_policy.return_value = dataonetypes()
#     mock_rule.return_value = dataonetypes()
#     output = self.generator.generate_public_access_policy()
#     self.assertEqual(
#       [u'read'],
#       output.__dict__['return_vals'][0].__dict__['permission'].return_vals
#     )
#     self.assertEqual(
#       ['public'],
#       output.__dict__['return_vals'][0].__dict__['subject'].return_vals
#     )
#
#
# #=========================================================================
# class Test_ResourceMapParser(
#   d1_common.testcasewithurlcompare.TestCaseWithURLCompare
# ):
#   def setUp(self):
#     #self.baseurl = 'https://localhost/mn/'
#     #         self.baseurl = 'http://127.0.0.1:8000'
#     self.ore_doc = open(make_absolute('./example_oai_ore.xml')).read()
#     self.parser = data_package.ResourceMapParser(self.ore_doc)
# #         self.parser = data_package.ResourceMapParser()
#
#   def tearDown(self):
#     pass
#
#   @mock.patch.object(data_package.ResourceMapParser, '_parse')
#   def test_init(self, mock_parse):
#     mock_parse.return_value = 'test'
#     output = data_package.ResourceMapParser('test')
#     self.assertEqual('test', output._resource_map)
#
#   @mock.patch('data_package.foresite.RdfLibParser.parse')
#   @mock.patch('data_package.foresite.RdfLibParser')
#   @mock.patch('data_package.foresite.ReMDocument')
#   def DO_NOT_test_parse(self, mock_doc, mock_parser, mock_parse):
#     mock_doc.return_value = foresite('doc')
#     mock_parser.return_value = foresite('doc')
#     mock_parse.return_value = foresite('doc')
#     rdf_xml_doc = 'test'
#     doc = self.parser._parse(rdf_xml_doc)
#     self.assertEqual(doc, 'https://cn.dataone.org/cn/v1/resolve/abc')
#
#   @mock.patch.object(data_package.ResourceMapParser, '_parse')
#   def test_get_resource_map(self, mock_parse):
#     mock_parse.return_value = 'test'
#     self.parser = data_package.ResourceMapParser('test')
#     output = self.parser.get_resource_map()
#     self.assertEqual('test', output)
#
#   @mock.patch('data_package.foresite.ResourceMap.graph')
#   @mock.patch.object(data_package.ResourceMapParser, 'get_resource_map')
#   def DO_NOT_test_get_resource_map_graph(self, mock_map, mock_foresite):
#     mock_map.graph.return_value = 'graph'
#     mock_foresite.return_value = 'map_graph'
#     output = self.parser.get_resource_map_graph()
#     self.assertEqual('graph', output)
#
#   # @patch.object(data_package.ResourceMapParser,'get_resource_map_graph')
#   # def test_get_resource_map_pid(self, mock_graph):
