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
''':mod:`resolver.workspace`
============================

:Synopsis:
 - Resolve a filesystem path that points to a directory to the contents
   of the directory by querying the query engine.
:Author: DataONE (Dahl)
'''

# Stdlib.
import pprint
import logging
import os
from StringIO import StringIO

# D1.
from d1_workspace.types.generated import generateFolderHelpText
from d1_workspace.types.generated import workspace_types

# App.
from d1_client_onedrive.impl import attributes
from d1_client_onedrive.impl import cache_memory as cache
from d1_client_onedrive.impl import command_processor
from d1_client_onedrive.impl import directory
from d1_client_onedrive.impl import directory_item
from d1_client_onedrive.impl import path_exception
from d1_client_onedrive.impl.resolver import author
from d1_client_onedrive.impl.resolver import taxa
from d1_client_onedrive.impl.resolver import region
from d1_client_onedrive.impl.resolver import time_period
from d1_client_onedrive.impl.resolver import single
from d1_client_onedrive.impl import util
import resolver_abc
import resource_map

# Set up logger for this module.
log = logging.getLogger(__name__)
# Set specific logging level for this module if specified.
try:
  log.setLevel(logging.getLevelName( \
               getattr(logging, 'ONEDRIVE_MODULES')[__name__]) )
except KeyError:
  pass

README = "readme.txt"


class WorkspaceFolderObjects(object):
  '''A workspace folder contains queries (that resolve to any number of matching
  PIDs) and PIDs that are specified directly. This class iteraterates over the
  queries and PIDs and issues Solr queries to get the records for each PID. This
  object then holds those records. Because the same object can be returned by
  any number of queries as well as be specified directly, the results are stored
  in a dictionary, keyed on the PID'''

  def __init__(self, command_processor, workspace_folder):
    self._command_processor = command_processor
    self._workspace_folder = workspace_folder
    self._records = self._get_records_for_identifiers()
    self._records.update(self._get_records_for_queries())
    self.helpText = u"Workspace Folder Object help text"

  def get_records(self):
    return self._records.values()

  def _get_records_for_identifiers(self):
    records = {}
    for pid in self._workspace_folder.identifier:
      try:
        records[pid] = self._command_processor.get_solr_record(pid)
      except path_exception.PathException:
        pass
    return records

  def _get_records_for_queries(self):
    records = {}
    for q in self._workspace_folder.query:
      response = self._command_processor.solr_query(q)
      for sci_obj in response['response']['docs']:
        records[sci_obj['id']] = sci_obj
        #log.debug(u"solr response doc: %s" % str(sci_obj))
    return records

  def helpSize(self):
    return len(self.helpText)

  def getHelp(self, offset=0, size=None):
    return self.helpText[offset:size]


