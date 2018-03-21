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
"""Hold the list of files and folders for a directory
"""

import collections
import logging

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)


class Directory(collections.MutableSequence):
  def __init__(self, init_list=None, disable_cache=False):
    self._list = []
    if init_list is not None:
      self._list.extend(init_list)
    self.disable_cache = disable_cache

  def __len__(self):
    return len(self._list)

  def __getitem__(self, i):
    return self._list[i]

  def __delitem__(self, i):
    del self._list[i]

  def __setitem__(self, i, v):
    self._list[i] = v

  def __unicode__(self):
    return str(self._list)

  def __str__(self):
    return str(self).encode('utf-8')

  def __repr__(self):
    return str(self)

  def insert(self, i, v):
    self._list.insert(i, v)
