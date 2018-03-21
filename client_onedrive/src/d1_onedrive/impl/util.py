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
"""Misc utilities that don't fit anywhere else
"""

import errno
import logging
import os
import platform
import pprint


def log_dump(s):
  logging.debug('-' * 100)
  logging.debug('{}: {}'.format(s, pprint.pformat(s)))


def ensure_dir_exists(path):
  try:
    os.makedirs(path)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise


def string_from_path_elements(path):
  return os.path.sep.join(path)


def is_root(path):
  return path == ['', '']


def os_format(txt):
  if platform.system() == "Windows":
    return txt.replace('\n', '\r\n').encode('utf16')
  else:
    return txt.encode('utf-8')
