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
"""Multiprocessed System Metadata iterator

Parallel download of a set of SystemMetadata documents from a CN or MN. The
SystemMetadata to download can be selected by the filters that are available in
the MNRead.listObjects() and CNRead.listObjects() API calls. For MNs, these
include: fromDate, toDate, formatId and identifier. For CNs, these include the
ones supported by MNs plus nodeId.

Note: Unhandled exceptions raised in client code while iterating over results
from this iterator, or in the iterator itself, will not be shown and may cause
the client code to hang. This is a limitation of the multiprocessing module.

If there is an error when retrieving a System Metadata, such as NotAuthorized,
an object that is derived from d1_common.types.exceptions.DataONEException is
returned instead.

Will create the same number of DataONE clients and HTTP or HTTPS connections as
the number of workers. A single connection is reused, first for retrieving a
page of results, then all System Metadata objects in the result.

There is a bottleneck somewhere in this iterator, but it's not pickle/unpickle
of sysmeta_pyxb.

Notes on MAX_QUEUE_SIZE:

Queues that become too large can cause deadlocks:
https://stackoverflow.com/questions/21641887/python-multiprocessing-process-hangs-on-join-for-large-queue
Each item in the queue is a potentially large SysMeta PyXB object, so we set a
low max queue size.
"""

import logging
import multiprocessing
import time

import d1_common.type_conversions
import d1_common.types.exceptions

import d1_client.mnclient_1_2
import d1_client.mnclient_2_0

# Defaults
OBJECT_LIST_PAGE_SIZE = 1000
MAX_WORKERS = 16
# See notes in module docstring before changing
MAX_RESULT_QUEUE_SIZE = 100
MAX_TASK_QUEUE_SIZE = 16
API_MAJOR = 2


class SystemMetadataIteratorMulti(object):
  def __init__(
      self,
      base_url,
      page_size=OBJECT_LIST_PAGE_SIZE,
      max_workers=MAX_WORKERS,
      max_result_queue_size=MAX_RESULT_QUEUE_SIZE,
      max_task_queue_size=MAX_TASK_QUEUE_SIZE,
      api_major=API_MAJOR,
      client_dict=None,
      list_objects_dict=None,
      get_sysmeta_dict=None,
      debug=False,
  ):
    self._base_url = base_url
    self._page_size = page_size
    self._max_workers = max_workers
    self._max_queue_size = max_result_queue_size
    self._max_task_queue_size = max_task_queue_size
    self._api_major = api_major
    self._client_dict = client_dict or {}
    self._list_objects_dict = list_objects_dict or {}
    self._get_sysmeta_dict = get_sysmeta_dict or {}
    self.total = _get_total_object_count(
      base_url, api_major, self._client_dict, self._list_objects_dict
    )
    self._debug = debug
    if debug:
      logger = multiprocessing.log_to_stderr()
      logger.setLevel(multiprocessing.SUBDEBUG)

  def __iter__(self):
    manager = multiprocessing.Manager()
    queue = manager.Queue(maxsize=self._max_queue_size)
    namespace = manager.Namespace()
    namespace.stop = False

    process = multiprocessing.Process(
      target=_get_all_pages,
      args=(
        queue, namespace, self._base_url, self._page_size, self._max_workers,
        self._max_task_queue_size, self._api_major, self._client_dict,
        self._list_objects_dict, self._get_sysmeta_dict, self.total
      ),
    )

    process.start()

    try:
      while True:
        error_dict_or_sysmeta_pyxb = queue.get()
        if error_dict_or_sysmeta_pyxb is None:
          logging.debug(
            '__iter__(): Received None sentinel value. Stopping iteration'
          )
          break
        elif isinstance(error_dict_or_sysmeta_pyxb, dict):
          yield d1_common.types.exceptions.create_exception_by_name(
            error_dict_or_sysmeta_pyxb['error'],
            identifier=error_dict_or_sysmeta_pyxb['pid'],
          )
        else:
          yield error_dict_or_sysmeta_pyxb
    except GeneratorExit:
      logging.debug('__iter__(): GeneratorExit exception')
      pass

    # If generator is exited before exhausted, provide clean shutdown of the
    # generator by signaling processes to stop, then waiting for them.
    logging.debug('__iter__(): Setting stop signal')
    namespace.stop = True
    # Prevent parent from leaving zombie children behind.
    while queue.qsize():
      logging.debug('__iter__(): queue.size(): Dropping unwanted result')
      queue.get()
    logging.debug('__iter__(): process.join(): Waiting for process to exit')
    process.join()


