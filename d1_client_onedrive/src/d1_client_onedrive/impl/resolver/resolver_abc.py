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
''':mod:`resolver.resolver_abc`
===============================

:Synopsis:
 - Abstract Base Class (ABC) for the resolvers.
 - The resolvers are a class of objects that translate filesystem paths to
   their corresponding files and folders.
:Author: DataONE (Dahl)
'''

# Stdlib.
import abc
import logging
import os

# App.
from impl import attributes
from impl import directory
from impl import directory_item
from impl import path_exception

# Set up logger for this module.
log = logging.getLogger(__name__)
#Set level specific for this module if specified
try:
  log.setLevel(logging.getLevelName( \
               getattr(logging,'ONEDRIVE_MODULES')[__name__]) )
except:
  pass

README_NAME = u"readme.txt"


class Resolver(object):
  __metaclass__ = abc.ABCMeta

  def __init__(self, options, command_processor):
    self._options = options
    self.command_processor = command_processor
    self.helpText = ""

  def get_attributes(self, path, fs_path=''):
    if self.hasHelpEntry(path):
      return attributes.Attributes(size=self.helpSize(), is_dir=False)
    raise path_exception.NoResultException()

  def get_directory(self, path, fs_path=''):
    raise path_exception.NoResultException()

  def read_file(self, path, size, offset, fs_path=''):
    if self.hasHelpEntry(path):
      return self.getHelp(offset, size)
    raise path_exception.NoResultException()

  #def invalid_directory_error(self):
  #  directory = Directory()
  #  self.append_parent_and_self_references(directory)
  #  directory.append(DirectoryItem('<non-existing directory>', 0, False))
  #  return directory

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

  def hasHelpEntry(self, path):
    if len(path) > 0:
      if path[0] == README_NAME and self.helpSize() > 0:
        return True
    return False

  def helpName(self):
    return README_NAME

  def helpSize(self):
    return len(self.helpText)

  def getHelp(self, offset=0, size=None):
    return self.helpText[offset:size]

  def getHelpDirectoryItem(self):
    return directory_item.DirectoryItem(README_NAME, size=self.helpSize(), is_dir=False)
