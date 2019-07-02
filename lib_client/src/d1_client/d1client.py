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
import io
import logging
import pathlib

import d1_common.const
import d1_common.object_format_cache
import d1_common.system_metadata
import d1_common.type_conversions
import d1_common.types.exceptions


import d1_client.cnclient
import d1_client.cnclient_2_0
import d1_client.mnclient
import d1_client.mnclient_1_2
import d1_client.mnclient_2_0


BASE_URL_TO_NODE_ID_DICT = {}


class DataONEClient(
    d1_client.mnclient_2_0.MemberNodeClient_2_0,
    d1_client.cnclient_2_0.CoordinatingNodeClient_2_0,
):
    """Perform high level operations against the DataONE infrastructure.

    The other Client classes are specific to CN or MN and to architecture version. This
    class provides a more abstract interface that can be used for interacting with any
    DataONE node regardless of type and version.

    """

    def __init__(self, *args, **kwargs):
        """See baseclient.DataONEBaseClient for args."""
        super().__init__(*args, **kwargs)
        self._log = logging.getLogger(__name__)
        self.object_format_cache = d1_common.object_format_cache.ObjectFormatListCache()

    def create_sciobj(
        self, pid, format_id, sciobj, vendor_specific_dict=None, **sysmeta_dict
    ):
        """Create a Science Object on a Memeber Node.

        Wrapper for MNStorage.create() that includes semi-automatic generation of System
        Metadata.

        Args:
            pid: str
                Persistent Identifier.

            format_id: str
                formatId of the Science Object.

            sciobj: str, bytes or file-like stream
                str: Path to file
                bytes: Bytes
                file-like stream: lxml.etree of XML doc to validate

            vendor_specific_dict: dict
                Pass additional, vendor specific parameters.

            **sysmeta_dict: dict

                Parameters to customize the System Metadata.

                See also:
                    d1_common.system_metadata.generate_system_metadata_pyxb()
        """
        sciobj_stream = self._resolve_to_stream(sciobj)
        return self.create(
            pid,
            sciobj_stream,
            self.create_sysmeta(pid, format_id, sciobj_stream, **sysmeta_dict),
            vendor_specific_dict,
        )

    def _resolve_to_stream(self, sciobj):
        """
        Args:
            sciobj: str, bytes or file-like stream
                str: Path to file
                bytes: Bytes
                file-like stream: lxml.etree of XML doc to validate

        Returns:
            stream

        """
        if isinstance(sciobj, io.IOBase):
            return sciobj
        elif isinstance(sciobj, bytes):
            return io.BytesIO(sciobj)
        elif isinstance(sciobj, pathlib.Path):
            return sciobj.open("rb")
        else:
            raise ValueError("Unable to create stream")

    def create_sysmeta(self, pid, format_id, sciobj_stream, **sysmeta_dict):
        if not self.object_format_cache.is_valid_format_id(format_id):
            raise d1_common.types.exceptions.InvalidSystemMetadata(
                0, "Unknown formatId: {}".format(format_id)
            )
        primary_str, equivalent_set = self.auth_subj_tup
        node_id = self.get_node_id()
        return d1_common.system_metadata.generate_system_metadata_pyxb(
            pid,
            format_id,
            sciobj_stream,
            primary_str,
            primary_str,
            node_id,
            **sysmeta_dict
        )

    def get_node_id(self):
        if self.base_url not in BASE_URL_TO_NODE_ID_DICT:
            BASE_URL_TO_NODE_ID_DICT[
                self.base_url
            ] = self.getCapabilities().identifier.value()
        return BASE_URL_TO_NODE_ID_DICT[self.base_url]


def get_api_major_by_base_url(
    base_url=d1_common.const.URL_DATAONE_ROOT, *client_arg_list, **client_arg_dict
):
    """Read the Node document from a node and return an int containing the latest D1 API
    version supported by the node.

    The Node document can always be reached through the v1 API and will list services
    for v1 and any later APIs versions supported by the node.

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
        return "mn"
    elif isinstance(d1_client_obj, d1_client.cnclient.CoordinatingNodeClient):
        return "cn"
    else:
        assert False, "Unable to determine d1_client type"


def get_version_tag_by_d1_client(d1_client_obj):
    api_major, api_minor = d1_client_obj.api_version_tup
    return d1_common.type_conversions.get_version_tag(api_major)


def get_client_class_by_version_tag(api_major):
    api_major = str(api_major)
    if api_major in ("v1", "1"):
        return d1_client.mnclient_1_2.MemberNodeClient_1_2
    elif api_major in ("v2", "2"):
        return d1_client.mnclient_2_0.MemberNodeClient_2_0
    else:
        raise ValueError("Unknown DataONE API version tag: {}".format(api_major))
