
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
import asyncio
import datetime
import logging
import pprint
import ssl

import aiohttp

import d1_common.const
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.url
import d1_common.utils.filesystem

DEFAULT_MAX_CONCURRENT_CONNECTIONS = 100
DEFAULT_RETRY_COUNT = 3


class AsyncDataONEClient:
    def __init__(
        self,
        base_url,
        timeout_sec=None,
        cert_pub_path=None,
        cert_key_path=None,
        disable_server_cert_validation=False,
        max_concurrent_connections=DEFAULT_MAX_CONCURRENT_CONNECTIONS,
        retry_count=DEFAULT_RETRY_COUNT,
    ):
        """Args:

        base_url: timeout_sec: cert_pub_path: cert_key_path:
        disable_server_cert_validation: max_concurrent_connections: Limit on concurrent
        outgoing connections enforced internally by aiohttp. retry_count:

        """
        self._logger = logging.getLogger(__name__)
        self._base_url = base_url
        self._retry_count = retry_count

        if not disable_server_cert_validation:
            ssl_ctx = ssl.create_default_context()  # cafile=
        else:
            # noinspection PyProtectedMember
            ssl_ctx = ssl._create_unverified_context()

        if cert_pub_path:
            ssl_ctx.load_cert_chain(cert_pub_path, cert_key_path)
            tcp_connector = aiohttp.TCPConnector(
                ssl_context=ssl_ctx, limit=max_concurrent_connections
            )  # ssl=False
        else:
            tcp_connector = aiohttp.TCPConnector(limit=max_concurrent_connections)

        self._session = aiohttp.ClientSession(
            connector=tcp_connector,
            timeout=aiohttp.ClientTimeout(total=timeout_sec),
            # headers={"Connection": "close"},
        )

    @property
    def session(self):
        return self._session

    async def close(self):
        await self._session.close()

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    # D1 API

    #    @contextlib.asynccontextmanager
    async def get(self, pid, vendor_specific=None):
        return await self._request_stream(
            "get", ["object", pid], vendor_specific=vendor_specific
        )

    async def get_and_save(
        self, pid, sciobj_path, create_missing_dirs=False, vendor_specific=None
    ):
        """Like MNRead.get(), but also retrieve the object bytes and store them in a
        local file at ``sciobj_path``. This method does not have the potential issue
        with excessive memory usage that get() with ``stream``=False has.

        Also see MNRead.get().

        """
        async with self.get(pid, vendor_specific=vendor_specific) as content:
            if create_missing_dirs:
                d1_common.utils.filesystem.create_missing_directories_for_file(
                    sciobj_path
                )
            with open(sciobj_path, "wb") as f:
                for chunk_str in await content.iter_chunks():
                    f.write(chunk_str)

    async def get_system_metadata(self, pid, vendor_specific=None):
        return await self._request_pyxb(
            "get", ["meta", pid], vendor_specific=vendor_specific
        )

    async def list_objects(
        self,
        fromDate=None,
        toDate=None,
        formatId=None,
        identifier=None,
        replicaStatus=None,
        nodeId=None,
        start=0,
        count=d1_common.const.DEFAULT_SLICE_SIZE,
        vendor_specific=None,
    ):
        return await self._request_pyxb(
            "get",
            "object",
            {
                "fromDate": fromDate,
                "toDate": toDate,
                "formatId": formatId,
                "identifier": identifier,
                "replicaStatus": replicaStatus,
                "nodeId": nodeId,
                "start": int(start),
                "count": int(count),
            },
            vendor_specific=vendor_specific,
        )

    async def get_log_records(
        self,
        fromDate=None,
        toDate=None,
        event=None,
        pidFilter=None,  # v1
        idFilter=None,  # v2
        start=0,
        count=d1_common.const.DEFAULT_SLICE_SIZE,
        vendor_specific=None,
    ):
        return await self._request_pyxb(
            "get",
            "log",
            {
                "fromDate": fromDate,
                "toDate": toDate,
                "event": event,
                "start": int(start),
                "count": int(count),
                "idFilter": idFilter or pidFilter,
            },
            vendor_specific=vendor_specific,
        )

    async def describe(self, pid, vendor_specific=None):
        """Get headers describing an object."""
        return await self._request_head(
            "head", ["object", pid], {}, vendor_specific=vendor_specific
        )

    async def synchronize(self, pid, vendor_specific=None):
        """Send an object synchronization request to the CN."""
        return await self._request_pyxb(
            "post",
            ["synchronize", pid],
            {},
            mmp_dict={"pid": pid},
            vendor_specific=vendor_specific,
        )

    async def list_nodes(self, vendor_specific=None):
        return await self._request_pyxb(
            "get", ["node"], {}, vendor_specific=vendor_specific
        )

    async def get_capabilities(self, *arg_list, **arg_dict):
        return await self.list_nodes(*arg_list, **arg_dict)

    # Private

    async def _request_pyxb(self, *arg_list, **arg_dict):
        async with await self._retry_request(*arg_list, **arg_dict) as response:
            self._assert_valid_response(response)
            self.dump_headers(response.headers)
            xml = await response.text()
            return d1_common.types.dataoneTypes.CreateFromDocument(xml)

    async def _request_stream(self, *arg_list, **arg_dict):
        async with await self._retry_request(*arg_list, **arg_dict) as response:
            self._assert_valid_response(response)
            return response.content
            # response.close()

    async def _request_head(self, *arg_list, **arg_dict):
        async with await self._retry_request(*arg_list, **arg_dict) as response:
            self._assert_valid_response(response)
            return response.headers
            # response.close()

    async def _retry_request(
        self,
        method_str,
        url_element_list,
        query_dict=None,
        mmp_dict=None,
        vendor_specific=None,
    ):
        e = None
        url = self._prep_url(url_element_list)
        params = self._prep_query_dict(query_dict) if query_dict else None
        data = mmp_dict
        headers = vendor_specific
        for i in range(self._retry_count):
            try:
                return await self._session.request(
                    method_str, url, params=params, data=data, headers=headers
                )
            except aiohttp.ClientError as e:
                self._logger.warning(
                    "Retrying due to exception: {}: {}".format(
                        e.__class__.__name__, str(e)
                    )
                )
                await asyncio.sleep(1.0)

        self._logger.error("Giving up after {} tries".format(self._retry_count))
        raise e

    def _prep_url(self, url_element_list):
        if isinstance(url_element_list, str):
            url_element_list = [url_element_list]
        prepped_url = d1_common.url.joinPathElements(
            self._base_url, "v2", *self._encode_path_elements(url_element_list)
        )
        self._logger.debug("Prepared URL: {}".format(prepped_url))
        return prepped_url

    def _prep_query_dict(self, query_dict):
        # self._slice_sanity_check(start, count)
        # self._date_span_sanity_check(fromDate, toDate)
        query_dict = self._remove_none_value_items(query_dict)
        query_dict = self._datetime_to_iso8601(query_dict)
        self._logger.debug("Prepared Query:\n{}".format(pprint.pformat(query_dict)))
        return query_dict

    def _encode_path_elements(self, path_element_list):
        return [
            d1_common.url.encodePathElement(v)
            if isinstance(v, (int, str))
            else d1_common.url.encodePathElement(v.value())
            for v in path_element_list
        ]

    def _assert_valid_response(self, response):
        if response.status != 200:
            raise d1_common.types.exceptions.create_exception_by_error_code(
                response.status, description=response.content
            )

    def _datetime_to_iso8601(self, query_dict):
        """Encode any datetime query parameters to ISO8601."""
        return {
            k: v if not isinstance(v, datetime.datetime) else v.isoformat()
            for k, v in list(query_dict.items())
        }

    def _remove_none_value_items(self, query_dict):
        return {k: v for k, v in list(query_dict.items()) if v is not None}

    def dump_headers(self, header_dict):
        self._logger.debug("Response headers:")
        for k, v in sorted(header_dict.items()):
            self._logger.debug("  {}: {}".format(k, v))
