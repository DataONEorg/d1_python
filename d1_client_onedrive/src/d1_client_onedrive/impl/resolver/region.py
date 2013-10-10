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
''':mod:`resolver.region`
=========================

:Synopsis:
 - Resolve a filesystem path pointing into a Region controlled hierarchy.
:Author: DataONE (Dahl)
'''

# Stdlib.
import hashlib
import httplib
import json
import logging
import os
import pprint
import socket
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
from impl import cache_disk

# Set up logger for this module.
log = logging.getLogger(__name__)
#Set level specific for this module if specified
try:
  log.setLevel(logging.getLevelName( \
               getattr(logging,'ONEDRIVE_MODULES')[__name__]) )
except:
  pass

log.setLevel(logging.DEBUG)

#GAZETTEER_HOST = '192.168.1.116'
GAZETTEER_HOST = 'stress-1-unm.test.dataone.org'

README = '''Region Folder

The Region folder provides a geographically ordered view of science data objects
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

For instance, if the current workspace folder contains two objects, one that has
data for California and Arizona and another that has data for Arizona and New
Mexico, both objects will appear under United States and under Arizona. But only
the first object will appear under California and only the second will appear
under New Mexico.
'''

README_TXT = 'readme.txt'


class Resolver(resolver_abc.Resolver):
  def __init__(self, options, command_processor):
    self._options = options
    self.command_processor = command_processor
    self.resource_map_resolver = resource_map.Resolver(options, command_processor)
    self._region_tree_cache = cache_disk.DiskCache(1000, 'cache_region_tree')
    self.helpText = README

  def get_attributes(self, path, workspace_folder_objects):
    log.debug(u'get_attributes: {0}'.format(util.string_from_path_elements(path)))

    return self._get_attribute(path, workspace_folder_objects)

  def get_directory(self, path, workspace_folder_objects):
    log.debug(u'get_directory: {0}'.format(util.string_from_path_elements(path)))

    return self._get_directory(path, workspace_folder_objects)

  def read_file(self, path, workspace_folder_objects, size, offset):
    log.debug(
      u'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(path), size, offset)
    )

    return self._read_file(path, workspace_folder_objects, size, offset)

  #
  # Private.
  #

  def _get_attribute(self, path, workspace_folder_objects, fs_path=''):
    if path == ['readme.txt']:
      return attributes.Attributes(len(self.helpText))

    merged_region_tree = self._get_merged_region_tree(workspace_folder_objects)
    region_tree_item, unconsumed_path = self._get_region_tree_item_and_unconsumed_path(
      merged_region_tree, path
    )
    if self._region_tree_item_is_pid(region_tree_item):
      try:
        return self.resource_map_resolver.get_attributes(
          [
            region_tree_item
          ] + unconsumed_path, fs_path
        )
      except path_exception.NoResultException:
        pass
    return attributes.Attributes(0, is_dir=True)

  def _get_directory(self, path, workspace_folder_objects):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)

    merged_region_tree = self._get_merged_region_tree(workspace_folder_objects)

    region_tree_item, unconsumed_path = self._get_region_tree_item_and_unconsumed_path(
      merged_region_tree, path
    )
    if self._region_tree_item_is_pid(region_tree_item):
      # If there is an unconsumed path section, the path exits through a valid
      # PID (any other exit would have raised an exception).
      #if len(unconsumed_path):
      return self.resource_map_resolver.get_directory(
        [
          region_tree_item
        ] + unconsumed_path
      )
      #else:
      #  # The user has attempted to "dir" a PID.
      #  raise path_exception.PathException('not a directory')

      # The whole path was consumed and a folder within the tree was returned.
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    #if self.hasHelpEntry(path):
    #  dir.append(self.getHelpDirectoryItem())

    for r in region_tree_item:
      dir.append(directory_item.DirectoryItem(r))

    # Add readme.txt to root.
    if not len(path):
      dir.append(directory_item.DirectoryItem('readme.txt'))

    return dir

  def _read_file(self, path, workspace_folder_objects, size, offset):
    if path == ['readme.txt']:
      return self.helpText[offset:size]

    merged_region_tree = self._get_merged_region_tree(workspace_folder_objects)
    region_tree_item, unconsumed_path = self._get_region_tree_item_and_unconsumed_path(
      merged_region_tree, path
    )

    if self._region_tree_item_is_pid(region_tree_item):
      return self.resource_map_resolver.read_file(
        [
          region_tree_item
        ] + unconsumed_path, size, offset
      )

  def _get_merged_region_tree(self, workspace_folder_objects):
    k = self._get_unique_dictionary_key(workspace_folder_objects)
    try:
      return self._region_tree_cache[k]
    except KeyError:
      pass

    geo_records = self._get_records_with_geo_bounding_box(workspace_folder_objects)

    merged_region_tree = {}
    for g in geo_records:
      t = self._get_region_tree_for_geo_record(g)
      self._merge_region_trees(merged_region_tree, t, g[0])

    self._region_tree_cache[k] = merged_region_tree
    return merged_region_tree

  def _get_unique_dictionary_key(self, workspace_folder_objects):
    m = hashlib.sha1()
    for r in workspace_folder_objects.get_records():
      m.update(r['id'])
    return m.hexdigest()

  def _get_region_tree_for_geo_record(self, geo_record):
    try:
      c = httplib.HTTPConnection(GAZETTEER_HOST)
      c.request('GET', '/region_tree/{0}/{1}/{2}/{3}'.format(*geo_record[1:]))
      return json.loads(c.getresponse().read())
    except (httplib.HTTPException, socket.error):
      return {'Reverse geocoding failed': {}}

  def _get_records_with_geo_bounding_box(self, workspace_folder_objects):
    geo_records = []
    for o in workspace_folder_objects.get_records():
      try:
        w = o['westBoundCoord']
        s = o['southBoundCoord']
        e = o['eastBoundCoord']
        n = o['northBoundCoord']
      except KeyError:
        pass
      else:
        geo_records.append((o['id'], w, s, e, n))
    return geo_records

  def _merge_region_trees(self, dst_tree, src_tree, pid):
    '''Merge conflicts occur if a folder in one tree is a file in the other. As
    the files are PIDs, this can only happen if a PID matches one of the
    geographical areas that the dataset covers and should be very rare. In such
    conflicts, the destination wins.'''
    for k, v in src_tree.items():
      # Prepend an underscore to the administrative area names, to make them
      # sort separately from the identifiers.
      #k = '_' + k
      if k not in dst_tree or dst_tree[k] is None:
        dst_tree[k] = {}
      dst_tree[k][pid] = None
      if v is not None:
        self._merge_region_trees(dst_tree[k], v, pid)

  def _get_region_tree_item_and_unconsumed_path(self, region_tree, path, parent_key=''):
    '''Return the region_tree item specified by path. An item can be a a folder
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
    '''
    # Handle valid item within region tree.
    if not len(path):
      if region_tree is None:
        return parent_key, []
      else:
        return region_tree, []
    # Handle valid exit through PID.
    if region_tree is None:
      return parent_key, path
    # Handle next level in path.
    if path[0] in region_tree.keys():
      return self._get_region_tree_item_and_unconsumed_path(
        region_tree[path[0]], path[1:], path[0]
      )
    else:
      raise path_exception.PathException('Invalid path')

    #if path[0] in region_tree.keys():
    #  if region_tree[path[0]] is None:
    #    return [path[0]], path
    #  else:

  def _region_tree_item_is_pid(self, region_tree_item):
    return isinstance(region_tree_item, basestring)
