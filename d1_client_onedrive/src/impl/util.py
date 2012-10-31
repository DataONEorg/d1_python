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
''':mod:`util`
==============

:Synopsis:
 - Misc utilities that don't fit anywhere else.
:Author: DataONE (Dahl)
'''

# Stdlib.
import collections
import logging
import os
import pprint

# App.
import os_escape

# Set up logger for this module.
log = logging.getLogger(__name__)

#def log_dump(s):
#  log.debug('{0}: {1}'.format(s, pprint.pformat(eval(s))))


def log_dump(s):
  log.debug(pprint.pformat(s))


def string_from_path_array(path):
  return os.path.sep.join(path)


def is_root(path):
  return path == ['', '']
