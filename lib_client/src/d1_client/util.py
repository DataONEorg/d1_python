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

import d1_common.type_conversions

import d1_client.cnclient
import d1_client.mnclient
import d1_client.mnclient_1_1
import d1_client.mnclient_2_0


def get_client_class_by_version_tag(api_major):
  api_major = str(api_major)
  if api_major in ('v1', '1'):
    return d1_client.mnclient_1_1.MemberNodeClient_1_1
  elif api_major in ('v2', '2'):
    return d1_client.mnclient_2_0.MemberNodeClient_2_0
  else:
    raise ValueError('Unknown DataONE API version tag: {}'.format(api_major))


def get_version_tag_by_d1_client(d1_client_obj):
  api_major, api_minor = d1_client_obj.api_version_tup
  return d1_common.type_conversions.get_version_tag(api_major)


def get_client_type(d1_client_obj):
  if isinstance(d1_client_obj, d1_client.mnclient.MemberNodeClient):
    return 'mn'
  elif isinstance(d1_client_obj, d1_client.cnclient.CoordinatingNodeClient):
    return 'cn'
  else:
    assert False, 'Unable to determine d1_client type'
