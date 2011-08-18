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
:Author: DataONE (dahl)
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

# 3rd party.
import iso8601

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


class Transaction(object):
  '''listObjects, public subject, unfiltered, randomly distributed.
  '''

  def __init__(self, profile=False):
    self.client = test_client.TestClient(settings.BASEURL)
    # Get page count.
    object_list = self.client.listObjects(start=0, count=0)
    # The integer divide causes n_pages to not include the last page, in the
    # likely case that the last page is less than PAGESIZE long.
    self.n_pages = object_list.total / settings.PAGESIZE
    self.profile = profile

  def list_objects(self):
    page_idx = random.randint(0, self.n_pages)
    if self.profile:
      vendor_specific = test_utilities.gmn_vse_enable_sql_profiling()
    else:
      vendor_specific = {}
    response = self.client.listObjectsResponse(
      start=page_idx * settings.PAGESIZE,
      count=settings.PAGESIZE,
      vendorSpecific=vendor_specific
    )
    assert (response.status == 200), 'Exception returned by listObjectsResponse'
    if self.profile:
      print response.read()

  def run(self):
    self.list_objects()


if __name__ == '__main__':
  trans = Transaction(profile=True)
  trans.run()
  #import cProfile
  #cProfile.run('trans.run()', 'profile')
