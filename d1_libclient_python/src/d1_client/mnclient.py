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
'''Module d1_client.mnclient
============================

:Created: 2011-01-21
:Author: DataONE (vieglais, dahl)
:Dependencies:
  - python 2.6

This module implements MemberNodeClient, which extends DataONEBaseClient
with functionality specific to Member Nodes.
'''
import logging
import urlparse
from d1_common import const
from d1_common import util
from d1baseclient import DataONEBaseClient
from d1_common.types import checksum_serialization
from d1_common.types import monitorlist_serialization
from d1_common.types import nodelist_serialization
from d1_common.types import pid_serialization
import objectlistiterator


class MemberNodeClient(DataONEBaseClient):

  def __init__(self, baseurl, defaultHeaders={}, timeout=10, keyfile=None,
               certfile=None, strictHttps=True):
    DataONEBaseClient.__init__(
      self,
      baseurl,
      defaultHeaders=defaultHeaders,
      timeout=timeout,
      keyfile=keyfile,
      certfile=certfile,
      strictHttps=strictHttps
    )
    self.logger = logging.getLogger('MemberNodeClient')

    self.methodmap.update(
      {
        'create': u'object/%(pid)s',
        'getchecksum': u'checksum/%(pid)s',
        'getobjectstatistics': u'monitor/object',
        'getoperationstatistics': u'monitor/event',
        'getcapabilities': u'node',
        'update': u'object_put/%(pid)s',
      }
    )

  def createResponse(self, token, pid, obj, sysmeta, vendor_specific=None):
    '''
    :param token:
    :type token: Authentication Token
    :param pid: 
    :type pid: Identifier
    :param obj:
    :type obj: Unicode or file like object
    :param sysmeta:
    :type: sysmeta: Unicode or file like object
    :returns: True on successful completion
    :return type: Boolean
    '''
    if vendor_specific is None:
      vendor_specific = {}
