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
:mod:`tier_1_mn_read_get`
=========================

:Created: 2011-04-22
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

import transaction


class Transaction(transaction.Transaction):
  def __init__(self):
    super().__init__()

  def d1_mn_api_call(self):
    """MNRead.get() called by regular user"""
    pid = self.select_random_public_object()
    client = self.create_public_client()
    response = client.getResponse(pid)
    self.check_response(response)
    response.read()


if __name__ == '__main__':
  t = Transaction()
  t.run()
  #import cProfile
  #cProfile.run('t.run()', 'profile')
