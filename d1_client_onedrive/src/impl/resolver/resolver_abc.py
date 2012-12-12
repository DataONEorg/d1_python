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
 - Base class for the resolvers.
 - The resolvers are a class of objects that translate filesystem paths to
   their corresponding files and folders.
:Author: DataONE (Dahl)
'''

# Stdlib.
import abc
import logging
import os

# App.
import directory
import directory_item

# Set up logger for this module.
log = logging.getLogger(__name__)


class Resolver(object):
  __metaclass__ = abc.ABCMeta

  def __init__(self):
    pass

  @abc.abstractmethod
  def get_attributes(self, path):
    pass

  @abc.abstractmethod
  def get_directory(self, path):
    pass

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

#  def _is_root(self, path):
#    return path == ['']
