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
import d1_common.type_conversions
import d1_common.types.dataoneTypes_v2_0
import d1_common.util

import d1_client.baseclient_2_0
import d1_client.cnclient_1_2


class CoordinatingNodeClient_2_0(
    d1_client.baseclient_2_0.DataONEBaseClient_2_0,
    d1_client.cnclient_1_2.CoordinatingNodeClient_1_2,
):
  """Extend DataONEBaseClient_2_0 and CoordinatingNodeClient_1_2 with functionality
  for Coordinating nodes that was added in v2.0 of the DataONE infrastructure.

  Updated in v2:

  - CNCore.listFormats() → ObjectFormatList
  - CNRead.listObjects(session[, fromDate][, toDate][, formatId]
  - MNRead.listObjects(session[, fromDate][, toDate][, formatId]

  The base implementations of listFormats() and listObjects() handle v2 when
  called through this class.

  https://releases.dataone.org/online/api-documentation-v2.0/apis/CN_APIs.html
  """

  def __init__(self, *args, **kwargs):
    """See baseclient.DataONEBaseClient for args."""
    super(CoordinatingNodeClient_2_0, self).__init__(*args, **kwargs)

    self.logger = logging.getLogger(__file__)

    self._api_major = 2
    self._api_minor = 0
    self._bindings = d1_common.type_conversions.get_bindings_by_api_version(
      self._api_major, self._api_minor
    )

  #=========================================================================
  # Core API
  #=========================================================================

  # CNCore.delete(session, id) → Identifier
  # DELETE /object/{id}

  def deleteResponse(self, pid):
    return self.DELETE(['object', pid])

  def delete(self, pid):
    response = self.deleteResponse(pid)
    return self._read_dataone_type_response(response, 'Identifier')

  #=========================================================================
  # CNRead
  #=========================================================================

  # CNRead.synchronize(session, pid) → boolean
  # POST /synchronize

  def synchronizeResponse(self, pid, vendorSpecific=None):
    mmp_dict = {
      'pid': pid,
    }
    return self.POST(['synchronize'], fields=mmp_dict, headers=vendorSpecific)

  def synchronize(self, pid, vendorSpecific=None):
    response = self.synchronizeResponse(pid, vendorSpecific)
    return self._read_boolean_response(response)

  #=========================================================================
  # CNView
  #=========================================================================

  # CNView.view(session, theme, id) → OctetStream
  # GET /views/{theme}/{id}

  def viewResponse(self, theme, did):
    return self.GET(['views', theme, did])

  def view(self, theme, did):
    response = self.viewResponse(theme, did)
    return self._read_stream_response(response)

  # CNView.listViews(session) → OptionList
  # GET /views

  def listViewsResponse(self):
    return self.GET(['views'])

  def listViews(self):
    response = self.listViewsResponse()
    return self._read_dataone_type_response(response, 'OptionList')

  #=========================================================================
  # CNDiagnostic
  #=========================================================================

  # CNDiagnostic.echoCredentials(session) → SubjectInfo
  # GET /diag/subject

  def echoCredentialsResponse(self):
    return self.GET(['diag', 'subject'])

  def echoCredentials(self):
    response = self.echoCredentialsResponse()
    return self._read_dataone_type_response(response, 'SubjectInfo')

  # CNDiagnostic.echoSystemMetadata(session, sysmeta) → SystemMetadata
  # POST /diag/sysmeta

  def echoSystemMetadataResponse(self, sysmeta_pyxb):
    mmp_dict = {
      'sysmeta': ('sysmeta.xml', sysmeta_pyxb.toxml('utf-8')),
    }
    return self.POST(['diag', 'sysmeta'], fields=mmp_dict)

  def echoSystemMetadata(self, sysmeta_pyxb):
    response = self.echoSystemMetadataResponse(sysmeta_pyxb)
    return self._read_dataone_type_response(response, 'SystemMetadata')

  # CNDiagnostic.echoIndexedObject(session, queryEngine, sysmeta, object) → OctetStream
  # POST /diag/object

  def echoIndexedObjectResponse(self, queryEngine, sysmeta_pyxb, obj):
    mmp_dict = {
      'queryEngine': queryEngine.encode('utf-8'),
      'object': ('content.bin', obj),
      'sysmeta': ('sysmeta.xml', sysmeta_pyxb.toxml('utf-8')),
    }
    return self.POST(['diag', 'object'], fields=mmp_dict)

  def echoIndexedObject(self, queryEngine, sysmeta_pyxb, obj):
    response = self.echoIndexedObjectResponse(queryEngine, sysmeta_pyxb, obj)
    return self._read_stream_response(response)
