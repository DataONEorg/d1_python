#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''Module d1_test_case
======================

:Synopsis: Extends unittest.TestCase with DataONE specific asserts.
:Created: 2011-04-27
:Author: DataONE (Dahl)
'''

import datetime
import unittest
import urlparse


class D1TestCase(unittest.TestCase):
  def assert_validate_method_name(self, context, method_name):
    valid_method_names = context.nodes['tier_1_methods']
    valid_method_names.extend(context.nodes['tier_2_methods'])
    valid_method_names.extend(context.nodes['tier_3_methods'])
    valid_method_names.extend(context.nodes['tier_4_methods'])
    valid_method_names.extend(context.nodes['tier_5_methods'])
    valid = False
    for valid_method_name in valid_method_names:
      if method_name == valid_method_name:
        valid = True
        break
    self.assertTrue(valid, 'Invalid method name: {0}'.format(method_name))

  def assert_response_headers(self, response):
    '''Required response headers are present.
    '''
    self.assertIn('Last-Modified', response)
    self.assertIn('Content-Length', response)
    self.assertIn('Content-Type', response)

  def assert_valid_date(self, date_str):
    self.assertTrue(datetime.datetime(*map(int, date_str.split('-'))))

  def B_object_collection_is_empty(self):
    '''Object collection is empty.
    '''
    client = test_client.TestClient(context.node['baseurl'])
    # Get object collection.
    object_list = client.listObjects(context.TOKEN)
    # Check header.
    self.assert_counts(object_list, 0, 0, 0)


def D_object_collection_is_populated(self):
  '''Object collection is populated.
  '''
  client = test_client.TestClient(context.node['baseurl'])
  # Get object collection.
  object_list = client.listObjects(context.TOKEN, count=d1_common.const.MAX_LISTOBJECTS)
  # Check header.
  self.assert_counts(object_list, 0, OBJECTS_TOTAL_DATA, OBJECTS_TOTAL_DATA)


def D_event_log_is_populated(self):
  '''Event log is populated.
  '''
  client = test_client.TestClient(context.node['baseurl'])
  logRecords = client.getLogRecords(context.TOKEN, datetime.datetime(1800, 1, 1))
  self.assertEqual(len(logRecords.logEntry), EVENTS_TOTAL)
  found = False
  for o in logRecords.logEntry:
    if o.identifier.value() == 'hdl:10255/dryad.654/mets.xml' and o.event == 'create':
      found = True
      break
  self.assertTrue(found)


def xml_validation(self):
  '''Returned XML document validates against the ObjectList schema.
  '''
  client = test_client.TestClient(context.node['baseurl'])
  response = client.listObjectsResponse(
    context.TOKEN, count=d1_common.const.MAX_LISTOBJECTS
  )
  xml_doc = response.read()
  d1_common.util.validate_xml(xml_doc)
