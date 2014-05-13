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
''':mod:`resolver.resolver_base`
===============================

:Synopsis:
 - Abstract Base Class (ABC) for the resolvers.
 - The resolvers are a class of objects that translate filesystem paths to
   their corresponding files and folders.
:Author:
  DataONE (Dahl)
'''

# Stdlib.
import abc
import logging
import os
from StringIO import StringIO

# App.
from d1_client_onedrive.impl import attributes
from d1_client_onedrive.impl import directory
from d1_client_onedrive.impl import directory_item
from d1_client_onedrive.impl import path_exception

log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

README_FILENAME = u'readme.txt'


class Resolver(object):
  #__metaclass__ = abc.ABCMeta

  def __init__(self, options, workspace):
    self._options = options
    self._workspace = workspace
    self._readme_txt = ''

  def append_parent_and_self_references(self, directory):
    directory.append(directory_item.DirectoryItem('.'))
    directory.append(directory_item.DirectoryItem('..'))

  def is_root(self, path):
    return path == ['', '']

  def _is_root(self, path):
    return not len(path)

  def _raise_exception_if_empty_directory(self, directory, msg=None):
    '''In hierarchies where ONEDrive dynamically renders directories only after
    having determined that there are contents for them, an empty directory
    means that the path is invalid.'''
    if len(directory) <= 2:
      raise path_exception.PathException(msg)

  def _raise_invalid_pid(self, pid):
    raise path_exception.PathException(u'Invalid PID: {0}'.format(pid))

  # Readme file.

  def _is_readme_file(self, path):
    return path and path[0] == README_FILENAME

  def _get_readme_text(self, size=None, offset=0):
    return self._readme_txt[offset:offset + size]

  def _get_readme_file_attributes(self):
    return attributes.Attributes(size=len(self._readme_txt), is_dir=False)

  def _get_readme_directory_item(self):
    return directory_item.DirectoryItem(
      README_FILENAME, size=len(
        self._readme_txt
      ), is_dir=True
    )

  def _get_readme_filename(self):
    return README_FILENAME
