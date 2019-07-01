#!/usr/bin/env python

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

PAGE_SIZE = 100
PAGE_COUNT = 1


async def main():
    d1_client.command_line.log_setup(is_debug=False)

    logging.getLogger("d1_client.aio.async_client").setLevel(logging.ERROR)
    logging.getLogger("d1_scimeta.util").setLevel(logging.ERROR)

    solr_client = d1_client.solr_client.SolrClient()
    client = d1_client.aio.async_client.AsyncDataONEClient()

    progress_logger = d1_common.utils.progress_logger.ProgressLogger(logger=log)

    for format_id in d1_scimeta.util.get_supported_format_id_list():
        schema_name = d1_scimeta.util.get_schema_name(format_id)
        out_dir_path = d1_common.utils.filesystem.abs_path(
            os.path.join("./test_xml", schema_name)
        )
        d1_common.utils.filesystem.create_missing_directories_for_dir(out_dir_path)

        task_name = "Download SciObj with formatId: {}".format(format_id)

        progress_logger.start_task_type(task_name, PAGE_SIZE * PAGE_COUNT)

        for i in range(PAGE_COUNT):
            await validate_bulk(
                client,
                out_dir_path,
                format_id,
                PAGE_SIZE,
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
