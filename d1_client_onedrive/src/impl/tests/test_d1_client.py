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
''':mod:`test_d1_client`
========================

:Synopsis:
 - Test the D1Client class.
:Author: DataONE (Dahl)
'''

# Stdlib.
import sys
import unittest

# D1.
sys.path.append('..')
import onedrive_d1_client
print d1_client.__file__

#class TestSolrClient(unittest.TestCase):
#  def setUp(self):
#    qes = query_engine_description.QueryEngineDescription()
#    qes.load('test_index/query_engine_description.xml')
#    self.s = solr_query.SolrQuery(qes)
#    self.facet_path_parser = facet_path_parser.FacetPathParser()
#
#
#  def test_100_query(self):
#    print self.s.query('/')
#
#
#  def _test_100_query(self):
#    dir_items = self.s.query('/')
#    self._assert_is_facet_name_list(dir_items)
#    dir_items = self.s.query('/@origin/#test/')
#    self._assert_is_facet_name_list(dir_items)
#
#
#  def test_200_create_facet_query_string(self):
#    str = self.s.create_facet_query_string('/test')
#    self.assertTrue(str.startswith('facet.field=origin&facet.field=noBoundingBox&facet.field=endDate'))
#    str = self.s.create_facet_query_string('/@origin/#a/@noBoundingBox/#b')
#    self.assertTrue(str.startswith('facet.field=projectText&facet.field=endDate&facet.field=family'))
#
#
#  def _assert_is_facet_name_list(self, dir_items):
#    for dir_item in dir_items:
#      self.assertTrue(self.facet_path_parser.is_facet_name(dir_item))
#
#
#if __name__ == "__main__":
#  unittest.main()
