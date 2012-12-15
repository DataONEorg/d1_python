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
''':mod:`resolver.resource_map`
===============================

:Synopsis:
 - Resolve a filesystem path pointing to a resource map.
:Author: DataONE (Dahl)
'''

# Stdlib.
import httplib
import logging
import os
import pprint
import sys

# D1.
import d1_client.data_package

# App.
sys.path.append('.')
import attributes
import cache
import command_processor
import d1_object
import directory
import directory_item
import facet_path_formatter
import facet_path_parser
import path_exception
import resolver_abc
import settings
import util

# Set up logger for this module.
log = logging.getLogger(__name__)


class Resolver(resolver_abc.Resolver):
  def __init__(self):
    self.command_processor = command_processor.CommandProcessor()
    self.d1_object_resolver = d1_object.Resolver()
    #self.facet_value_cache = cache.Cache(settings.MAX_FACET_NAME_CACHE_SIZE)

    # The resource map resolver handles only one hierarchy level, so anything
    # that has more levels is handed to the d1_object resolver.
    # If the object is not a resource map, control is handed to the d1_object
    # resolver.

  def get_attributes(self, path):
    log.debug('get_attributes: {0}'.format(util.string_from_path_elements(path)))

    # The resource map resolver handles only one hierarchy level, so anything
    # that has more levels is handed to the d1_object resolver.
    if len(path) > 1 or not self._is_resource_map(path[0]):
      return self.d1_object_resolver.get_attributes(path)

    return self._get_attribute(path)

  def get_directory(self, path):
    log.debug('get_directory: {0}'.format(util.string_from_path_elements(path)))

    if len(path) > 1 or not self._is_resource_map(path[0]):
      return self.d1_object_resolver.get_directory(path)

    return self._get_directory(path)

  def read_file(self, path, size, offset):
    log.debug(
      'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(
          path
        ), size, offset
      )
    )

    #    if len(path) > 1 or not self._is_resource_map(path[0]):
    return self.d1_object_resolver.read_file(path, size, offset)

    #    return self._get_directory(path)

    # Private.

  def _get_attribute(self, path):
    return attributes.Attributes(self._get_resource_map_size(path[0]), is_dir=True)

  def _get_directory(self, path):
    resource_map = self.command_processor.get_science_object_through_cache(path[0])
    pids = self.deserialize_resource_map(resource_map)
    return [directory_item.DirectoryItem(pid) for pid in pids]

  def _get_resource_map_size(self, pid):
    return {
      'total': self.get_total_size_of_objects_in_resource_map,
      'number': self.get_number_of_objects_in_resource_map,
      'zero': self.get_zero,
    }[settings.FOLDER_SIZE_FOR_RESOURCE_MAPS](pid)

  def _is_resource_map(self, pid):
    #try:
    description = self.command_processor.get_object_info_through_cache(pid)
    #except:
    #self._raise_invalid_pid(pid)
    return description['format_id'] == d1_client.data_package.RDFXML_FORMATID

  def _get_description(self, pid):
    #try:
    return self.command_processor.get_object_info_through_cache(pid)
    #except:
    #self._raise_invalid_pid(pid)

  def _raise_invalid_pid(self, pid):
    raise path_exception.PathException('Invalid PID: {0}'.format(pid))

    #    except Exception as e:
    #      print e
    #    except httplib.BadStatusLine as e:
    #      # BadStatusLine means that the object was not found on the server
    #      return False

  def deserialize_resource_map(self, resource_map):
    package = d1_client.data_package.DataPackage()
    package._parse_rdf_xml(resource_map)
    return sorted(package.scidata_dict.keys())

  def get_total_size_of_objects_in_resource_map(self, resource_map_pid):
    resource_map = self.command_processor.get_science_object_through_cache(
      resource_map_pid
    )
    pids = self.deserialize_resource_map(resource_map)
    total = 0
    for pid in pids:
      o = self.command_processor.get_object_info_through_cache(pid)
      total += o['size']
    return total

  def get_number_of_objects_in_resource_map(self, resource_map_pid):
    resource_map = self.command_processor.get_science_object_through_cache(
      resource_map_pid
    )
    return len(self.deserialize_resource_map(resource_map))

  def get_zero(self, pid):
    return 0

    #    for sci_obj_pid, sci_obj in package.scidata_dict.items():
    #      print sci_obj_pid
    #      print sci_obj.meta

    #    {
    #     'original_pid': None, 
    #     'pid': None, 
    #     'scidata_dict': 
    #      {u'r_test3.scidata.1.2012111515031353017039':
    #        <d1_client.data_package.DataObject object at 0x32edf90>,
    #        u'r_test3.scidata.2.2012111515031353017039':
    #        <d1_client.data_package.DataObject object at 0x32f5890>
    #      },
    #      'sysmeta': None,
    #      'resmap': None,
    #      'scimeta':
    #        <d1_client.data_package.DataObject object at 0x3300110>
    #    }

    # Private.

  def ___docs___():
    # Documentation of the foresite Python library
    # As far as I can tell, this is it, in its entirety!

    # Import everything

    #from foresite import *
    #from rdflib import URIRef, Namespace

    # Create an aggregation

    a = Aggregation('my-aggregation-uri')

    # Set properties on the aggregation. The first defaults to dc:title, the
    # second explicitly sets it as dcterms:created.

    a.title = "My Aggregation"
    a._dcterms.created = "2008-07-10T12:00:00"

    # And retrieve properties:

    print a._dc.title
    # [rdflib.Literal('My Aggregation', ...
    print a.created
    # [rdflib.Literal('2008-07-10T12:00:00', ...

    # Note that they become lists as any property can be added multiple times.

    # Create and Aggregate two resources

    res = AggregatedResource('my-photo-1-uri')
    res.title = "My first photo"
    res2 = AggregatedResource('my-photo-2-uri')
    res2.title = "My second photo"
    a.add_resource(res)
    a.add_resource(res2)

    # Create and associate an agent (without a URI) with the aggregation

    me = Agent()
    me.name = "Rob Sanderson"
    a.add_agent(me, 'creator')

    # If no URI assigned, then it will be a blank node:

    print me.uri
    #rdflib.BNode(...

    # Create an agent with a URI:

    you = Agent('uri-someone-else')

    # Register an Atom serializer with the aggregation. The registration creates
    # a new ResourceMap, which needs a URI.

    serializer = AtomSerializer()
    rem = a.register_serialization(serializer, 'my-atom-rem-uri')

    # And fetch the serialisation.

    remdoc = a.get_serialization()
    print remdoc.data
    #<feed ...

    # Or, equivalently:

    remdoc = rem.get_serialization()
    print remdoc.data
    #<feed ...

    # Resource Maps can be created by hand:

    rem2 = ResourceMap('my-rdfa-rem-uri')
    rem2.set_aggregation(a)

    # And have their own serializers:

    rdfa = RdfLibSerializer('rdfa')
    rem2.register_serialization(rdfa)
    remdoc2 = rem2.get_serialization()
    print remdoc2.data
    #<div id="ore:ResourceMap" xmlns...

    # Possible values for RdfLibSerializer: rdf (rdf/xml), pretty-xml (pretty
    # rdf/xml), nt (n triples), turtle, n3, rdfa (Invisible RDFa XHTML snippet)

    # Parsing existing Resource Maps. The argument to ReMDocument can be a
    # filename or a URL.

    remdoc = ReMDocument(
      "http://www.openarchives.org/ore/0.9/atom-examples/atom_dlib_maxi.atom"
    )
    ap = AtomParser()
    rem = ap.parse(remdoc)
    aggr = rem.aggregation

    # Or an RDF Parser, which requires format to be set on the rem document:

    rdfp = RdfLibParser()
    remdoc2.format = 'rdfa' # done by the serializer by default
    print rdfp.parse(remdoc2)
    # <foresite.ore.ResourceMap object ...

    # Possible values for format: xml, trix, n3, nt, rdfa

    # And then re-serialise in a different form:

    rdfxml = RdfLibSerializer('xml')
    rem2 = aggr.register_serialization(rdfxml, 'my-rdf-rem-uri')
    remdoc3 = rem2.get_serialization()

    # Creating arbitrary triples:

    something = ArbitraryResource('uri-random')
    a.add_triple(something)

    # And then treat them like any object

    something.title = "Random Title"
    something._rdf.type = URIRef('http://somewhere.org/class/something')

    #To add in additional namespaces:

    utils.namespaces['nss'] = Namespace('http://nss.com/namespace/ns')
    utils.namespaceSearchOrder.append('nss')
    utils.elements['nss'] = ['element1', 'element2', 'element3']

    # And finally, some options that can be set to change the behaviour of the
    # library:

    utils.assignAgentUri = True # instead of blank node, assign UUID URI
    utils.proxyType = 'UUID' # instead of oreproxy.org, assign UUID proxy

    # If you try to serialize an unconnected graph, there are several
    # possibilities:

    utils.unconnectedAction = 'ignore' # serialize anyway
    utils.unconnectedAction = 'drop' # drop unconnected parts of graph
    utils.unconnectedAction = 'warn' # print a warning to stdout
    utils.unconnectedAction = 'raise' # raise exception


if __name__ == '__main__':
  r = Resolver()
  r.deserialize_resource_map()
