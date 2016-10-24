#!/usr/bin/env python
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

"""Module gmn.tests.test_file_lock
====================================

Unit tests for GMN concurrency.

:Created: 2015-07-02
:Author: DataONE (Flynn)
:Dependencies:
  - python 2.7
"""

# Stdlib.
import unittest
import logging
import threading
import time
import glob
import sys
import os
import re
from datetime import datetime
from mock import patch, PropertyMock
sys.path.append(
  '/home/mark/d1/d1_python/d1_mn_generic/mn/d1_mn_generic/src/service/mn/management/commands'
)
# D1
try:
  import d1_common.types.dataoneTypes
  import d1_common.types.exceptions
  import d1_common.const
  import service.mn.management.commands.process_replication_queue as process_replication_queue
  import service.mn.models as models
except ImportError, e:
  sys.stderr.write('Import error: {}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/api-common-python/src/d1_common\n'
  )
  raise
try:
  import d1_client
except ImportError, e:
  sys.stderr.write('Import error: {}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/itk/d1-python/src/d1_client\n'
  )
  raise

# Test.
# import test_context as context
# import gmn_test_client


def session(subject):
  return {'VENDOR_INCLUDE_SUBJECTS': subject}


class TestConcurrency(unittest.TestCase):
  def setUp(self):
    pass

  def test_file_lock(self):
    pid_list = ['anterior1.jpg', '10Dappend2.txt', '10Dappend1.txt']
    self._create_replication_queue()
    cmd = process_replication_queue.Command()
    options = {'verbosity': "verbose"}
    cmd.handle_noargs()

  def _create_replication_queue(self):
    for sysmeta_path in sorted(
      glob.glob(
        os.path.join(
          '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_objects', '*.sysmeta'
        )
      )
    ):
      # Get name of corresponding object and open it.
      object_path = re.match(r'(.*)\.sysmeta', sysmeta_path).group(1)
      object_file = open(object_path, 'r')

      # The pid is stored in the sysmeta.
      sysmeta_file = open(sysmeta_path, 'r')
      sysmeta_xml = sysmeta_file.read()
      sysmeta_obj = d1_common.types.dataoneTypes.CreateFromDocument(sysmeta_xml)
      rep_queue_obj = models.ReplicationQueue()
      rep_queue_obj.status_id = 1
      rep_queue_obj.source_node_id = 2
      rep_queue_obj.pid = sysmeta_obj.identifier.value()
      rep_queue_obj.timestamp = datetime.now()
      rep_queue_obj.save()
