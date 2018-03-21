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
"""Test the OneDriveSolrClient
"""

import d1_onedrive.impl.clients.onedrive_solr_client as onedrive_solr_client

import d1_test.d1_test_case

options = {}


class TestOptions():
  pass


class TestOneDriveSolrClient(d1_test.d1_test_case.D1TestCase):
  def setup_method(self):
    options = TestOptions()
    options.base_url = 'https://localhost/'
    options.solr_query_path = ''
    options.solr_query_timeout_sec = 30
    options.max_objects_for_query = 10
    self.c = onedrive_solr_client.OneDriveSolrClient(options)

  def test_1000(self):
    """__init__()"""
    pass