#    data = None
#    files = []
#    if isinstance(basestring, obj):
#      data['object'] = obj
#    else:
#      files.append(('object', 'content.bin', obj))
#    if isinstance(basestring, sysmeta):
#      data['systemmetadata'] = sysmeta
#    else:
#      files.append(('sysmeta','systemmetadata.xml', sysmeta))
    url = self.RESTResourceURL('create', pid=pid)
    headers = self._getAuthHeader(token)
    headers.update(vendor_specific)
    files = [('object', 'content.bin', obj), ('sysmeta', 'systemmetadata.xml', sysmeta), ]
    return self.POST(url, files=files, headers=headers)

  def create(self, token, pid, obj, sysmeta, vendor_specific=None):
    response = self.createResponse(token, pid, obj, sysmeta, vendor_specific)
    return self.isHttpStatusOK(response.status)

  def updateResponse(self, token, pid, obj, new_pid, sysmeta, vendor_specific=None):
    '''
    :param token:
    :type token: Authentication Token
    :param pid: The identifier of the object that is being updated 
    :type pid: Identifier
    :param obj: Science Data
    :type obj: Unicode or file like object
    :param new_pid: The identifier that will become the replacement
                    identifier for the existing object after the
                    update.
    :type new_pid: Identifier
    :param sysmeta:
    :type: sysmeta: Unicode or file like object
    :returns: True on successful completion
    :return type: Boolean
    '''
    if vendor_specific is None:
      vendor_specific = {}

    url = self.RESTResourceURL('update', pid=pid)
    headers = self._getAuthHeader(token)
    headers['newPid'] = new_pid
    headers.update(vendor_specific)
    files = [('object', 'content.bin', obj), ('sysmeta', 'systemmetadata.xml', sysmeta), ]
    return self.POST(url, files=files, headers=headers)

  def update(self, token, pid, obj, new_pid, sysmeta, vendor_specific=None):
    response = self.updateResponse(token, pid, obj, new_pid, sysmeta, vendor_specific)
    return self.isHttpStatusOK(response.status)

  def deleteResponse(self, token, pid):
    '''Delete a SciObj from MN.
    '''
    url = self.RESTResourceURL('get', pid=pid)
    response = self.DELETE(url, headers=self._getAuthHeader(token))
    return response

  def delete(self, token, pid):
    response = self.deleteResponse(token, pid)
    format = response.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = pid_serialization.Identifier()
    return deser.deserialize(response.read(), format)

  def getChecksumResponse(self, token, pid, checksumAlgorithm=None):
    url = self.RESTResourceURL('getchecksum', pid=pid)
    url_params = {'checksumAgorithm': checksumAlgorithm, }
    response = self.GET(url, url_params=url_params, headers=self._getAuthHeader(token))
    return response

  def getChecksum(self, token, pid, checksumAlgorithm=None):
    response = self.getChecksumResponse(token, pid, checksumAlgorithm)
    format = response.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = checksum_serialization.Checksum('<dummy>')
    return deser.deserialize(response.read(), format)

  def replicate(self, token, sysmeta, sourceNode):
    raise Exception('Not Implemented')

  def synchronizationFailed(self, message):
    raise Exception('Not Implemented')

  def getObjectStatisticsResponse(
    self, token, fromDate=None,
    toDate=None, format=None,
    day=None, pid=None
  ):
    url = self.RESTResourceURL('getobjectstatistics')
    url_params = {
      'fromDate': fromDate,
      'toDate': toDate,
      'format': format,
      'day': day,
      'pid': pid,
    }
    return self.GET(url, url_params=url_params, headers=self._getAuthHeader(token))

  def getObjectStatistics(
    self, token, fromDate=None,
    toDate=None, format=None,
    day=None, pid=None
  ):
    response = self.getObjectStatisticsResponse(
      token, fromDate=fromDate,
      toDate=toDate,
      format=format,
      day=day, pid=pid
    )
    format = response.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = monitorlist_serialization.MonitorList()
    if self.logger.getEffectiveLevel() == logging.DEBUG:
      logging.debug("FORMAT = %s" % format)
    return deser.deserialize(response.read(), format)

  def getOperationStatisticsResponse(
    self,
    token,
    fromDate=None,
    toDate=None,
    objectFromDate=None,
    objectToDate=None,
    requestor=None,
    day=None,
    event=None,
    format=None
  ):
    url = self.RESTResourceURL('getoperationstatistics')
    url_params = {
      'fromDate': fromDate,
      'toDate': toDate,
      'objectFromDate': objectFromDate,
      'objectToDate': objectToDate,
      'requestor': requestor,
      'day': day,
      'event': event,
      'format': format,
    }
    return self.GET(url, url_params=url_params, headers=self._getAuthHeader(token))

  def getOperationStatistics(
    self,
    token,
    fromDate=None,
    toDate=None,
    objectFromDate=None,
    objectToDate=None,
    requestor=None,
    day=None,
    event=None,
    format=None
  ):
    response = self.getOperationStatisticsResponse(
      token,
      fromDate=fromDate,
      toDate=toDate,
      objectFromDate=objectFromDate,
      objectToDate=objectToDate,
      requestor=requestor,
      day=day,
      event=event,
      format=format
    )
    format = response.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = monitorlist_serialization.MonitorList()
    return deser.deserialize(response.read(), format)

  def getStatus(self):
    raise Exception('Not Implemented')

  def getCapabilitiesResponse(self):
    url = self.RESTResourceURL('getcapabilities')
    return self.GET(url)

  def getCapabilities(self):
    response = self.getCapabilitiesResponse()
    format = response.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = nodelist_serialization.NodeList()
    return deser.deserialize(response.read(), format)

  def describeResponse(self, token, pid):
    url = self.RESTResourceURL('get', pid=pid)
    response = self.HEAD(url, headers=self._getAuthHeader(token))
    return response

  def describe(self, token, pid):
    '''This method provides a lighter weight mechanism than
    MN_crud.getSystemMetadata() for a client to determine basic properties of
    the referenced object.

    :param: (string) Identifier of object to retrieve.
    :return: mimetools.Message or raises DataONEException.

    TODO: May need to be completely removed (since clients should use CNs for
    object discovery).
    '''
    return self.describeResponse(token, pid)
