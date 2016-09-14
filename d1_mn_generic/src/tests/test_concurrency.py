#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
"""Module gmn.tests.test_concurrency
====================================

Unit tests for GMN concurrency.

:Created: 2011-07-06
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

# Stdlib.
import unittest
import logging
import threading
import time

# D1
try:
  import d1_common.types.dataoneTypes
  import d1_common.types.exceptions
  import d1_common.const
except ImportError, e:
  sys.stderr.write('Import error: {}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/api-common-python/src/d1_common\n'
  )
  raise
try:
  import d1_client
  import d1_client.systemmetadata
  import d1_common.xml_compare
except ImportError, e:
  sys.stderr.write('Import error: {}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/itk/d1-python/src/d1_client\n'
  )
  raise

# Test.
import test_context as context
import gmn_test_client


def session(subject):
  return {'VENDOR_INCLUDE_SUBJECTS': subject}

# ==============================================================================


class concurrent_read(threading.Thread):
  def __init__(self, key, sleep_before, sleep_after):
    self.key = key
    self.sleep_before = sleep_before
    self.sleep_after = sleep_after
    threading.Thread.__init__(self)

  def run(self):
    client = gmn_test_client.GMNTestClient(context.gmn_url)

    #print 'starting read({}, {}, {})'.format(self.key,
    #                                            self.sleep_before,
    #                                            self.sleep_after)

    self.response = client.concurrency_read_lock(
      self.key,
      str(self.sleep_before),
      str(self.sleep_after),
      headers=session(d1_common.const.SUBJECT_TRUSTED)
    )

    self.val = self.response.read()

    #print 'ended read(({}, {}, {})'.format(self.key,
    #                                          self.sleep_before,
    #                                          self.sleep_after)

    # ==============================================================================


class concurrent_write(threading.Thread):
  def __init__(self, key, val, sleep_before, sleep_after):
    self.key = key
    self.val = val
    self.sleep_before = sleep_before
    self.sleep_after = sleep_after
    threading.Thread.__init__(self)

  def run(self):
    client = gmn_test_client.GMNTestClient(context.gmn_url)

    #print 'starting write({}, {}, {})'.format(self.key,
    #                                             self.sleep_before,
    #                                             self.sleep_after)

    self.response = client.concurrency_write_lock(
      self.key,
      self.val,
      str(self.sleep_before),
      str(self.sleep_after),
      headers=session(d1_common.const.SUBJECT_TRUSTED)
    )

    #print 'ended write({}, {}, {})'.format(self.key,
    #                                          self.sleep_before,
    #                                          self.sleep_after)

    # ==============================================================================


class concurrent_dictionary_id(threading.Thread):
  def __init__(self, lock, ids):
    self.lock = lock
    self.ids = ids
    threading.Thread.__init__(self)

  def run(self):
    client = gmn_test_client.GMNTestClient(context.gmn_url)

    #print 'starting id'

    self.response = client.concurrency_get_dictionary_id(
      headers=session(d1_common.const.SUBJECT_TRUSTED)
    )

    id = self.response.read()

    self.lock.acquire()
    self.ids[id] = True
    self.lock.release()

    #print 'ended id'

    # ==============================================================================


class TestConcurrency(unittest.TestCase):
  def setUp(self):
    context.gmn_url = 'http://0.0.0.0:80/mn/'
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    # Clear out the server side test locks.
    client.concurrency_clear()

  def tearDown(self):
    pass

  def test_010_single_locking_object(self):
    """Verify that all calls share single locking object.
    """
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    n_threads = threading.active_count()
    lock = threading.Lock()
    ids = {}
    for i in range(100):
      id = concurrent_dictionary_id(lock, ids)
      id.start()
    while threading.active_count() != n_threads:
      time.sleep(1)
    self.assertEqual(len(ids), 1)

  def test_020_sync_read(self):
    """Series of sync reads on any PID returns <undef>.
    """
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    for i in range(100):
      reader = concurrent_read('key_{}'.format(i), 0, 0)
      reader.start()
      reader.join()
      self.assertEqual(reader.val, '<undef>')

  def test_030_sync_write_read(self):
    """Series of sync write-reads return written values.
    """
    client = gmn_test_client.GMNTestClient(context.gmn_url)
    for i in range(100):
      writer = concurrent_write('key_{}'.format(i), 'val_{}'.format(i), 0, 0)
      writer.start()
      writer.join()
    for i in range(100):
      reader = concurrent_read('key_{}'.format(i), 0, 0)
      reader.start()
      reader.join()
      self.assertEqual(reader.val, 'val_{}'.format(i))

  def test_040_async_write_read(self):
    """Series of async write-reads return written values (writers block readers)
    """
    n_threads = threading.active_count()
    for i in range(100):
      write = concurrent_write('key_{}'.format(i), 'val_{}'.format(i), 1, 1)
      write.start()
    readers = []
    for i in range(100):
      reader = concurrent_read('key_{}'.format(i), 1, 1)
      reader.start()
      readers.append(reader)
    while threading.active_count() != n_threads:
      time.sleep(1)
    for i in range(100):
      self.assertEqual(readers[i].val, 'val_{}'.format(i))

  def test_050_concurrent_multiple_reads(self):
    """Series of async reads return written values (readers do not block readers)
    """
    n_threads = threading.active_count()
    for i in range(100):
      write = concurrent_write('key_{}'.format(i), 'val_{}'.format(i), 1, 1)
      write.start()
    readers = []
    for j in range(2):
      for i in range(100):
        reader = concurrent_read('key_{}'.format(i), 1, 1)
        reader.start()
        readers.append(reader)
    while threading.active_count() != n_threads:
      time.sleep(1)
    for i in range(100):
      self.assertEqual(readers[i].val, 'val_{}'.format(i))


if __name__ == "__main__":
  import sys
  #from node_test_common import loadTestInfo, initMain
  #unittest.main(argv=sys.argv, verbosity=2)
  suite = unittest.TestLoader().loadTestsFromTestCase(TestConcurrency)
  unittest.TextTestRunner(verbosity=2).run(suite)
