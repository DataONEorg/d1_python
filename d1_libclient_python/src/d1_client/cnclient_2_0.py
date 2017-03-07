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

# Stdlib
import logging

# D1
import d1_common.const
import d1_common.types.dataoneTypes_v2_0
import d1_common.util

# App
import baseclient_2_0
import cnclient_1_1


class CoordinatingNodeClient_2_0(
    baseclient_2_0.DataONEBaseClient_2_0,
    cnclient_1_1.CoordinatingNodeClient_1_1,
):
  """Extend DataONEBaseClient_2_0 and CoordinatingNodeClient_1_1 with functionality
  for Coordinating nodes that was added in v2.0 of the DataONE infrastructure.

  For details on how to use these methods, see:

  https://releases.dataone.org/online/api-documentation-v2.0/apis/CN_APIs.html
  """

  def __init__(self, *args, **kwargs):
    """See baseclient.DataONEBaseClient for args."""
    self.logger = logging.getLogger(__file__)
    kwargs.setdefault('api_major', 2)
    kwargs.setdefault('api_minor', 0)
    baseclient_2_0.DataONEBaseClient_2_0.__init__(self, *args, **kwargs)
    cnclient_1_1.CoordinatingNodeClient_1_1.__init__(self, *args, **kwargs)

  #=========================================================================
  # Core API
  #=========================================================================

  # CNCore.listFormats() → ObjectFormatList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.listFormats
  # v2.0: The structure of v2_0.Types.ObjectFormat has changed.

  def listFormatsResponse(self):
    return self.GET('formats')

  def listFormats(self):
    response = self.listFormatsResponse()
    return self._read_dataone_type_response(response, 'ObjectFormatList')

  @d1_common.util.utf8_to_unicode
  def deleteObjectResponse(self, pid):
    return self.DELETE(['object', pid])

  @d1_common.util.utf8_to_unicode
  def deleteObject(self, pid):
    response = self.deleteObjectResponse(pid)
    return self._read_dataone_type_response(response, 'Identifier')

  #=========================================================================
  # Read API
  #=========================================================================

  @d1_common.util.utf8_to_unicode
  def listObjectsResponse(
      self,
      fromDate=None,
      toDate=None,
      objectFormat=None,
      replicaStatus=None,
      nodeId=None,
      start=0,
      count=d1_common.const.DEFAULT_LISTOBJECTS,
      vendorSpecific=None,
  ):
    self._slice_sanity_check(start, count)
    self._date_span_sanity_check(fromDate, toDate)
    query = {
      'fromDate': fromDate,
      'toDate': toDate,
      'formatId': objectFormat,
      'replicaStatus': replicaStatus,
      'nodeId': nodeId,
      'start': int(start),
      'count': int(count),
    }
    return self.GET('object', query=query, headers=vendorSpecific)

  @d1_common.util.utf8_to_unicode
  def listObjects(
      self,
      fromDate=None,
      toDate=None,
      objectFormat=None,
      replicaStatus=None,
      nodeId=None,
      start=0,
      count=d1_common.const.DEFAULT_LISTOBJECTS,
      vendorSpecific=None,
  ):
    response = self.listObjectsResponse(
      fromDate=fromDate, toDate=toDate, objectFormat=objectFormat,
      replicaStatus=replicaStatus, nodeId=nodeId, start=start, count=count,
      vendorSpecific=vendorSpecific
    )
    return self._read_dataone_type_response(response, 'ObjectList')
