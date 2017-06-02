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

import cnclient_1_1
import baseclient_2_0

import d1_common.util
import d1_common.const
import d1_common.types.dataoneTypes_v2_0


class CoordinatingNodeClient_2_0(
    baseclient_2_0.DataONEBaseClient_2_0,
    cnclient_1_1.CoordinatingNodeClient_1_1,
):
  """Extend DataONEBaseClient_2_0 and CoordinatingNodeClient_1_1 with functionality
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
    self.logger = logging.getLogger(__file__)
    kwargs.setdefault('api_major', 2)
    kwargs.setdefault('api_minor', 0)
    baseclient_2_0.DataONEBaseClient_2_0.__init__(self, *args, **kwargs)
    cnclient_1_1.CoordinatingNodeClient_1_1.__init__(self, *args, **kwargs)

  #=========================================================================
  # Core API
  #=========================================================================

  @d1_common.util.utf8_to_unicode
  def deleteResponse(self, pid):
    return self.DELETE(['object', pid])

  @d1_common.util.utf8_to_unicode
  def delete(self, pid):
    response = self.deleteResponse(pid)
    return self._read_dataone_type_response(response, 'Identifier')
