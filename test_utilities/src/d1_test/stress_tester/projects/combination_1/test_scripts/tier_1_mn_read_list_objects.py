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
"""
:mod:`tier_1_mn_read_list_objects`
==================================

:Created: 2011-04-22
:Author: DataONE (Dahl)
"""

import random

import transaction

# Config
page_size = 1000


class Transaction(transaction.Transaction):
  def __init__(self):
    super().__init__()
    self.total = self.get_object_total()

  def get_object_total(self):
    client = self.create_client_for_cn()
    try:
      res = client.listObjects(count=0, start=0)
    except Exception as e:
      with open('/tmp/stress_test_error.html', 'w') as f:
        f.write(str(e))
      raise
    else:
      return res.total

  # Definition of listObjects from mnclient.py:
  #
  # def listObjects(self, fromDate=None, toDate=None, formatId=None,
  #                 replicaStatus=None, start=0,
  #                 count=d1_common.const.DEFAULT_LISTOBJECTS,
  #                 vendorSpecific=None):

  def d1_mn_api_call(self):
    """MNRead.ListObjects()"""
    client = self.create_client_for_cn()
    start = random.randint(0, self.total - 1)
    count = page_size
    if start + count >= self.total - 1:
      count = self.total - start
    response = client.listObjectsResponse(start=start, count=count)
    self.check_response(response)


if __name__ == '__main__':
  t = Transaction()
  t.run()
  #import cProfile
  #cProfile.run('t.run()', 'profile')
