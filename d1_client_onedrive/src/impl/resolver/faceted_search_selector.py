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
''':mod:`faceted_search_selector`
=================================

:Synopsis:
 - Disable faceted searching once an object has been selected.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import os

# D1.

# App.
from directory import Directory, DirectoryItem
import facet_path_parser
import resolver_abc

# Set up logger for this module.
log = logging.getLogger(__name__)


class Resolver(resolver_abc.Resolver):
  def __init__(self):
    self.facet_path_parser = facet_path_parser.FacetPathParser()

  def resolve(self, path):
    facet_section, object_section = self.facet_path_parser \
      .split_path_to_facet_and_object_sections(path)
    directory = Directory()
    self.append_parent_and_self_references(directory)
    if len(object_section):
      self.append_package_items(directory, object_section)
    else:
      self.append_facet_directories(directory, facet_section)
    return directory
