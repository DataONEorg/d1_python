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
"""Perform high level operations against the DataONE infrastructure

The other Client classes are specific to CN or MN and to architecture version.
This class provides a more abstract interface that can be used for interacting
with any DataONE node regardless of type and version.
"""

# Stdlib
import logging
import time

# D1
import d1_common.const
import d1_common.util

# App
import cnclient_2_0
import mnclient_2_0

# Config.

# Seconds data remains in cache.
MAX_CACHE_AGE = 60

COMMANDS = ['resolve', 'total', 'list', 'meta', 'get']


def showHelp():
  print 'd1client command [options]'
  print 'Command = one of [%s]' % ",".join(COMMANDS)


class DataONEObject(object):
  def __init__(
      self, pid, cnBaseUrl=d1_common.const.URL_DATAONE_ROOT, forcenew=False
  ):
    self._pid = pid
    self._locations = []
    self._relations = None
    self._relations_t = 0
    self._systemmetadata = None
    self._content = None
    self._client = None
    self._cnBaseUrl = cnBaseUrl
    if forcenew:
      self._client = DataONEClient(
        credentials=self.getCredentials(), cnBaseUrl=self._cnBaseUrl
      )

  def getCredentials(self):
    """Override this method to retrieve credentials that can be used to
        authenticate and retrieve a token for further operations.
        """
    return {}

  def _getClient(self, forcenew=False):
    """Internal method used to retrieve an instance of a DataONE client that
        can be used for interacting with the DataONE services.
        """
    if self._client is None or forcenew:
      self._client = DataONEClient(
        credentials=self.getCredentials(), cnBaseUrl=self._cnBaseUrl
      )
    return self._client

  def getLocations(self, forcenew=False):
    """Retrieve a list of node base urls known to hold a copy of this object.

        :param forcenew: The locations are cached. This causes the cache to be
          refreshed.
        :type forcenew: boolean
        :returns: List of object locations.
        :return type: PyXB ObjectLocationList.
        """
    if len(self._locations) < 1 or forcenew:
      self._getClient()
      self._locations = self._client.resolve(self._pid)
    return self._locations

  def getSystemMetadata(self, forcenew=False):
    """
        :param forcenew: The System Metadata objects are cached. This causes the
          cache to be refreshed.
        :type forcenew: boolean
        :returns: List of object locations.
        :return type: PyXB ObjectLocationList.
        """
    if self._systemmetadata is None or forcenew:
      self._getClient()
      self._systemmetadata = self._client.getSystemMetadata(self._pid)
    return self._systemmetadata

  def getRelatedObjects(self, forcenew=False):
    t = time.time()
    if t - self._relations_t > MAX_CACHE_AGE:
      forcenew = True
    if self._relations is None or forcenew:
      self._getClient()
      self._relations = self._client.getRelatedObjects(self._pid)
      self._relations_t = t
    return self._relations

  def save(self, outstr):
    """Persist a copy of the bytes of this object.

        :param out_flo: file like object open for writing.
        :type out_flo: File Like Object
        :returns: None
        :return type: NoneType
        """
    self._getClient()
    instr = self._client.get(self._pid)
    while True:
      data = instr.read(4096)
      if not data:
        return
      outstr.write(data)

  def get(self):
    self._getClient()
    return self._client.get(self._pid)


#=========================================================================


