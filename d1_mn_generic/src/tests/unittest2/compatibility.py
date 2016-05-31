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

import os
import sys

try:
  from functools import wraps
except ImportError:
  # only needed for Python 2.4
  def wraps(_):
    def _wraps(func):
      return func

    return _wraps


__unittest = True


def _relpath_nt(path, start=os.path.curdir):
  """Return a relative version of a path"""

  if not path:
    raise ValueError("no path specified")
  start_list = os.path.abspath(start).split(os.path.sep)
  path_list = os.path.abspath(path).split(os.path.sep)
  if start_list[0].lower() != path_list[0].lower():
    unc_path, rest = os.path.splitunc(path)
    unc_start, rest = os.path.splitunc(start)
    if bool(unc_path) ^ bool(unc_start):
      raise ValueError("Cannot mix UNC and non-UNC paths (%s and %s)" % (path, start))
    else:
      raise ValueError(
        "path is on drive %s, start on drive %s" % (path_list[0], start_list[0])
      )
  # Work out how much of the filepath is shared by start and path.
  for i in range(min(len(start_list), len(path_list))):
    if start_list[i].lower() != path_list[i].lower():
      break
  else:
    i += 1

  rel_list = [os.path.pardir] * (len(start_list) - i) + path_list[i:]
  if not rel_list:
    return os.path.curdir
  return os.path.join(*rel_list)


# default to posixpath definition
def _relpath_posix(path, start=os.path.curdir):
  """Return a relative version of a path"""

  if not path:
    raise ValueError("no path specified")

  start_list = os.path.abspath(start).split(os.path.sep)
  path_list = os.path.abspath(path).split(os.path.sep)

  # Work out how much of the filepath is shared by start and path.
  i = len(os.path.commonprefix([start_list, path_list]))

  rel_list = [os.path.pardir] * (len(start_list) - i) + path_list[i:]
  if not rel_list:
    return os.path.curdir
  return os.path.join(*rel_list)


if os.path is sys.modules.get('ntpath'):
  relpath = _relpath_nt
else:
  relpath = _relpath_posix
