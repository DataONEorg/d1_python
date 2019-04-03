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
"""Async ObjectList Iterator.

Fast retrieval of ObjectInfo from a DataONE Node.

"""

import asyncio
import logging

import d1_common.types.exceptions

DEFAULT_OBJECT_LIST_PAGE_SIZE = 1000
DEFAULT_MAX_CONCURRENT_D1_REST_CALLS = 20


class ObjectListIteratorAsync:
    def __init__(
        self,
        async_client,
        page_size=DEFAULT_OBJECT_LIST_PAGE_SIZE,
        list_objects_args_dict=None,
        max_concurrent_d1_rest_calls=DEFAULT_MAX_CONCURRENT_D1_REST_CALLS,
    ):
        self._logger = logging.getLogger(__name__)
        self._client = async_client
        self._page_size = page_size
        self._list_objects_args_dict = list_objects_args_dict or {}
        self._max_concurrent_d1_rest_calls = max_concurrent_d1_rest_calls

    async def itr(self):
        object_count = await self._get_total_object_count()

        self._logger.debug("Object count: {}".format(object_count))

        page_count = (object_count - 1) // self._page_size + 1
        self._logger.debug(
            "Page count: {} at {} events per page".format(page_count, self._page_size)
        )

        # Debug
        # page_count = 10

        task_set = set()

        for page_idx in range(page_count):
            if len(task_set) >= self._max_concurrent_d1_rest_calls:
                done_set, task_set = await asyncio.wait(
                    task_set, return_when=asyncio.FIRST_COMPLETED
                )

                async for item_pyxb in self._iter_done(done_set):
                    yield item_pyxb

            task_set.add(self._get_page(page_idx))

        done_set, task_set = await asyncio.wait(task_set)

        async for item_pyxb in self._iter_done(done_set):
            yield item_pyxb

    async def _get_page(self, page_idx):
        page_start_idx = page_idx * self._page_size
        try:
            return await self._client.list_objects(
                start=page_start_idx,
                count=self._page_size,
                **self._list_objects_args_dict
            )
        except d1_common.types.exceptions.DataONEException as e:
            self._logger.debug(
                'Skipped slice. page_idx={} page_start_idx={} page_size={} error="{}"'.format(
                    page_idx, page_start_idx, self._page_size, e.friendly_format()
                )
            )

    async def _iter_done(self, done_set):
        for iter_task in done_set:
            for item_pyxb in iter_task.result().objectInfo:
                yield item_pyxb

    async def _get_total_object_count(self):
        args_dict = self._list_objects_args_dict.copy()
        args_dict["count"] = 0
        return await self._client.list_objects(**args_dict).total
        return await self._client.list_objects(**args_dict).total
