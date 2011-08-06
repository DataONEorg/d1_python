#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
:mod:`tier_3_mn_storage_create`
===============================

:Created: 2011-04-22
:Author: DataONE (dahl)
:Dependencies:
  - python 2.6
'''

# Std.
import datetime
import random
import sys
import StringIO
import time
import uuid
import xml.sax.saxutils

# 3rd party.
import iso8601

# D1.
sys.path.append('./client')
sys.path.append('./projects/gmn/test_scripts/client')
import d1_common.const
import d1_common.types.exceptions
import d1_test_case

# App.
sys.path.append('./client')
sys.path.append('./projects/gmn/test_scripts/client')
import d1_common.const
import test_client
import test_utilities
import generate_random_sysmeta

baseurl = 'http://localhost/mn'


class Transaction(object):
  def __init__(self):
    self.custom_timers = {}

  def session(self, subject):
    return {'VENDOR_OVERRIDE_SESSION': subject}

  def generate_random_file(self, num_bytes):
    return StringIO.StringIO(
      "".join(chr(random.randrange(0, 255)) for i in xrange(num_bytes))
    )

  def create_random_object(self):
    '''Create a single test object.
    '''
    client = test_client.TestClient(baseurl)

    #scidata_path = test_utilities.get_resource_path(
    #  'd1_testdocs/test_objects/hdl%3A10255%2Fdryad.167%2Fmets.xml')
    #sysmeta_path = test_utilities.get_resource_path(
    #  'd1_testdocs/test_objects/hdl%3A10255%2Fdryad.167%2Fmets.xml.sysmeta')

    pid_created = '__invalid_test_object__' + str(uuid.uuid1())

    scidata_size = random.randint(1, 2000)
    checksum_algorithm = 'SHA-1'

    scidata_file = self.generate_random_file(scidata_size)

    scidata_file.seek(0)
    checksum = test_utilities.calculate_checksum(scidata_file, checksum_algorithm)

    sysmeta = generate_random_sysmeta.generate_random_sysmeta(
      pid_created, scidata_size, checksum
    )

    scidata_file.seek(0)
    try:
      client.create(
        pid_created,
        scidata_file,
        sysmeta,
        vendorSpecific=self.session('test_user_1')
      )
    except:
      pass

  def run(self):
    start_timer = time.time()
    self.create_random_object()
    latency = time.time() - start_timer

    self.custom_timers['create'] = latency


if __name__ == '__main__':
  trans = Transaction()
  trans.run()
  print trans.custom_timers
