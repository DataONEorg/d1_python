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
import rdflib.namespace
import rdflib.term
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
CITO_DOCUMENTS_PREDICATE = 'http://purl.org/spar/cito/documents'
CITO_IS_DOCUMENTED_BY_PREDICATE = 'http://purl.org/spar/cito/isDocumentedBy'

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
    serialized_resource_map = self._serialize_resource_map(resource_map)
    # TODO: See ticket #4107.
    return serialized_resource_map.replace(
      '<rdfs1:isDefinedBy>http://www.openarchives.org/ore/terms/</rdfs1:isDefinedBy>',
      '<rdfs1:isDefinedBy rdf:resource="http://www.openarchives.org/ore/terms/"/>'
    )

  def generate_system_metadata_for_resource_map(self, resource_map, checksum_algorithm):
    '''Generate a system metadata object for a resource map. The generated
    system metadata object is intended for use in DataONE API methods such as
    MNStorage.Create(). The object contains an access control rule allowing
    public access. For simple use cases with public access, the object can
    often be used as is. For more complex use cases, the object can be modified
    programmatically before use.
    '''
    size = len(science_object)
    now = datetime.datetime.now()
    sys_meta = generate_sys_meta(pid, format_id, size, md5, now)
    return sys_meta

    checksum = self._generate_checksum(resource_map)
    size = len(resource_map)
    return self.session.create_system_metadata(pid, checksum, size, RDFXML_FORMATID)

  #
  # Private.
  #

  def _generate_resource_map(self, aggregation_id, resource_map_id, relations):
    '''Generate an OAI-ORE resource map.
    :relations: {metaid:[data id, data id, ...], ...}
    '''
    uris = {}
    foresite.utils.namespaces['cito'] = rdflib.namespace.Namespace(CITO_NS)
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
    return rdflib.term.URIRef(self.dataone_root + D1_API_RESOLVE_REST_PATH + pid)

  def _aggregation_uri_from_pid(self, pid):
    return rdflib.term.URIRef(
      self.dataone_root + D1_API_RESOLVE_REST_PATH + pid + '#aggregation'
    )

  def _append_slash(self, path):
    if not path.endswith('/'):
      path += '/'
    return path

  def generate_sys_meta(pid, format_id, size, md5, now):
    sys_meta = dataoneTypes.systemMetadata()
    sys_meta.identifier = pid
    sys_meta.formatId = format_id
    sys_meta.size = size
    sys_meta.rightsHolder = SYSMETA_RIGHTSHOLDER
    sys_meta.checksum = dataoneTypes.checksum(md5)
    sys_meta.checksum.algorithm = 'MD5'
    sys_meta.dateUploaded = now
    sys_meta.dateSysMetadataModified = now
    sys_meta.accessPolicy = generate_public_access_policy()
    return sys_meta

  def _generate_checksum(self, resource_map, algorithm='SHA-1'):
    h = d1_common.util.get_checksum_calculator_by_dataone_designator(algorithm)
    h.update(resource_map)
    return h.hexdigest()

  def generate_public_access_policy():
    accessPolicy = dataoneTypes.accessPolicy()
    accessRule = dataoneTypes.AccessRule()
    accessRule.subject.append(d1_common.const.SUBJECT_PUBLIC)
    permission = dataoneTypes.Permission('read')
    accessRule.permission.append(permission)
    accessPolicy.append(accessRule)
    return accessPolicy

#===============================================================================


class ResourceMapParser():
  def __init__(self, rdf_xml_doc):
    ''':rdf_xml_doc: A string containing a OAI-ORE document in RDF-XML
    format'''
    self._resource_map = self._parse(rdf_xml_doc)

  def _parse(self, rdf_xml_doc):
    '''Parse a string containing a OAI-ORE document in RDF-XML
    format to a Foresite ResourceMap object'''
    foresite_doc = foresite.ReMDocument('file:data', data=rdf_xml_doc)
    # Possible values for format: xml, trix, n3, nt, rdfa
    foresite_doc.format = 'xml'
    rdf_libparser = foresite.RdfLibParser()
    return rdf_libparser.parse(foresite_doc)
    pass

  def get_resource_map_pid(self):
    return str(self._resource_map)

  def get_all_triples(self):
    triples = []
    for subject, arbitrary_resource in self._resource_map.triples.items():
      for s, p, o in arbitrary_resource.graph:
        triples.append((str(s), str(p), str(o)))
    return triples

  def get_all_predicates(self):
    predicates = []
    for subject, arbitrary_resource in self._resource_map.triples.items():
      for p in arbitrary_resource.predicates():
        predicates.append(str(p))
    return predicates

  def get_identifiers_referenced_by_package(self):
    triples = self.get_all_triples()
    pids = []
    for s, p, o in triples:
      if p == DATAONE_IDENTIFIER_PREDICATE:
        pids.append(o)
    return pids

  def get_sci_meta_pids(self):
    return self.get_sci_relations()[0]

  def get_sci_data_pids(self):
    return self.get_sci_relations()[1]

  def get_sci_relations(self):
    triples = self.get_all_triples()
    sci_meta = set()
    sci_data = set()
    for s, p, o in triples:
      if p == CITO_DOCUMENTS_PREDICATE:
        sci_meta.add(s)
        sci_data.add(o)
      if p == CITO_IS_DOCUMENTED_BY_PREDICATE:
        sci_meta.add(o)
        sci_data.add(s)
    return list(sci_meta), list(sci_data)

  def get_aggregation(self):
    return self._resource_map.aggregation

  def get_graphs(self):
    return self._resource_map.graph
