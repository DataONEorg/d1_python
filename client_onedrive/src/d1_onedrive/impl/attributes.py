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
"""Hold the size and other attributes for a file or folder
"""

import logging

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)


class Attributes(object):
  def __init__(self, size=0, date=None, is_dir=False):
    self._size_ = size
    self._date_ = date
    self._is_dir_ = is_dir

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __repr__(self):
    return '{}({})'.format(self.__class__, self.__dict__)

  def size(self):
    return self._size_

  def date(self):
    return self._date_

  def is_dir(self):
    return self._is_dir_
