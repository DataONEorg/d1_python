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
:Author:
  DataONE (Dahl)
'''

# Stdlib.
import httplib
import logging
import os
import pprint
import sys

# D1.

# App.
from d1_client_onedrive.impl import attributes
from d1_client_onedrive.impl import cache_memory as cache
from d1_client_onedrive.impl import directory
from d1_client_onedrive.impl import directory_item
from d1_client_onedrive.impl import path_exception
from d1_client_onedrive.impl import util
import resolver_base
import resource_map

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)

# Any open ranges have been closed by the command processor, so don't have to
# deal with those here.


class Resolver(resolver_base.Resolver):
  def __init__(self, options, workspace):
    super(Resolver, self).__init__(options, workspace)
    self.resource_map_resolver = resource_map.Resolver(options, workspace)
    #self.facet_value_cache = cache.Cache(self._options.max_facet_name_cache_size)

    # The time_period resolver handles hierarchy levels:
    # / = Decades
    # /decade = all variations for group
    # All longer paths are handled by d1_object resolver.

  def get_attributes(self, workspace_folder, path):
    log.debug(u'get_attributes: {0}'.format(util.string_from_path_elements(path)))
    if self._is_readme_file(path):
      return self._get_readme_file_attributes()

    if len(path) <= 2:
      return self._get_attribute(path)

    return self.resource_map_resolver.get_attributes(workspace_folder, path[2:])

  def get_directory(self, workspace_folder, path):
    log.debug(u'get_directory: {0}'.format(util.string_from_path_elements(path)))

    if len(path) <= 2:
      return self._get_directory(workspace_folder, path)

    return self.resource_map_resolver.get_directory(workspace_folder, path[2:])

  def read_file(self, workspace_folder, path, size, offset):
    log.debug(
      u'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(path), size, offset)
    )
    if self._is_readme_file(path):
      return self._get_readme_text(size, offset)
    if len(path) <= 2:
      raise path_exception.PathException(u'Invalid file')
    return self.resource_map_resolver.read_file(workspace_folder, path[2:], size, offset)

  # Private.

  def _get_attribute(self, path):
    return attributes.Attributes(0, is_dir=True)

  def _get_directory(self, workspace_folder, path):
    if len(path) == 0:
      return self._resolve_decades(workspace_folder)
    elif len(path) == 1:
      decade_range_str = path[0]
      return self._resolve_years_in_decade(decade_range_str, workspace_folder)
    else:
      try:
        year = int(path[1])
      except ValueError:
        raise path_exception.PathException(u'Expected year element in path')
      else:
        return self._resolve_objects_in_year(year, workspace_folder)

  def _resolve_decades(self, workspace_folder):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    sites = set()
    for pid in workspace_folder['items']:
      record = self._workspace.get_object_record(pid)
      if 'beginDate' in record and 'endDate' in record:
        for decade in self._decade_ranges_in_date_range(
          record['beginDate'], record['endDate']
        ):
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

  def _resolve_years_in_decade(self, decade, workspace_folder):
    first_year_in_decade = self._validate_and_split_decade_range(decade)[0]
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    sites = set()
    for pid in workspace_folder['items']:
      record = self._workspace.get_object_record(pid)
      if 'beginDate' in record and 'endDate' in record:
        for year in self._years_in_date_range_within_decade(
          first_year_in_decade, record['beginDate'], record['endDate']
        ):
          sites.add(str(year))
    dir.extend([directory_item.DirectoryItem(a) for a in sites])
    self._raise_exception_if_empty_directory(dir)
    return dir

  def _resolve_objects_in_year(self, year, workspace_folder):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    for pid in workspace_folder['items']:
      record = self._workspace.get_object_record(pid)
      if 'beginDate' in record and 'endDate' in record:
        if self._is_year_in_date_range(year, record['beginDate'], record['endDate']):
          if record.has_key("resourceMap"):
            for rmap_id in record['resourceMap']:
              dir.append(directory_item.DirectoryItem(rmap_id))
          else:
            dir.append(directory_item.DirectoryItem(record['id']))
          #dir.append(directory_item.DirectoryItem(o['id']))
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
      raise path_exception.PathException(u'Expected decade range on form yyyy-yyyy')
    else:
      return first_year, last_year
