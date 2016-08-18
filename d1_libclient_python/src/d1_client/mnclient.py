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

'''
Implements functionality defined in v1.0 of the DataONE service specifications
for Member Nodes.

See the `Member Node APIs <http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html>`_
details on how to use the methods in this class.

:Created: 2011-01-21
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import logging
import sys

# D1.
try:
    import d1_common.const
    # import d1_common.types.dataoneTypes_v1
    import d1_common.util
    import d1_common.date_time
except ImportError as e:
    sys.stderr.write('Import error: {0}\n'.format(str(e)))
    sys.stderr.write('Try: easy_install DataONE_Common\n')
    raise

# App.
import d1baseclient


class MemberNodeClient(d1baseclient.DataONEBaseClient):
  def __init__(self, *args, **kwargs):
    """See d1baseclient.DataONEBaseClient for args."""
    self.logger = logging.getLogger(__file__)
    kwargs.setdefault('api_major', 1)
    kwargs.setdefault('api_minor', 0)
    d1baseclient.DataONEBaseClient.__init__(self, *args, **kwargs)

  # ============================================================================
  # MNCore
  # ============================================================================

  # MNCore.getCapabilities() → Node
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNCore.getCapabilities

  def getCapabilitiesResponse(self, vendorSpecific=None):
      if vendorSpecific is None:
          vendorSpecific = {}
      url = self._rest_url('node')
      return self.GET(url, headers=vendorSpecific)

  def getCapabilities(self, vendorSpecific=None):
      response = self.getCapabilitiesResponse(vendorSpecific=vendorSpecific)
      return self._read_dataone_type_response(response, 'Node')

  # ============================================================================
  # MNRead
  # ============================================================================

  # MNRead.getChecksum(session, pid[, checksumAlgorithm]) → Checksum
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNRead.getChecksum

  @d1_common.util.utf8_to_unicode
  def getChecksumResponse(self, pid, checksumAlgorithm=None,
                          vendorSpecific=None):
      if vendorSpecific is None:
          vendorSpecific = {}
      url = self._rest_url('checksum/%(pid)s', pid=pid)
      query = {
          'checksumAlgorithm': checksumAlgorithm,
      }
      return self.GET(url, query=query, headers=vendorSpecific)

  @d1_common.util.utf8_to_unicode
  def getChecksum(self, pid, checksumAlgorithm=None, vendorSpecific=None):
      response = self.getChecksumResponse(
          pid,
          checksumAlgorithm,
          vendorSpecific)
      return self._read_dataone_type_response(response, 'Checksum')

  # MNRead.synchronizationFailed(session, message) → Boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNRead.synchronizationFailed

  @d1_common.util.utf8_to_unicode
  def synchronizationFailedResponse(self, message, vendorSpecific=None):
      if vendorSpecific is None:
          vendorSpecific = {}
      url = self._rest_url('error')
      mime_multipart_files = [
          ('message', 'message', message.serialize().encode('utf-8')),
      ]
      return self.POST(
          url, files=mime_multipart_files, headers=vendorSpecific)

  @d1_common.util.utf8_to_unicode
  def synchronizationFailed(self, message, vendorSpecific=None):
      response = self.synchronizationFailedResponse(message, vendorSpecific)
      return self._read_boolean_response(response)

  # ============================================================================
  # MNStorage
  # ============================================================================

  # MNStorage.create(session, pid, object, sysmeta) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNStorage.create

  @d1_common.util.utf8_to_unicode
  def createResponse(self, pid, obj, sysmeta, vendorSpecific=None):
      if vendorSpecific is None:
          vendorSpecific = {}
      url = self._rest_url('object')
      mime_multipart_fields = [
          ('pid', pid.encode('utf-8')),
      ]
      mime_multipart_files = [
          ('object', 'content.bin', obj),
          ('sysmeta', 'sysmeta.xml', sysmeta.toxml().encode('utf-8')),
      ]
      return self.POST(url, fields=mime_multipart_fields,
                       files=mime_multipart_files, headers=vendorSpecific)

  @d1_common.util.utf8_to_unicode
  def create(self, pid, obj, sysmeta, vendorSpecific=None):
      response = self.createResponse(pid, obj, sysmeta,
                                     vendorSpecific=vendorSpecific)
      return self._read_dataone_type_response(response, 'Identifier')

  # MNStorage.update(session, pid, object, newPid, sysmeta) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNStorage.update

  @d1_common.util.utf8_to_unicode
  def updateResponse(self, pid, obj, newPid, sysmeta, vendorSpecific=None):
      if vendorSpecific is None:
          vendorSpecific = {}
      url = self._rest_url('object/%(pid)s', pid=pid)
      mime_multipart_fields = [
          ('newPid', newPid.encode('utf-8')),
      ]
      mime_multipart_files = [
          ('object', 'content.bin', obj),
          ('sysmeta', 'sysmeta.xml', sysmeta.toxml().encode('utf-8')),
      ]
      return self.PUT(url, fields=mime_multipart_fields,
                      files=mime_multipart_files, headers=vendorSpecific)

  @d1_common.util.utf8_to_unicode
  def update(self, pid, obj, newPid, sysmeta, vendorSpecific=None):
      response = self.updateResponse(pid, obj, newPid, sysmeta,
                                     vendorSpecific=vendorSpecific)
      return self._read_dataone_type_response(response, 'Identifier')

  # MNStorage.delete(session, pid) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNStorage.delete

  @d1_common.util.utf8_to_unicode
  def deleteResponse(self, pid, vendorSpecific=None):
      if vendorSpecific is None:
          vendorSpecific = {}
      url = self._rest_url('object/%(pid)s', pid=pid)
      response = self.DELETE(url, headers=vendorSpecific)
      return response

  @d1_common.util.utf8_to_unicode
  def delete(self, pid, vendorSpecific=None):
      response = self.deleteResponse(pid, vendorSpecific=vendorSpecific)
      return self._read_dataone_type_response(response, 'Identifier')

  # MNStorage.systemMetadataChanged(session, pid, serialVersion, dateSysMetaLastModified) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNStorage.systemMetadataChanged

  @d1_common.util.utf8_to_unicode
  def systemMetadataChangedResponse(self, pid, serialVersion,
                                    dateSysMetaLastModified,
                                    vendorSpecific=None):
      if vendorSpecific is None:
          vendorSpecific = {}
      url = self._rest_url('dirtySystemMetadata')
      mime_multipart_fields = [
          ('pid', pid.encode('utf-8')),
          ('serialVersion', str(serialVersion)),
          ('dateSysMetaLastModified',
              d1_common.date_time.to_xsd_datetime(dateSysMetaLastModified)),
      ]
      return self.POST(
          url, fields=mime_multipart_fields, headers=vendorSpecific)

  @d1_common.util.utf8_to_unicode
  def systemMetadataChanged(self, pid, serialVersion, dateSysMetaLastModified,
                            vendorSpecific=None):
      response = self.systemMetadataChangedResponse(pid, serialVersion,
                                                    dateSysMetaLastModified,
                                                    vendorSpecific)
      return self._read_boolean_response(response)

  # ============================================================================
  # MNReplication
  # ============================================================================

  # MNReplication.replicate(session, sysmeta, sourceNode) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNReplication.replicate

  @d1_common.util.utf8_to_unicode
  def replicateResponse(self, sysmeta, sourceNode, vendorSpecific=None):
      if vendorSpecific is None:
          vendorSpecific = {}
      url = self._rest_url('replicate')
      mime_multipart_files = [
          ('sysmeta', 'sysmeta.xml', sysmeta.toxml().encode('utf-8')),
      ]
      mime_multipart_fields = [
          ('sourceNode', sourceNode.encode('utf-8')),
      ]
      return self.POST(url, files=mime_multipart_files,
                       fields=mime_multipart_fields, headers=vendorSpecific)

  @d1_common.util.utf8_to_unicode
  def replicate(self, sysmeta, sourceNode, vendorSpecific=None):
      response = self.replicateResponse(sysmeta, sourceNode, vendorSpecific)
      return self._read_boolean_response(response)

  # MNReplication.getReplica(session) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNReplication.getReplica

  @d1_common.util.utf8_to_unicode
  def getReplicaResponse(self, pid, vendorSpecific=None):
      if vendorSpecific is None:
          vendorSpecific = {}
      url = self._rest_url('replica/%(pid)s', pid=pid)
      return self.GET(url, headers=vendorSpecific)

  def getReplica(self, pid, vendorSpecific=None):
      response = self.getReplicaResponse(pid, vendorSpecific)
      return self._read_stream_response(response)
