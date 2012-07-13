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
:mod:`tier_1_mn_core_get_log_records`
=====================================

:Created: 2011-04-22
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Std.
import datetime
import os
import random
import sys
import time
import uuid
import xml.sax.saxutils
import StringIO

# D1.
import d1_common.const
import d1_common.types.exceptions
import d1_common.types.generated.dataoneTypes as dataoneTypes

import d1_client.mnclient

import d1_instance_generator
import d1_instance_generator.random_data
import d1_instance_generator.systemmetadata
import d1_instance_generator.accesspolicy

# App.
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
sys.path.append(_here('../../../shared/'))
import settings
import pem_in_http_header

# Config
page_size = 1000


class Transaction(object):
  def __init__(self):
    self.custom_timers = {}
    self.total = self.get_log_records_total()
    print self.total

  def get_log_records_total(self):
    client = self.create_client()
    try:
      res = client.getLogRecords(count=0, start=0)
    except Exception as e:
      with open('/tmp/stress_test_error.html', 'w') as f:
        f.write(str(e))
      raise
    else:
      return res.total

  def run(self):
    start_timer = time.time()
    self.get_log_records_on_member_node()
    latency = time.time() - start_timer

    self.custom_timers['get_log_records'] = latency

  def get_log_records_on_member_node(self):
    client = self.create_client()
    start = random.randint(0, self.total - 1)
    count = page_size
    if start + count >= self.total - 1:
      count = self.total - start
    try:
      res = client.getLogRecords(start=start, count=count)
    except Exception as e:
      with open('/tmp/stress_test_error.html', 'w') as f:
        f.write(str(e))
      raise

  def create_client(self):
    cert_path = os.path.join(
      settings.CLIENT_CERT_DIR, settings.SUBJECT_WITH_CN_PERMISSIONS
    )
    key_path = settings.CLIENT_CERT_PRIVATE_KEY_PATH
    return d1_client.mnclient.MemberNodeClient(
      base_url=settings.BASEURL,
      cert_path=cert_path,
      key_path=key_path
    )


if __name__ == '__main__':
  t = Transaction()
  t.run()
  #import cProfile
  #cProfile.run('t.run()', 'profile')
