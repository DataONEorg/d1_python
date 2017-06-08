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

from __future__ import absolute_import

import logging

import d1_common
import d1_common.const
import d1_common.date_time
import d1_common.type_conversions
import d1_common.util

import d1_client.baseclient_2_0
import d1_client.mnclient_1_1


class MemberNodeClient_2_0(
    d1_client.baseclient_2_0.DataONEBaseClient_2_0,
    d1_client.mnclient_1_1.MemberNodeClient_1_1,
):
  """Extend DataONEBaseClient_2_0 and MemberNodeClient_1_1 with functionality
  for Member nodes that was added in v2.0 of the DataONE infrastructure.

  For details on how to use these methods, see:

  https://releases.dataone.org/online/api-documentation-v2.0/apis/MN_APIs.html
  """

  def __init__(self, *args, **kwargs):
    """See baseclient.DataONEBaseClient for args."""
    super(MemberNodeClient_2_0, self).__init__(*args, **kwargs)

    self.logger = logging.getLogger(__file__)

    self._api_major = 2
    self._api_minor = 0
    self._bindings = d1_common.type_conversions.get_bindings_by_api_version(
      self._api_major, self._api_minor
    )

  # MNStorage.updateSystemMetadata(session, pid, sysmeta) → boolean
  # http://jenkins-1.dataone.org/documentation/unstable/API-Documentation-development/apis/MN_APIs.html#MNStorage.updateSystemMetadata

  @d1_common.util.utf8_to_unicode
  def updateSystemMetadataResponse(
      self, pid, sysmeta_pyxb, vendorSpecific=None
  ):
    mmp_dict = {
      'pid': pid.encode('utf-8'),
      'sysmeta': ('sysmeta.xml', sysmeta_pyxb.toxml('utf-8')),
    }
    return self.PUT('meta', fields=mmp_dict, headers=vendorSpecific)

  @d1_common.util.utf8_to_unicode
  def updateSystemMetadata(self, pid, sysmeta_pyxb, vendorSpecific=None):
    response = self.updateSystemMetadataResponse(
      pid, sysmeta_pyxb, vendorSpecific
    )
    return self._read_boolean_response(response)
