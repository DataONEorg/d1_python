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

import logging

import d1_common.const
import d1_common.date_time
import d1_common.type_conversions
import d1_common.util

import d1_client.baseclient


class MemberNodeClient(
    d1_client.baseclient.DataONEBaseClient,
):
  """Extend DataONEBaseClient by adding REST API wrappers for APIs that are available on
  Member Nodes.

  For details on how to use these methods, see:

  https://releases.dataone.org/online/api-documentation-v2.0/apis/MN_APIs.html
  """

  def __init__(self, *args, **kwargs):
    """See baseclient.DataONEBaseClient for args."""
    super().__init__(*args, **kwargs)

    self.logger = logging.getLogger(__file__)

    self._api_major = 1
    self._api_minor = 0
    self._bindings = d1_common.type_conversions.get_bindings_by_api_version(
      self._api_major, self._api_minor
    )

  # ============================================================================
  # MNCore
  # ============================================================================

  # MNCore.getCapabilities() → Node
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNCore.getCapabilities

  def getCapabilitiesResponse(self, vendorSpecific=None):
    return self.GET('node', headers=vendorSpecific)

  def getCapabilities(self, vendorSpecific=None):
    response = self.getCapabilitiesResponse(vendorSpecific=vendorSpecific)
    return self._read_dataone_type_response(response, 'Node')

  # ============================================================================
  # MNRead
  # ============================================================================

  # MNRead.getChecksum(session, pid[, checksumAlgorithm]) → Checksum
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNRead.getChecksum

  def getChecksumResponse(
      self, pid, checksumAlgorithm=None, vendorSpecific=None
  ):
    query = {
      'checksumAlgorithm': checksumAlgorithm,
    }
    return self.GET(['checksum', pid], query=query, headers=vendorSpecific)

  def getChecksum(self, pid, checksumAlgorithm=None, vendorSpecific=None):
    response = self.getChecksumResponse(pid, checksumAlgorithm, vendorSpecific)
    return self._read_dataone_type_response(response, 'Checksum')

  # MNRead.synchronizationFailed(session, message) → Boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNRead.synchronizationFailed

  def synchronizationFailedResponse(self, message, vendorSpecific=None):
    mmp_dict = {
      'message': ('message', message),
    }
    return self.POST('error', fields=mmp_dict, headers=vendorSpecific)

  def synchronizationFailed(self, message, vendorSpecific=None):
    response = self.synchronizationFailedResponse(message, vendorSpecific)
    return self._read_boolean_response(response)

  # ============================================================================
  # MNStorage
  # ============================================================================

  # MNStorage.create(session, pid, object, sysmeta) → Identifier
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNStorage.create

  def createResponse(self, pid, obj, sysmeta_pyxb, vendorSpecific=None):
    mmp_dict = {
      'pid': pid.encode('utf-8'),
      'object': ('content.bin', obj),
      'sysmeta': ('sysmeta.xml', sysmeta_pyxb.toxml('utf-8')),
    }
    return self.POST('object', fields=mmp_dict, headers=vendorSpecific)

  def create(self, pid, obj, sysmeta_pyxb, vendorSpecific=None):
    response = self.createResponse(
      pid, obj, sysmeta_pyxb, vendorSpecific=vendorSpecific
    )
    return self._read_dataone_type_response(response, 'Identifier')

  # MNStorage.update(session, pid, object, newPid, sysmeta) → Identifier
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNStorage.update

  def updateResponse(self, pid, obj, newPid, sysmeta_pyxb, vendorSpecific=None):
    mmp_dict = {
      'newPid': newPid.encode('utf-8'),
      'object': ('content.bin', obj),
      'sysmeta': ('sysmeta.xml', sysmeta_pyxb.toxml('utf-8')),
    }
    return self.PUT(['object', pid], fields=mmp_dict, headers=vendorSpecific)

  def update(self, pid, obj, newPid, sysmeta_pyxb, vendorSpecific=None):
    response = self.updateResponse(
      pid, obj, newPid, sysmeta_pyxb, vendorSpecific=vendorSpecific
    )
    return self._read_dataone_type_response(response, 'Identifier')

  # MNStorage.delete(session, pid) → Identifier
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNStorage.delete

  def deleteResponse(self, pid, vendorSpecific=None):
    response = self.DELETE(['object', pid], headers=vendorSpecific)
    return response

  def delete(self, pid, vendorSpecific=None):
    response = self.deleteResponse(pid, vendorSpecific=vendorSpecific)
    return self._read_dataone_type_response(response, 'Identifier')

  # MNStorage.systemMetadataChanged(session, pid, serialVersion, dateSysMetaLastModified) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNStorage.systemMetadataChanged

  def systemMetadataChangedResponse(
      self, pid, serialVersion, dateSysMetaLastModified, vendorSpecific=None
  ):
    mmp_dict = {
      'pid':
        pid.encode('utf-8'),
      'serialVersion':
        str(serialVersion),
      'dateSysMetaLastModified':
        d1_common.date_time.xsd_datetime_str_from_dt(dateSysMetaLastModified),
    }
    return self.POST(
      'dirtySystemMetadata', fields=mmp_dict, headers=vendorSpecific
    )

  def systemMetadataChanged(
      self, pid, serialVersion, dateSysMetaLastModified, vendorSpecific=None
  ):
    response = self.systemMetadataChangedResponse(
      pid, serialVersion, dateSysMetaLastModified, vendorSpecific
    )
    return self._read_boolean_response(response)

  # ============================================================================
  # MNReplication
  # ============================================================================

  # MNReplication.replicate(session, sysmeta, sourceNode) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNReplication.replicate

  def replicateResponse(self, sysmeta_pyxb, sourceNode, vendorSpecific=None):
    mmp_dict = {
      'sysmeta': ('sysmeta.xml', sysmeta_pyxb.toxml('utf-8')),
      'sourceNode': sourceNode.encode('utf-8'),
    }
    return self.POST('replicate', fields=mmp_dict, headers=vendorSpecific)

  def replicate(self, sysmeta_pyxb, sourceNode, vendorSpecific=None):
    response = self.replicateResponse(sysmeta_pyxb, sourceNode, vendorSpecific)
    return self._read_boolean_response(response)

  # MNRead.getReplica(session, pid) → OctetStream
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNRead.getReplica

  def getReplicaResponse(self, pid, vendorSpecific=None):
    return self.GET(['replica', pid], headers=vendorSpecific)

  def getReplica(self, pid, vendorSpecific=None):
    response = self.getReplicaResponse(pid, vendorSpecific)
    return self._read_stream_response(response)
