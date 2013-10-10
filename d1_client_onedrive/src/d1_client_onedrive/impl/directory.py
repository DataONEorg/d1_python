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
''':mod:`directory`
===================

:Synopsis:
 - Hold the list of files and folders for a directory.
:Author: DataONE (Dahl)
'''

# Stdlib.
import collections
import logging
import os

# App.
import directory_item
import os_escape

# Set up logger for this module.
log = logging.getLogger(__name__)
#Set level specific for this module if specified
try:
  log.setLevel(logging.getLevelName( \
               getattr(logging,'ONEDRIVE_MODULES')[__name__]) )
except:
  pass


class Directory(collections.MutableSequence):
  def __init__(self, init_list=None):
    self.list = list()
    if init_list is not None:
      self.list.extend(init_list)

  def __len__(self):
    return len(self.list)

  def __getitem__(self, i):
    return self.list[i]

  def __delitem__(self, i):
    del self.list[i]

  def __setitem__(self, i, v):
    self.list[i] = v

  def __unicode__(self):
    return unicode(self.list)

  def __str__(self):
    return unicode(self).encode('utf-8')

  def __repr__(self):
    return str(self)

  def insert(self, i, v):
    self.list.insert(i, v)

  def names(self):
    return [d.name() for d in self.list]
