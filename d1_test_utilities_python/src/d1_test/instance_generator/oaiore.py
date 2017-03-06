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
:mod:`oaiore`
=============

:Synopsis: Example of forming a package form a Science Metadata Object and a
  Science Data Object.
:Created: 2011-08-08
:Author: DataONE (Vieglais, Dahl)

Requires:
  RDFLib
  Foresite python library, available in svn at:
    https://foresite-toolkit.googlecode.com/svn/foresite-python/trunk
"""

# Stdlib
import sys
import optparse
import logging

# 3rd party
from rdflib import Namespace, URIRef
import foresite
import foresite.utils

#----------------------------------------------------------------------


def main():
  logging.basicConfig(level=logging.INFO)
  if len(sys.argv) < 4:
    print "Generate an OAI-ORE resource map.\n"
    print "  oaiore.py map_id sci_meta_id data_id [data_id ...]\n"
    print "Need at least three PIDs as input.\n"
    sys.exit()
  resources = {sys.argv[2]: sys.argv[3:]}
  resource_map = generate_resource_map(
    resourcemap_id=sys.argv[1], relations=resources
  )
  print serialize_resource_map(resource_map)


def generate_resource_map(
  resourcemap_id="resouce_map_id", aggregation_id="aggregation_id", relations={}
):
  """
  relations = {metaid:[data id, data id, ...], ...}
  """
  uris = {}
  foresite.utils.namespaces['cito'] = Namespace("http://purl.org/spar/cito/")
  aggr = foresite.Aggregation(aggregation_id)
  for sci_id in relations.keys():
    sci_uri = URIRef(u'https://cn.dataone.org/object/%s' % sci_id)
    meta_res = foresite.AggregatedResource(sci_uri)
    meta_res._dcterms.identifier = sci_id
    for data_id in relations[sci_id]:
      data_uri = URIRef('https://cn.dataone.org/object/%s' % data_id)
      data_res = foresite.AggregatedResource(data_uri)
      data_res._dcterms.identifier = data_id
      data_res._cito.isDocumentedBy = sci_uri
      #TODO: multiple entries for documents?
      meta_res._cito.documents = data_uri
      aggr.add_resource(data_res)
    aggr.add_resource(meta_res)
  resmap = foresite.ResourceMap(
    "https://cn.dataone.org/object/%s" % resourcemap_id
  )
  resmap._dcterms.identifier = resourcemap_id
  resmap.set_aggregation(aggr)
  return resmap


def generate(format='xml'):
  assert (
    format in [
      'xml',
      'pretty-xml',
      'n3',
      'rdfa',
      'json',
      'pretty-json',
      'turtle',
      'nt',
      'trix',
    ]
  )
  res = example1()
  serializer = foresite.RdfLibSerializer(format)
  res.register_serialization(serializer)
  doc = res.get_serialization()
  return doc.data


def serialize_resource_map(resourcemap, format='xml'):
  assert (
    format in [
      'xml',
      'pretty-xml',
      'n3',
      'rdfa',
      'json',
      'pretty-json',
      'turtle',
      'nt',
      'trix',
    ]
  )
  serializer = foresite.RdfLibSerializer(format)
  resourcemap.register_serialization(serializer)
  doc = resourcemap.get_serialization()
  return doc.data


def example1():
  """Basic example of a single science metadata document and a science data
  object. That the two form a package is inferred by their presence in the
  resource map aggregation.

  Relationships between aggregated items are defined using terms from the CITO
  ontology (
  http://speroni.web.cs.unibo.it/cgi-bin/lode/req.py?req=http:/purl.org/spar/cito
  ) as described in the DataCite to RDF mapping by David Shotton and Silvio
  Peroni in:

  http://opencitations.wordpress.com/2011/06/30/datacite2rdf-mapping-datacite-metadata-scheme-terms-to-ontologies-2/

  """
  #Add the cito namespace
  foresite.utils.namespaces['cito'] = Namespace("http://purl.org/spar/cito/")

  scidata_id = "scidata_id"
  scidata_uri = URIRef('https://cn.dataone.org/object/%s' % scidata_id)
  scimeta_id = "scimeta_id"
  scimeta_uri = URIRef('https://cn.dataone.org/object/%s' % scimeta_id)

  #create a reference to the science data
  #Create a resolvable URI for the object
  res_1 = foresite.AggregatedResource(scidata_uri)
  #Capture the DataONE identifier as a dcterms:identifier entry
  res_1._dcterms.identifier = scidata_id
  #optional description
  res_1._dcterms.description = "A reference to a science data object using a DataONE identifier"
  #res_1._dcterms.type = URIRef('http://purl.org/dc/dcmitype/Dataset')
  res_1._cito.isDocumentedBy = scimeta_uri

  #create a reference to the science metadata
  res_2 = foresite.AggregatedResource(scimeta_uri)
  #Capture the DataONE identifier as a dcterms:identifier entry
  res_2._dcterms.identifier = scimeta_id
  # We could reference the science data here - but that only works for a
  # single data set
  #res_2._dcterms.references = scidata_id
  res_2._dcterms.description = "A reference to a science metadata document using a DataONE identifier."
  res_2._cito.documents = scidata_uri

  #create the aggregation
  #The identifier here is arbitrary, using an internal id here.
  aggr = foresite.Aggregation("aggregation_id")
  aggr._dcterms.title = "Simple aggregation of science metadata and data"

  #and add the aggregate resources to the aggregation
  aggr.add_resource(res_1)
  aggr.add_resource(res_2)

  #Now create the resource map that will hold the aggregation
  #The identifier for the resource map is treated similarly to the identifiers
  #for the data and metadata entries.
  resource_map_id = "resource_map_id"
  resmap = foresite.ResourceMap(
    "https://cn.dataone.org/object/%s" % resource_map_id
  )
  resmap._dcterms.identifier = resource_map_id
  resmap.set_aggregation(aggr)
  return resmap


if __name__ == '__main__':
  main()
