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
Module d1pythonitk.d1objectIterator
===================================
 
:Created: 20100122
:Author: vieglais

'''


class ObjectListIterator(object):
  '''Implements an iterator that iterates over the entire ObjectList for a 
  DataONE node.  Data is retrieved from the target only when required.
  '''

  def __init__(self, client, start=0, startTime=None):
    '''Initializes the iterator.
    
     TODO: Extend this with date range and other restrictions

    :param DataOneClient client: The client instance for retrieving stuff.
    :param integer start: The starting index value
    '''
    self._objectList = None
    self._czero = 0
    self._client = client
    self._pagesize = 500
    self.startTime = startTime
    self._loadMore(start=start)
    self._maxitem = self._objectList.total

  def __iter__(self):
    return self

  def next(self):
    '''Implements the next() method for the iterator.  Returns the next 
    ObjectInfo instance.
    '''
    if self._citem >= self._maxitem:
      raise StopIteration
    if self._citem >= len(self._objectList.objectInfo):
      self._loadMore(start=self._czero + len(self._objectList.objectInfo))
      if len(self._objectList.objectInfo) < 1:
        raise StopIteration
    res = self._objectList.objectInfo[self._citem]
    self._citem += 1
    return res

  def _loadMore(self, start=0):
    '''Retrieves the next page of results
    '''
    self._czero = start
    self._citem = 0
    self._objectList = self._client.listObjects(
      start=start, count=self._pagesize,
      startTime=self.startTime
    )

  def __len__(self):
    '''Implements len(ObjectListIterator)
    '''
    return self._maxitem

#===============================================================================
if __name__ == "__main__":
  '''A simple demonstration of the iterator.  Walks over the list of objects
  available from a given node.
  '''
  import d1pythonitk.client
  import sys
  #target = "http://dev-dryad-mn.dataone.org/mn"
  #target = "http://129.24.0.15/mn"
  target = "http://knb-mn.ecoinformatics.org/knb"
  if len(sys.argv) > 1:
    target = sys.argv[1]
  client = d1pythonitk.client.DataOneClient(target=target)
  ol = ObjectListIterator(client)
  counter = 0
  print "Total of %d items." % len(ol)
  for o in ol:
    counter += 1
    print "==== #%d ====" % counter
    print "Identifier = %s" % o.identifier
    print "Last Modified = %s" % o.dateSysMetadataModified
    print "Object Format = %s" % o.objectFormat
    print "Size (bytes) = %s" % o.size
    print "Get URL = %s" % client.getObjectUrl(id=o.identifier)
    print "Meta URL = %s" % client.getMetaUrl(id=o.identifier)
