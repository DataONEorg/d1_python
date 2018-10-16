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
Module d1_client.objectlistiterator
===================================

Implements an iterator that iterates over the entire ObjectList for a
DataONE node. Data is retrieved from the target only when required.

:Created: 2010-04-07
:Author: DataONE (Vieglais)
:Dependencies:
  - python 2.6
"""

import http.client
import logging

import pyxb

import d1_common.types.exceptions


class ObjectListIterator(object):
  """Implements an iterator that iterates over the entire ObjectList for a
  DataONE node. Data is retrieved from the target only when required.
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
    self.log = logging.getLogger(self.__class__.__name__)
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
    """Implements the next() method for the iterator.  Returns the next
    ObjectInfo instance. Loads more if at the end of the page and there's more
    pages to load.
    """
    self.log.debug(
      "%d / %d (%d)" %
      (self._citem, self._maxitem, len(self._object_list.objectInfo))
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
    """Retrieves the next page of results
    """
    self.log.debug("Loading page starting from %d" % start)
    self._czero = start
    self._pageoffs = 0
    try:
      pyxb.RequireValidWhenParsing(validation)
      self._object_list = self._client.listObjects(
        start=start, count=self._pagesize, fromDate=self._fromDate,
        nodeId=self._nodeId
      )
    except http.client.BadStatusLine as e:
      self.log.warning("Server responded with Bad Status Line. Retrying in 5sec")
      self._client.connection.close()
      if trys > 3:
        raise e
      trys += 1
      self._loadMore(start, trys)
    except d1_common.types.exceptions.ServiceFailure as e:
      self.log.error(e)
      if trys > 3:
        raise e
      trys += 1
      self._loadMore(start, trys, validation=False)

  def __len__(self):
    """Implements len(ObjectListIterator)
        """
    return self._maxitem
