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
''':mod:`resolver.taxa`
=======================

:Synopsis:
 - Resolve a filesystem path pointing into a Taxa controlled hierarchy.
:Author: DataONE (Dahl)
'''

# Stdlib.
import httplib
import logging
import os
import pprint
import sys

# D1.

# App.
sys.path.append('.')
from impl import attributes
from impl import cache_memory as cache
from impl import command_processor
from impl import directory
from impl import directory_item
from impl import path_exception
import resolver_abc
#from impl #import settings
from impl import util
import resource_map

# Set up logger for this module.
log = logging.getLogger(__name__)

# Example object list:
#[{'author': 'Libe Washburn', 'id': 'doi:10.6073/AA/knb-lter-mcr.32.9'},
# {'author': 'David Foster', 'id': 'doi:10.6073/AA/knb-lter-hfr.41.12'},
# {'author': 'Libe Washburn',
#  'id': 'doi:10.6085/AA/CUYXXX_015MTBD014R00_20100811.50.1'},
# {'id': 'resourceMap_SH15XX_015MHP2014R00_20110412.50.1'},
# {'id': 'resourceMap_SH15XX_015MXTI004R00_20050420.50.6'},
#
# {'id': 'www1.usgs.gov_vip_kimo_metakimospatial.xml', 'kingdom': ['Plantae']},
#
# {'id': 'nrdata.nps.gov_gos_2167323.xml', 'kingdom': ['Plantae']},
# {'id': 'nrdata.nps.gov_gos_2168743.xml', 'kingdom': ['Plantae']}]


class Resolver(resolver_abc.Resolver):
  def __init__(self, options, command_processor):
    self._options = options
    self.command_processor = command_processor
    self.resource_map_resolver = resource_map.Resolver(options, command_processor)
    #self.facet_value_cache = cache.Cache(self._options.MAX_FACET_NAME_CACHE_SIZE)

    self.classifications = [
      'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species',
      'scientificName'
    ]

  # The taxa resolver handles hierarchy levels:
  # / = all classifications with one or more members (e.g., /kingdom)
  # /classification = all unique values for classification (e.g., /kingdom/Plantae)
  # /classification/value = all objects
  # All longer paths are handled by d1_object resolver.

  def get_attributes(self, path):
    log.debug('get_attributes: {0}'.format(util.string_from_path_elements(path)))

    if len(path) >= 3:
      return self.resource_map_resolver.get_attributes(path[2:])

    return self._get_attribute(path)

  def get_directory(self, path, workspace_folder_objects):
    log.debug('get_directory: {0}'.format(util.string_from_path_elements(path)))

    if len(path) >= 3:
      return self.resource_map_resolver.get_directory(path[2:])

    return self._get_directory(path, workspace_folder_objects)

  def read_file(self, path, size, offset):
    log.debug(
      'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(path), size, offset)
    )

    if len(path) >= 3:
      return self.resource_map_resolver.read_file(path[2:], size, offset)

    raise path_exception.PathException('Invalid file')

  # Private.

  def _get_attribute(self, path):
    return attributes.Attributes(0, is_dir=True)

  def _get_directory(self, path, workspace_folder_objects):
    if len(path) == 0:
      return self._resolve_taxa_root(workspace_folder_objects)

    classification = path[0]

    if len(path) == 1 and classification in self.classifications:
      return self._resolve_taxa_classification(classification, workspace_folder_objects)

    classification_value = path[1]

    return self._resolve_taxa_classification_value(
      classification, classification_value, workspace_folder_objects
    )

  def _resolve_taxa_root(self, workspace_folder_objects):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    for g in self.classifications:
      for o in workspace_folder_objects.get_records():
        if g in o.keys():
          dir.append(directory_item.DirectoryItem(g))
          break
    return dir

  def _resolve_taxa_classification(self, classification, workspace_folder_objects):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    u = self._get_unique_values_for_classification(
      classification, workspace_folder_objects
    )
    return [directory_item.DirectoryItem(v) for v in u]

  def _resolve_taxa_classification_value(
    self, classification, value, workspace_folder_objects
  ):
    dir = directory.Directory()
    for o in workspace_folder_objects.get_records():
      try:
        if value in o[classification]:
          dir.append(directory_item.DirectoryItem(o['id']))
      except KeyError:
        pass
    # As empty folders in the taxa tree are pruned in the root and first level,
    # an empty folder here can only be due to an invalid path.
    if not len(dir):
      raise path_exception.PathException('Invalid taxonomic classification value')
    self.append_parent_and_self_references(dir)
    return dir

  def _get_unique_values_for_classification(
    self, classification, workspace_folder_objects
  ):
    u = set()
    for o in workspace_folder_objects.get_records():
      try:
        for v in o[classification]:
          u.add(v)
      except KeyError:
        pass
    return u
