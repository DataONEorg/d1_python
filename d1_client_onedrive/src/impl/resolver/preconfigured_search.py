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
''':mod:`resolver.preconfigured_search`
=======================================

:Synopsis:
 - Resolve a filesystem path to a preconfigured solr query.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import os

# D1.
from directory import Directory, DirectoryItem
import resolver_abc

# Set up logger for this module.
log = logging.getLogger(__name__)


class Resolver(resolver_abc.Resolver):
  def __init__(self):
    pass

  def resolve(self, path):
    directory = Directory()
    self.append_parent_and_self_references(directory)
    directory.append(DirectoryItem('<not implemented>', 0))
    #directory.append(DirectoryItem('Received path: {0}'.format(path), 0))
    directory.append(DirectoryItem('Received path: {0}'.format(path.replace('/', '')), 0))
    return directory
