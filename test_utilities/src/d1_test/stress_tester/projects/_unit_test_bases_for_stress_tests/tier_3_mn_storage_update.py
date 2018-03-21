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
:mod:`tier_3_mn_storage_update`
===============================

:Created: 2011-04-22
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

import os

import context
import pytest
import test_client

import d1_test_case


class TestUpdate(d1_test_case.D1TestCase):
  def test_(self):
    pass

  def test_object_update(self):
    """Update an object.
    """
    # New object.
    # SysMeta
    sysmeta_file = 'hdl%3A10255%2Fdryad.669%2Fmets.xml.sysmeta'
    sysmeta_path = os.path.join(self.opts.obj_path, sysmeta_file)
    sysmeta_xml = open(sysmeta_path).read()
    # SciData
    object_path = os.path.splitext(sysmeta_path)[0]
    object_str = open(object_path, 'rb')
    #
    obsoleted_pid = 'AnserMatrix.htm'
    new_pid = 'update_object_pid'
    # Update.
    client = test_client.TestClient(context.node['baseurl'])
    response = client.updateResponse(
      context.TOKEN, obsoleted_pid, object_str, new_pid, sysmeta_xml
    )
    return response

  def delete(self):
    """MN_crud.delete() in GMN and libraries.
    """
    client = test_client.TestClient(context.node['baseurl'])
    # Find the PID for a random object that exists on the server.
    pid = self.find_valid_pid(client)
    # Delete the object on GMN.
    pid_deleted = client.delete(context.TOKEN, pid)
    assert pid == pid_deleted.value()
    # Verify that the object no longer exists.
    # We check for SyntaxError raised by the XML deserializer when it attempts
    # to deserialize a DataONEException. The exception is caused by the body
    # being empty since describe() uses a HEAD request.
    with pytest.raises(SyntaxError):
      client.describe(context.TOKEN, pid)
