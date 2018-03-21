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
"""Base resolver

Abstract Base Class (ABC) for the resolvers.

The resolvers are a class of objects that translate filesystem paths to their
corresponding files and folders.
"""

import logging

# App
from d1_onedrive.impl import attributes
from d1_onedrive.impl import onedrive_exceptions

log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

README_FILENAME = 'readme.txt'


class Resolver(object):
  #__metaclass__ = abc.ABCMeta

  def __init__(self, options, object_tree):
    self._options = options
    self._object_tree = object_tree
    self._readme_txt = ''

  def is_root(self, path):
    return path == ['', '']

  def _is_root(self, path):
    return not len(path)

  def _raise_exception_if_empty_directory(self, directory, msg=None):
    """In hierarchies where ONEDrive dynamically renders directories only after
    having determined that there are contents for them, an empty directory
    means that the path is invalid."""
    if len(directory) <= 2:
      raise onedrive_exceptions.PathException(msg)

  def _raise_invalid_pid(self, pid):
    raise onedrive_exceptions.PathException('Invalid PID: {}'.format(pid))

  # Readme file.

  def _is_readme_file(self, path):
    return path and path[0] == README_FILENAME

  def _get_readme_text(self, size=None, offset=0):
    return self._readme_txt[offset:offset + size]

  def _get_readme_file_attributes(self):
    return attributes.Attributes(size=len(self._readme_txt), is_dir=False)

  def _get_readme_filename(self):
    return README_FILENAME
