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
:mod:`tier_1_mn_core_getlogrecords`
===================================

:Created: 2011-04-22
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Std.
import datetime
import sys
import time

# D1.
import d1_common.const

# App.

# Path to modules shared between projects.
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
import sys
sys.path.append(_here('../../../projects/_shared/'))

import settings
import test_client


class Transaction(object):
  def __init__(self, profile=False):
    self.custom_timers = {}

  def list_objects(self):
    '''Get first page of log records.
    '''
    client = test_client.TestClient(settings.BASEURL)

    object_list = client.listObjects(start=0, count=0)

    #self.assertEqual(object_list.start, 0)
    #self.assertEqual(object_list.count, 0)
    #self.assertTrue(object_list.total >= 15)
    #
    #context.object_total = object_list.total
    #assert (resp.code == 200), 'Bad HTTP Response'
    #assert ('Example Web Page' in resp.get_data()), 'Failed Content Verification'

  def run(self):
    start_timer = time.time()
    self.list_objects()
    latency = time.time() - start_timer

    self.custom_timers['list_objects'] = latency


if __name__ == '__main__':
  trans = Transaction(profile=True)
  trans.run()
  #import cProfile
  #cProfile.run('trans.run()', 'profile')
