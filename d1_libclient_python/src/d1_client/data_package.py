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
"""
:mod:`data_package`
===================

:Synopsis:
  Read and write DataONE data packages (OAI-ORE Resource Maps).

  Includes convenience functions to perform the most common parsing and
  generating tasks for Resource Maps.

  See `Data Packaging <http://mule1.dataone.org/ArchitectureDocs-current/design/DataPackage.html>`_
  for more information about how Resource Maps are used in DataONE.
:Created: 2012-03-29
:Author: DataONE (Vieglais, Dahl)
:Requires:
  RDFLib ($ pip install rdflib)
  Google Foresite Toolkit ($ pip install google.foresite-toolkit)
"""

# https://groups.google.com/forum/#!msg/foresite/3vS3_ZZ8Aj0/8tr_SgjbTAUJ
# http://code.google.com/p/foresite-toolkit/source/browse/foresite-python/trunk/foresite/README.txt?r=85

# Stdlib
#import xml.dom.minidom.parse
#import xml.dom.minidom
import datetime

# 3rd party
import foresite
import foresite.utils
import rdflib
import rdflib.namespace
import rdflib.term
import rdflib.plugin
import rdflib.graph

# D1
import d1_common.types.dataoneTypes_v2_0 as dataoneTypes
import d1_common.checksum
import d1_common.const
import d1_common.url
import d1_common.util

rdflib.plugin.register(
  'sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor'
)
rdflib.plugin.register(
  'sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult'
)

ALLOWABLE_PACKAGE_SERIALIZATIONS = (
  'xml', 'pretty-xml', 'n3', 'rdfa', 'json', 'pretty-json', 'turtle', 'nt',
  'trix'
)
RDFXML_FORMATID = 'http://www.openarchives.org/ore/terms'
CITO_NS = 'http://purl.org/spar/cito/'
D1_API_RESOLVE_REST_PATH = 'v1/resolve/'

#=========================================================================