def _get_all_pages(
    queue, namespace, base_url, page_size, max_workers, max_task_queue_size,
    api_major, client_dict, list_objects_dict, get_sysmeta_dict, n_total
):
  logging.info('Creating pool of {} workers'.format(max_workers))
  pool = multiprocessing.Pool(processes=max_workers)
  n_pages = (n_total - 1) // page_size + 1

  for page_idx in range(n_pages):
    if namespace.stop:
      logging.debug('_get_all_pages(): Page iter: Received stop signal')
      break
    try:
      pool.apply_async(
        _get_page, args=(
          queue, namespace, base_url, page_idx, n_pages, page_size, api_major,
          client_dict, list_objects_dict, get_sysmeta_dict
        )
      )
    except Exception as e:
      logging.debug(
        '_get_all_pages(): pool.apply_async() error="{}"'.format(str(e))
      )
    # The pool does not support a clean way to limit the number of queued tasks
    # so we have to access the internals to check the queue size and wait if
    # necessary.
    # noinspection PyProtectedMember
    while pool._taskqueue.qsize() > max_task_queue_size:
      if namespace.stop:
        logging.debug(
          '_get_all_pages(): Waiting to queue task: Received stop signal'
        )
        break
      # logging.debug('_get_all_pages(): Waiting to queue task')
      time.sleep(1)

  # Workaround for workers hanging at exit.
  # pool.terminate()
  logging.debug(
    '_get_all_pages(): pool.close(): Preventing more tasks for being added to the pool'
  )
  pool.close()
  logging.debug(
    '_get_all_pages(): pool.join(): Waiting for the workers to exit'
  )
  pool.join()
  logging.debug(
    '_get_all_pages(): queue.put(None): Sending None sentinel value to stop the generator'
  )
  queue.put(None)


def _get_page(
    queue, namespace, base_url, page_idx, n_pages, page_size, api_major,
    client_dict, list_objects_dict, get_sysmeta_dict
):
  logging.debug('_get_page(): page_idx={} n_pages={}'.format(page_idx, n_pages))

  if namespace.stop:
    logging.debug('_get_page(): Received stop signal before listObjects()')
    return

  client = _create_client(base_url, api_major, client_dict)

  try:
    object_list_pyxb = client.listObjects(
      start=page_idx * page_size, count=page_size, **list_objects_dict
    )
  except Exception as e:
    logging.error(
      '_get_page(): listObjects() failed. page_idx={} page_total={} error="{}"'
      .format(page_idx, n_pages, str(e))
    )
    return

  logging.debug(
    '_get_page(): Retrieved page. page_idx={} n_items={}'.
    format(page_idx, len(object_list_pyxb.objectInfo))
  )

  i = 0
  for object_info_pyxb in object_list_pyxb.objectInfo:
    logging.debug('_get_page(): Iterating over objectInfo. i={}'.format(i))
    i += 1
    if namespace.stop:
      logging.debug('_get_page(): objectInfo iter: Received stop signal')
      break
    _get_sysmeta(
      client, queue, object_info_pyxb.identifier.value(), get_sysmeta_dict
    )


def _get_sysmeta(client, queue, pid, get_sysmeta_dict):
  logging.debug('_get_sysmeta(): pid="{}"'.format(pid))
  try:
    sysmeta_pyxb = client.getSystemMetadata(pid, get_sysmeta_dict)
  except d1_common.types.exceptions.DataONEException as e:
    logging.debug(
      '_get_sysmeta(): getSystemMetadata() failed. pid="{}" error="{}"'
      .format(pid, str(e))
    )
    queue.put({'pid': pid, 'error': e.name})
  except Exception as e:
    logging.debug(
      '_get_sysmeta(): getSystemMetadata() failed. pid="{}" error="{}"'
      .format(pid, str(e))
    )
  else:
    queue.put(sysmeta_pyxb)


def _create_client(base_url, api_major, client_dict):
  logging.debug(
    '_create_client(): api="v{}"'.format(1 if api_major <= 1 else 2)
  )
  if api_major <= 1:
    return d1_client.mnclient_1_2.MemberNodeClient_1_2(base_url, **client_dict)
  else:
    return d1_client.mnclient_2_0.MemberNodeClient_2_0(base_url, **client_dict)


def _get_total_object_count(
    base_url, api_major, client_dict, list_objects_dict
):
  client = _create_client(base_url, api_major, client_dict)
  args_dict = list_objects_dict.copy()
  args_dict['count'] = 0
  return client.listObjects(**args_dict).total
