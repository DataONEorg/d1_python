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
''':mod:`path_exception`
========================

:Synopsis:
 - Type that gets raised as exception for invalid paths.
:Author: DataONE (Dahl)
'''

import inspect
import logging

# Set up logger for this module.
log = logging.getLogger(__name__)
# Set specific logging level for this module if specified.
try:
  log.setLevel(logging.getLevelName(logging.ONEDRIVE_MODULES[__name__]))
except (KeyError, AttributeError):
  pass


class PathException(Exception):
  def __init__(self, message):
    Exception.__init__(self, message)
    trace = u', '.join([u'{0}({1})'.format(s[1], s[2]) for s in inspect.stack()[1:5]])
    log.debug(u'PathException("{0}"): {1}'.format(message, trace))


class NoResultException(Exception):
  def __init__(self, message=""):
    Exception.__init__(self, message)
