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
''':mod:`download_test_index`
=============================

:Synopsis:
 - Download XML files for searches on each of the searchable facets.
:Author: DataONE (Dahl)
'''

# Stdlib.
import os
import shutil
import urllib

# 3rd party.
try:
  import pyxb
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install PyXB\n')
  raise

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes

# Set up logger for this module.
log = logging.getLogger(__name__)


class DownloadFacetValues(object):
  def __init__(self):
    self.doc = None

  def load(self, xml_path):
    self.doc = dataoneTypes.CreateFromDocument(open(xml_path, 'rb').read())

  def get_searchable_facet_names(self):
    self.assert_initialized()
    query_field_names = []
    for qf in self.doc.queryField:
      if qf.searchable == True:
        query_field_names.append(qf.name)
    return query_field_names

  def assert_initialized(self):
    assert (self.doc is not None)

  def download_facet_values(self):
    '''Download facet values for testing.'''
    self.load('query_engine_description.xml')
    fields = self.get_searchable_facet_names()
    for field in fields:
      print field
      url = 'https://cn-dev-unm-1.test.dataone.org/cn/v1/query/solr/?q=*%3A*&rows=0&facet=on&facet.field={0}'.format(
        field
      )
      fi = urllib.urlopen(url)
      fo = open('facet_values/facet_{0}.xml'.format(field), 'wb')
      shutil.copyfileobj(fi, fo)


if __name__ == "__main__":
  d = DownloadFacetValues()
  d.download_facet_values()
