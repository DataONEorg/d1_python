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
"""
:mod:`solr_query`
=================

:Synopsis:
  This is an example on how to use the DataONE Client Library for Python. It
  shows how to:

  - Query DataONE's Solr index
  - Display the results

:Author:
  DataONE (Dahl)

:Created:
  2013-04-19

:Requires:
  - Python 2.6 or 2.7.
  - DataONE Common Library for Python (automatically installed as a dependency)
  - DataONE Client Library for Python (sudo pip install dataone.libclient)
"""

# Stdlib
import logging
import pprint

# D1
import d1_client.solr_client
import d1_client.mnclient


def main():
  logging.basicConfig()
  logging.getLogger('').setLevel(logging.DEBUG)

  # Connect to the DataONE Coordinating Nodes in the default (production) environment.
  c = d1_client.solr_client.SolrConnection()

  search_result = c.search({
    'q': 'id:[* TO *]', # Filter for search
    'rows': 10, # Number of results to return
    'fl': 'formatId', # List of fields to return for each result
  })

  pprint.pprint(search_result)


if __name__ == '__main__':
  main()
