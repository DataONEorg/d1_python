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
""":mod:`resolver.taxa`
=======================

:Synopsis:
 - Resolve a filesystem path pointing into a Taxa controlled hierarchy.
:Author:
  DataONE (Dahl)
"""

import logging

import d1_onedrive.impl.resolver.resolver_base
import d1_onedrive.impl.resolver.resource_map
from d1_onedrive.impl import attributes
from d1_onedrive.impl import directory
from d1_onedrive.impl import onedrive_exceptions
from d1_onedrive.impl import util

log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

README_TXT = """Taxa Folder

This folder contains the items of the object_tree folder (the parent
of this folder) grouped by their taxonomic classications.

Items for which there is no taxonomic information are not included in these
folders.
"""

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


class Resolver(d1_onedrive.impl.resolver.resolver_base.Resolver):
  def __init__(self, options, object_tree):
    super().__init__(options, object_tree)
    self._resource_map_resolver = d1_onedrive.impl.resolver.resource_map.Resolver(
      options, object_tree
    )
    self._readme_txt = util.os_format(README_TXT)

    self._classifications = [
      'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species',
      'scientificName'
    ]

  # The taxa resolver handles hierarchy levels:
  # / = all classifications with one or more members (e.g., /kingdom)
  # /classification = all unique values for classification (e.g., /kingdom/Plantae)
  # /classification/value = all objects
  # All longer paths are handled by d1_object resolver.

  def get_attributes(self, object_tree_folder, path):
    log.debug('get_attributes: {}'.format(util.string_from_path_elements(path)))

    if self._is_readme_file(path):
      return self._get_readme_file_attributes()

    if len(path) <= 2:
      return self._get_attributes(path)

    return self._resource_map_resolver.get_attributes(
      object_tree_folder, path[2:]
    )

  def get_directory(self, object_tree_folder, path):
    log.debug('get_directory: {}'.format(util.string_from_path_elements(path)))

    if len(path) <= 2:
      return self._get_directory(object_tree_folder, path)

    return self._resource_map_resolver.get_directory(path[2:])

  def read_file(self, object_tree_folder, path, size, offset):
    log.debug(
      'read_file: {}, {}, {}'.
      format(util.string_from_path_elements(path), size, offset)
    )
    if self._is_readme_file(path):
      return self._get_readme_text(size, offset)
    if len(path) <= 2:
      raise onedrive_exceptions.PathException('Invalid file')
    return self._resource_map_resolver.read_file(path[2:], size, offset)

  # Private.

  def _get_attributes(self, path):
    return attributes.Attributes(0, is_dir=True)

  def _get_directory(self, object_tree_folder, path):
    if len(path) == 0:
      return self._resolve_taxa_root(object_tree_folder)

    classification = path[0]

    if len(path) == 1 and classification in self._classifications:
      return self._resolve_taxa_classification(
        classification, object_tree_folder
      )

    classification_value = path[1]

    return self._resolve_taxa_classification_value(
      classification, classification_value, object_tree_folder
    )

  def _resolve_taxa_root(self, object_tree_folder):
    d = directory.Directory()
    for g in self._classifications:
      if g in object_tree_folder['items']:
        d.append(g)
        break
    return d

  def _resolve_taxa_classification(self, classification, object_tree_folder):
    return self._get_unique_values_for_classification(
      classification, object_tree_folder
    )

  def _resolve_taxa_classification_value(
      self, classification, value, object_tree_folder
  ):
    d = directory.Directory()
    for pid in object_tree_folder.get_records['items']:
      record = self._object_tree.get_object_record(pid)
      try:
        if value in record[classification]:
          d.append(record['id'])
      except KeyError:
        pass
    # As empty folders in the taxa tree are pruned in the root and first level,
    # an empty folder here can only be due to an invalid path.
    if not len(d):
      raise onedrive_exceptions.PathException(
        'Invalid taxonomic classification value'
      )
    return d

  def _get_unique_values_for_classification(
      self, classification, object_tree_folder
  ):
    u = set()
    for pid in object_tree_folder['items']:
      record = self._object_tree.get_object_record(pid)
      try:
        for v in record[classification]:
          u.add(v)
      except KeyError:
        pass
    return u
