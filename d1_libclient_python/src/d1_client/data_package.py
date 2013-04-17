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
'''
:mod:`data_package`
===================

:Synopsis: Read and write DataONE data packages (OAI-ORE resource maps)
:Created: 2012-03-29
:Author: DataONE (Vieglais, Pippin, Dahl)

:Requires:
  RDFLib ($ pip install rdflib)
  Google Foresite Toolkit ($ pip install google.foresite-toolkit)
'''

#https://groups.google.com/forum/#!msg/foresite/3vS3_ZZ8Aj0/8tr_SgjbTAUJ
#http://code.google.com/p/foresite-toolkit/source/browse/foresite-python/trunk/foresite/README.txt?r=85

# Stdlib.
#import xml.dom.minidom.parse
#import xml.dom.minidom
import StringIO
import codecs
import datetime
import hashlib
import logging
import optparse
import os
import pprint
import sys

# 3rd party.
import pyxb
import foresite
#from foresite import *
#from rdflib import URIRef, Namespace, Graph
import rdflib.Namespace
import rdflib.URIRef
import foresite
import foresite.utils

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.const
import d1_client.data_package
import d1_client.mnclient

# D1.
import d1_common.const
import d1_common.util as util
from d1_common.types.exceptions import DataONEException

ALLOWABLE_PACKAGE_SERIALIZATIONS = (
  'xml', 'pretty-xml', 'n3', 'rdfa', 'json', 'pretty-json', 'turtle', 'nt', 'trix'
)
RDFXML_FORMATID = 'http://www.openarchives.org/ore/terms'

RDF_NS = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
CITO_NS = 'http://purl.org/spar/cito/'
DCTERMS_NS = 'http://purl.org/dc/terms/'

DATAONE_IDENTIFIER_PREDICATE = 'http://purl.org/dc/terms/identifier'

#D1_API_OBJECT_REST_PATH = 'object/'
D1_API_RESOLVE_REST_PATH = 'v1/resolve/'

#===============================================================================


class ResourceMapGenerator():
  def __init__(self, dataone_root=d1_common.const.URL_DATAONE_ROOT):
    self.dataone_root = self._append_slash(dataone_root)

  def simple_generate_resource_map(
    self, resource_map_pid, science_metadata_pid, science_data_pids
  ):
    '''Generate an OAI-ORE resource map for the common scenario where one
    resource map describes an aggregation containing a single Science Metadata
    object and one or more Science Data objects described by that object.

    The resource map is generated in RDF:XML format, currently the only format
    supported by DataONE.

    :resource_map_pid: The PID for the resource map itself.
    :science_metadata_pid: The PID for a single Science Metadata object.
    :science_data_pids: A list of one or more Science Data objects described by
      the Science Metadata object.
    '''
    relations = {science_metadata_pid: science_data_pids}
    resource_map = self._generate_resource_map(
      self._aggregation_uri_from_pid(resource_map_pid), resource_map_pid, relations
    )
    return self._serialize_resource_map(resource_map)

  '''Generate an OAI-ORE resource map.
  :relations: {metaid:[data id, data id, ...], ...}
  '''

  def _generate_resource_map(self, aggregation_id, resource_map_id, relations):
    uris = {}
    foresite.utils.namespaces['cito'] = rdflib.Namespace(CITO_NS)
    aggr = foresite.Aggregation(aggregation_id)
    for sci_id in relations.keys():
      sci_uri = self._resolvable_uri_from_pid(sci_id)
      meta_res = foresite.AggregatedResource(sci_uri)
      meta_res._dcterms.identifier = sci_id
      for data_id in relations[sci_id]:
        data_uri = self._resolvable_uri_from_pid(data_id)
        data_res = foresite.AggregatedResource(data_uri)
        data_res._dcterms.identifier = data_id
        data_res._cito.isDocumentedBy = sci_uri
        #TODO: multiple entries for documents?
        meta_res._cito.documents = data_uri
        aggr.add_resource(data_res)
      aggr.add_resource(meta_res)
    resmap = foresite.ResourceMap(self._resolvable_uri_from_pid(resource_map_id))
    resmap._dcterms.identifier = resource_map_id
    resmap.set_aggregation(aggr)
    return resmap

  def _serialize_resource_map(self, resourcemap, serialization_format='xml'):
    self._assert_is_valid_serialization_format(serialization_format)
    serializer = foresite.RdfLibSerializer(serialization_format)
    resourcemap.register_serialization(serializer)
    doc = resourcemap.get_serialization()
    return doc.data

  def _assert_is_valid_serialization_format(self, serialization_format):
    assert (serialization_format in ALLOWABLE_PACKAGE_SERIALIZATIONS)

  def _resolvable_uri_from_pid(self, pid):
    return rdflib.URIRef(self.dataone_root + D1_API_RESOLVE_REST_PATH + pid)

  def _aggregation_uri_from_pid(self, pid):
    return rdflib.URIRef(
      self.dataone_root + D1_API_RESOLVE_REST_PATH + pid + '#aggregation'
    )

  def _append_slash(self, path):
    if not path.endswith('/'):
      path += '/'
    return path

#===============================================================================


class ResourceMapParser():
  def __init__(self):
    pass

  def get_identifiers_referenced_by_package(self, rdf_xml_doc):
    ''':rdf_xml_doc: A string containing a OAI-ORE document in RDF-XML
    format'''
    # foresite.ore.AggregatedResource -> OREResource
    pids = []
    for aggregated_resource in self.get_aggregation(rdf_xml_doc):
      graph = aggregated_resource.graph
      for s, p, o in graph:
        # s = subject = rdflib.URIRef.URIRef
        # p = predicate = rdflib.URIRef.URIRef
        # o = object = rdflib.Literal.Literal or rdflib.URIRef.URIRef
        if str(p) == DATAONE_IDENTIFIER_PREDICATE:
          pids.append(str(o))
    return pids

  def get_triples_by_package(self, rdf_xml_doc):
    ''':rdf_xml_doc: A string containing a OAI-ORE document in RDF-XML
    format'''
    triples = []
    for aggregated_resource in self.get_aggregation(rdf_xml_doc):
      graph = aggregated_resource.graph
      for s, p, o in graph:
        # s = subject = rdflib.URIRef.URIRef
        # p = predicate = rdflib.URIRef.URIRef
        # o = object = rdflib.Literal.Literal or rdflib.URIRef.URIRef
        triples.append((str(s), str(p), str(o)))
    return triples

  def get_rdflib_graphs_by_package(self, rdf_xml_doc):
    ''':rdf_xml_doc: A string containing a OAI-ORE document in RDF-XML
    format'''
    return [
      aggregated_resource.graph
      for aggregated_resource in self.get_aggregation(rdf_xml_doc)
    ]

  def get_aggregation(self, rdf_xml_doc):
    resource_map = self.parse(rdf_xml_doc)
    return resource_map.aggregation

  def parse(self, rdf_xml_doc):
    '''Parse a string containing a OAI-ORE document in RDF-XML
    format to a Foresite ResourceMap object'''
    foresite_doc = foresite.ReMDocument('file:data', data=rdf_xml_doc)
    foresite_doc.format = 'xml'
    rdf_libparser = foresite.RdfLibParser()
    return rdf_libparser.parse(foresite_doc)
