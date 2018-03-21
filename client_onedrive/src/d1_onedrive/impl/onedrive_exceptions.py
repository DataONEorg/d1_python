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
"""Type that gets raised as exception for invalid paths
"""

import inspect
import logging

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)


class PathException(Exception):
  def __init__(self, message):
    Exception.__init__(self, message)
    trace = ', '.join(
      ['{}({})'.format(s[1], s[2]) for s in inspect.stack()[1:5]]
    )
    log.debug('PathException("{}"): {}'.format(message, trace))


class ONEDriveException(Exception):
  def __init__(self, message):
    Exception.__init__(self, message)
    trace = ', '.join(
      ['{}({})'.format(s[1], s[2]) for s in inspect.stack()[1:5]]
    )
    log.debug('ONEDriveException("{}"): {}'.format(message, trace))


class NoResultException(Exception):
  def __init__(self, message=""):
    Exception.__init__(self, message)
