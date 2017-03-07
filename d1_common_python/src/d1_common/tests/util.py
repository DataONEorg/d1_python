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
import codecs
import xml

# 3rd party
import pyxb

# D1
import d1_common.types.dataoneTypes as dataoneTypes
import d1_common.types.dataoneErrors as dataoneErrors
import d1_common.util

# Stdlib
import os

# D1
import d1_common.types.dataoneTypes_v2_0 as v2


def get_test_filepath(filename):
  return os.path.join(d1_common.util.abs_path('test_docs'), filename)


def read_test_file(filename, mode_str='rb'):
  with open(get_test_filepath(filename), mode_str) as f:
    return f.read()


def read_utf8_to_unicode(filename):
  utf8_path = get_test_filepath(filename)
  unicode_file = codecs.open(utf8_path, encoding='utf-8', mode='r')
  return unicode_file.read()


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
