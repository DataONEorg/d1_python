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
''':mod:`facet_path_parser`
===========================

:Synopsis:
 - Convert between facet list and filesystem path.
:Author:
 - DataONE (Dahl)

Notes on the faceted path format:

- A facet path is on the form:
  [/@facet_name_1/#facet_value_1/.../@facet_name_N/#facet_value_N]/
  [pid_folder/[folder_1/.../folder_N/[file]]]
- The path is represented as a list of path segments.
- The facet path consists of two sections. Both sections are optional.
- The first section, if present, must be a list of facets, representing a
  faceted search. All of the facet elements must start with one of the two
  facet decorators.
- The second section, if present, must be a folder hierarchy that starts with a
  DataONE PID and may contain more elements, pointing to specific information
  about the object. It cannot contain any elements starting with one of the
  two facet decorators.
- If none of the two sections are present, the path points to the root, which
  will then show the names of all available facets and the PIDs of all objects
  in DataONE. The list will be truncated.
- All facet folders must appear before non-facet folders.
- The last element in the facet section can be a facet name, causing possible
  facet values for that name to be included in the directory listing.
- The last element in the facet section can be a complete facet, causing names
  of unapplied facets to be included in the directory listing.
- The elements in the facet sections must start with a facet name and alternate
  between facet names and facet values.

Implementation notes:

- path is a list of path elements
- e is a path element, excluding any path separators
'''

# Stdlib.
import logging
import os
import sys

# App.
sys.path.append('..')
import path_exception
import settings
import util

# Set up logger for this module.
log = logging.getLogger(__name__)


class FacetPathParser(object):
  def __init__(
    self,
    facet_name_decorator=settings.FACET_NAME_DECORATOR,
    facet_value_decorator=settings.FACET_VALUE_DECORATOR
  ):
    self.facet_name_decorator = facet_name_decorator
    self.facet_value_decorator = facet_value_decorator

  def split_path_to_facet_and_object_sections(self, path):
    i = self._index_of_last_facet_name_or_value(path)
    if i is None:
      facet_section, object_section = [], path
    else:
      facet_section, object_section = path[:i + 1], path[i + 1:]
    self._raise_if_invalid_facet_section(facet_section)
    self._raise_if_invalid_object_section(object_section)
    return facet_section, object_section

  def facets_from_path(self, path):
    pairs = self._pair_path_elements(path)
    return self._undecorate_pairs(pairs)

  # Private.

  def _pair_path_elements(self, path):
    p = path[:]
    p.append(None)
    return zip(p[::2], p[1::2])

  def _undecorate_pairs(self, pairs):
    return [self._undecorate_facet(p) for p in pairs]

  #  def decorate_facet(self, facet):
  #    return self.decorate_facet_name(facet[0]), \
  #      self.decorate_facet_value(facet[1])

  def _undecorate_facet(self, facet):
    return self.undecorate_facet_name(facet[0]), \
      self.undecorate_facet_value(facet[1])

#  def decorate_facet_name(self, facet_name):
#    assert(not self._is_facet_name(facet_name))
#    return self.facet_name_decorator + facet_name

  def undecorate_facet_name(self, facet_name):
    self._raise_if_not_facet_name(facet_name)
    return facet_name[1:]

#  def decorate_facet_value(self, facet_value):
#    assert(not self._is_facet_value(facet_value))
#    return self.facet_value_decorator + facet_value

  def undecorate_facet_value(self, facet_value):
    if facet_value is None:
      return None
    self._raise_if_not_facet_value(facet_value)
    return facet_value[1:]

#  def dir_contains_facet_names(self, path):
#    if util.is_root(path):
#      return True
#    e = self._get_tail(path)
#    return self._is_facet_value(e)

#  def dir_contains_facet_values(self, path):
#    if util.is_root(path):
#      return False
#    e = self._get_tail(path)
#    return self._is_facet_name(e)

  def _index_of_last_facet_name_or_value(self, path):
    last = None
    for i, e in enumerate(path):
      if self._is_facet_name_or_value(e):
        last = i
    return last

#  def path_before_facets(self, path):
#    self._assert_is_abs_path(path)
#    i = self._find_index_of_first_facet(path)
#    if i is None:
#      return None
#    return os.path.sep.join(path.split(os.path.sep)[:i + 1])

#  def path_after_facets(self, path):
#    i = self._find_last_facet(path)
#    if i is None:
#      path = self._split_path_and_strip_empty(path)
#    else:
#      path = self._split_path_and_strip_empty(path)[i + 2:]
#    if not len(path):
#      return '/'
#    return os.path.join(*path)

#  def has_one_or_more_facets(self, path):
#    return self._find_index_of_first_facet(path) is not None

  def _raise_if_invalid_facet_section(self, path):
    self._raise_if_facet_section_contains_object_elements(path)
    self._raise_if_facet_section_is_incorrectly_ordered(path)

  def _raise_if_facet_section_contains_object_elements(self, path):
    for e in path:
      if not self._is_facet_name_or_value(e):
        raise path_exception.PathException('Expected facet element. Got: {0}'.format(e))

  def _raise_if_facet_section_is_incorrectly_ordered(self, path):
    for i, e in enumerate(path):
      if self._is_facet_name_position(i):
        self._raise_if_not_facet_name(e)
      else:
        self._raise_if_not_facet_value(e)

  def _raise_if_not_facet_name(self, e):
    if not self._is_facet_name(e):
      raise path_exception.PathException('Expected facet name. Got: {0}'.format(e))

  def _raise_if_not_facet_value(self, e):
    if not self._is_facet_value(e):
      raise path_exception.PathException('Expected facet value. Got: {0}'.format(e))

  def _is_facet_name_position(self, i):
    return not bool(i & 1)

#  def _is_facet_value_position(self, i):
#    return not self._is_facet_name_position(i)

  def _raise_if_invalid_object_section(self, path):
    self._raise_if_object_section_contains_facet_elements(path)

  def _raise_if_object_section_contains_facet_elements(self, path):
    for e in path:
      if self._is_facet_name_or_value(e):
        raise path_exception.PathException('Expect object element. Got: {0}'.format(e))

#  def _is_only_facet_elements(self, path):
#    for e in path:
#      if not self._is_facet_name_or_value(e):
#        return False
#    return True

#  def _is_only_object_elements(self, path):
#    for e in path:
#      if self._is_facet_name_or_value(e):
#        return False
#    return True

#print self._find_index_of_first_facet(path)
#return self._find_index_of_first_facet(path) is None

#  def _find_index_of_first_facet(self, path):
#    for i, f in enumerate(path[:-1]):
#      if self.is_facet((f, path[i + 1])):
#        return i

#  def _find_index_of_last_facet(self, path):
#    last = None
#    for i, f in enumerate(path[:-1]):
#      if self.is_facet((f, path[i + 1])):
#        last = i
#    return last

#  def is_facet(self, facet):
#    return self._is_facet_name(facet[0]) and self._is_facet_value(facet[1])

  def _is_facet_name_or_value(self, e):
    return self._is_facet_name(e) or self._is_facet_value(e)

  def _is_facet_name(self, e):
    if e is None or not len(e):
      return False
    return e[0] == self.facet_name_decorator

  def _is_facet_value(self, e):
    if e is None or not len(e):
      return False
    return e[0] == self.facet_value_decorator

#  def _get_tail(self, path):
#    if not len(path):
#      return None
#    return path[-1]
