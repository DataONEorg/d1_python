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
:mod:`tier_1_mn_core_getlogrecords`
===================================

:Created: 2011-04-22
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

import datetime

import context
import test_client

import d1_test_case

EVENTS_TOTAL = 123


class Test040GetLogRecords(d1_test_case.D1TestCase):
  def test_010_create_events(self):
    """Event log contains the correct number of create events.
    """
    client = test_client.TestClient(context.node['baseurl'])
    log_records = client.getLogRecords(
      context.TOKEN, datetime.datetime(1800, 1, 1), event='create'
    )
    # Each object must have exactly one create event.
    # TODO: This would miss a situation where one object is missing a create
    # event and another object makes up for it by having two.
    assert log_records.total == context.object_total

  def test_020_get_total_events(self):
    """Get total number of events.
    """
    client = test_client.TestClient(context.node['baseurl'])
    log_records = client.getLogRecords(
      context.TOKEN, datetime.datetime(1800, 1, 1)
    )
    context.log_records_total = log_records.total

  @d1_test_case.skip('TODO')
  def xevent_log_contains_create_events(self):
    """Event log contains create events for all objects that are
    currently known.
    Timestamp slicing includes the correct object.
    """
    dates = []
    for object_list in context.slices:
      for object_info in object_list.objectInfo:
        dates.append(object_info.dateSysMetadataModified)
    client = test_client.TestClient(context.node['baseurl'])
    logRecords = client.getLogRecords(
      '<dummy token>', datetime.datetime(1800, 1, 1)
    )
    assert len(logRecords.logEntry) == EVENTS_TOTAL
    found = False
    for o in logRecords.logEntry:
      if o.identifier.value() == 'hdl:10255/dryad.654/mets.xml' and o.event == 'create':
        found = True
        break
    assert found
