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
:mod:`get_and_display_data_package`
===================================

:Synopsis:
  This is an example on how to use the DataONE Client Library for Python. It
  shows how to:

  - Download a Resource Map (Data Package)
  - Parse and display the Resource Map.

:Author:
  DataONE (Dahl)

:Created:
  2013-03-04

:Requires:
  - Python 2.6 or 2.7.
  - DataONE Common Library for Python (automatically installed as a dependency)
  - DataONE Client Library for Python (sudo pip install dataone.libclient)
"""

# Stdlib
import logging

# D1
import d1_client.data_package
import d1_client.mnclient

# Config.

# The identifier (PID) of the DataONE Data Package (Resource Map) to download
# and display. Data packages have Format ID
# http://www.openarchives.org/ore/terms.
SCIENCE_OBJECT_PID = 'dakoop_test-PKG'

# BaseURL for the Member Node on which the science object resides. If the script
# is run on the same server as the Member Node, this can be localhost.
MN_BASE_URL = 'https://mn-demo-6.test.dataone.org/knb/d1/mn'
#MN_BASE_URL = 'https://localhost/mn'

# Paths to the certificate and key to use when retrieving the object. This is
# required if the object is not publicly accessible. If the certificate has the
# key embedded, the _KEY setting should be set to None. If the objects have
# public access, these can both be set to None.
CERTIFICATE_FOR_CREATE = None
CERTIFICATE_FOR_CREATE_KEY = None


def main():
  logging.basicConfig()
  logging.getLogger('').setLevel(logging.DEBUG)

  # Create a Member Node client that can be used for running commands against
  # a specific Member Node.
  client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
    MN_BASE_URL, cert_path=CERTIFICATE_FOR_CREATE,
    key_path=CERTIFICATE_FOR_CREATE_KEY
  )

  # Use the client to get a data package as a string (Format ID
  # http://www.openarchives.org/ore/terms).
  resource_map_xml = client.get(SCIENCE_OBJECT_PID).read()

  # Create a resource map parser.
  resource_map_parser = d1_client.data_package.ResourceMapParser(
    resource_map_xml
  )

  # Use the resource map parser to parse the resource map. Then display it.

  print '\nResource Map PID:'
  print resource_map_parser.get_resource_map_pid()

  print '\nTriples:'

  for s, p, o in resource_map_parser.get_all_triples():
    print 'subject:   ' + s
    print 'predicate: ' + p
    print 'object:    ' + o
    print

  print '\nAll PIDs in aggregation: '

  for pid in resource_map_parser.get_aggregated_pids():
    print 'PID: ' + pid

  print '\nSience Metadata PIDs in aggregation: '

  for pid in resource_map_parser.get_aggregated_science_metadata_pids():
    print 'PID: ' + pid

  print '\nSience Data PIDs in aggregation: '

  for pid in resource_map_parser.get_aggregated_science_data_pids():
    print 'PID: ' + pid


if __name__ == '__main__':
  main()
