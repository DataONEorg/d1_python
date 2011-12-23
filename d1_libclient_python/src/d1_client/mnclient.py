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
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6

This module implements MemberNodeClient, which extends DataONEBaseClient
with functionality specific to Member Nodes.
'''

# Stdlib.
import logging
import sys
import urlparse

# D1.
import d1_common.const
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.util

# App.
import d1baseclient
import objectlistiterator


class MemberNodeClient(d1baseclient.DataONEBaseClient):
  def __init__(self,
               base_url,
               timeout=d1_common.const.RESPONSE_TIMEOUT, 
               defaultHeaders=None,
               cert_path=None, 
               key_path=None, 
               strict=True, 
               capture_response_body=False,
               version='v1'):
    '''Connect to a DataONE Member Node.
    
    :param base_url: DataONE Node REST service BaseURL
    :type host: string
    :param timeout: Time in seconds that requests will wait for a response.
    :type timeout: integer
    :param defaultHeaders: headers that will be sent with all requests.
    :type defaultHeaders: dictionary
    :param cert_path: Path to a PEM formatted certificate file.
    :type cert_path: string
    :param key_path: Path to a PEM formatted file that contains the private key
      for the certificate file. Only required if the certificate file does not
      itself contain a private key. 
    :type key_path: string
    :param strict: Raise BadStatusLine if the status line can’t be parsed
      as a valid HTTP/1.0 or 1.1 status line.
    :type strict: boolean
    :param capture_response_body: Capture the response body from the last
      operation and make it available in last_response_body.
    :type capture_response_body: boolean
    :returns: None    
    '''
    d1baseclient.DataONEBaseClient.__init__(self, base_url=base_url,
      timeout=timeout, defaultHeaders=defaultHeaders, cert_path=cert_path,
      key_path=key_path, strict=strict,
      capture_response_body=capture_response_body, version=version)
    self.logger = logging.getLogger('MemberNodeClient')
    # A dictionary that provides a mapping from method name (from the DataONE
    # APIs) to a string format pattern that will be appended to the URL.
    self.methodmap.update({
      # MNCore
      'ping': u'monitor/ping',
      'getCapabilities': u'node',
      # MNRead
      'getChecksum': u'checksum/%(pid)s',      
      # MNStorage
      'create': u'object/%(pid)s',
      'update': u'object_put/%(pid)s',
      'delete': u'object/%(pid)s',
      'systemMetadataChanged': 'dirtySystemMetadata',
      # MNReplication
      'replicate': 'replicate',
      'getReplica': 'replica/%(pid)s',
    })


  # ============================================================================
  # MNCore
  # ============================================================================
  
  # MNCore.ping() → Boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNCore.ping

  def ping(self, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('ping')    
    response = self.GET(url, headers=vendorSpecific)
    return self._capture_and_get_ok_status(response)

  # MNCore.getCapabilities() → Node
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNCore.getCapabilities

  def getCapabilitiesResponse(self, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('getCapabilities')
    return self.GET(url, headers=vendorSpecific)


  def getCapabilities(self, vendorSpecific=None):
    response = self.getCapabilitiesResponse(vendorSpecific=vendorSpecific)
    return self._capture_and_deserialize(response)

  # ============================================================================
  # MNRead
  # ============================================================================

  # MNRead.getChecksum(session, pid[, checksumAlgorithm]) → Checksum
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNRead.getChecksum
    
  @d1_common.util.str_to_unicode
  def getChecksumResponse(self, pid, checksumAlgorithm=None,
                          vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}    
    url = self._rest_url('getChecksum', pid=pid)
    query = {
      'checksumAlgorithm': checksumAlgorithm,
    }
    return self.GET(url, query=query, headers=vendorSpecific)

  
  @d1_common.util.str_to_unicode
  def getChecksum(self, pid, checksumAlgorithm=None, vendorSpecific=None):
    response = self.getChecksumResponse(pid, checksumAlgorithm, vendorSpecific)
    return self._capture_and_deserialize(response)


  # ============================================================================
  # MNStorage
  # ============================================================================

  # MNStorage.create(session, pid, object, sysmeta) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNStorage.create
  
  @d1_common.util.str_to_unicode
  def createResponse(self, pid, obj, sysmeta, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('create', pid=pid)
    # Serialize sysmeta to XML.
    sysmeta_xml = sysmeta.toxml()
    mime_multipart_files = [
      ('object', 'content.bin', obj),
      ('sysmeta','sysmeta.xml', sysmeta_xml.encode('utf-8')),
    ]
    return self.POST(url, files=mime_multipart_files, headers=vendorSpecific)


  @d1_common.util.str_to_unicode
  def create(self, pid, obj, sysmeta, vendorSpecific=None):
    response = self.createResponse(pid, obj, sysmeta,
                                   vendorSpecific=vendorSpecific)
    return self._capture_and_get_ok_status(response)

  # MNStorage.update(session, pid, object, newPid, sysmeta) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNStorage.update
  
  @d1_common.util.str_to_unicode
  def updateResponse(self, pid, obj, new_pid, sysmeta, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('update', pid=pid)
    headers = {}
    headers['newPid'] = new_pid
    headers.update(vendorSpecific)
    files = [
      ('object', 'content.bin', obj),
      ('sysmeta','systemmetadata.xml', sysmeta),
    ]
    # TODO: Should be PUT against /object. Instead is POST against
    # /object_put. Change when PUT support in Django is fixed.
    return self.POST(url, files=files, headers=headers)


  @d1_common.util.str_to_unicode
  def update(self, pid, obj, new_pid, sysmeta, vendorSpecific=None):
    response = self.updateResponse(pid, obj, new_pid, sysmeta,
                                   vendorSpecific=vendorSpecific)
    return self.capture_and_get_ok_status(response)

  # MNStorage.delete(session, pid) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNStorage.delete

  @d1_common.util.str_to_unicode
  def deleteResponse(self, pid, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('get', pid=pid)
    response = self.DELETE(url, headers=vendorSpecific)
    return response

  
  @d1_common.util.str_to_unicode
  def delete(self, pid, vendorSpecific=None):
    response = self.deleteResponse(pid, vendorSpecific=vendorSpecific)
    return self._capture_and_deserialize(response)

  # MNStorage.systemMetadataChanged(session, pid, serialVersion, dateSysMetaLastModified) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNStorage.systemMetadataChanged
  
  @d1_common.util.str_to_unicode
  def systemMetadataChangedResponse(self, pid, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('systemMetadataChanged')
    mime_multipart_files = [
      ('pid', 'pid', pid.toxml().encode('utf-8')),
    ]
    return self.POST(url, files=mime_multipart_files, headers=vendorSpecific)


  @d1_common.util.str_to_unicode
  def systemMetadataChanged(self, pid, vendorSpecific=None):
    response = self.systemMetadataChangedResponse(pid, vendorSpecific)
    return self._capture_and_get_ok_status(response)


  # ============================================================================
  # MNReplication
  # ============================================================================

  # MNReplication.replicate(session, sysmeta, sourceNode) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNReplication.replicate

  @d1_common.util.str_to_unicode
  def replicateResponse(self, sysmeta, sourceNode, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('replicate')
    mime_multipart_files = [
      ('sysmeta', 'sysmeta', sysmeta.toxml().encode('utf-8')),
    ]
    mime_multipart_fields = [
      ('sourceNode', sourceNode.encode('utf-8')),
    ]
    return self.POST(url, files=mime_multipart_files,
                     fields=mime_multipart_fields, headers=vendorSpecific)


  @d1_common.util.str_to_unicode
  def replicate(self, sysmeta, sourceNode, vendorSpecific=None):
    response = self.replicateResponse(sysmeta, sourceNode, vendorSpecific)
    return self._capture_and_get_ok_status(response)

  # MNReplication.getReplica(session) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNReplication.getReplica

  @d1_common.util.str_to_unicode
  def getReplica(self, pid, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('getReplica', pid=pid)
    return self.GET(url, headers=vendorSpecific)

