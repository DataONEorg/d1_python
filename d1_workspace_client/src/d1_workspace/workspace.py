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
""":mod:`workspace`
===================

:Synopsis:
  Hold a local cache of the online workspace definition with Solr records for
  all identifiers and the results of all queries. Expose a simple API to query
  and refresh the cache. Keep a pickled version of the cache on disk.
:Author:
  DataONE (Dahl)
"""
"""
TERMS

wdef: The in-memory representation of the workspace definition as a PyXB object.
The master description of the user's workspace, (eventually) downloaded from the
online service. Only contains the folder tree, identifiers and queries that are
in the workspace. It does not contain any information about the identifiers and
the results of the queries.

wdef_disk: Workspace definition on disk. Stored as an xml file.

wcache: Workspace cache. The in-memory version of the complete workspace.
Contains the workspace hierarchy as described in the workspace definition and
contains all the records for the identifiers and the results of the queries.

wcache_disk: The workspace cache pickled on disk.


SYNC:

- load the workspace cache from disk. if this fails, start with empty workspace

- refresh:

  - load the workspace definition from disk (eventually from online service)

  - iterate over the cache and remove anything not in the definition:
    - an entire folder
    - a manually selected pid
    - a query

  - iterate over the definition and add anything to the cache that is not already there.

  - iterate over the cache and:
    - get any missing records for manually selected pids
    - run "count" queries to find mismatches between the cache and online queries.
      - if there's a mismatch, rerun query
"""

# Stdlib
import logging
try:
  import cPickle as pickle
except ImportError:
  import pickle
import os
import pprint

# App
import check_dependencies
import command_processor
from log_decorator import log_func
import settings
import util
import workspace_definition
import workspace_exception


