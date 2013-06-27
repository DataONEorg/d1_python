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
''':mod:`resolver.time_period`
==============================

:Synopsis:
 - Resolve a filesystem path pointing into a TimePeriod controlled hierarchy.
:Author: DataONE (Dahl)
'''

# Stdlib.
import httplib
import logging
import os
import pprint
import sys

# D1.

# App.
sys.path.append('.')
from impl import attributes
from impl import cache_memory as cache
from impl import command_processor
import d1_object
from impl import directory
from impl import directory_item
from impl import path_exception
import resolver_abc
#from impl #import settings
from impl import util

# Set up logger for this module.
log = logging.getLogger(__name__)

# Any open ranges have been closed by the command processor, so don't have to
# deal with those here.


class Resolver(resolver_abc.Resolver):
  def __init__(self, command_processor):
    self.command_processor = command_processor
    self.d1_object_resolver = d1_object.Resolver(command_processor)
    #self.facet_value_cache = cache.Cache(self._options.MAX_FACET_NAME_CACHE_SIZE)

    # The time_period resolver handles hierarchy levels:
    # / = Decades
    # /decade = all variations for group
    # All longer paths are handled by d1_object resolver.

  def get_attributes(self, path): #workspace_folder_objects
    log.debug('get_attributes: {0}'.format(util.string_from_path_elements(path)))

    if len(path) >= 3:
      return self.d1_object_resolver.get_attributes(path[2:])

    return self._get_attribute(path)

  def get_directory(self, path, workspace_folder_objects):
    log.debug('get_directory: {0}'.format(util.string_from_path_elements(path)))

    if len(path) >= 3:
      return self.d1_object_resolver.get_directory(path[2:])

    return self._get_directory(path, workspace_folder_objects)

  def read_file(self, path, size, offset):
    log.debug(
      'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(path), size, offset)
    )

    if len(path) >= 3:
      return self.d1_object_resolver.read_file(path[2:], size, offset)

    raise path_exception.PathException('Invalid file')

  # Private.

  def _get_attribute(self, path):
    return attributes.Attributes(0, is_dir=True)

  def _get_directory(self, path, workspace_folder_objects):
    if len(path) == 0:
      return self._resolve_decades(workspace_folder_objects)
    elif len(path) == 1:
      decade_range_str = path[0]
      return self._resolve_years_in_decade(decade_range_str, workspace_folder_objects)
    else:
      try:
        year = int(path[1])
      except ValueError:
        raise path_exception.PathException('Expected year element in path')
      else:
        return self._resolve_objects_in_year(year, workspace_folder_objects)

  def _resolve_decades(self, workspace_folder_objects):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    sites = set()
    for o in workspace_folder_objects.get_records():
      if 'beginDate' in o and 'endDate' in o:
        for decade in self._decade_ranges_in_date_range(o['beginDate'], o['endDate']):
          sites.add(decade)
    dir.extend([directory_item.DirectoryItem(a) for a in sites])
    return dir

  #def _add_decade_if_date_is_populated(self, sites, record, date_field):
  #  try:
  #    d = record['beginDate']
  #  except LookupError:
  #    pass
  #  else:
  #    sites.add(self._decade_from_date(d))

  #def _decade_from_date(self, d):
  #  decade = d.year / 10 * 10
  #  return '{0}-{1}'.format(decade, decade + 9)

  def _resolve_years_in_decade(self, decade, workspace_folder_objects):
    first_year_in_decade = self._validate_and_split_decade_range(decade)[0]
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    sites = set()
    for o in workspace_folder_objects.get_records():
      if 'beginDate' in o and 'endDate' in o:
        for year in self._years_in_date_range_within_decade(
          first_year_in_decade, o['beginDate'], o['endDate']
        ):
          sites.add(str(year))
    dir.extend([directory_item.DirectoryItem(a) for a in sites])
    self._raise_exception_if_empty_directory(dir)
    return dir

  def _resolve_objects_in_year(self, year, workspace_folder_objects):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    for o in workspace_folder_objects.get_records():
      if 'beginDate' in o and 'endDate' in o:
        if self._is_year_in_date_range(year, o['beginDate'], o['endDate']):
          dir.append(directory_item.DirectoryItem(o['id']))
    self._raise_exception_if_empty_directory(dir)
    return dir

  def _decade_ranges_in_date_range(self, begin_date, end_date):
    '''Return a list of decades which is covered by date range'''
    begin_dated = begin_date.year / 10
    end_dated = end_date.year / 10
    decades = []
    for d in range(begin_dated, end_dated + 1):
      decades.append('{0}-{1}'.format(d * 10, d * 10 + 9))
    return decades

  def _is_year_in_date_range(self, year, begin_date, end_date):
    return year >= begin_date.year and year <= end_date.year

  def _years_in_date_range_within_decade(self, decade, begin_date, end_date):
    '''Return a list of years in one decade which is covered by date range'''
    begin_year = begin_date.year
    end_year = end_date.year
    if begin_year < decade:
      begin_year = decade
    if end_year > decade + 9:
      end_year = decade + 9
    return range(begin_year, end_year + 1)

  def _validate_and_split_decade_range(self, decade):
    try:
      first_year, last_year = decade.split('-')
      if len(first_year) != 4 or len(last_year) != 4:
        raise ValueError
      first_year, last_year = int(first_year), int(last_year)
      if first_year > last_year:
        raise ValueError
    except ValueError:
      raise path_exception.PathException('Expected decade range on form yyyy-yyyy')
    else:
      return first_year, last_year
