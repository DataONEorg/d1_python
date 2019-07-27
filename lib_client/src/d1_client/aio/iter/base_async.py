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
"""Base for Async ObjectList and EventLog Iterator.
"""
import asyncio
import logging

import d1_common.types.exceptions

import d1_client.aio.async_client

PAGE_SIZE_ERROR_STR = """
The remote node returned a result page that contains fewer than the
requested number of records. As pages are downloaded concurrently by
this iterator, it cannot compensate. To ensure that all objects are
found by the iterator, switch to the traditional synchronous
version of this iterator. To skip this check, create the iterator with
ignore_errors=True. If using a command line client, start the client
with the the --ignore-errors switch.
"""


class IteratorBaseAsync(object):
    def __init__(
        self,
        async_client,
        page_size=d1_client.aio.async_client.DEFAULT_PAGE_SIZE,
        list_arg_dict=None,
    ):
        self.log = logging.getLogger(__name__)
        self.async_client = async_client
        self.page_size = page_size
        self.list_arg_dict = list_arg_dict or {}
        self._total = None
        self.task_set = set()
        self.another_task_set = set()
        self.result_set = set()
        self.ignore_errors = False

    async def __aiter__(self):
        """Async iterator returning pyxb objects."""
        await self.import_all()
        while self.task_set or self.another_task_set or self.result_set:
            self.log.debug(
                "task_set={} another_task_set={} result_set={}".format(
                    len(self.task_set), len(self.another_task_set), len(self.result_set)
                )
            )
            if not self.result_set:
                await self.await_task()
                continue
            yield self.result_set.pop()

    @property
    async def total(self):
        if self._total is None:
            self._total = await self.get_total_count()
        return self._total

    def calc_page_count(self, total_count):
        n_pages = (total_count - 1) // self.page_size + 1
        return n_pages

    # Async tasks

    async def add_task(self, task_func):
        if len(self.task_set) >= self.async_client.max_concurrent:
            await self.await_task()
        self.task_set.add(task_func)

    async def await_task(self):
        self.another_task_set.update(self.task_set)
        self.task_set.clear()
        result_set, new_task_set = await asyncio.wait(
            self.another_task_set, return_when=asyncio.FIRST_COMPLETED
        )
        self.another_task_set = new_task_set
        for r in result_set:
            try:
                # Raise any exception that occurred in task.
                r.result()
            except Exception as e:
                if self.ignore_errors:
                    self.log.debug(
                        "Continuing after error (ignore_errors=True): {}".format(str(e))
                    )
                else:
                    self.log.exception("Iterator error:")
                    raise

    async def await_all(self):
        while self.task_set or self.another_task_set:
            await self.await_task()

    def _page_check(self, page_idx, page_count, received_page_size):
        self.log.debug(
            "page_idx={} page_count={} received_page_size={} requested_page_size={}".format(
                page_idx, page_count, received_page_size, self.page_size
            )
        )
        if (
            (not self.ignore_errors)
            and page_idx < page_count - 1
            and received_page_size != self.page_size
        ):
            raise d1_common.types.exceptions.ServiceFailure(
                0,
                "{} page_idx={} page_count={} received_page_size={} requested_page_size={}".format(
                    PAGE_SIZE_ERROR_STR.strip(),
                    page_idx,
                    page_count,
                    received_page_size,
                    self.page_size,
                ),
            )

    # Override

    async def import_all(self):
        raise NotImplementedError

    async def import_page(self, page_idx, page_count):
        raise NotImplementedError

    async def get_total_count(self):
        raise NotImplementedError
