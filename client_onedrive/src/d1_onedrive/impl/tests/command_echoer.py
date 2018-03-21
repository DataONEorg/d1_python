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
"""Echo commands back for unit testing / TDD.
"""

import logging

# Set up logger for this module.
log = logging.getLogger(__name__)


class CommandEchoer():
  def __init__(self):
    pass

  def solr_query_raw(self, query_string):
    return query_string

  def solr_query(self, applied_facets=None, filter_queries=None):
    return applied_facets, filter_queries

  def get_science_object_through_cache(self, pid):
    return pid

  def get_system_metadata_through_cache(self, pid):
    return pid
