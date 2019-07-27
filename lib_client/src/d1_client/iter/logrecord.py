#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
"""Iterate over Event Logs for Science Objects available on Member Nodes.

This is a serial implementation. See :ref:`d1_client/ref/iterators:DataONE
Iterators` for an overview of the available iterator types and implementations.

"""

import d1_common.const


class LogRecordIterator(object):
    """Log Record Iterator."""

    def __init__(
        self,
        client,
        get_log_records_arg_dict=None,
        start=0,
        count=d1_common.const.DEFAULT_SLICE_SIZE,
    ):
        """Log Record Iterator.

        Args:

          client: d1_client.cnclient.CoordinatingNodeClient or
          d1_client.mnclient.MemberNodeClient

            A client that has been initialized with the ``base_url`` and, optionally,
            other connection parameters for the DataONE node from which log records are
            to be retrieved.

            Log records for an object are typically available only to subjects that have
            elevated permissions on the object, so an unauthenticated (public)
            connection may not receive any log records. See the CoordinatingNodeClient
            and MemberNodeClient classes for details on how to authenticate.

          get_log_records_arg_dict: dict

            If this argument is set, it is passed as keyword arguments to
            `getLogRecords()`.

            The iterator calls the `getLogRecords()` API method as necessary to retrieve
            the log records. The method supports a limited set of filtering
            capabilities, Currently, `fromDate`, `toDate`, `event`, `pidFilter` and
            `idFilter`.

            To access these filters, use this argument to pass a dict which matching
            keys and the expected values. E.g.:

            ::

              { 'fromDate': datetime.datetime(2009, 1, 1) }

          start : int

            If a section of the log records have been retrieved earlier, they can be
            skipped by setting a start value.

          count : int

            The number of log records to retrieve in each `getLogRecords()` call.

            Depending on network conditions and Node implementation, changing this value
            from its default may affect performance and resource usage.

        """
        self._get_log_records_arg_dict = get_log_records_arg_dict or {}
        self._client = client
        self._start = start
        self._count = count
        assert "start" not in self._get_log_records_arg_dict
        assert "count" not in self._get_log_records_arg_dict
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
