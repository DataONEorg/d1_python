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
""":mod:`check_dependencies`
============================

:Synopsis:
 - Check the dependencies by attempting to import them.
:Author: DataONE (Dahl)
"""

# Stdlib
import logging
import platform


def check_dependencies():
  exceptions = []
  messages = []

  try:
    import pyxb
  except ImportError as e:
    exceptions.append(e)
    messages.append(u'PyXB: Try "sudo pip install pyxb"\n')

  if len(exceptions):
    log.critical(u'Importing of the following dependencies failed.')
    for msg in messages:
      log.critical(msg)
    log.critical(u'Import errors:')
    for e in exceptions:
      log.critical(str(e))

    return False

  return True
