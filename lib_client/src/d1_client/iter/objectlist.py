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
"""Implements an iterator that iterates over the entire ObjectList for a DataONE node.
Data is retrieved from the target only when required.

The ObjectListIterator takes a CoordinatingNodeClient or MemberNodeClient together with
filters to select a set of objects. It returns an iterator object which enables using a
Python ``for`` loop for iterating over the matching objects. Using the
ObjectListIterator is appropriate in circumstances where a large percentage of the total
number of objecs is expected to be returned or when one of the limited number of filters
can be used for selecting the desired set of objects.

If more fine grained filtering is required, DataONE's Solr index should be used. It can
be accessed using the :ref:`Solr Client <solr_client>`.

Object information is retrieved from the Node only when required. This avoids storing a
large object list in memory.

The ObjectListIterator repeatedly calls the Node's ``listObjects()`` API method. The CN
implementation of this method yields only public objects and objects for which the
caller has access. This is also how ``listObjects()`` is implemented in the
:term:`Metacat` and :term:`GMN` Member Nodes. However, other MNs are free to chose how
or if to implement access control for this method.

To authenticate to the target Node, provide a valid CILogon signed certificate when
creating the CoordinatingNodeClient or MemberNodeClient.


Example:

::

  #!/usr/bin/env python
  from d1_client import d1baseclient
  from d1_client.objectlistiterator import ObjectListIterator

  # The Base URL for a DataONE Coordinating Node or Member Node.
  base_url = 'https://cn.dataone.org/cn'
  # Start retrieving objects from this position.
  start = 0
  # Maximum number of entries to retrieve.
  max = 500
  # Maximum number of entries to retrieve per call.
  pagesize = 100

  client = d1baseclient.DataONEBaseClient(base_url)
  ol = ObjectListIterator(client, start=start, pagesize=pagesize, max=max)
  counter = start
  print "---"
  print "total: %d" % len(ol)
  print "---"
  for o in ol:
    print "-"
    print "  item     : %d" % counter
    print "  pid      : %s" % o.identifier.value()
    print "  modified : %s" % o.dateSysMetadataModified
    print "  format   : %s" % o.formatId
    print "  size     : %s" % o.size
    print "  checksum : %s" % o.checksum.value()
    print "  algorithm: %s" % o.checksum.algorithm
    counter += 1

Output::

  ---
  total: 5
  ---
  -
    item     : 1
    pid      : knb-lter-lno.9.1
    modified : 2011-01-13 18:42:32.469000
    format   : eml://ecoinformatics.org/eml-2.0.1
    size     : 6751
    checksum : 9039F0388DC76B1A13B0F139520A8D90
    algorithm: MD5
  -
    item     : 2
    pid      : LB30XX_030MTV2021R00_20080516.50.1
    modified : 2011-01-12 22:51:00.774000
    format   : eml://ecoinformatics.org/eml-2.0.1
    size     : 14435
    checksum : B2200FB7FAE18A3517AA9E2EA680EE09
    algorithm: MD5
  -
    ...

"""

import http.client
import logging

import pyxb

import d1_common.types.exceptions


class ObjectListIterator(object):
    """Implements an iterator that iterates over the entire ObjectList for a DataONE
    node.

    Data is retrieved from the target only when required.

    """

    def __init__(
        self, client, start=0, fromDate=None, pagesize=500, max=-1, nodeId=None
    ):
        """Initializes the iterator.

        TODO: Extend this with date range and other restrictions

        :param client: The client instance for retrieving stuff.
        :type client: DataONEBaseClient or derivative
        :param start: The zero based starting index value (0)
        :type start: integer
        :param fromDate:
        :type fromDate: DateTime
        :param pagesize: Number of items to retrieve in a single request (page, 500)
        :type pagesize: integer
        :param max: Maximum number of items to retrieve (all)
        :type max: integer

        """
        self._log = logging.getLogger(__name__)
        self._object_list = None
        self._czero = 0
        self._citem = 0
        self._pageoffs = 0
        self._client = client

        if 0 <= max < pagesize:
            pagesize = max

        self._pagesize = pagesize

        self._fromDate = fromDate
        self._nodeId = nodeId

        self._loadMore(start=start)

        if max > 0:
            self._maxitem = max
        else:
            self._maxitem = self._object_list.total

    def __iter__(self):
        return self

    def __next__(self):
        """Implements the next() method for the iterator.

        Returns the next ObjectInfo instance. Loads more if at the end of the page and
        there's more pages to load.

        """
        self._log.debug(
            "%d / %d (%d)"
            % (self._citem, self._maxitem, len(self._object_list.objectInfo))
        )
        if self._citem >= self._maxitem:
            raise StopIteration
        if (self._pageoffs) >= len(self._object_list.objectInfo):
            self._loadMore(start=self._czero + len(self._object_list.objectInfo))
            if len(self._object_list.objectInfo) < 1:
                raise StopIteration
        res = self._object_list.objectInfo[self._pageoffs]
        self._citem += 1
        self._pageoffs += 1
        return res

    def _loadMore(self, start=0, trys=0, validation=True):
        """Retrieves the next page of results."""
        self._log.debug("Loading page starting from %d" % start)
        self._czero = start
        self._pageoffs = 0
        try:
            pyxb.RequireValidWhenParsing(validation)
            self._object_list = self._client.listObjects(
                start=start,
                count=self._pagesize,
                fromDate=self._fromDate,
                nodeId=self._nodeId,
            )
        except http.client.BadStatusLine as e:
            self._log.warning("Server responded with Bad Status Line. Retrying in 5sec")
            self._client.connection.close()
            if trys > 3:
                raise e
            trys += 1
            self._loadMore(start, trys)
        except d1_common.types.exceptions.ServiceFailure as e:
            self._log.error(e)
            if trys > 3:
                raise e
            trys += 1
            self._loadMore(start, trys, validation=False)

    def __len__(self):
        """Implements len(ObjectListIterator)"""
        return self._maxitem
