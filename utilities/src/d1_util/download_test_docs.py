#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2018 DataONE
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

"""Download randomly selected Science Metadata objects from CN.

This is an example on how to use the DataONE Science Metadata library for Python. It
shows how to:

- Query the DataONE Solr index for a random selection of object identifiers for a given
  formatId.
- Download objects with high bandwith throughput by using the async DataONEClient to
  perform concurrent downloads.
"""

import asyncio
import io
import logging
import os
import random

import d1_scimeta.util

import d1_common.types.exceptions

import d1_common.utils.filesystem
import d1_common.utils.progress_logger

import d1_client.aio.async_client
import d1_client.command_line
import d1_client.solr_client
from d1_client.solr_client import Param

log = logging.getLogger(__name__)

DEFAULT_PAGE_COUNT = 1


async def main():
    parser = d1_client.command_line.get_standard_arg_parser(__doc__)
    parser.add_argument(
        "--page-count", default=DEFAULT_PAGE_COUNT, help="Number of bulk downloads to perform"
    )
    parser.add_argument(
        "out_path",
        help="Path to dir in which to save the downloaded files"
    )
    args = parser.parse_args()
    d1_client.command_line.log_setup(args.debug)

    solr_client = d1_client.solr_client.SolrClient()
    client = d1_client.aio.async_client.AsyncDataONEClient(
        **d1_client.command_line.args_adapter(args)
    )

    progress_logger = d1_common.utils.progress_logger.ProgressLogger(logger=log)

    for format_id in d1_scimeta.util.get_supported_format_id_list():
        schema_name = d1_scimeta.util.get_schema_name(format_id)
        out_dir_path = os.path.join(args.out_path, schema_name)
        d1_common.utils.filesystem.create_missing_directories_for_dir(out_dir_path)

        task_name = "Download SciObj with formatId: {}".format(format_id)

        progress_logger.start_task_type(task_name, args.page_size * args.page_count)

        for i in range(args.page_count):
            await validate_bulk(
                client,
                out_dir_path,
                format_id,
                args.page_size,
                solr_client,
                progress_logger,
                task_name,
            )

        progress_logger.end_task_type(task_name)

    await client.close()

    progress_logger.completed()


async def validate_bulk(
    client, out_dir_path, format_id, pid_count, solr_client, progress_logger, task_name
):

    progress_logger.start_task(task_name)

    pid_list = await get_random_pid_list(solr_client, format_id, pid_count)

    if not pid_list:
        progress_logger.event(
            "Solr query returned no objects for formatId: {}".format(format_id)
        )
        return

    progress_logger.event(
        "Solr returned randomly selected PIDs for formatId: {}".format(format_id),
        len(pid_list),
    )

    task_set = set()

    for pid in pid_list:
        task_set.add(download(client, out_dir_path, pid, format_id, progress_logger))

    await asyncio.wait(task_set)


async def download(client, out_dir_path, pid, format_id, progress_logger):
    try:
        sciobj_f = io.BytesIO()
        await client.get(sciobj_f, pid)
    except d1_common.types.exceptions.DataONEException as e:
        progress_logger.event("Download failed. formatId: {}".format(format_id))
        log.error(
            'Download failed. formatId="{}" pid="{}" error="{}"'.format(
                format_id, pid, str(e)
            )
        )
        return

    try:
        await save_xml(out_dir_path, pid, sciobj_f)
    except d1_scimeta.util.SciMetaError as e:
        progress_logger.event("XML save to file failed: {}".format(str(e)))
        log.error(
            'XML save to file failed. out_dir_path="{}" pid="{}" error="{}"'.format(
                out_dir_path, pid, str(e)
            )
        )
    else:
        progress_logger.event("XML file saved. formatId: {}".format(format_id))


async def save_xml(out_dir_path, pid, sciobj_f):
    xml_path = os.path.join(
        out_dir_path, d1_common.utils.filesystem.gen_safe_path_element(pid) + ".xml"
    )
    d1_scimeta.util.save_bytes_to_file(xml_path, sciobj_f.getvalue())


async def get_random_pid_list(solr_client, format_id, pid_count):
    """Query Solr for a list of randomly selected PIDs of objects with a given
    formatId."""
    search_result = solr_client.search(
        q=Param("formatId", format_id),
        rows=pid_count,
        fl=["id", "formatIdx"],
        sort="random_{} desc".format(random.randint(10000, 99999)),
    )
    return [d["id"] for d in search_result["response"]["docs"]]


if __name__ == "__main__":
    asyncio.run(main())
