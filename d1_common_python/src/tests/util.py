#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2014 DataONE
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

# Stdlib.
import xml

# 3rd party.
import pyxb

# D1.
#import d1_common.types.dataoneTypes as dataoneTypes
import d1_common.types.dataoneTypes as dataoneTypes
import d1_common.types.dataoneErrors as dataoneErrors


def deserialize_and_check(doc, shouldfail=False):
  try:
    obj = dataoneTypes.CreateFromDocument(doc)
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
