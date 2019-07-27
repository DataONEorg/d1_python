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
"""Async EventLog Iterator.

Fast retrieval of event logs from a DataONE node.

Uses the getLogRecords() DataONE API to retrieve Log and logEntry objects. The logEntry
objects are returned to the user.
"""
import d1_client.aio.async_client
import d1_client.aio.iter.base_async


class EventLogIteratorAsync(d1_client.aio.iter.base_async.IteratorBaseAsync):
    def __init__(
        self,
        async_client,
        page_size=d1_client.aio.async_client.DEFAULT_PAGE_SIZE,
        list_arg_dict=None,
    ):
        super().__init__(async_client, page_size, list_arg_dict)

    async def import_all(self):
        """Import all Event Logs on remote MN."""
        self.log.info("Starting Event Log import")
        log_pyxb = await self.async_client.get_log_records(
            start=0, count=0, **self.list_arg_dict
        )
        total_count = log_pyxb.total
        self.log.debug("Total event log count: {}".format(total_count))
        if not total_count:
            self.log.error("Aborted: MNRead.getLogRecords() returned empty list")
            return
        page_count = self.calc_page_count(total_count)
        for page_idx in range(page_count):
            await self.add_task(self.import_page(page_idx, page_count))

    async def import_page(self, page_idx, page_count):
        """Import all Events in page"""
        self.log.debug(
            "Starting import of Events on page {}/{}".format(page_idx + 1, page_count)
        )
        page_start_idx = page_idx * self.page_size
        log_pyxb = await self.async_client.get_log_records(
            start=page_start_idx, count=self.page_size, **self.list_arg_dict
        )
        self._page_check(page_idx, page_count, len(log_pyxb.logEntry))
        for log_entry_pyxb in log_pyxb.logEntry:
            self.result_set.add(log_entry_pyxb)

    async def get_total_count(self):
        args_dict = self.list_arg_dict.copy()
        args_dict["count"] = 0
        return (await self.async_client.get_log_records(**args_dict)).total