class Resolver(resolver_abc.Resolver):
  def __init__(self, options, command_processor):
    super(Resolver, self).__init__(options, command_processor)
    self.resource_map_resolver = resource_map.Resolver(options, command_processor)
    self.load_workspace(options.WORKSPACE_XML)
    self.resolvers = {
      u'Authors': author.Resolver(self._options, self.command_processor),
      u'Regions': region.Resolver(self._options, self.command_processor),
      u'Taxa': taxa.Resolver(self._options, self.command_processor),
      u'TimePeriods': time_period.Resolver(self._options, self.command_processor),
      u'All': single.Resolver(self._options, self.command_processor),
    }
    #self.facet_value_cache = cache.Cache(self._options.MAX_FACET_NAME_CACHE_SIZE)
    self._generateHelp()

  def get_attributes(self, path, fs_path=''):
    log.debug(u'get_attributes: {0}'.format(util.string_from_path_elements(path)))

    # All items rendered by the Workspace Resolver are folders. Anything else
    # is deferred to one of the child resolvers.
    try:
      return super(Resolver, self).get_attributes(path, fs_path)
    except path_exception.NoResultException:
      pass

    # To determine where the path transitions from the workspace to the
    # controlled hierarchy, we check for the controlled hierarchy root names.
    # This means that those names are reserved. They can not be used as
    # workspace folder names by the user.
    workspace_folder = self._get_workspace_folder(path)

    # All workspace items are folders.
    if workspace_folder is not None:
      if len(path) > 0:
        if path[-1] == self.helpName():
          return attributes.Attributes(
            size=self.folderHelpSize(
              workspace_folder
            ), is_dir=False
          )
      return attributes.Attributes(is_dir=True)

    # If the path is not to a workspace folder root, a valid path must go to a
    # controlled hierarchy root or subfolder THROUGH a workspace folder root. In
    # that case, the first path element that matches the reserved name of one of
    # the controlled hierarchy roots becomes the separator between the two
    # sections and determines which resolver to use for the tail section of the
    # path.
    workspace_path, resolver, controlled_path = \
      self._split_path_by_reserved_name(path)

    # If the workspace_path is not valid now, then the path is invalid.
    workspace_folder = self._get_workspace_folder(workspace_path)
    if workspace_folder is None:
      raise path_exception.PathException(u'Invalid folder')

    if resolver == self.helpName():
      return attributes.Attributes(
        size=self.folderHelpSize(
          workspace_folder
        ), is_dir=False
      )

    # Now have all information required for gathering information about all the
    # objects in the workspace folder and dispatching to a controlled hierarchy
    # resolver.
    workspace_folder_objects = WorkspaceFolderObjects(
      self.command_processor, workspace_folder
    )
    return self.resolvers[resolver].get_attributes(
      controlled_path, workspace_folder_objects
    )

  def get_directory(self, path, preconfigured_query=None, fs_path=''):
    # the directory will typically be in the cache. already retrieved by
    # get_attributes, since get_attributes() needs to know how many items
    # there are in the directory, in order to return that count.
    log.debug(u'get_directory: {0}'.format(util.string_from_path_elements(path)))

    # To determine where the path transitions from the workspace to the
    # controlled hierarchy, we check for the controlled hierarchy root names.
    # This means that those names are reserved. They can not be used as
    # workspace folder names by the user.

    workspace_folder = self._get_workspace_folder(path)

    # If the path is to a workspace folder root, render the roots of the
    # controlled hierarchies and workspace subfolders. No need to get the object
    # metadata from solr at this point, as it is not yet known if the user will
    # actually enter one of the controlled hierarchies.
    if workspace_folder is not None:
      res = self._resolve_workspace_folder(workspace_folder)
      if self.folderHelpSize(workspace_folder) > 0:
        res.append(self.getHelpDirectoryItem())
      return res

    # If the path is not to a workspace folder root, a valid path must go to a
    # controlled hierarchy root or subfolder THROUGH a workspace folder root. In
    # that case, the first path element that matches the reserved name of one of
    # the controlled hierarchy roots becomes the separator between the two
    # sections and determines which resolver to use for the tail section of the
    # path.
    workspace_path, resolver, controlled_path = \
      self._split_path_by_reserved_name(path)

    # If the workspace_path is not valid now, then the path is invalid.
    workspace_folder = self._get_workspace_folder(workspace_path)
    if workspace_folder is None:
      raise path_exception.PathException(u'Invalid folder')

    # Now have all information required for gathering information about all the
    # objects in the workspace folder and dispatching to a controlled hierarchy
    # resolver.
    workspace_folder_objects = WorkspaceFolderObjects(
      self.command_processor, workspace_folder
    )
    return self.resolvers[resolver].get_directory(
      controlled_path, workspace_folder_objects
    )

  def read_file(self, path, size, offset, fs_path=''):
    log.debug(
      u'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(
          path
        ), size, offset
      )
    )
    try:
      return super(Resolver, self).read_file(path, size, offset, fs_path=fs_path)
    except path_exception.NoResultException:
      pass

    workspace_folder = self._get_workspace_folder(path)

    if workspace_folder is not None:
      if len(path) > 0:
        if path[-1] == workspace_folder.helpName():
          return self.getFolderHelp(workspace_folder, offset, size)
          #return workspace_folder.getHelp(offset, size)
      raise path_exception.PathException(u'Invalid file')

    workspace_path, resolver, controlled_path = \
      self._split_path_by_reserved_name(path)

    workspace_folder = self._get_workspace_folder(workspace_path)
    if workspace_folder is None:
      raise path_exception.PathException(u'Invalid folder')

    if resolver == self.helpName():
      res = self.getFolderHelp(workspace_folder, offset, size)
      return res

    workspace_folder_objects = WorkspaceFolderObjects(
      self.command_processor, workspace_folder
    )

    return self.resolvers[resolver].read_file(
      controlled_path, workspace_folder_objects, size, offset
    )

  def load_workspace(self, workspace_xml):
    '''Loads the workspace XML document
    '''
    self._workspace = self._create_workspace_from_xml_doc(workspace_xml)
    #Additional processing to flush cache etc

  def folderHelpSize(self, folder):
    '''Return the size of the help text for a folder
    '''
    try:
      return len(folder._helpText)
    except AttributeError:
      #Generate help text for folder
      self.getFolderHelp(folder)
      return len(folder._helpText)
    pass

  def getFolderHelp(self, folder, offset=0, size=None):
    '''Return help text for specific folder. If not available, then the
    help text is generated by reviewing the folder attributes. The help text
    is then attached to the folder object for future use.
    #TODO: consider thread safety for this.
    '''
    try:
      test = folder._helpText
    except AttributeError:
      #Need to generate the help text
      folder._helpText = util.os_format(generateFolderHelpText(folder))
    res = folder._helpText[offset:size]
    return res

  #
  # Private.
  #

  def _generateHelp(self):
    res = StringIO()
    t = u"ONEDrive Workspace Overview"
    res.write(t)
    res.write(u"\n")
    res.write(u"%s\n" % u"=" * len(t))
    res.write(u"\n")
    res.write(
      u"""
The ONEDrive Workspace folder contains objects that match queries specified
in the workspace configuration and individual identifiers
    """
    )
    return res.getvalue()

  def _create_workspace_from_xml_doc(self, xml_doc_path):
    xml_doc = open(xml_doc_path, 'rb').read()
    return workspace_types.CreateFromDocument(xml_doc)

  def _split_path_by_reserved_name(self, path):
    '''Return: workspace_path, resolver, controlled_path
    '''
    for i, e in enumerate(path):
      if e in self.resolvers:
        return path[:i], path[i], path[i + 1:]
      elif e == self.helpName():
        return path[:i], path[i], path[i + 1:]
    raise path_exception.PathException(u'Invalid folder: %s' % str(path))

  def _resolve_workspace_folder(self, workspace_folder):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    self.append_folders(dir, workspace_folder)
    #if self.helpSize() > 0:
    #  dir.append(self.getHelpDirectoryItem())
    dir.extend([directory_item.DirectoryItem(name) for name in sorted(self.resolvers)])
    return dir

  def append_folders(self, d, workspace_folder):
    for f in workspace_folder.folder:
      d.append(directory_item.DirectoryItem(f.name))
    return d

  # A workspace folder can contain other folders, identifiers or queries.
  # Identifiers and queries are rendered directly into a folder.

  #def is_workspace_folder(self, path):
  #  return self._get_workspace_folder(path) is not None

  # workspace = root Folder
  # To iterate over
  #  folders in Folder: Folder.folder
  #  PIDs in Folder: Folder.identifier
  #  SOLR queries in Folder: Folder.query

  def _get_workspace_folder(self, path):
    '''Given a path, return the members of that path from the workspace.
    '''
    return self._get_workspace_folder_recursive(self._workspace, path, 0)

  def _get_workspace_folder_recursive(self, folder, path, c):
    if len(path) == c:
      return folder
    for f in folder.folder:
      if f.name == path[c]:
        return self._get_workspace_folder_recursive(f, path, c + 1)
