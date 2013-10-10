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
''':mod:`resolver.d1_science_object`
====================================

:Synopsis:
 - Resolve a DataONE Science Object.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import os

# D1.

# App.
from d1_client_onedrive.impl import directory
from d1_client_onedrive.impl import directory_item
from d1_client_onedrive.impl import path_exception
import resolver_abc

# Set up logger for this module.
log = logging.getLogger(__name__)
# Set specific logging level for this module if specified.
try:
  log.setLevel(logging.getLevelName( \
               getattr(logging, 'ONEDRIVE_MODULES')[__name__]) )
except KeyError:
  pass


class Resolver(resolver_abc.Resolver):
  def __init__(self, options, command_processor):
    self._options = options
    self.command_processor = command_processor

  def get_attributes(self, path):
    raise path_exception.PathException('<not implemented>')

  def get_directory(self, path):
    raise path_exception.PathException('<not implemented>')

    #reading the object bytes
    sysm = self.get_system_metadata(pid)
    if offset + size > sysm.size:
      size = sysm.size - offset
    #trigger loading of the data if necessary
    self.get(pid)
    return self.datacache[pid][offset:offset + size]
