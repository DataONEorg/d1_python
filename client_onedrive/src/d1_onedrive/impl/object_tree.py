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
"""Object Tree

Based on a source tree that contains only PIDs and queries, maintain the object
tree that is browsed through the ONEDrive filesystem.

Cache the information on disk between runs of ONEDrive.
"""

import logging
import pickle

import d1_onedrive.impl.clients.onedrive_d1_client as onedrive_d1_client
import d1_onedrive.impl.clients.onedrive_solr_client as onedrive_solr_client
import d1_onedrive.impl.onedrive_exceptions as onedrive_exceptions


class ObjectTree():
  def __init__(self, options, source_tree):
    self._options = options
    self._source_tree = source_tree
    self._solr_client = onedrive_solr_client.OneDriveSolrClient(options)
    self._d1_client = onedrive_d1_client.DataONEClient(options)

  def __enter__(self):
    self._create_cache()
    self.refresh()
    return self

  def __exit__(self, type, value, traceback):
    self._pickle_cache_to_disk()

  def refresh(self):
    """Synchronize the local tree of Solr records for DataONE identifiers and
    queries with the reference tree.
    """
    if self._source_tree.cache_is_stale():
      self._source_tree.refresh()
      logging.info('Refreshing object tree')
      self._init_cache()
      self.sync_cache_with_source_tree()

  def get_folder(self, path, root=None):
    """Get the contents of an object tree folder"""
    return self._get_cache_folder_recursive(path, root)

  def get_object_tree_folder_name(self, object_tree_folder):
    return object_tree_folder['name']

  def get_object_record(self, pid):
    """Get an object that has already been cached in the object tree.
    Caching happens when the object tree is refreshed.
    """
    try:
      return self._cache['records'][pid]
    except KeyError:
      raise onedrive_exceptions.ONEDriveException('Unknown PID')

  def get_object_record_with_sync(self, pid):
    """Get an object that may not currently be in the cache. If the object is
    not in the cache, an attempt is made to retrieve the record from a CN on the
    fly. If the object is found, it is cached before being returned to the user.
    This allows the object tree caching system to be used for objects that are
    not in the object tree. ONEDrive uses this functionality for the FlatSpace
    folder. """
    try:
      return self._cache['records'][pid]
    except KeyError:
      return self._get_uncached_object_record(pid)

  def add_object_to_cache(self, pid):
    """Attempt to add a specific object to the cache. Objects are normally only
    added to the object tree during refresh. This method is used by the
    FlatSpace resolver.
    """
    self._create_cache_item_for_pid(None, pid)

  def get_science_object(self, pid):
    return self._d1_client.get_science_object(pid)

  def get_system_metadata(self, pid):
    return self._d1_client.get_system_metadata_as_string(pid)

  def get_source_tree_folder(self, path):
    return self._source_tree.get_filtered_sub_tree(path)

  def _get_individually_synced_object_pids(self):
    return list(self._cache['individually_synced'].keys())

  #
  # Private.
  #

  def _create_cache(self):
    self._init_cache()
    self._unpickle_cache_from_disk()

  def _init_cache(self):
    self._cache = {'tree': {}, 'records': {}, 'individually_synced': {}}

  def _get_uncached_object_record(self, pid):
    self._create_cache_item_for_pid(None, pid)
    try:
      return self._cache['records'][pid]
    except KeyError:
      raise onedrive_exceptions.ONEDriveException('Unknown PID')

  def _unpickle_cache_from_disk(self):
    try:
      with open(self._options.object_tree_cache_path, 'rb') as f:
        self._cache = pickle.load(f)
    except (IOError, pickle.PickleError):
      pass

  def _pickle_cache_to_disk(self):
    with open(self._options.object_tree_cache_path, 'wb') as f:
      pickle.dump(self._cache, f)

  def sync_cache_with_source_tree(self):
    for folder, path in self._source_tree.iterate_filtered_tree():
      self._add_filtered_tree_to_cache(folder, path)

  def _add_filtered_tree_to_cache(self, filtered_tree, path):
    cache_folder = self._get_or_create_cache_folder_recursive(path)
    self._create_cache_items(cache_folder, filtered_tree)

  def _get_or_create_cache_folder_recursive(
      self, path, folder=None, rpath=None
  ):
    if folder is None:
      folder = self._cache['tree']
    if rpath is None:
      rpath = []
    dirs = folder.setdefault('dirs', {})
    if not path:
      return folder
    return self._get_or_create_cache_folder_recursive(
      path[1:], dirs.setdefault(path[0], {'name': path[0]}), rpath + [path[0]]
    )

  def _create_cache_items(self, cache_folder, source_tree_folder):
    items = cache_folder.setdefault('items', {})
    self._create_cache_item_for_pids(items, source_tree_folder)
    self._create_cache_items_for_queries(items, source_tree_folder)

  def _create_cache_item_for_pids(self, cache_folder, source_tree_folder):
    for pid in source_tree_folder['identifiers']:
      self._create_cache_item_for_pid(cache_folder, pid)

  def _create_cache_item_for_pid(self, cache_folder, pid):
    """The source tree can contain identifiers that are no longer valid (or
    were never valid). Any items for which a Solr record cannot be retrieved are
    silently skipped.
    """
    try:
      record = self._solr_client.get_solr_record(pid)
    except onedrive_exceptions.ONEDriveException:
      pass
    else:
      self._create_cache_item(cache_folder, record)

  def _create_cache_items_for_queries(self, cache_folder, source_tree_folder):
    for query in source_tree_folder['queries']:
      self._create_cache_items_for_query(cache_folder, query)

  def _create_cache_items_for_query(self, cache_folder, query):
    records = self._solr_client.run_solr_query(query)
    for record in records:
      self._create_cache_item(cache_folder, record)

  def _create_cache_item(self, cache_folder, record):
    if cache_folder is not None:
      cache_folder[record['id']] = True
    else:
      self._cache['individually_synced'][record['id']] = True
    self._cache['records'][record['id']] = record

  def _get_cache_folder_recursive(self, path, folder=None):
    logging.debug('path={}'.format(path))
    if folder is None:
      folder = self._cache['tree']
    if not path:
      return folder
    try:
      return self._get_cache_folder_recursive(path[1:], folder['dirs'][path[0]])
    except KeyError:
      raise onedrive_exceptions.ONEDriveException('Invalid path')
