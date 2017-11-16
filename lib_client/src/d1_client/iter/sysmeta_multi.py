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

If there is an error when retrieving a System Metadata, such as NotAuthorized,
an object that is derived from d1_common.types.exceptions.DataONEException is
returned instead.

Will create the same number of DataONE clients and HTTP or HTTPS connections as
the number of workers. A single connection is reused, first for retrieving a
page of results, then all System Metadata objects in the result.

There is a bottleneck somewhere in this iterator, but it's not pickle/unpickle
of sysmeta_pyxb.
"""

from __future__ import absolute_import

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
MAX_QUEUE_SIZE = 100
API_MAJOR = 2
POOL_SIZE_FACTOR = 100


class SystemMetadataIteratorMulti(object):
  def __init__(
      self,
      base_url,
      page_size=OBJECT_LIST_PAGE_SIZE,
      max_workers=MAX_WORKERS,
      max_queue_size=MAX_QUEUE_SIZE,
      api_major=API_MAJOR,
      client_dict=None,
      list_objects_dict=None,
      get_sysmeta_dict=None,
  ):
    self._base_url = base_url
    self._page_size = page_size
    self._max_workers = max_workers
    self._max_queue_size = max_queue_size
    self._api_major = api_major
    self._client_dict = client_dict or {}
    self._list_objects_dict = list_objects_dict or {}
    self._get_sysmeta_dict = get_sysmeta_dict or {}
    self.total = _get_total_object_count(
      base_url, api_major, self._client_dict, self._list_objects_dict
    )

  def __iter__(self):
    manager = multiprocessing.Manager()
    queue = manager.Queue(maxsize=self._max_queue_size)
    namespace = manager.Namespace()
    namespace.stop = False

    process = multiprocessing.Process(
      target=_get_all_pages,
      args=(
        queue, namespace, self._base_url, self._page_size, self._max_workers,
        self._api_major, self._client_dict, self._list_objects_dict,
        self._get_sysmeta_dict, self.total
      ),
    )

    process.start()

    try:
      while True:
        error_dict_or_sysmeta_pyxb = queue.get()
        if error_dict_or_sysmeta_pyxb is None:
          logging.debug('Received None sentinel value. Stopping iteration')
          break
        elif isinstance(error_dict_or_sysmeta_pyxb, dict):
          yield d1_common.types.exceptions.create_exception_by_name(
            error_dict_or_sysmeta_pyxb['error'],
            identifier=error_dict_or_sysmeta_pyxb['pid'],
          )
        else:
          yield error_dict_or_sysmeta_pyxb
    except GeneratorExit:
      pass

    # If generator is exited before exhausted, provide clean shutdown of the
    # generator by signaling processes to stop, then waiting for them.
    logging.debug('Setting stop flag')
    namespace.stop = True

    # Prevent parent from leaving zombie children behind.
    process.join()


def _get_all_pages(
    queue, namespace, base_url, page_size, max_workers, api_major, client_dict,
    list_objects_dict, get_sysmeta_dict, n_total
):
  logging.info('Creating pool of {} workers'.format(max_workers))
  pool = multiprocessing.Pool(processes=max_workers)
  n_pages = (n_total - 1) / page_size + 1

  for page_idx in range(n_pages):
    if namespace.stop:
      logging.debug('Stop flag detected in page iterator')
      break
    try:
      pool.apply_async(
        _get_page, args=(
          queue, namespace, base_url, page_idx, n_pages, page_size, api_major,
          client_dict, list_objects_dict, get_sysmeta_dict
        )
      )
    except RuntimeError as e:
      logging.debug('pool.apply_async() error="{}"'.format(str(e)))
    # The pool does not support a clean way to limit the number of queued tasks
    # so we have to access the internals to check the queue size and wait if
    # necessary.
    # noinspection PyProtectedMember
    while pool._taskqueue.qsize() > max_workers * POOL_SIZE_FACTOR:
      if namespace.stop:
        logging.debug('Stop flag detected while waiting to queue task')
        break
      logging.debug('Waiting to queue task')
      time.sleep(1)
  # Prevent any more tasks from being submitted to the pool. Once all the
  # tasks have been completed the worker processes will exit.
  pool.close()
  # Wait for the worker processes to exit
  pool.join()
  # Use None as sentinel value to stop the generator
  queue.put(None)


def _get_page(
    queue, namespace, base_url, page_idx, n_pages, page_size, api_major,
    client_dict, list_objects_dict, get_sysmeta_dict
):
  logging.debug('_get_page(): page_idx={} n_pages={}'.format(page_idx, n_pages))
  client = _create_client(base_url, api_major, client_dict)
  try:
    object_list_pyxb = client.listObjects(
      start=page_idx * page_size, count=page_size, **list_objects_dict
    )
  except RuntimeError as e:
    logging.error(
      '_get_page(): listObjects() failed. page_idx={} page_total={} error="{}"'
      .format(page_idx, n_pages, str(e))
    )
  else:
    for object_info_pyxb in object_list_pyxb.objectInfo:
      if namespace.stop:
        logging.debug('_get_page(): Received stop flag')
        break
      _get_sysmeta(
        client, queue, object_info_pyxb.identifier.value(), get_sysmeta_dict
      )


def _get_sysmeta(client, queue, pid, get_sysmeta_dict):
  try:
    sysmeta_pyxb = client.getSystemMetadata(pid, get_sysmeta_dict)
  except d1_common.types.exceptions.DataONEException as e:
    logging.debug(
      '_get_sysmeta(): getSystemMetadata() failed. pid="{}" error="{}"'
      .format(pid, str(e))
    )
    queue.put({'pid': pid, 'error': e.name})
  except RuntimeError as e:
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
