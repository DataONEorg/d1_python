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
''' 
Module d1_client.logrecorditerator
==================================

Implements an iterator that iterates over the entire set of LogRecords 
for a DataONE node.  Data is retrieved from the target only when required.

:Created: 2010-07-24
:Author: DataONE (Vieglais)
:Dependencies:
  - python 2.6
  
Example:

::

  import d1_client.client
  import sys
  logging.basicConfig(level=logging.INFO)
  target = "http://dev-dryad-mn.dataone.org/mn"
  client = d1_client.client.DataOneClient(target=target)
  log_record_iterator = LogRecordIterator(client)
  for event in log_record_iterator:
    print "Event    = %s" % event.event
    print "Timestamp  = %s" % event.dateLogged.isoformat()
    print "IP Addres  = %s" % event.ipAddress
    print "Identifier = %s" % event.identifier
    print "User agent = %s" % event.userAgent
    print "Subject  = %s" % event.subject
    print '-' * 79
'''

import logging


class LogRecordIterator(object):
  '''Implements an iterator that iterates over the entire set of LogRecords 
  for a DataONE node.  Data is retrieved from the target only when required.
  '''

  def __init__(self, client, startTime=None):
    '''Initializes the iterator.
    
     TODO: Extend this with date range and other restrictions

    :param DataOneClient client: The client instance for retrieving stuff.
    :param integer start: The starting index value
    '''
    self._logRecords = None
    self._czero = 0
    self._client = client
    self._pagesize = 500
    self._loadMore(start=start)

  def __iter__(self):
    return self

  def next(self):
    '''Implements the next() method for the iterator.  Returns the next 
    logEntry instance.
    '''
    if self._citem >= len(self._logRecords.logEntry):
      try:
        self._loadMore(start=self._czero + len(self._logRecords.logEntry))
      except Exception, e:
        logging.exception(e)
        raise StopIteration
      if len(self._logRecords.logEntry) < 1:
        raise StopIteration
    res = self._logRecords.logEntry[self._citem]
    self._citem += 1
    return res

  def _loadMore(self, start=0):
    '''Retrieves the next page of results
    '''
    self._czero = start
    self._citem = 0
    self._logRecords = self._client.getLogRecords(
      start=start, count=self._pagesize,
      startTime=self.startTime
    )
