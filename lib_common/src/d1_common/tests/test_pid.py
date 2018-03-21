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

import xml.sax

import pyxb

import d1_common.types

import d1_test.d1_test_case

EG_PID_GMN = (
  '<?xml version="1.0" encoding="utf-8"?>\n'
  '<d1:identifier xmlns:d1="http://ns.dataone.org/service/types/v1"\n'
  ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
  ' xsi:schemaLocation="http://ns.dataone.org/service/types/v1 '
  'file:/home/roger/eclipse_workspace_d1/d1_common_python/src/d1_schemas/dataoneTypes.xsd">'
  'testpid</d1:identifier>', 'testpid',
)

# TODO.
EG_PID_KNB = ("""""", '',)

# Blank pid.
EG_BAD_PID_1 = (
  '<?xml version="1.0" encoding="utf-8"?>\n'
  '<d1:identifier xmlns:d1="http://ns.dataone.org/service/types/v1"\n'
  ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
  ' xsi:schemaLocation="http://ns.dataone.org/service/types/v1 '
  'file:/home/roger/eclipse_workspace_d1/d1_common_python/src/d1_schemas/dataoneTypes.xsd">'
  '</d1:identifier>', 'testpid',
)

# Missing identifier.
EG_BAD_PID_2 = ("""<?xml version="1.0" encoding="utf-8"?>""", 'testpid',)


class TestPID(d1_test.d1_test_case.D1TestCase):
  def deserialize_pid_and_check(self, doc, raises_pyxb_exc=False):
    try:
      obj = d1_common.types.dataoneTypes.CreateFromDocument(doc[0])
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if raises_pyxb_exc:
        return
      else:
        raise
    if raises_pyxb_exc:
      raise Exception('Did not receive expected exception')
    assert obj.value() == doc[1]

  def test_1000(self):
    """deserialize gmn: Deserialize: XML -> PID (GMN)"""
    self.deserialize_pid_and_check(EG_PID_GMN)

  def test_1010(self):
    """deserialize knb: Deserialize: XML -> PID (KNB)"""
    # TODO.
    #doctest(EG_PID_KNB)

  def test_1020(self):
    """deserialize bad 1: Deserialize: XML -> PID (bad 1)"""
    self.deserialize_pid_and_check(EG_BAD_PID_1, raises_pyxb_exc=True)

  def test_1030(self):
    """deserialize bad 2: Deserialize: XML -> PID (bad 2)"""
    self.deserialize_pid_and_check(EG_BAD_PID_2, raises_pyxb_exc=True)