class ResourceMapGenerator():
  def __init__(self, dataone_root=d1_common.const.URL_DATAONE_ROOT):
    self.dataone_root = self._append_slash(dataone_root)

  def simple_generate_resource_map(
      self, resource_map_pid, science_metadata_pid, science_data_pids
  ):
    """Generate an OAI-ORE resource map for the common scenario where one
        resource map describes an aggregation containing a single Science Metadata
        object and one or more Science Data objects described by that object.

        The resource map is generated in RDF:XML format, currently the only format
        supported by DataONE.

        :resource_map_pid: The PID for the resource map itself.
        :science_metadata_pid: The PID for a single Science Metadata object.
        :science_data_pids: A list of one or more Science Data objects described by
          the Science Metadata object.
        """
    # Foresite for Python generates an Aggregation section with isDefinedBy
    # on this form:
    # <rdfs1:isDefinedBy>http://www.openarchives.org/ore/terms/</rdfs1:isDefinedBy>
    # A more common form is:
    # <rdfs1:isDefinedBy rdf:resource="http://www.openarchives.org/ore/terms/"/>
    # It is unclear to me if the first form is valid. Both the Java and Python
    # version of the Foresite library does parse it correctly though.
    relations = {science_metadata_pid: science_data_pids}
    resource_map = self._generate_resource_map(
      self._aggregation_uri_from_pid(resource_map_pid), resource_map_pid,
      relations
    )
    serialized_resource_map = self._serialize_resource_map(resource_map)
    return serialized_resource_map

  def generate_system_metadata_for_resource_map(
      self, resource_map_pid, resource_map, rights_holder,
      checksum_algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM
  ):
    """Generate a system metadata object for a resource map. The generated
        system metadata object is intended for use in DataONE API methods such as
        MNStorage.Create(). The object contains an access control rule allowing
        public access. For simple use cases with public access, the object can
        often be used as is. For more complex use cases, the object can be modified
        programmatically before use.
        """
    size = len(resource_map)
    checksum = d1_common.checksum.create_checksum_object(
      resource_map, checksum_algorithm
    )
    return self._generate_sys_meta(
      resource_map_pid, RDFXML_FORMATID, size, checksum, rights_holder
    )

  # Private.
  #

  def _generate_resource_map(self, aggregation_id, resource_map_id, relations):
    """Generate an OAI-ORE resource map.
        :relations: {metaid:[data id, data id, ...], ...}
        """
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
        # TODO: multiple entries for documents?
        meta_res._cito.documents = data_uri
        aggr.add_resource(data_res)
      aggr.add_resource(meta_res)
    resmap = foresite.ResourceMap(
      self._resolvable_uri_from_pid(resource_map_id)
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

  def _resolvable_uri_from_pid(self, pid):
    return rdflib.term.URIRef(
      self.dataone_root + D1_API_RESOLVE_REST_PATH +
      d1_common.url.encodePathElement(pid)
    )

  def _aggregation_uri_from_pid(self, pid):
    return rdflib.term.URIRef(
      self.dataone_root + D1_API_RESOLVE_REST_PATH +
      d1_common.url.encodePathElement(pid) + '#aggregation'
    )

  def _append_slash(self, path):
    if not path.endswith('/'):
      path += '/'
    return path

  def _generate_sys_meta(
      self, pid, format_id, size, checksum, rights_holder, modified=None
  ):
    if modified is None:
      modified = datetime.datetime.now()
    sys_meta = dataoneTypes.systemMetadata()
    sys_meta.identifier = pid
    sys_meta.formatId = format_id
    sys_meta.size = size
    sys_meta.rightsHolder = rights_holder
    sys_meta.checksum = checksum
    sys_meta.dateUploaded = modified
    sys_meta.dateSysMetadataModified = modified
    sys_meta.accessPolicy = self.generate_public_access_policy()
    return sys_meta

  def generate_public_access_policy(self):
    accessPolicy = dataoneTypes.accessPolicy()
    accessRule = dataoneTypes.AccessRule()
    accessRule.subject.append(d1_common.const.SUBJECT_PUBLIC)
    permission = dataoneTypes.Permission('read')
    accessRule.permission.append(permission)
    accessPolicy.append(accessRule)
    return accessPolicy


#=========================================================================


class ResourceMapParser():
  """Parse a string containing a OAI-ORE document in RDF-XML and provide
    convenient access to information required by many DataONE clients, such as
    lists of aggregated science data and science metadata identifiers.
    """

  def __init__(self, rdf_xml_doc):
    """:rdf_xml_doc: A string containing a OAI-ORE document in RDF-XML
        format
        """
    self._resource_map = self._parse(rdf_xml_doc)

  def _parse(self, rdf_xml_doc):
    """Parse a string containing a OAI-ORE document in RDF-XML
        format to a Foresite ResourceMap object
        """
    foresite_doc = foresite.ReMDocument('file:data', data=rdf_xml_doc)
    # Possible values for format: xml, trix, n3, nt, rdfa
    foresite_doc.format = 'xml'
    rdf_libparser = foresite.RdfLibParser()
    return rdf_libparser.parse(foresite_doc)

  def get_resource_map(self):
    """Return the main Foresite ResourceMap object"""
    return self._resource_map

  def get_resource_map_graph(self):
    """Return the main Foresite ResourceMap graph. This graph contains all
        the triples in the ResourceMap section of the OAI-ORE document
        """
    return self.get_resource_map().graph

  def get_aggregation(self):
    """Return the main Foresite Aggregation object
        """
    return self.get_resource_map().aggregation

  def get_aggregation_graph(self):
    """Return the main Foresite Aggregation graph. This graph contains all the
        triples in the Aggregation section of the OAI-ORE document
        """
    return self.get_aggregation().graph

  def get_resource_map_pid(self):
    """Return the DataONE Persistent Identifier for the resource map
        """
    g = self.get_resource_map_graph()
    q = """
      PREFIX dcterms: <http://purl.org/dc/terms/>

      SELECT ?pid
      WHERE {
        ?o dcterms:identifier ?pid .
      }
    """
    return str([o[0] for o in g.query(q)][0])

  def get_merged_graph(self):
    """Return a rdflib.graph.Graph object that contains all the triples in the
        OAI-ORE document
        """
    graph = rdflib.graph.Graph()
    for s, p, o in self._resource_map.graph:
      graph.add((s, p, o))
    for s, p, o in self._resource_map.aggregation.graph:
      graph.add((s, p, o))
      try:
        for s2, p2, o2 in self._resource_map.aggregation.triples[o].graph:
          graph.add((s2, p2, o2))
      except KeyError:
        pass
    return graph

  def get_all_triples(self):
    """Return a list of tuples that contain all the triples in the OAI-ORE
        document
        """
    g = self.get_merged_graph()
    return [(str(s), str(p), str(o)) for s, p, o in g]

  def get_all_predicates(self):
    """Return a list of all unique predicates in the OAI-ORE document
        """
    g = self.get_merged_graph()
    q = """
      SELECT DISTINCT ?p
      WHERE {
        ?s ?p ?o .
      }
    """
    return map(str, [o[0] for o in g.query(q)])

  def get_subject_objects_by_predicate(self, predicate):
    """Return all subject/objects in the OAI-ORE document with a given predicate
        """
    g = self.get_merged_graph()
    # I tried allowing passing the predicate directly, but I could not get it
    # working. According to http://rdf.myexperiment.org/howtosparql?page=PREFIX,
    # the following queries are equivalent:
    #
    # PREFIX mebase: <http://rdf.myexperiment.org/ontologies/base/>
    # PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    #
    # SELECT ?a ?text
    # WHERE {
    #   ?a rdf:type mebase:Announcement .
    #   ?a mebase:text ?text
    # }
    #
    # and
    #
    # SELECT ?a ?text
    # WHERE {
    # ?a <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>
    #   <http://rdf.myexperiment.org/ontologies/base/Announcement> .
    #   ?a <http://rdf.myexperiment.org/ontologies/base/text> ?text
    # }
    #
    # But I could not make a query on the second form work. It just
    # returned zero results.
    q = """
      PREFIX dc: <http://purl.org/dc/elements/1.1/>
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      PREFIX rdfs1: <http://www.w3.org/2001/01/rdf-schema#>
      PREFIX ore: <http://www.openarchives.org/ore/terms/>
      PREFIX dcterms: <http://purl.org/dc/terms/>
      PREFIX cito: <http://purl.org/spar/cito/>

      SELECT DISTINCT ?s ?o
      WHERE {{
        ?s {0} ?o .
      }}
    """.format(predicate)
    return [(str(s), str(o)) for s, o in g.query(q)]

  def get_aggregated_pids(self):
    g = self.get_merged_graph()
    q = """
      PREFIX ore: <http://www.openarchives.org/ore/terms/>
      PREFIX dcterms: <http://purl.org/dc/terms/>

      SELECT ?pid
      WHERE {
        ?s ore:aggregates ?o .
        ?o dcterms:identifier ?pid .
      }
    """
    return map(str, [o[0] for o in g.query(q)])

  def get_aggregated_science_metadata_pids(self):
    g = self.get_merged_graph()
    q = """
      PREFIX ore: <http://www.openarchives.org/ore/terms/>
      PREFIX dcterms: <http://purl.org/dc/terms/>
      PREFIX cito: <http://purl.org/spar/cito/>

      SELECT DISTINCT ?pid
      WHERE {
        ?s ore:aggregates ?o .
        ?o cito:documents ?o2 .
        ?o dcterms:identifier ?pid .
      }
    """
    return map(str, [o[0] for o in g.query(q)])

  def get_aggregated_science_data_pids(self):
    g = self.get_merged_graph()
    q = """
      PREFIX ore: <http://www.openarchives.org/ore/terms/>
      PREFIX dcterms: <http://purl.org/dc/terms/>
      PREFIX cito: <http://purl.org/spar/cito/>

      SELECT DISTINCT ?pid
      WHERE {
        ?s ore:aggregates ?o .
        ?o cito:isDocumentedBy ?o2 .
        ?o dcterms:identifier ?pid .
      }
    """
    return map(str, [o[0] for o in g.query(q)])
