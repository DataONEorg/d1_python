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
"""LogRecordIterator

An iterator that provides a convenient way to retrieve log records from a
DataONE node and iterate over the results. Log records are automatically
retrieved from the node in batches as required. The returned log records can be
filtered by providing arguments to getLogRecords() via the getlogRecords_dict
parameter.
"""


class LogRecordIterator(object):
  def __init__(
      self,
      client,
      getlogRecords_dict=None,
      start=0,
      count=1000,
  ):
    """
    :param client: The client that will be used for calling getlogRecords()
    :param getlogRecords_dict: Parameters for getLogRecords()
    :param start: Index of first record to retrieve, default 0
    :param pageSize: Number of records to retrieve in each batch, default 1000
    """
    self._getLogRecords_dict = getlogRecords_dict or {}
    self._client = client
    self._start = start
    self._count = count
    assert 'start' not in self._getLogRecords_dict
    assert 'count' not in self._getLogRecords_dict

  def __iter__(self):
    start = self._start
    while True:
      log_pyxb = self._client.getLogRecords(
        start=start, count=self._count, **self._getLogRecords_dict
      )
      for log_entry_pyxb in log_pyxb.logEntry:
        yield log_entry_pyxb

      start += log_pyxb.count

      if start >= log_pyxb.total:
        break
