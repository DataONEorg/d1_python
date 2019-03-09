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

import aiohttp
import asyncio
import ssl

import d1_common.url


class AsyncCoordinatingNodeClient_2_0:
    def __init__(self, base_url, timeout_sec=None, cert_pub_path=None, cert_key_path=None, disable_server_side_cert_validation=False):
        """
        Args:
            base_url:
            timeout_sec:
            cert_pub_path:
            cert_key_path:
            disable_server_side_cert_validation:
        """
        self._base_url = base_url
        if cert_pub_path and cert_key_path:
            # ssl_ctx = ssl.create_default_context(cafile=cert_pub_path)
            ssl_ctx = ssl._create_unverified_context()
            ssl_ctx.load_cert_chain(cert_pub_path, cert_key_path)
            # client_side_cert_connector = aiohttp.TCPConnector(ssl=False)
            client_side_cert_connector = aiohttp.TCPConnector(ssl_context=ssl_ctx)
        else:
            client_side_cert_connector = None
        self._session = aiohttp.ClientSession(
            connector=client_side_cert_connector,
            timeout=aiohttp.ClientTimeout(total=timeout_sec),

        )


    async def close(self):
        await self._session.close()


    async def describe(self, pid):
        """Get headers describing an object

        Args:
            pid:
        """
        async with self._session.head(
            self._prep_url(["v2", "object", pid])
        ) as response:
            # print('describe_headers={}'.format(response.headers))
            # print('describe_body={}'.format(await response.text()))
            return response.status

    async def synchronize(self, pid):
        """Send an object synchronization request to the CN

        Args:
            pid:
        """
        async with session.post(
            self._prep_url(["v2", "synchronize"]), data={"pid": pid}
        ) as response:
            # print('synchronize_headers={}'.format(response.headers))
            # print('synchronize_body={}'.format(await response.text()))
            return response.status

    def _prep_url(self, rest_path_list):
        """
        Args:
            rest_path_list:
        """
        if isinstance(rest_path_list, str):
            rest_path_list = [rest_path_list]
        prepped_url = d1_common.url.joinPathElements(
            # self._base_url, *self._encode_path_elements(rest_path_list)
            self._base_url, *rest_path_list
        )
        # print('prepped_url="{}"'.format(prepped_url))
        return prepped_url

    def _encode_path_elements(self, path_element_list):
        """
        Args:
            path_element_list:
        """
        return [
            d1_common.url.encodePathElement(v)
            if isinstance(v, (int, str))
            else d1_common.url.encodePathElement(v.value())
            for v in path_element_list
        ]
