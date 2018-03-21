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
"""Iterate over the nodes that are registered in a DataONE environment

For each Node in the environment, returns a PyXB representation of a DataONE
Node document.

https://releases.dataone.org/online/api-documentation-v2.0/
apis/Types.html#Types.Node
"""

import logging

import d1_client.cnclient_2_0

API_MAJOR = 2


class NodeListIterator(object):
  def __init__(
      self,
      base_url,
      api_major=API_MAJOR,
      client_dict=None,
      listNodes_dict=None,
  ):
    self._base_url = base_url
    self._api_major = api_major
    self._client_dict = client_dict or {}
    self._listNodes_dict = listNodes_dict

  def __iter__(self):
    client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
      self._base_url, **self._client_dict
    )
    # The NodeList type does not support slicing.
    node_list_pyxb = client.listNodes()
    logging.debug(
      'Retrieved {} Node documents'.format(len(node_list_pyxb.node))
    )
    for node_pyxb in sorted(
        node_list_pyxb.node, key=lambda x: x.identifier.value()
    ):
      yield node_pyxb
