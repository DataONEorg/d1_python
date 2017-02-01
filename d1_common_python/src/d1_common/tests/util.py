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

# Stdlib
import xml

# 3rd party
import pyxb

# D1
import d1_common.types.dataoneTypes as dataoneTypes
import d1_common.types.dataoneErrors as dataoneErrors


# Stdlib
import os

# D1
import d1_common.types.dataoneTypes_v2_0 as v2


def make_absolute(p):
  return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)


def read_test_file(filename, mode_str='rb'):
  with open(
    os.path.join(make_absolute('test_docs'), filename), mode_str
  ) as f:
    return f.read()


def read_test_xml(filename, mode_str='r'):
  xml_str = read_test_file(filename, mode_str)
  xml_obj = v2.CreateFromDocument(xml_str)
  return xml_obj


def deserialize_and_check(doc, shouldfail=False):
  try:
    dataoneTypes.CreateFromDocument(doc)
  except (pyxb.PyXBException, xml.sax.SAXParseException):
    if shouldfail:
      return
    else:
      raise
  if shouldfail:
    raise Exception('Did not receive expected exception')


def deserialize_exception_and_check(doc, shouldfail=False):
  try:
    obj = dataoneErrors.CreateFromDocument(doc)
  except (pyxb.PyXBException, xml.sax.SAXParseException):
    if shouldfail:
      return
    else:
      raise
  if shouldfail:
    raise Exception('Did not receive expected exception')
  return obj
