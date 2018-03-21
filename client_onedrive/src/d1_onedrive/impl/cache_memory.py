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
"""Cache Python objects in memory

Cache Python objects with a limit on how many objects can be cached. When the
cache reaches a configured size, adding a new object causes the oldest object to
be removed. The oldest object is the object that was added first of the objects
still in the cache.
"""

import logging

from . import util

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)


class Cache(dict):
  def __init__(self, max_items):
    self._max_items = max_items
    self._keys = []
    self._data = {}

  def __repr__(self):
    return '{}({})'.format(self.__class__, self.__dict__)

  def __setitem__(self, key, value):
    if key not in self._data:
      self._keys.append(key)
    self._delete_oldest_item_if_full()
    self._data[key] = value

  def __getitem__(self, key):
    return self._data[key]

  def __delitem__(self, key):
    del self._data[key]
    self._keys.remove(key)

  def __len__(self):
    return len(self._data)

  def keys(self):
    return list(self._keys)

  def copy(self):
    copyDict = dict()
    copyDict._data = self._data.copy()
    copyDict._keys = self._keys[:]
    return copyDict

  def log_dump(self):
    log.debug('-' * 100)
    log.debug('Cache:')
    util.log_dump(self._data)
    log.debug('-' * 100)

  # Private.

  def _delete_oldest_item_if_full(self):
    if len(self) == self._max_items:
      self._delete_oldest_item()

  def _delete_oldest_item(self):
    oldest_key = self._keys[0]
    del self[oldest_key]
