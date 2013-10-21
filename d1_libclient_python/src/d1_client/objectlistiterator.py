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
Module d1_client.objectlistiterator
===================================

Implements an iterator that iterates over the entire ObjectList for a
DataONE node. Data is retrieved from the target only when required.

:Created: 2010-04-07
:Author: DataONE (Vieglais)
:Dependencies:
  - python 2.6

Example::

  $ python objectlistiterator.py -b "https://cn.dataone.org/cn" -m 5 -s 1000
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
    item     : 3
    pid      : SHLX00_XXXITBDXLSR01_20080220.40.1
    modified : 2011-01-14 00:07:57.851000
    format   : application/octet-stream
    size     : 108927
    checksum : 023DAF91DCFDC5AD75BA09B25A7E1A9F
    algorithm: MD5
  -
    item     : 4
    pid      : knb-lter-arc.156.1
    modified : 2011-01-13 18:30:07.686000
    format   : eml://ecoinformatics.org/eml-2.0.1
    size     : 6227
    checksum : EFF4BE6A23EB5273FCE7F4E716519A46
    algorithm: MD5
  -
    item     : 5
    pid      : SH30XX_030MXTI009R00_20070917.40.1
    modified : 2011-01-13 20:39:44.491000
    format   : application/octet-stream
    size     : 1519909
    checksum : 0D2EA212DB6D60C53E456C145C331D65
    algorithm: MD5
'''
import logging
import sys
import httplib
import time
import pyxb
import d1_common.types.exceptions

# D1
try:
  from d1_client import d1baseclient
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install DataONE_Common\n')
  raise

from optparse import OptionParser


class ObjectListIterator(object):
  '''Implements an iterator that iterates over the entire ObjectList for a
  DataONE node.  Data is retrieved from the target only when required.
  '''

  def __init__(self, client, start=0, fromDate=None, pagesize=500, max=-1):
    '''Initializes the iterator.

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
    '''
    self.log = logging.getLogger(self.__class__.__name__)
    self._objectList = None
    self._czero = 0
    self._citem = 0
    self._pageoffs = 0
    self._client = client
    if max >= 0 and max < pagesize:
      pagesize = max
    self._pagesize = pagesize
    self.fromDate = fromDate
    self._loadMore(start=start)
    if max > 0:
      self._maxitem = max
    else:
      self._maxitem = self._objectList.total

  def __iter__(self):
    return self

  def totalObjectCount(self):
    '''Returns the total number of objects in the
    '''
    return self._objectlist.total

  def next(self):
    '''Implements the next() method for the iterator.  Returns the next
    ObjectInfo instance. Loads more if at the end of the page and there's more
    pages to load.
    '''
    self.log.debug(
      "%d / %d (%d)" % (
        self._citem, self._maxitem, len(
          self._objectList.objectInfo
        )
      )
    )
    if self._citem >= self._maxitem:
      raise StopIteration
    if (self._pageoffs) >= len(self._objectList.objectInfo):
      self._loadMore(start=self._czero + len(self._objectList.objectInfo))
      if len(self._objectList.objectInfo) < 1:
        raise StopIteration
    res = self._objectList.objectInfo[self._pageoffs]
    self._citem += 1
    self._pageoffs += 1
    return res

  def _loadMore(self, start=0, trys=0, validation=True):
    '''Retrieves the next page of results
    '''
    self.log.debug("Loading page starting from %d" % start)
    self._czero = start
    self._pageoffs = 0
    try:
      pyxb.RequireValidWhenParsing(validation)
      self._objectList = self._client.listObjects(
        start=start, count=self._pagesize,
        fromDate=self.fromDate
      )
    except httplib.BadStatusLine as e:
      self.log.warn("Server responded with Bad Status Line. Retrying in 5sec")
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
    self._client.connection.close()

  def __len__(self):
    '''Implements len(ObjectListIterator)
    '''
    return self._maxitem

#===============================================================================

if __name__ == "__main__":
  '''A simple demonstration of the iterator.  Walks over the list of objects
  available from a given node. Output is in YAML.
  '''
  parser = OptionParser()
  default_base_url = 'https://cn.dataone.org/cn'
  parser.add_option(
    '-b',
    '--base_url',
    dest='base_url',
    default=default_base_url,
    help='ListObjects from BASEURL (default=%s)' % default_base_url
  )
  parser.add_option('-l', '--loglevel', dest='llevel', default=20, type='int',
                 help='Reporting level: 10=debug, 20=Info, 30=Warning, ' +\
                     '40=Error, 50=Fatal')
  parser.add_option(
    '-s',
    '--start',
    dest='start',
    default=0,
    type='int',
    help='Start retrieving objects from this position (default=0'
  )
  parser.add_option(
    '-m',
    '--max',
    dest='max',
    default=500,
    type='int',
    help='Maximum number of entries to retrieve (500)'
  )
  parser.add_option(
    '-p',
    '--page',
    dest='pagesize',
    default=100,
    type='int',
    help='Maximum number of entries to retrieve per call (100)'
  )
  (options, args) = parser.parse_args()
  if options.llevel not in [10, 20, 30, 40, 50]:
    options.llevel = 20
  logging.basicConfig(level=int(options.llevel))

  client = d1baseclient.DataONEBaseClient(options.base_url)
  ol = ObjectListIterator(
    client, start=options.start,
    pagesize=options.pagesize,
    max=options.max
  )
  counter = options.start
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
