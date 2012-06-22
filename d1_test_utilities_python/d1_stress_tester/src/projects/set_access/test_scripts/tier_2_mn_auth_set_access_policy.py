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
:mod:`tier_2_mn_auth_set_access_policy`
=======================================

:Created: 2011-08-09
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Std.
import datetime
import os
import random
import sys
import StringIO
import threading
import time
import uuid
import xml.sax.saxutils

# D1.
import d1_common.const
import d1_common.types.exceptions

# App.

# Path to modules shared between projects.
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
import sys
sys.path.append(_here('../../../projects/_shared/'))

import settings
import test_client
import test_utilities
import d1_test_case
import generate_random_sysmeta

page_idx = 0
page_idx_lock = threading.Lock()


class Transaction(object):
  def __init__(self, profile=False):
    #self.custom_timers = {}
    self.client = test_client.TestClient(settings.BASEURL)
    # Get total object count.
    object_list = self.client.listObjects(start=0, count=0)
    self.n_pages, rem = divmod(object_list.total, settings.PAGESIZE)
    if rem:
      self.n_pages += 1
    self.profile = profile

#  def set_random_access_policy(self, pid):
#    access_policy = generate_random_sysmeta.generate_random_access_policy()
#    #print access_policy.toxml()
#    if self.profile:
#      vendor_specific = test_utilities.gmn_vse_enable_sql_profiling()
#    else:
#      vendor_specific = {}
#    vendor_specific.update(
#      #d1_common.const.SUBJECT_TRUSTED
#      test_utilities.gmn_vse_provide_subject('trusted'))
#    response = self.client.setAccessPolicyResponse(pid, access_policy,
#                           vendorSpecific=vendor_specific)
#    assert (response.status == 200), \
#      'Exception returned by setAccessPolicyResponse'
#    if self.profile:
#      print response.read()

  def set_random_access_policies(self):
    global page_idx
    if page_idx >= self.n_pages:
      return
    object_list = self.client.listObjects(
      start=page_idx * settings.PAGESIZE,
      count=settings.PAGESIZE
    )
    #print object_list.toxml()
    for obj in object_list.objectInfo:
      pid = obj.identifier.value()
      #print pid
      self.set_random_access_policy(pid)
    with page_idx_lock:
      page_idx += 1
    print '\r{0}'.format(page_idx)

  def run(self):
    #start_timer = time.time()
    self.set_random_access_policies()
    #latency = time.time() - start_timer
    #self.custom_timers['set_access_policy'] = latency

if __name__ == '__main__':
  trans = Transaction(profile=False)
  trans.run()
  #import cProfile
  #cProfile.run('trans.run()', 'profile')
