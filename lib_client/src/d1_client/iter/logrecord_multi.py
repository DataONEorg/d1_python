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
"""Multiprocessed LogRecord Iterator

Fast retrieval of event log records from a DataONE Node.

See additional notes in SysMeta iter docstring.
"""

import logging
import multiprocessing
import time

import d1_common.types.exceptions

import d1_client.mnclient_1_2
import d1_client.mnclient_2_0

# Defaults
LOG_RECORD_PAGE_SIZE = 1000
MAX_WORKERS = 16
# See notes in module docstring for SysMeta iterator before changing
MAX_RESULT_QUEUE_SIZE = 100
MAX_TASK_QUEUE_SIZE = 16
API_MAJOR = 2


class LogRecordIteratorMulti(object):
  def __init__(
      self,
      base_url,
      page_size=LOG_RECORD_PAGE_SIZE,
      max_workers=MAX_WORKERS,
      max_result_queue_size=MAX_RESULT_QUEUE_SIZE,
      max_task_queue_size=MAX_TASK_QUEUE_SIZE,
      api_major=API_MAJOR,
      client_dict=None,
      get_log_records_dict=None,
      debug=False,
  ):
    self._base_url = base_url
    self._page_size = page_size
    self._max_workers = max_workers
    self._max_result_queue_size = max_result_queue_size
    self._max_task_queue_size = max_task_queue_size
    self._api_major = api_major
    self._client_dict = client_dict or {}
    self._get_log_records_dict = get_log_records_dict or {}
    self.total = _get_total_object_count(
      base_url, api_major, self._client_dict, self._get_log_records_dict
    )
    self._debug = debug
    if debug:
      logger = multiprocessing.log_to_stderr()
      logger.setLevel(multiprocessing.SUBDEBUG)

  def __iter__(self):
    manager = multiprocessing.Manager()
    queue = manager.Queue(maxsize=self._max_result_queue_size)
    namespace = manager.Namespace()
    namespace.stop = False

    process = multiprocessing.Process(
      target=_get_all_pages,
      args=(
        queue, namespace, self._base_url, self._page_size, self._max_workers,
        self._max_task_queue_size, self._api_major, self._client_dict,
        self._get_log_records_dict, self.total,
      ),
    )

    process.start()

    try:
      while True:
        error_dict_or_log_pyxb = queue.get()
        if error_dict_or_log_pyxb is None:
          logging.debug(
            '__iter__(): Received None sentinel value. Stopping iteration'
          )
          break
        elif isinstance(error_dict_or_log_pyxb, dict):
          yield d1_common.types.exceptions.create_exception_by_name(
            error_dict_or_log_pyxb['error'],
            identifier=error_dict_or_log_pyxb['pid'],
          )
        else:
          yield error_dict_or_log_pyxb
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
    api_major, client_dict, get_log_records_dict, n_total
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
          client_dict, get_log_records_dict
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
    client_dict, get_log_records_dict
):
  logging.debug('_get_page(): page_idx={} n_pages={}'.format(page_idx, n_pages))

  if namespace.stop:
    logging.debug('_get_page(): Received stop signal before listObjects()')
    return

  client = _create_client(base_url, api_major, client_dict)

  try:
    log_records_pyxb = client.getLogRecords(
      start=page_idx * page_size, count=page_size, **get_log_records_dict
    )
  except Exception as e:
    logging.error(
      '_get_page(): getLogRecords() failed. page_idx={} page_total={} error="{}"'
      .format(page_idx, n_pages, str(e))
    )
    return

  logging.debug(
    '_get_page(): Retrieved page. page_idx={} n_items={}'.
    format(page_idx, len(log_records_pyxb.logEntry))
  )

  i = 0
  for log_entry_pyxb in log_records_pyxb.logEntry:
    logging.debug('_get_page(): Iterating over logEntry. i={}'.format(i))
    i += 1
    if namespace.stop:
      logging.debug('_get_page(): logEntry iter: Received stop signal')
      break
    queue.put(log_entry_pyxb)


def _create_client(base_url, api_major, client_dict):
  logging.debug(
    '_create_client(): api="v{}"'.format(1 if api_major <= 1 else 2)
  )
  if api_major <= 1:
    return d1_client.mnclient_1_2.MemberNodeClient_1_2(base_url, **client_dict)
  else:
    return d1_client.mnclient_2_0.MemberNodeClient_2_0(base_url, **client_dict)


def _get_total_object_count(
    base_url, api_major, client_dict, get_log_records_dict
):
  client = _create_client(base_url, api_major, client_dict)
  args_dict = get_log_records_dict.copy()
  args_dict['count'] = 0
  return client.getLogRecords(**args_dict).total
