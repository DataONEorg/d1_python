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

''':mod:`command_processor`
===========================

:Synopsis:
 - Interface to the backends.
:Author:
 - DataONE (Dahl)
'''

# Stdlib.
import logging
import os

# App.
import settings


# Set up logger for this module.
log = logging.getLogger(__name__)


class CommandProcessor(object):
  def __init__():




  def split_path_to_facet_and_object_sections(self, path):
    p = self._split_path(path)
    i = self._index_of_last_facet_name_or_value(p)
    if i is None:
      facet_section, object_section = [], p
    else:
      facet_section, object_section = p[:i + 1], p[i + 1:]
    self._raise_if_invalid_facet_section(facet_section)
    self._raise_if_invalid_object_section(object_section)
    return facet_section, object_section


  def undecorate_facets(self, p):
    facets = []
    for i, e in enumerate(p):
      if self._is_facet_name_position(i):
        facets.append(self.undecorate_facet_name(e))
      else:
        facets.append(self.undecorate_facet_value(e))
    return facets


  #def decorate_facets(self, facets):
  #  p = []
  #  for i, e in enumerate(facets):
  #    if self._is_facet_name_position(i):
  #      p.append(self.decorate_facet_name(e))
  #    else:
  #      p.append(self.decorate_facet_value(e))
  #  return self._join_path(p)


  def undecorated_tail(self, path):
    p = self._split_path(path)
    e = self._get_tail(p)
    if self.is_facet_name(e):
      return self.undecorate_facet_name(e)
    if self.is_facet_value(e):
      return self.undecorate_facet_value(e)
    return e


  def decorate_facet(self, facet):
    return self.decorate_facet_name(facet[0]), \
      self.decorate_facet_value(facet[1])


  def undecorate_facet(self, facet):
    return self.undecorate_facet_name(facet[0]), \
      self.undecorate_facet_value(facet[1])


  def decorate_facet_name(self, facet_name):
    assert(not self.is_facet_name(facet_name))
    return self.facet_name_decorator + facet_name


  def undecorate_facet_name(self, facet_name):
    assert(self.is_facet_name(facet_name))
    return facet_name[1:]


  def decorate_facet_value(self, facet_value):
    assert(not self.is_facet_value(facet_value))
    return self.facet_value_decorator + facet_value


  def undecorate_facet_value(self, facet_value):
    assert(self.is_facet_value(facet_value))
    return facet_value[1:]


  def dir_contains_facet_names(self, path):
    if self.is_root(path):
      return True
    e = self._get_tail(path)
    return self.is_facet_value(e)


  def dir_contains_facet_values(self, path):
    if self.is_root(path):
      return False
    e = self._get_tail(path)
    return self.is_facet_name(e)


  # ----------------------------------------------------------------------------

  def _index_of_last_facet_name_or_value(self, p):
    last = None
    for i, e in enumerate(p):
      if self._is_facet_name_or_value(e):
        last = i
    return last


  #def path_before_facets(self, path):
  #  self._assert_is_abs_path(path)
  #  i = self._find_index_of_first_facet(path)
  #  if i is None:
  #    return None
  #  return os.path.sep.join(path.split(os.path.sep)[:i + 1])


  #def path_after_facets(self, path):
  #  i = self._find_last_facet(path)
  #  if i is None:
  #    p = self._split_path_and_strip_empty(path)
  #  else:
  #    p = self._split_path_and_strip_empty(path)[i + 2:]
  #  if not len(p):
  #    return '/'
  #  return os.path.join(*p)



  #def has_one_or_more_facets(self, path):
  #  return self._find_index_of_first_facet(path) is not None


  def _raise_if_invalid_facet_section(self, p):
    self._raise_if_facet_section_contains_object_elements(p)
    self._raise_if_facet_section_is_incorrectly_ordered(p)


  def _raise_if_facet_section_contains_object_elements(self, p):
    for e in p:
      if not self._is_facet_name_or_value(e):
        raise path_exception.PathException(
          'Expected facet element. Got: {0}'.format(e))


  def _raise_if_facet_section_is_incorrectly_ordered(self, p):
    facet_name_value_toggle = True
    for e in p:
      if facet_name_value_toggle:
        if not self.is_facet_name(e):
          raise path_exception.PathException(
            'Expected facet name. Got: {0}'.format(e))
      else:
        if not self.is_facet_value(e):
          raise path_exception.PathException(
            'Expected facet value. Got: {0}'.format(e))
      facet_name_value_toggle = not facet_name_value_toggle


  def _is_facet_name_position(self, i):
    return not bool(i & 1)


  def _is_facet_value_position(self, i):
    return not self._is_facet_name_position(i)


  def _raise_if_invalid_object_section(self, p):
    self._raise_if_object_section_contains_facet_elements(p)


  def _raise_if_object_section_contains_facet_elements(self, p):
    for e in p:
      if self._is_facet_name_or_value(e):
        raise path_exception.PathException(
          'Expect object element. Got: {0}'.format(e))


  def _is_only_facet_elements(self, p):
    for e in p:
      if not self._is_facet_name_or_value(e):
        return False
    return True


  def _is_only_object_elements(self, p):
    for e in p:
      if self._is_facet_name_or_value(e):
        return False
    return True

    #print self._find_index_of_first_facet(p)
    #return self._find_index_of_first_facet(p) is None


  #def _find_index_of_first_facet(self, p):
  #  for i, f in enumerate(p[:-1]):
  #    if self.is_facet((f, p[i + 1])):
  #      return i


  #def _find_index_of_last_facet(self, p):
  #  last = None
  #  for i, f in enumerate(p[:-1]):
  #    if self.is_facet((f, p[i + 1])):
  #      last = i
  #  return last
  #

  def is_facet(self, facet):
    return self.is_facet_name(facet[0]) and self.is_facet_value(facet[1])


  def _is_facet_name_or_value(self, e):
    return self.is_facet_name(e) or self.is_facet_value(e)


  def is_facet_name(self, e):
    if not len(e):
      return False
    return e[0] == self.facet_name_decorator


  def is_facet_value(self, e):
    if not len(e):
      return False
    return e[0] == self.facet_value_decorator


  def is_root(self, path):
    return path == os.path.sep


  def _split_path_and_strip_empty(self, path):
    self._assert_is_abs_path(path)
    return path.rstrip(os.path.sep).split(os.path.sep)[1:]


  def _split_path(self, path):
    self._assert_is_abs_path(path)
    return path.split(os.path.sep)[1:]


  def _join_path(self, p):
    return os.path.sep.join(p)


  def _get_tail(self, p):
    if not len(p):
      return None
    return p[-1]


  def _assert_is_abs_path(self, path):
    assert(os.path.isabs(path))
