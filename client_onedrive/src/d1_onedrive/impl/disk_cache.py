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
"""Cache Python objects on disk

Cache Python objects with a limit on how many objects can be cached. When the
cache reaches a configured size, adding a new object causes the oldest object to
be removed. The oldest object is the object that was added first of the objects
still in the cache.
"""

import logging
import os
import pickle
import urllib.error
import urllib.parse
import urllib.request

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)


class DiskCache(dict):
  def __init__(self, max_items, cache_directory_path):
    self._max_items = max_items
    self._cache_directory_path = cache_directory_path
    self._make_cache_directory(cache_directory_path)
    self._n_items = self._count_items_in_cache()

  def clear(self):
    return self._clear_cache()

  def __repr__(self):
    return '{}({})'.format(self.__class__, self.__dict__)

  def __setitem__(self, key, value):
    self._delete_oldest_file_if_full()
    self._write_key_value_to_disk(key, value)
    self._n_items += 1

  def __getitem__(self, key):
    try:
      return self._read_value_of_key_from_disk(key)
    except IOError:
      raise KeyError

  def __delitem__(self, key):
    try:
      os.unlink(self._path_from_key(key))
    except OSError:
      raise KeyError
    else:
      self._n_items -= 1

  def __len__(self):
    return self._n_items

  def _count_items_in_cache(self):
    return len(os.listdir(self._cache_directory_path))

  def _clear_cache(self):
    for f in os.listdir(self._cache_directory_path):
      os.unlink(os.path.join(self._cache_directory_path, f))
    self._n_items = 0

  def _delete_oldest_file_if_full(self):
    if self._n_items == self._max_items:
      self._delete_oldest_file()
      self._n_items -= 1

  def _delete_oldest_file(self):
    # The resolution of mtime is 1 second. There is another field with
    # nanosecond resolution, but I'm not sure if it's cross platform. Since it
    # doesn't much matter which of the oldest entries are deleted, regular mtime
    # is used.
    oldest_mtime = None
    oldest_fname = None
    for f in os.listdir(self._cache_directory_path):
      mtime = os.stat(os.path.join(self._cache_directory_path, f)).st_mtime
      if oldest_mtime is None or oldest_mtime > mtime:
        oldest_mtime = mtime
        oldest_fname = f
    os.unlink(os.path.join(self._cache_directory_path, oldest_fname))

  def _path_from_key(self, key):
    return os.path.join(
      self._cache_directory_path, self._filename_from_key(key)
    )

  def _filename_from_key(self, key):
    return urllib.parse.quote(key.encode('utf-8'), safe='') # doseq=True

  def _write_key_value_to_disk(self, key, value):
    with open(self._path_from_key(key), 'wb') as f:
      pickle.dump(value, f)

  def _read_value_of_key_from_disk(self, key):
    with open(self._path_from_key(key), 'rb') as f:
      return pickle.load(f)

  def _make_cache_directory(self, cache_directory_path):
    try:
      os.makedirs(cache_directory_path)
    except OSError:
      pass

  ## Disk cashed _get_query() for faster debugging.
  #def _get_query(self, params):
  #  query_url = urllib.urlencode(params, doseq=True)
  #  sha1 = hashlib.sha1(query_url).hexdigest()
  #  try:
  #    with open(os.path.join('cache', sha1)) as f:
  #      log.debug('SOLR DISK CACHE({0}, {1})'.format(sha1, query_url))
  #      response = f.read()
  #  except IOError:
  #    log.debug("SOLR GET = %s" % query_url)
  #    response = self._solr_connection.get(query_url)
  #    with open(os.path.join('cache', sha1), 'w') as f:
  #      f.write(response)
  #  return eval(response)
