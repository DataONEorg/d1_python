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
"""Resolve region

Resolve a filesystem path pointing into a Region controlled hierarchy.
"""

import hashlib
import http.client
import json
import logging
import socket

import d1_onedrive.impl.resolver.resolver_base
import d1_onedrive.impl.resolver.resource_map
# App
from d1_onedrive.impl import attributes
from d1_onedrive.impl import directory
from d1_onedrive.impl import disk_cache
from d1_onedrive.impl import onedrive_exceptions
from d1_onedrive.impl import util

# D1

log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

#GAZETTEER_HOST = '192.168.1.116'
GAZETTEER_HOST = 'stress-1-unm.test.dataone.org'

README_TXT = """Region Folder

This folder provides a geographically ordered view of science data objects
for which the geographical area being covered is known to DataONE. Objects with
unknown geographical coverage do not appear in this folder.

The earth is divided into countries. Within the countries, there are various
administrative areas that differ in organization from country to country. There
can be several layers of administrative areas. For instance, in the US, there
are states and within the states, there are counties.

The Region folder arranges the science objects into folders that represent these
administrative areas. In a given level of the Region tree, all the science
objects that contain data for that administrative area will appear. Lower level
folders do not contain more science objects. They simply contain the same
science objects as in the current level, only arranged into smaller
administrative areas.

For instance, if the current object_tree folder contains two objects, one that has
data for California and Arizona and another that has data for Arizona and New
Mexico, both objects will appear under United States and under Arizona. But only
the first object will appear under California and only the second will appear
under New Mexico.
"""


