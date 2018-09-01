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
"""Perform high level operations against the DataONE infrastructure

The other Client classes are specific to CN or MN and to architecture version.
This class provides a more abstract interface that can be used for interacting
with any DataONE node regardless of type and version.
"""
import d1_common.type_conversions

import d1_client.cnclient
import d1_client.mnclient
import d1_client.mnclient_1_2
import d1_client.mnclient_2_0


class DataONEClient(object):
  pass


def get_api_major_by_base_url(base_url, *client_arg_list, **client_arg_dict):
  """Read the Node document from a node and return an int containing the latest
  D1 API version supported by the node

  The Node document can always be reached through the v1 API and will list
  services for v1 and any later APIs versions supported by the node.
  """
  api_major = 0
  client = d1_client.mnclient.MemberNodeClient(
    base_url, *client_arg_list, **client_arg_dict
  )
  node_pyxb = client.getCapabilities()
  for service_pyxb in node_pyxb.services.service:
    if service_pyxb.available:
      api_major = max(api_major, int(service_pyxb.version[-1]))
  return api_major


def get_client_type(d1_client_obj):
  if isinstance(d1_client_obj, d1_client.mnclient.MemberNodeClient):
    return 'mn'
  elif isinstance(d1_client_obj, d1_client.cnclient.CoordinatingNodeClient):
    return 'cn'
  else:
    assert False, 'Unable to determine d1_client type'


def get_version_tag_by_d1_client(d1_client_obj):
  api_major, api_minor = d1_client_obj.api_version_tup
  return d1_common.type_conversions.get_version_tag(api_major)


def get_client_class_by_version_tag(api_major):
  api_major = str(api_major)
  if api_major in ('v1', '1'):
    return d1_client.mnclient_1_2.MemberNodeClient_1_2
  elif api_major in ('v2', '2'):
    return d1_client.mnclient_2_0.MemberNodeClient_2_0
  else:
    raise ValueError('Unknown DataONE API version tag: {}'.format(api_major))
