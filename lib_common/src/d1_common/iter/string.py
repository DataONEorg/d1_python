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
"""Generator that returns the bytes of a string in chunks
"""

import io

import d1_common.const


class StringIterator(object):
  def __init__(self, string, chunk_size=d1_common.const.DEFAULT_CHUNK_SIZE):
    self._string = string
    self._chunk_size = chunk_size

  def __iter__(self):
    f = io.StringIO(self._string)
    while True:
      chunk_str = f.read(self._chunk_size)
      if not chunk_str:
        break
      yield chunk_str

  def __len__(self):
    return len(self._string)

  @property
  def size(self):
    return len(self._string)
