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
"""Base for multiprocessed DataONE type iterator."""

import logging
import multiprocessing
import time

import d1_common.types.exceptions

import d1_client.mnclient_1_2
import d1_client.mnclient_2_0


# Defaults
PAGE_SIZE = 1000
MAX_WORKERS = 16
# See notes in module docstring for SysMeta iterator before changing
MAX_RESULT_QUEUE_SIZE = 100
MAX_TASK_QUEUE_SIZE = 16
API_MAJOR = 2


logger = logging.getLogger(__name__)

# fmt: off
class MultiprocessedIteratorBase(object):
    def __init__(
        self,
            base_url, page_size, max_workers, max_result_queue_size,
            max_task_queue_size, api_major, client_arg_dict, page_arg_dict,
            item_proc_arg_dict, page_func, iter_func, item_proc_func,
    ):
        self._base_url = base_url
        self._page_size = page_size
        self._max_workers = max_workers
        self._max_result_queue_size = max_result_queue_size
        self._max_task_queue_size = max_task_queue_size
        self._api_major = api_major
        self._client_arg_dict = client_arg_dict or {}
        self._page_arg_dict = page_arg_dict or {}
        self._item_proc_arg_dict = item_proc_arg_dict or {}
        self._page_func = page_func
        self._iter_func = iter_func
        self._item_proc_func = item_proc_func
        self._total = None

    @property
    def total(self):
        if self._total is None:
            client = create_client(
                self._base_url, self._api_major, self._client_arg_dict
            )
            page_pyxb = self._page_func(client)(
                start=0, count=0, **self._page_arg_dict
            )
            self._total = page_pyxb.total
        return self._total

    def __iter__(self):
        manager = multiprocessing.Manager()
        queue = manager.Queue(maxsize=self._max_result_queue_size)
        namespace = manager.Namespace()
        namespace.stop = False

        process = multiprocessing.Process(
            target=_get_all_pages,
            args=(
                queue, namespace, self._base_url, self._page_size, self._max_workers,
                self._max_task_queue_size, self._api_major, self._client_arg_dict,
                self._page_arg_dict, self._item_proc_arg_dict, self._page_func,
                self._iter_func, self._item_proc_func, self.total
            ),
        )

        process.start()

        try:
            while True:
                item_result = queue.get()
                if item_result is None:
                    logger.debug("Received None sentinel value. Stopping iteration")
                    break
                elif isinstance(item_result, dict):
                    logger.debug('Raising exception received as dict. dict="{}"'.format(item_result))
                    yield d1_common.types.exceptions.create_exception_by_name(
                        item_result["error"],
                        identifier=item_result["pid"],
                    )
                else:
                    yield item_result
        except GeneratorExit:
            logger.debug("GeneratorExit exception")
            pass

        # If generator is exited before exhausted, provide clean shutdown of the
        # generator by signaling processes to stop, then waiting for them.
        logger.debug("Setting stop signal")
        namespace.stop = True
        # Prevent parent from leaving zombie children behind.
        while queue.qsize():
            logger.debug("Dropping unwanted result")
            queue.get()
        logger.debug("Waiting for process to exit")
        process.join()


def _get_all_pages(
    queue, namespace, base_url, page_size, max_workers, max_task_queue_size, api_major,
    client_arg_dict, page_arg_dict, item_proc_arg_dict, page_func, iter_func, item_proc_func, n_total
):
    logger.debug("Creating pool of {} workers".format(max_workers))
    pool = multiprocessing.Pool(processes=max_workers)
    n_pages = (n_total - 1) // page_size + 1

    for page_idx in range(n_pages):
        if namespace.stop:
            logger.debug("Received stop signal")
            break
        try:
            pool.apply_async(
                _get_page,
                args=(
                    queue, namespace, base_url, page_idx, n_pages, page_size, api_major,
                    client_arg_dict, page_arg_dict, item_proc_arg_dict, page_func,
                    iter_func, item_proc_func
                ),
            )
        except Exception as e:
            logger.debug('Continuing after exception. error="{}"'.format(str(e)))
        # The pool does not support a clean way to limit the number of queued tasks
        # so we have to access the internals to check the queue size and wait if
        # necessary.
        while pool._taskqueue.qsize() > max_task_queue_size:
            if namespace.stop:
                logger.debug("Received stop signal")
                break
            # logger.debug('_get_all_pages(): Waiting to queue task')
            time.sleep(1)

    # Workaround for workers hanging at exit.
    # pool.terminate()
    logger.debug("Preventing more tasks for being added to the pool")
    pool.close()
    logger.debug("Waiting for the workers to exit")
    pool.join()
    logger.debug("Sending None sentinel value to stop the generator")
    queue.put(None)


def _get_page(
    queue, namespace, base_url, page_idx, n_pages, page_size, api_major,
    client_arg_dict, page_arg_dict, item_proc_arg_dict, page_func, iter_func, item_proc_func
):
    logger.debug("Processing page. page_idx={} n_pages={}".format(page_idx, n_pages))

    if namespace.stop:
        logger.debug("Received stop signal")
        return

    client = create_client(base_url, api_major, client_arg_dict)

    try:
        page_pyxb = page_func(client)(
            start=page_idx * page_size, count=page_size, **page_arg_dict
        )
    except Exception as e:
        logger.error(
            'Unable to get page. page_idx={} page_total={} error="{}"'.format(
                page_idx, n_pages, str(e)
            )
        )
        return

    iterable_pyxb = iter_func(page_pyxb)

    logger.debug(
        "Starting page item iteration. page_idx={} n_items={}".format(
            page_idx, len(iterable_pyxb)
        )
    )

    for item_pyxb in iterable_pyxb:
        if namespace.stop:
            logger.debug("Received stop signal")
            break
        queue.put(item_proc_func(client, item_pyxb, item_proc_arg_dict))

    logger.debug("Completed page")


def create_client(base_url, api_major, client_arg_dict):
    if api_major in (1, "1", "v1"):
        return d1_client.mnclient_1_2.MemberNodeClient_1_2(base_url, **client_arg_dict)
    else:
        return d1_client.mnclient_2_0.MemberNodeClient_2_0(base_url, **client_arg_dict)
