#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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

"""Utilities for use with async_client.
"""
import d1_common.type_conversions
import d1_common.types.exceptions
import d1_common.xml


async def probe_node_type_major(self, client, node_id):
    """Determine if node is a CN or MN and the major version API to
    use."""
    try:
        node_pyxb = await self.get_node_doc(client)
    except d1_common.types.exceptions.DataONEException as e:
        raise d1_common.types.exceptions.ServiceFailure(
            "Could not find a functional CN or MN at the provided BaseURL. "
            'base_url="{}" error="{}"'.format(
                self.opt_dict["baseurl"], e.friendly_format()
            )
        )

    is_cn = d1_common.type_conversions.pyxb_get_type_name(node_pyxb) == "NodeList"

    if is_cn:
        self.assert_is_known_node_id(node_pyxb, node_id)
        self._logger.info(
            "Importing from CN: {}. filtered on MN: {}".format(
                d1_common.xml.get_req_val(
                    self.find_node(node_pyxb, self.opt_dict["baseurl"]).identifier
                ),
                node_id,
            )
        )
        return "cn", "v2"
    else:
        self._logger.info(
            "Importing from MN: {}".format(
                d1_common.xml.get_req_val(node_pyxb.identifier)
            )
        )
        return "mn", self.find_node_api_version(node_pyxb)


def find_node(node_list_pyxb, base_url):
    """Search NodeList for Node that has {base_url}.

    Return matching Node or None

    """
    for node_pyxb in node_list_pyxb.node:
        if node_pyxb.baseURL == base_url:
            return node_pyxb


async def get_node_doc(client):
    """If self.opt_dict["baseurl"] is a CN, return the NodeList.

    If it's a MN, return the Node doc.

    """
    return await client.get_capabilities()


def assert_is_known_node_id(node_list_pyxb, node_id, base_url):
    """When importing from a CN, ensure that the NodeID which the ObjectList will be
    filtered by is known to the CN."""
    node_pyxb = find_node_by_id(node_list_pyxb, node_id)
    assert node_pyxb is not None, (
        "The NodeID of this GMN instance is unknown to the CN at the provided BaseURL. "
        'node_id="{}" base_url="{}"'.format(node_id, base_url)
    )


def find_node_api_version(node_pyxb):
    """Find the highest API major version supported by node."""
    max_major = 0
    for s in node_pyxb.services.service:
        max_major = max(max_major, int(s.version[1:]))
    return max_major


def find_node_by_id(node_list_pyxb, node_id):
    """Search NodeList for Node with {node_id}.

    Return matching Node or None

    """
    for node_pyxb in node_list_pyxb.node:
        # if node_pyxb.baseURL == base_url:
        if d1_common.xml.get_req_val(node_pyxb.identifier) == node_id:
            return node_pyxb