class Workspace(object):
  def __init__(self, **options):
    """options: Override any of the defaults in settings.py by passing in
    key/value pairs where the key is in lower case. For instance:
    workspace_def_path=/tmp/my_file.xml will override the workspace_def_path
    default.
    """
    check_dependencies.check_dependencies()
    self._options = self._set_options(**options)
    self._command_processor = command_processor.CommandProcessor(self._options)
    util.ensure_dir_exists(self._options['workspace_cache_root'])

  def _set_options(self, **options_override):
    """Copy defaults from settings.py and optionally override them"""
    options = {}
    for k, v in settings.__dict__.items():
      if not k.isupper():
        continue
      try:
        options[k.lower()] = options_override[k.lower()]
      except KeyError:
        options[k.lower()] = v
    return options

  def __enter__(self):
    self._create_wdef()
    self._create_wcache()
    return self

  def __exit__(self, type, value, traceback):
    self._flush_wcache()

  def refresh(self):
    """Synchronize the local cache of the workspace with the workspace
    definition then add any missing Solr records and query results.
    """
    logging.info('Refreshing workspace')
    self._init_wcache()
    self.sync_wcache_with_wdef()
    self._wcache['workspace_timestamp'] = self._workspace_modified_timestamp()

  def get_folder(self, path, root=None):
    """Get the contents of a cached workspace folder"""
    return self._get_wcache_folder_recursive(path, root)

  def get_workspace_folder_name(self, workspace_folder):
    return workspace_folder['name']

  def get_object_record(self, pid):
    """This function is normally used for retriving records for objects cached
    in the workspace. Caching happens when the workspace is refreshed. The
    function can also be used for retriving records for objects that are
    currently not in the workspace. In that case, an attempt is made to retrieve
    the record from a CN on the fly. This allows the workspace caching system to
    be used for objects that are not in the workspace. ONEDrive uses this
    functionality for the FlatSpace folder.
    """
    try:
      return self._wcache['records'][pid]
    except KeyError:
      return self._get_uncached_object_record(pid)

  def get_science_object(self, pid):
    return self._command_processor.get_science_object(pid)

  def get_system_metadata(self, pid):
    return self._command_processor.get_system_metadata_as_string(pid)

  def get_wdef_folder(self, path):
    return self._get_wdef_folder_recursive(path)

  #
  # Private.
  #

  def _create_wcache(self):
    self._init_wcache()
    self._unpickle_wcache_from_disk()
    if self._wcache_is_stale():
      self.refresh()

  def _init_wcache(self):
    self._wcache = {
      'tree': {
        'name': self._wdef.name,
      },
      'records': {},
      'workspace_timestamp': None,
    }

  def _workspace_modified_timestamp(self):
    return os.path.getmtime(self._options['workspace_def_path'])

  def _get_uncached_object_record(self, pid):
    self._create_wcache_item_for_pid(None, pid)
    try:
      return self._wcache['records'][pid]
    except KeyError:
      raise workspace_exception.WorkspaceException('Unknown PID')

  def _wcache_is_stale(self):
    return self._wcache['workspace_timestamp'] is None or \
     self._wcache['workspace_timestamp'] < self._workspace_modified_timestamp()

  def _flush_wcache(self):
    self._pickle_wcache_to_disk()

  def _create_wdef(self):
    self._wdef = workspace_definition.WorkspaceDefinition(
      self._options['workspace_def_path']
    ).wdef

  def _unpickle_wcache_from_disk(self):
    try:
      with open(self._options['workspace_cache_path'], 'rb') as f:
        self._wcache = pickle.load(f)
    except (IOError, pickle.PickleError):
      pass

  def _pickle_wcache_to_disk(self):
    with open(self._options['workspace_cache_path'], 'wb') as f:
      pickle.dump(self._wcache, f)

  def sync_wcache_with_wdef(self):
    self._remove_wcache_items_no_longer_in_wdef()
    self._add_new_wdef_items_to_wcache()
    self._get_missing_solr_records()

  def _remove_wcache_items_no_longer_in_wdef(self):
    pass

  def _add_new_wdef_items_to_wcache(self):
    self._add_wdef_folder_to_wcache(self._wdef, [])
    for folder, path in self._iterate_wdef_recursive():
      self._add_wdef_folder_to_wcache(folder, path)

  def _add_wdef_folder_to_wcache(self, wdef_folder, path):
    wcache_folder = self._get_or_create_wcache_folder_recursive(path)
    self._create_wcache_items(wcache_folder, wdef_folder)

  def _iterate_wdef_recursive(self, wdef=None, path=None):
    if wdef is None:
      wdef = self._wdef
    if path is None:
      path = []
    for f in wdef.folder:
      yield f, path + [f.name]
      for f in self._iterate_wdef_recursive(f, path + [f.name]):
        yield f

  def _get_wdef_folder_recursive(self, path, wdef=None):
    if wdef is None:
      wdef = self._wdef
    if not path:
      return wdef
    for f in wdef.folder:
      if f.name == path[0]:
        return self._get_wdef_folder_recursive(path[1:], f)

  def _get_or_create_wcache_folder_recursive(
    self, path, folder=None, rpath=None
  ):
    if folder is None:
      folder = self._wcache['tree']
    if rpath is None:
      rpath = []
    dirs = folder.setdefault('dirs', {})
    if not path:
      return folder
    return self._get_or_create_wcache_folder_recursive(
      path[1:], dirs.setdefault(path[0], {'name': path[0]}), rpath + [path[0]]
    )

  def _create_wcache_items(self, wcache_folder, wdef_folder):
    items = wcache_folder.setdefault('items', {})
    self._create_wcache_item_for_pids(items, wdef_folder)
    self._create_wcache_items_for_queries(items, wdef_folder)

  def _create_wcache_item_for_pids(self, wcache_folder, wdef_folder):
    for pid in wdef_folder.identifier:
      self._create_wcache_item_for_pid(wcache_folder, pid)

  def _create_wcache_item_for_pid(self, wcache_folder, pid):
    """A workspace can contain identifiers that are no longer valid (or were
    never valid). Any items for which a Solr record cannot be retrieved are
    silently skipped."""
    try:
      record = self._command_processor.get_solr_record(pid)
    except workspace_exception.WorkspaceException:
      pass
    else:
      self._create_wcache_item(wcache_folder, record)

  def _create_wcache_items_for_queries(self, wcache_folder, wdef_folder):
    for query in wdef_folder.query:
      self._create_wcache_items_for_query(wcache_folder, query)

  def _create_wcache_items_for_query(self, wcache_folder, query):
    records = self._command_processor.run_solr_query(query)
    for record in records:
      self._create_wcache_item(wcache_folder, record)

  def _create_wcache_item(self, wcache_folder, record):
    if wcache_folder is not None:
      wcache_folder[record['id']] = True
    self._wcache['records'][record['id']] = record

  def _get_missing_solr_records(self):
    pass

  def _get_wcache_folder_recursive(self, path, folder=None):
    logging.debug('path={0}'.format(path))
    if folder is None:
      folder = self._wcache['tree']
    if not path:
      return folder
    try:
      return self._get_wcache_folder_recursive(
        path[1:], folder['dirs'][path[0]]
      )
    except KeyError:
      raise workspace_exception.WorkspaceException('Invalid path')
