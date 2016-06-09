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
'''
Module d1_client.logrecorditerator
==================================

Implements an iterator that iterates over the entire set of LogRecords
for a DataONE node. Data is retrieved from the target only when required.
:Created: 2010-07-24
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''


class LogRecordIterator(object):
  '''Implements an iterator that iterates over the entire set of LogRecords
    for a DataONE node.  Data is retrieved from the target only when required.
    '''

  def __init__(self, client, fromDate=None, toDate=None, start=0, pageSize=1000):
    '''Initializes the iterator.

        :param client: The client that will be used for interacting with the CN or MN.
        :type client: cnclient.CoordinatingNodeClient or mnclient.MemberNodeClient
        :param fromDate: The earliest date for which to retrieve log records.
        :type fromDate: datetime.datetime()
        :param toDate: The latest date for which to retrieve log records.
        :type toDate: datetime.datetime()
        :param timeSlice: The time period for which to .
        :type toDate: datetime.datetime()
        '''
    self._log_records = None
    self._client = client
    self._from_date = fromDate
    self._to_date = toDate
    self._start = start
    self._page_size = pageSize
    self._log_records_idx = 0
    self._n_log_records = 0

  def __iter__(self):
    return self

  def next(self):
    '''Implements the next() method for the iterator. Returns the next
        logEntry instance.
        '''
    if self._log_records_idx == self._n_log_records:
      self._load_more()
    log_entry = self._log_records.logEntry[self._log_records_idx]
    self._log_records_idx += 1
    return log_entry

  def _load_more(self):
    '''Retrieves the next page of results.
        '''
    self._log_records_idx = 0
    self._log_records = self._client.getLogRecords(
      start=self._start,
      count=self._page_size,
      fromDate=self._from_date,
      toDate=self._to_date
    )
    self._n_log_records = len(self._log_records.logEntry)
    if not self._n_log_records:
      raise StopIteration
    self._start += self._n_log_records
