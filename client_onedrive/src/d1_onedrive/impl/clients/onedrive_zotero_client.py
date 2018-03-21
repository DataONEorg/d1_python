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
"""Hold a local cache of the online Zotero library

Provide overview of what has changed in the online Zotero library since last
sync.

Expose a simple API to query and refresh the cache.
"""

# Zotero API:
# http://programminghistorian.org/lessons/zotero-api/intro-to-the-zotero-api

# For syncing with finer granularity in the future:
# https://www.zotero.org/support/dev/web_api/v3/syncing

import http.client
import logging
import os
import re

# App
import d1_onedrive.impl.onedrive_exceptions
# 3rd party
import pyzotero

try:
  import pickle as pickle
except ImportError:
  import pickle


class ZoteroClient(object):
  def __init__(self, options):
    self._options = options
    self._user_id = self._get_setting('ZOTERO_USER')
    self._api_access_key = self._get_setting('ZOTERO_API_ACCESS_KEY')
    self._check_api_key()
    self._zotero_client = pyzotero.zotero.Zotero(
      self._user_id, 'user', self._api_access_key
    )

  def __enter__(self):
    self._init_cache()
    self._unpickle_from_disk()
    return self

  def __exit__(self, type, value, traceback):
    self._pickle_to_disk()

  def refresh(self):
    """Refresh the local cache of the online Zotero library if stale.
    """
    while self.cache_is_stale():
      logging.info('Refreshing Zotero Library cache')
      self.force_refresh()

  def force_refresh(self):
    self._init_cache()
    self._cache['collection_trees'] = self._create_collection_trees()
    self._cache['filtered_tree'] = self.create_filtered_tree()
    self._cache['library_version'] = self._get_current_library_version()

  def get_filtered_sub_tree(self, path):
    """Get a sub-tree rooted at [path] that contains only DataONE items. The
    path is a list of collection names.
    """
    return self._get_filtered_sub_tree_recursive(path)

  def iterate_collection_trees(self):
    for collection_tree in self._cache['collection_trees']:
      yield collection_tree, [collection_tree['name']]
      for f in self.iterate_collection_tree(collection_tree):
        yield f

  def iterate_collection_tree(self, collection_tree, path=None):
    if path is None:
      path = []
    for collection in collection_tree['collections']:
      yield collection, path + [collection['name']]
      for f in self.iterate_collection_tree(
          collection, path + [collection['name']]
      ):
        yield f

  def iterate_filtered_tree(self, filtered_tree=None, path=None):
    if filtered_tree is None:
      filtered_tree = self._cache['filtered_tree']
      yield filtered_tree, []
    if path is None:
      path = []
    for f in filtered_tree['collections']:
      yield filtered_tree['collections'][f], path + [f]
      for f in self.iterate_filtered_tree(
          filtered_tree['collections'][f], path + [f]
      ):
        yield f

  def cache_is_stale(self):
    current_library_version = self._get_current_library_version()
    logging.debug(
      'Zotero online version: {}. Cached version: {}'.
      format(self._cache['library_version'], current_library_version)
    )
    return self._cache['library_version'] < current_library_version

  #
  # Private.
  #

  def _get_setting(self, key):
    try:
      return self._options.__dict__[key.lower()]
    except KeyError:
      try:
        return os.environ[key]
      except KeyError:
        raise d1_onedrive.impl.onedrive_exceptions.ONEDriveException(
          'Required value must be set in settings.py or OS environment: {}'.
          format(key)
        )

  def _init_cache(self):
    self._cache = {
      'filtered_tree': {},
      'collections': None,
      'library_version': 0,
    }

  def _create_collection_trees(self):
    collections = self._zotero_client.collections()
    return self._arrange_collections_into_collection_trees(collections)

  def _arrange_collections_into_collection_trees(self, collections):
    # The Zotero API returns the tree of collections as a flat list where each
    # collection includes the key to its parent. The root collection returns
    # False as its parent. It's more convenient to work with the collection tree
    # recursively, so the tree is built here.
    #
    # Since Python creates references instead of copies when objects are
    # appended to a list, the tree can be built with only two passes.
    t = dict((e['collectionKey'], e) for e in collections)
    for e in collections:
      e['collections'] = []
    for e in collections:
      if e['parent']:
        t[e['parent']]['collections'].append(e)
    # May now have many trees. Return the ones that start at root (they include
    # all others)
    trees = []
    for e in collections:
      if not e['parent']:
        trees.append(e)
    return trees

  def create_filtered_tree(self):
    filtered_tree = {}
    for t in self._cache['collection_trees']:
      self._create_filtered_trees_from_collections_recursive(filtered_tree, t)
    self._add_top_level_items_to_filtered_tree_root(filtered_tree)
    return filtered_tree

  def _create_filtered_trees_from_collections_recursive(
      self, filtered_tree, collection_tree
  ):
    sub_tree = {
      'collections': {},
    }
    self._add_collection_items_to_filtered_tree(sub_tree, collection_tree)
    filtered_tree.setdefault('collections', {})
    filtered_tree['collections'][collection_tree['name']] = sub_tree
    for c in collection_tree['collections']:
      self._create_filtered_trees_from_collections_recursive(sub_tree, c)

  def _add_collection_items_to_filtered_tree(self, filtered_tree, collection):
    filtered_tree.setdefault('identifiers', [])
    filtered_tree.setdefault('queries', [])
    collection_items = self._zotero_client.collection_items(
      collection['collectionKey']
    )
    for i in collection_items:
      self._add_item_to_filtered_tree_if_dataone_pid(filtered_tree, i)
      self._add_item_to_filtered_tree_if_dataone_query(filtered_tree, i)

  def _add_top_level_items_to_filtered_tree_root(self, filtered_tree):
    # Notes about top
    # https://groups.google.com/forum/#!topic/zotero-dev/MsJ3JBvpNrM
    # Parents are typically top-level objects with metadata, and children are
    # usually things like notes and file attachments.
    filtered_tree.setdefault('identifiers', [])
    filtered_tree.setdefault('queries', [])
    top_level_items = self._zotero_client.everything(self._zotero_client.top())
    for i in top_level_items:
      self._add_item_to_filtered_tree_if_dataone_pid(filtered_tree, i)
      self._add_item_to_filtered_tree_if_dataone_query(filtered_tree, i)

  def _add_item_to_filtered_tree_if_dataone_pid(self, filtered_tree, item):
    #tree.setdefault('identifiers', [])
    m = re.match(r'(https://cn.dataone.org/cn/v1/resolve/)(.*)', item['url'])
    if m:
      filtered_tree['identifiers'].append(m.group(2))

  def _add_item_to_filtered_tree_if_dataone_query(self, filtered_tree, item):
    #filtered_tree.setdefault('queries', [])
    m = re.match(
      r'(https://cn.dataone.org/cn/v1/query/solr/\?)(.*)', item['url']
    )
    if m:
      filtered_tree['queries'].append(m.group(2))

  def _unpickle_from_disk(self):
    try:
      with open(self._options.zotero_cache_path, 'rb') as f:
        self._cache = pickle.load(f)
    except (IOError, pickle.PickleError):
      pass

  def _pickle_to_disk(self):
    with open(self._options.zotero_cache_path, 'wb') as f:
      pickle.dump(self._cache, f)

  def _get_filtered_sub_tree_recursive(self, path, filtered_tree=None):
    if filtered_tree is None:
      filtered_tree = self._cache['filtered_tree']
    if not path:
      return filtered_tree
    try:
      return self._get_filtered_sub_tree_recursive(
        path[1:], filtered_tree['collections'][path[0]]
      )
    except KeyError:
      raise d1_onedrive.impl.onedrive_exceptions.ONEDriveException(
        'Invalid path'
      )

  def _check_api_key(self):
    host = 'api.zotero.org'
    url = '/users/{}/items?limit=1&key={}&v=3'.format(
      self._user_id, self._api_access_key
    )
    connection = http.client.HTTPSConnection(host)
    connection.request('GET', url)
    if connection.getresponse().status == 403:
      raise d1_onedrive.impl.onedrive_exceptions.ONEDriveException(
        'Invalid Zotero User ID or API key. UserID: {}, API Key: {}.'
        .format(self._user_id, self._api_access_key)
      )

  def _get_current_library_version(self):
    # As far as I can tell, this information is not exposed in pyzotero, so
    # I use a direct web api call.
    host = 'api.zotero.org'
    url = '/users/{}/items?limit=1&format=versions&key={}&v=3'.format(
      self._user_id, self._api_access_key
    )
    connection = http.client.HTTPSConnection(host)
    connection.request('GET', url)
    response = connection.getresponse()
    return int(response.getheader('Last-Modified-Version'))
