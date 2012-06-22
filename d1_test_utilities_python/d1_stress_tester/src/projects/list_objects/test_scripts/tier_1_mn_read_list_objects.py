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

# Path to modules shared between projects.
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
import sys
sys.path.append(_here('../../../projects/_shared/'))

import settings

# Config

cert_dir = './projects/_shared/certificates/certificates'
cert_key = './projects/_shared/certificates/local_test_client_cert.nopassword.key'


class Transaction(object):
  def __init__(self):
    self.custom_timers = {}

  def run(self):
    start_timer = time.time()
    self.list_objects_on_member_node()
    latency = time.time() - start_timer

    self.custom_timers['create'] = latency

  def list_objects_on_member_node(self):
    client = self.create_client()
    res = client.listObjects()
    print len(res.objectInfo)

  def create_client(self):
    return d1_client.mnclient.MemberNodeClient(
      base_url=settings.BASEURL,
      cert_path=self.get_random_certificate(),
      key_path=cert_key
    )

  def get_random_certificate(self):
    return os.path.join(cert_dir, random.choice(os.listdir(cert_dir)))


if __name__ == '__main__':
  t = Transaction()
  t.run()
  #import cProfile
  #cProfile.run('t.run()', 'profile')
