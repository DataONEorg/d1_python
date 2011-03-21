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
'''Module d1_client.d1client
============================

This module implements:

- DataONEClient, which uses CN- and MN clients to perform high level operations
  against the DataONE infrastructure.

- DataONEObject, which wraps a single object and adds functionality such as
  resolve and get.

:Created: 2011-01-26
:Author: DataONE (vieglais, dahl)
:Dependencies:
  - python 2.6
'''

import logging
import urlparse
from d1_common import const
from d1_common.types import exceptions
import cnclient
import mnclient
import objectlistiterator
import time

MAX_CACHE_AGE = 60 #seconds data remains in cache


class DataONEObject(object):
  def __init__(self, pid, cnBaseUrl=const.URL_DATAONE_ROOT):
    self.pid = pid
    self._locations = []
    self._relations = None
    self._relations_t = 0
    self._systemmetadata = None
    self._content = None
    self.__client = None
    self._cnBaseUrl = cnBaseUrl

  def getCredentials(self):
    '''Override this method to retrieve credentials that can be used to
    authenticate and retrieve a token for further operations.
    '''
    return {}

  def _getClient(self, forcenew=False):
    '''Internal method used to retrieve an instance of a DataONE client that
    can be used for interacting with the DataONE services.
    '''
    if self.__client is None or forcenew:
      self.__client = DataONEClient(
        credentials=self.getCredentials(
        ), cnBaseUrl=self._cnBaseUrl
      )
    return self.__client

  def getLocations(self, forcenew=False):
    '''Retrieve a list of node base urls known to hold a copy of this object.
    '''
    if len(self._locations) < 1 or forcenew:
      cli = self._getClient()
      self._locations = cli.resolve(self.pid)
    return self._locations

  def getSystemMetadata(self, forcenew=False):
    if self._systemmetadata is None or forcenew:
      cli = self._getClient()
      self._systemmetadata = cli.getSystemMetadata(self.pid)
    return self._systemmetadata

  def getRelatedObjects(self, forcenew=False):
    t = time.time()
    if t - self._relations_t > MAX_CACHE_AGE:
      forcenew = True
    if self._relations is None or forcenew:
      cli = self._getClient()
      self._relations = cli.getRelatedObjects(self.pid)
      self._relations_t = t
    return self._relations

  def load(self, outstr):
    '''Persist a copy of the bytes of this object to outstr, which is a 
    file like object open for writing.
    '''
    cli = self._getClient()
    instr = cli.get(self.pid)
    while True:
      data = instr.read(4096)
      if not data:
        return
      outstr.write(data)

  def save(self, filename):
    '''Save the object to a local file
    '''
    outstr = file(filename, "wb")
    self.realize(outstr)
    outstr.close()

  def get(self):
    cli = self._getClient()
    return cli.get(self.pid)

#===============================================================================