class DataONEClient(object):
  def __init__(
      self, cnBaseUrl=d1_common.const.URL_DATAONE_ROOT, credentials=None
  ):
    """DataONEClient, which uses CN- and MN clients to perform high level
        operations against the DataONE infrastructure.
        """
    if credentials is None:
      credentials = {}
    self._cnBaseUrl = cnBaseUrl
    self._cn = None
    self._mn = None
    self._credentials = credentials
    self._authToken = None
    self._sysmetacache = {}
    self._logger = logging.getLogger('DataONEClient')

  def _getCN(self, forcenew=False):
    if self._cn is None or forcenew:
      self._cn = cnclient_2_0.CoordinatingNodeClient_2_0(
        base_url=self._cnBaseUrl
      )
    return self._cn

  def _getMN(self, base_url, forcenew=False):
    if self._mn is None or forcenew:
      self._mn = mnclient_2_0.MemberNodeClient_2_0(base_url=base_url)
    elif self._mn.base_url != base_url:
      self._mn = mnclient_2_0.MemberNodeClient_2_0(base_url=base_url)
    return self._mn

  def getAuthToken(self, forcenew=False):
    """Returns an authentication token using the credentials provided when
        this client was instantiated.

        :return type: AuthToken
        """
    if self._authToken is None or forcenew:
      self._authToken = None
    return self._authToken

  @d1_common.util.utf8_to_unicode
  def resolve(self, pid):
    """
        :return type: list of base_url
        """
    cn = self._getCN()
    result = cn.resolve(pid)
    # result.objectLocation.sort(key='priority')
    res = []
    for location in result.objectLocation:
      res.append(location.baseURL)
    return res

  @d1_common.util.utf8_to_unicode
  def get(self, pid):
    """Returns a stream open for reading that returns the bytes of the object
        identified by PID.
        :return type: HTTPResponse
        """
    locations = self.resolve(pid)
    for location in locations:
      mn = self._getMN(location)
      try:
        return mn.get(pid)
      except Exception, e:
        self._logger.exception(e)
    raise Exception('Object could not be retrieved from any resolved targets')

  @d1_common.util.utf8_to_unicode
  def create(
      self,
      targetNodeId=None,
  ):
    """
        """
    pass

  @d1_common.util.utf8_to_unicode
  def getSystemMetadata(self, pid):
    """
        """
    if pid in self._sysmetacache:
      return self._sysmetacache[pid]
    cn = self._getCN()
    self._sysmetacache[pid] = cn.getSystemMetadata(pid)
    return self._sysmetacache[pid]

  @d1_common.util.utf8_to_unicode
  def getRelatedObjects(self, pid):
    """
        :return type: list of DataONEObject
        """
    relations = {
      'obsoletes': [],
      'obsoletedBy': [],
      'derivedFrom': [],
      'describedBy': [],
      'describes': [],
    }
    sysmeta_pyxb = self.getSystemMetadata(pid)
    try:
      for pid in sysmeta_pyxb.obsoletes:
        relations['obsoletes'].append(pid.value())
    except TypeError:
      pass
    try:
      for pid in sysmeta_pyxb.obsoletedBy:
        relations['obsoletedBy'].append(pid.value())
    except TypeError:
      pass
    # TODO: These need to be augmented by querying agains the appropriate resource map(s).
    #    for pid in sysmeta_pyxb.derivedFrom:
    #      relations['derivedFrom'].append(pid.value())
    #    for pid in sysmeta_pyxb.describedBy:
    #      relations['describedBy'].append(pid.value())
    #    for pid in sysmeta_pyxb.describes:
    #      relations['describes'].append(pid.value())
    return relations

  @d1_common.util.utf8_to_unicode
  def isData(self, pid):
    """Returns True is pid refers to a data object.

        Determine this by looking at the describes property of the System Metadata.
        """
    sysmeta_pyxb = self.getSystemMetadata(pid)
    return len(sysmeta_pyxb.describes) == 0

  @d1_common.util.utf8_to_unicode
  def isScienceMetadata(self, pid):
    """return True if pid refers to a science metadata object
        """
    sysmeta_pyxb = self.getSystemMetadata(pid)
    return len(sysmeta_pyxb.describes) > 0

  @d1_common.util.utf8_to_unicode
  def getScienceMetadata(self, pid):
    """Retrieve the pid for science metadata object for the specified PID. If
        PID refers to a science metadata object, then that object is returned.
        """
    if self.isScienceMetadata(pid):
      return [
        pid,
      ]
    res = []
    sysmeta_pyxb = self.getSystemMetadata(pid)
    for id in sysmeta_pyxb.describedBy:
      res.append(id.value())
    return res

  @d1_common.util.utf8_to_unicode
  def getData(self, pid):
    if self.isData(pid):
      return [
        pid,
      ]
    res = []
    sysmeta_pyxb = self.getSystemMetadata(pid)
    for id in sysmeta_pyxb.describes:
      res.append(id.value())
    return res
