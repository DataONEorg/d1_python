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

# Stdlib.
import os
import sys
import StringIO
#import xml.dom.minidom.parse
import xml.dom.minidom
import sys
import optparse
import logging

# 3rd party.
import rdflib.Namespace
import rdflib.URIRef
import foresite
import foresite.utils

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

D1_API_OBJECT_REST_PATH = 'object/'
D1_API_RESOLVE_REST_PATH = 'resolve/'

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
      resource_map_pid, resource_map_pid, relations
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
      sci_uri = self._uri_from_pid(sci_id)
      meta_res = foresite.AggregatedResource(sci_uri)
      meta_res._dcterms.identifier = sci_id
      for data_id in relations[sci_id]:
        data_uri = self._uri_from_pid(data_id)
        data_res = foresite.AggregatedResource(data_uri)
        data_res._dcterms.identifier = data_id
        data_res._cito.isDocumentedBy = sci_uri
        #TODO: multiple entries for documents?
        meta_res._cito.documents = data_uri
        aggr.add_resource(data_res)
      aggr.add_resource(meta_res)
    resmap = foresite.ResourceMap(
      self.dataone_root + D1_API_RESOLVE_REST_PATH + resource_map_id
    )
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

  def _uri_from_pid(self, pid):
    return rdflib.URIRef(self.dataone_root + D1_API_OBJECT_REST_PATH + pid)

  def _append_slash(self, path):
    if not path.endswith('/'):
      path += '/'
    return path