class DataONEClient(object):
  def __init__(self, cnBaseUrl=const.URL_DATAONE_ROOT, credentials={}):
    self.cnBaseUrl = cnBaseUrl
    self.cn = None
    self.mn = None
    self.credentials = credentials
    self.authToken = None
    self._sysmetacache = {}
    self.logger = logging.getLogger('DataONEClient')

  def _getCN(self, forcenew=False):
    if self.cn is None or forcenew:
      self.cn = cnclient.CoordinatingNodeClient(baseurl=self.cnBaseUrl)
    return self.cn

  def _getMN(self, baseurl, forcenew=False):
    if self.mn is None or forcenew:
      self.mn = mnclient.MemberNodeClient(baseurl=baseurl)
    elif self.mn.baseurl != baseurl:
      self.mn = mnclient.MemberNodeClient(baseurl=baseurl)
    return self.mn

  def getAuthToken(self, forcenew=False):
    '''Returns an authentication token using the credentials provided when
    this client was instantiated.
    
    :return type: AuthToken
    '''
    if self.authToken is None or forcenew:
      self.authToken = None
    return self.authToken

  def resolve(self, pid):
    '''
    :return type: list of baseurl
    '''
    cn = self._getCN()
    token = self.getAuthToken()
    result = cn.resolve(token, pid)
    #result.objectLocation.sort(key='priority')
    res = []
    for location in result.objectLocation:
      res.append(location.baseURL)
    return res

  def get(self, pid):
    '''Returns a stream open for reading that returns the bytes of the object
    identified by PID. 
    :return type: HTTPResponse
    '''
    locations = self.resolve(pid)
    token = self.getAuthToken()
    for location in locations:
      self.logger.debug(location)
      mn = self._getMN(location)
      try:
        return mn.get(token, pid)
      except Exception, e:
        self.logger.exception(e)
    raise Exception('Object could not be retrieved from any resolved targets')
    return None

  def create(self, targetNodeId=None, ):
    '''
    '''
    pass

  def getSystemMetadata(self, pid):
    '''
    '''
    if self._sysmetacache.has_key(pid):
      return self._sysmetacache[pid]
    cn = self._getCN()
    token = self.getAuthToken()
    self._sysmetacache[pid] = cn.getSystemMetadata(token, pid)
    return self._sysmetacache[pid]

  def getRelatedObjects(self, pid):
    '''
    :return type: list of DataONEObject
    '''
    relations = {
      'obsoletes': [],
      'obsoletedBy': [],
      'derivedFrom': [],
      'describedBy': [],
      'describes': [],
    }
    sysmeta = self.getSystemMetadata(pid)
    for pid in sysmeta.obsoletes:
      relations['obsoletes'].append(pid.value())
    for pid in sysmeta.obsoletedBy:
      relations['obsoletedBy'].append(pid.value())
    for pid in sysmeta.derivedFrom:
      relations['derivedFrom'].append(pid.value())
    for pid in sysmeta.describedBy:
      relations['describedBy'].append(pid.value())
    for pid in sysmeta.describes:
      relations['describes'].append(pid.value())
    return relations

  def isData(self, pid):
    '''Returns True is pid refers to a data object.
    
    Determine this by looking at the describes property of the system metadata.
    '''
    sysmeta = self.getSystemMetadata(pid)
    return len(sysmeta.describes) == 0

  def isScienceMetadata(self, pid):
    '''return True if pid refers to a science metadata object
    '''
    sysmeta = self.getSystemMetadata(pid)
    return len(sysmeta.describes) > 0

  def getScienceMetadata(self, pid):
    '''Retrieve the pid for science metadata object for the specified PID. If 
    PID refers to a science metadata object, then that object is returned. 
    '''
    if self.isScienceMetadata(pid):
      return [pid, ]
    res = []
    sysmeta = self.getSystemMetadata(pid)
    for id in sysmeta.describedBy:
      res.append(id.value())
    return res

  def getData(self, pid):
    if self.isData(pid):
      return [pid, ]
    res = []
    sysmeta = self.getSystemMetadata(pid)
    for id in sysmeta.describes:
      res.append(id.value())
    return res

  def getObjects(self, pids):
    '''
    '''
    pass

  def listObjects(self, start=0, count=const.DEFAULT_LISTOBJECTS):
    '''
    '''
    cli = self._getCN()
    return objectlistiterator.ObjectListIterator(cli, start=start, max=count)

#===============================================================================
import sys

COMMANDS = ['resolve', 'total', 'list', 'meta', 'get']


def showHelp():
  print 'd1client command [options]'
  print 'Command = one of [%s]' % ",".join(COMMANDS)


if __name__ == '__main__':
  if len(sys.argv) < 2:
    showHelp()
    sys.exit(1)
  command = sys.argv[1].lower()
  if command not in COMMANDS:
    showHelp()
    sys.exit(1)

  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option(
    '-b',
    '--baseurl',
    dest='baseurl',
    default='URL_DATAONE_ROOT',
    help='Use BASEURL instead of predefined targets for testing'
  )
  parser.add_option(
    '-p',
    '--pid',
    dest='pid',
    default=None,
    help='Use PID for testing existing object access'
  )
  parser.add_option(
    '-c',
    '--checksum',
    dest='checksum',
    default=None,
    help='CHECKSUM for specified PID.'
  )
  parser.add_option('-l', '--loglevel', dest='llevel', default=20,
                type='int',
                help='Reporting level: 10=debug, 20=Info, 30=Warning, ' +\
                     '40=Error, 50=Fatal')
  (options, args) = parser.parse_args(sys.argv[2:])
  if options.llevel not in [10, 20, 30, 40, 50]:
    options.llevel = 20
  logging.basicConfig(level=int(options.llevel))

  if command == 'resolve':
    if options.pid is None:
      print '-p PID is required for resolve operation.'
      sys.exit(1)
    obj = DataONEObject(options.pid)
    for loc in obj.getLocations():
      print loc
  elif command == 'total':
    cli = DataONEClient(cnBaseUrl=options.baseurl)
    objlist = cli.listObjects(start=0, count=0)
    print "total: %d" % objlist.totalObjectCount()
  elif command == 'list':
    pass
  elif command == 'meta':
    pass
  elif command == 'get':
    pass
