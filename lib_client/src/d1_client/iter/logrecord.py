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
filtered by providing arguments to getLogRecords() via the
get_log_records_arg_dict parameter.
"""

import d1_common.const


class LogRecordIterator(object):
  def __init__(
      self,
      client,
      get_log_records_arg_dict=None,
      start=0,
      count=d1_common.const.DEFAULT_SLICE_SIZE,
  ):
    self._get_log_records_arg_dict = get_log_records_arg_dict or {}
    self._client = client
    self._start = start
    self._count = count
    assert 'start' not in self._get_log_records_arg_dict
    assert 'count' not in self._get_log_records_arg_dict
    self.total = self._get_log_records().total

  def __iter__(self):
    start = self._start
    while True:
      log_pyxb = self._get_log_records(start, self._count)
      for log_entry_pyxb in log_pyxb.logEntry:
        yield log_entry_pyxb

      start += log_pyxb.count

      if start >= self.total:
        break

  def _get_log_records(self, start=0, count=0):
    return self._client.getLogRecords(
      start=start, count=count, **self._get_log_records_arg_dict
    )
