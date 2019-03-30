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
"""Log Record Iterator.

Iterator that provides a convenient way to retrieve log records from a DataONE node and
iterate over the results.

Log records are automatically retrieved from the node in batches as required.


The LogRecordIterator takes a CoordinatingNodeClient or MemberNodeClient together with
filters to select a set of log records. It returns an iterator object which enables
using a Python ``for`` loop for iterating over the matching log records.

Log records are retrieved from the Node only when required. This avoids storing a large
list of records in memory.

The LogRecordIterator repeatedly calls the Node's ``getLogRecords()`` API method. The
CN implementation of this method yields log records for objects for which the caller
has access. Log records are not provided for public objects. This is also how
``getLogRecords()`` is implemented in the :term:`Metacat` Member Node. In
:term:`GMN`, the requirements for authentication for this method are configurable.
Other MNs are free to chose how or if to implement access control for this method.

To authenticate to the target Node, provide a valid CILogon signed certificate when
creating the CoordinatingNodeClient or MemberNodeClient.

See the `CNCore.getLogRecords()
<https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.getLogRecords>`_ and `MNCore.getLogRecords()
<https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNCore.getLogRecords>`_
specifications in the `DataONE Architecture Documentation
<https://releases.dataone.org/online/api-documentation-v2.0.1/index.html>`_ for more
information.

Example
-------

::

  #!/usr/bin/env python

  import d1_client.client
  import sys

  logging.basicConfig(level=logging.INFO)
  target = "https://mn-unm-1.dataone.org/mn"
  client = d1_client.client.MemberNodeClient(target=target)
  log_record_iterator = LogRecordIterator(client)
  for event in log_record_iterator:
    print "Event    = %s" % event.event
    print "Timestamp  = %s" % event.dateLogged.isoformat()
    print "IP Addres  = %s" % event.ipAddress
    print "Identifier = %s" % event.identifier
    print "User agent = %s" % event.userAgent
    print "Subject  = %s" % event.subject
    print '-' * 79

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
