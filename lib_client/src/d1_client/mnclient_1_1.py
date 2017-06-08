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
import d1_common.type_conversions

import d1_client.baseclient_1_1
import d1_client.mnclient


class MemberNodeClient_1_1(
    d1_client.baseclient_1_1.DataONEBaseClient_1_1,
    d1_client.mnclient.MemberNodeClient,
):
  """Extend DataONEBaseClient_1_1 and MemberNodeClient with functionality
  for Member nodes that was added in v1.1 of the DataONE infrastructure.

  For details on how to use these methods, see:

  https://releases.dataone.org/online/api-documentation-v2.0/apis/MN_APIs.html
  """

  def __init__(self, *args, **kwargs):
    """See baseclient.DataONEBaseClient for args."""
    super(MemberNodeClient_1_1, self).__init__(*args, **kwargs)

    self.logger = logging.getLogger(__file__)

    self._api_major = 1
    self._api_minor = 1
    self._bindings = d1_common.type_conversions.get_bindings_by_api_version(
      self._api_major, self._api_minor
    )
