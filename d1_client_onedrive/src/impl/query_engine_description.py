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
''':mod:`query_engine_description`
==================================

:Synopsis:
 - Cache and manipulate a queryEngineDescription.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import os

# 3rd party.
#import pyxb

# D1.
#import d1_common.types.generated.dataoneTypes as dataoneTypes

# Set up logger for this module.
log = logging.getLogger(__name__)


class QueryEngineDescription(object):
  def __init__(self):
    self.doc = None

  def download(self, query_url):
    i = urllib.urlopen(query_url)
    self.read(i)

  def load(self, xml_path):
    i = open(xml_path, 'rb').read()
    self.read(i)

  def read(self, xml_flo):
    self.doc = dataoneTypes.CreateFromDocument(xml_flo)

  def get_searchable_facet_names(self):
    self.assert_is_initialized()
    query_field_names = []
    for qf in self.doc.queryField:
      if qf.searchable == True:
        query_field_names.append(qf.name)
    return query_field_names

  def assert_is_initialized(self):
    assert self.doc is not None