class Resolver(d1_onedrive.impl.resolver.resolver_base.Resolver):
  def __init__(self, options, object_tree):
    super().__init__(options, object_tree)
    self._resource_map_resolver = d1_onedrive.impl.resolver.resource_map.Resolver(
      options, object_tree
    )
    self._region_tree_cache = disk_cache.DiskCache(
      options.region_tree_max_cache_items, options.region_tree_cache_path
    )
    self._readme_txt = util.os_format(README_TXT)

  def get_attributes(self, object_tree_folder, path):
    log.debug('get_attributes: {}'.format(util.string_from_path_elements(path)))

    return self._get_attributes(object_tree_folder, path)

  def get_directory(self, object_tree_folder, path):
    log.debug('get_directory: {}'.format(util.string_from_path_elements(path)))

    return self._get_directory(object_tree_folder, path)

  def read_file(self, object_tree_folder, path, size, offset):
    log.debug(
      'read_file: {}, {}, {}'.
      format(util.string_from_path_elements(path), size, offset)
    )

    return self._read_file(object_tree_folder, path, size, offset)

  #
  # Private.
  #

  def _get_attributes(self, object_tree_folder, path):
    if path == ['readme.txt']:
      return attributes.Attributes(len(self._readme_txt))

    merged_region_tree = self._get_merged_region_tree(object_tree_folder)
    region_tree_item, unconsumed_path = self._get_region_tree_item_and_unconsumed_path(
      merged_region_tree, path
    )
    if self._region_tree_item_is_pid(region_tree_item):
      try:
        return self._resource_map_resolver.get_attributes(
          object_tree_folder,
          [region_tree_item] + unconsumed_path
        )
      except onedrive_exceptions.NoResultException:
        pass
    return attributes.Attributes(0, is_dir=True)

  def _get_directory(self, object_tree_folder, path):
    dir = directory.Directory()

    merged_region_tree = self._get_merged_region_tree(object_tree_folder)

    region_tree_item, unconsumed_path = self._get_region_tree_item_and_unconsumed_path(
      merged_region_tree, path
    )
    if self._region_tree_item_is_pid(region_tree_item):
      # If there is an unconsumed path section, the path exits through a valid
      # PID (any other exit would have raised an exception).
      #if len(unconsumed_path):
      return self._resource_map_resolver.get_directory(
        object_tree_folder,
        [region_tree_item] + unconsumed_path
      )
      #else:
      #  # The user has attempted to "dir" a PID.
      #  raise onedrive_exceptions.PathException('not a directory')

      # The whole path was consumed and a folder within the tree was returned.
    dir = directory.Directory()
    #if self._has_readme_entry(path):
    #  dir.append(self._get_readme_filename())

    for r in region_tree_item:
      dir.append(r)

    # Add readme.txt to root.
    if not path:
      dir.append('readme.txt')

    return dir

  def _read_file(self, object_tree_folder, path, size, offset):
    if path == ['readme.txt']:
      return self._readme_txt[offset:offset + size]

    merged_region_tree = self._get_merged_region_tree(object_tree_folder)
    region_tree_item, unconsumed_path = self._get_region_tree_item_and_unconsumed_path(
      merged_region_tree, path
    )

    if self._region_tree_item_is_pid(region_tree_item):
      return self._resource_map_resolver.read_file(
        object_tree_folder,
        [region_tree_item] + unconsumed_path, size, offset
      )

  def _get_merged_region_tree(self, object_tree_folder):
    k = self._get_unique_dictionary_key(object_tree_folder)
    try:
      return self._region_tree_cache[k]
    except KeyError:
      pass

    geo_records = self._get_records_with_geo_bounding_box(object_tree_folder)

    merged_region_tree = {}
    for g in geo_records:
      t = self._get_region_tree_for_geo_record(g)
      self._merge_region_trees(merged_region_tree, t, g[0])

    self._region_tree_cache[k] = merged_region_tree
    return merged_region_tree

  def _get_unique_dictionary_key(self, object_tree_folder):
    m = hashlib.sha1()
    for pid in object_tree_folder['items']:
      m.update(pid)
    return m.hexdigest()

  def _get_region_tree_for_geo_record(self, geo_record):
    try:
      c = http.client.HTTPConnection(GAZETTEER_HOST)
      c.request('GET', '/region_tree/{}/{}/{}/{}'.format(*geo_record[1:]))
      return json.loads(c.getresponse().read())
    except (http.client.HTTPException, socket.error):
      return {'Reverse geocoding failed': {}}

  def _get_records_with_geo_bounding_box(self, object_tree_folder):
    geo_records = []
    for pid in object_tree_folder['items']:
      record = self._object_tree.get_object_record(pid)
      try:
        w = record['westBoundCoord']
        s = record['southBoundCoord']
        e = record['eastBoundCoord']
        n = record['northBoundCoord']
      except KeyError:
        pass
      else:
        geo_records.append((pid, w, s, e, n))
    return geo_records

  def _merge_region_trees(self, dst_tree, src_tree, pid):
    """Merge conflicts occur if a folder in one tree is a file in the other. As
    the files are PIDs, this can only happen if a PID matches one of the
    geographical areas that the dataset covers and should be very rare. In such
    conflicts, the destination wins."""
    for k, v in list(src_tree.items()):
      # Prepend an underscore to the administrative area names, to make them
      # sort separately from the identifiers.
      #k = '_' + k
      if k not in dst_tree or dst_tree[k] is None:
        dst_tree[k] = {}
      dst_tree[k][pid] = None
      if v is not None:
        self._merge_region_trees(dst_tree[k], v, pid)

  def _get_region_tree_item_and_unconsumed_path(
      self, region_tree, path, parent_key=''
  ):
    """Return the region_tree item specified by path. An item can be a a folder
    (represented by a dictionary) or a PID (represented by None).

    This function is also used for determining which section of a path is within
    the region tree and which section should be passed to the next resolver. To
    support this, the logic is as follows:

    - If the path points to an item in the region tree, the item is returned and
      the path, having been fully consumed, is returned as an empty list.

    - If the path exits through a valid PID in the region tree, the PID is
      returned for the item and the section of the path that was not consumed
      within the region tree is returned.

    - If the path exits through a valid folder in the region tree, an "invalid
      path" PathException is raised. This is because only the PIDs are valid
      "exit points" in the tree.

    - If the path goes to an invalid location within the region tree, an
      "invalid path" PathException is raised.
    """
    # Handle valid item within region tree.
    if not path:
      if region_tree is None:
        return parent_key, []
      else:
        return region_tree, []
    # Handle valid exit through PID.
    if region_tree is None:
      return parent_key, path
    # Handle next level in path.
    if path[0] in list(region_tree.keys()):
      return self._get_region_tree_item_and_unconsumed_path(
        region_tree[path[0]], path[1:], path[0]
      )
    else:
      raise onedrive_exceptions.PathException('Invalid path')

    #if path[0] in region_tree.keys():
    #  if region_tree[path[0]] is None:
    #    return [path[0]], path
    #  else:

  def _region_tree_item_is_pid(self, region_tree_item):
    return isinstance(region_tree_item, str)
