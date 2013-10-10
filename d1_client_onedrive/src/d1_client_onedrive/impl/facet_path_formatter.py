#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
''':mod:`facet_path_formatter`
==============================

:Synopsis:
 - Decorate facet elements for use as filesystem elements.
:Author:
 - DataONE (Dahl)

See facet_path_parser.py for notes on the faceted path format.
'''

# Stdlib.
import logging
import os
import sys

# App.
sys.path.append('..')
import settings
import util

# Set up logger for this module.
log = logging.getLogger(__name__)
#Set level specific for this module if specified
try:
  log.setLevel(logging.getLevelName( \
               getattr(logging,'ONEDRIVE_MODULES')[__name__]) )
except:
  pass


class FacetPathFormatter(object):
  def __init__(
    self,
    facet_name_decorator=settings.FACET_NAME_DECORATOR,
    facet_value_decorator=settings.FACET_VALUE_DECORATOR
  ):
    self.facet_name_decorator = facet_name_decorator
    self.facet_value_decorator = facet_value_decorator

  def decorate_facet(self, facet):
    return self.decorate_facet_name(facet[0]), \
      self.decorate_facet_value(facet[1])

  def decorate_facet_name(self, facet_name):
    self._raise_if_already_facet_name(facet_name)
    return self.facet_name_decorator + facet_name

  def decorate_facet_value(self, facet_value):
    self._raise_if_already_facet_value(facet_value)
    return self.facet_value_decorator + facet_value

  # Private.

  def _raise_if_already_facet_name(self, e):
    if self._is_facet_name(e):
      raise Exception(u'Internal error: Is already facet name: {0}'.format(e))

  def _raise_if_already_facet_value(self, e):
    if self._is_facet_value(e):
      raise Exception(u'Internal error: Is already facet value: {0}'.format(e))

  def _is_facet_name(self, e):
    return e[0] == self.facet_name_decorator

  def _is_facet_value(self, e):
    return e[0] == self.facet_value_decorator
