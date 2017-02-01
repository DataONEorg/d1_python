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
"""Multithreaded ObjectList iterator
"""

# Stdlib
import datetime
import json
import logging
import multiprocessing
import sys
import unittest
import urlparse

# 3rd party
import responses # pip install responses
import requests

# D1
import d1_common.type_conversions

# App
sys.path.append('..')
import d1_client.mnclient_1_1
import d1_client.mnclient_2_0
import d1_common.types.dataoneTypes_v1_1 as v1
import d1_common.types.dataoneTypes_v2_0 as v2


logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)


N_OBJECTS_PER_PAGE = 1000
MAX_WORKERS = 10
MAX_QUEUE = 100
MAJOR_VERSION = 2


def multi_object_list_iterator(
  base_url, page_size=N_OBJECTS_PER_PAGE, max_workers=MAX_WORKERS,
  max_queue=MAX_QUEUE, major_version=MAJOR_VERSION, **listObjectsArgs
):
  d1_common.type_conversions.set_default_pyxb_namespace(major_version)

  manager = multiprocessing.Manager()
  queue = manager.Queue(maxsize=max_queue)

  process = multiprocessing.Process(
    target=_i,
    args=(base_url, page_size, queue, max_workers, listObjectsArgs),
  )

  process.start()

  while True:
    v = queue.get()
    if v is not None:
      print v
      yield v2.CreateFromDocument(v)
    else:
      break

  process.join()


def _i(base_url, page_size, queue, max_workers, listObjectsArgs):
  pool = multiprocessing.Pool(processes=max_workers)

  logging.error("A"*100)
  sys.stdout.flush()

  _launch_workers(base_url, page_size, pool, queue, listObjectsArgs)

  logging.error("B"*100)
  sys.stdout.flush()

  logging.error("C"*100)
  sys.stdout.flush()


def _launch_workers(base_url, page_size, pool, queue, listObjectsArgs):
  logging.error("1"*100)
  sys.stdout.flush()
  client = d1_client.mnclient_2_0.MemberNodeClient_2_0(base_url)
  n_total = client.listObjects(count=0).total
  print n_total
  n_pages = (n_total - 1) / page_size + 1
  for page_idx in range(n_pages):
    print page_idx, n_pages
    pool.apply_async(
      _getPage,
      args=(base_url, page_idx, n_pages, page_size, queue, listObjectsArgs)
    )
  pool.close()
  pool.join()
  queue.put(None)


def _getPage(base_url, page_idx, n_pages, page_size, queue, listObjectsArgs):
  logging.error("test")
  sys.stdout.flush()

  client = d1_client.mnclient_2_0.MemberNodeClient_2_0(base_url)
  try:
    print '7' * 100
    sys.stdout.flush()

    object_list_pyxb = client.listObjects(
      start=page_idx * page_size, count=page_size, **listObjectsArgs
    )

    print len(object_list_pyxb.objectInfo)
    sys.stdout.flush()

    print 'Retrieved page: {}/{}'.format(page_idx + 1, n_pages)
    sys.stdout.flush()
    # logging.info('Retrieved page: {}/{}'.format(n_total, page_size + 1))

    for object_info_pyxb in object_list_pyxb.objectInfo:
      logging.error("put")
      sys.stdout.flush()

      object_info_xml = object_info_pyxb.toxml('utf-8')
      print object_info_xml
      sys.stdout.flush()
      queue.put(object_info_xml)
      # queue.put(str(page_idx))

    # return "test"
    # return object_list.objectInfo.toxml()

  except Exception as e:
    logging.exception(e.message)
    print '9' * 100
    sys.stdout.flush()
