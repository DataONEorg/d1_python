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
"""Generator that returns the bytes of a file in chunks
"""

import os

import d1_common.const


class FileIterator(object):
  def __init__(self, path, chunk_size=d1_common.const.DEFAULT_CHUNK_SIZE):
    self._path = path
    self._chunk_size = chunk_size
    self._byte_count = os.path.getsize(path)

  def __iter__(self):
    with open(self._path, 'rb') as f:
      while True:
        chunk_str = f.read(self._chunk_size)
        if not chunk_str:
          break
        yield chunk_str

  @property
  def size(self):
    return self._byte_count


class FileLikeObjectIterator(object):
  def __init__(self, file, chunk_size=d1_common.const.DEFAULT_CHUNK_SIZE):
    self._file = file
    self._chunk_size = chunk_size

  def __iter__(self):
    while True:
      chunk_str = self._file(self._chunk_size)
      if not chunk_str:
        break
      yield chunk_str

  @property
  def size(self):
    return len(self._file)
