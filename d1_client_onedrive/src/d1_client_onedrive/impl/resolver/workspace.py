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
:Author:
  DataONE (Dahl)
'''

# Stdlib.
import pprint
import logging
import os
from StringIO import StringIO

# D1.
from d1_workspace.types.generated import workspace_types
from d1_workspace.workspace_exception import WorkspaceException

# App.
from d1_client_onedrive.impl import attributes
from d1_client_onedrive.impl import cache_memory as cache
from d1_client_onedrive.impl import directory
from d1_client_onedrive.impl import directory_item
from d1_client_onedrive.impl import path_exception
from d1_client_onedrive.impl.resolver import author
from d1_client_onedrive.impl.resolver import taxa
from d1_client_onedrive.impl.resolver import region
from d1_client_onedrive.impl.resolver import time_period
from d1_client_onedrive.impl.resolver import single
from d1_client_onedrive.impl import util
import resolver_base
import resource_map

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)


class Resolver(resolver_base.Resolver):
  def __init__(self, options, workspace):
    super(Resolver, self).__init__(options, workspace)
    self.resource_map_resolver = resource_map.Resolver(options, workspace)
    self.resolvers = {
      u'All': single.Resolver(options, workspace),
      u'Authors': author.Resolver(options, workspace),
      u'Regions': region.Resolver(options, workspace),
      u'Taxa': taxa.Resolver(options, workspace),
      u'TimePeriods': time_period.Resolver(options, workspace),
    }

  def get_attributes(self, workspace_root, path):
    log.debug(u'get_attributes: {0}'.format(util.string_from_path_elements(path)))

    # All items rendered by the Workspace Resolver are folders. Anything else is
    # deferred to one of the child resolvers.

    # To determine where the path transitions from the workspace to the
    # controlled hierarchy, we check for the controlled hierarchy root names.
    # This means that those names are reserved. They can not be used as
    # workspace folder names by the user.

    try:
      workspace_folder = self._workspace.get_folder(path, workspace_root)
    except WorkspaceException:
      pass
    else:
      return attributes.Attributes(is_dir=True)

      #if len(path) > 0:
      #  if path[-1] == self.get_help_name():
      #    return attributes.Attributes(size=self.folderHelpSize(workspace_folder),
      #                                 is_dir=False)

      # If the path is not to a workspace folder root, a valid path must go to a
      # controlled hierarchy root or subfolder THROUGH a workspace folder root. In
      # that case, the first path element that matches the reserved name of one of
      # the controlled hierarchy roots becomes the separator between the two
      # sections and determines which resolver to use for the tail section of the
      # path.
    workspace_path, root_name, controlled_path = self._split_path_by_reserved_name(path)

    # If the workspace_path is not valid now and is not the readme file, then
    # the path is invalid.
    try:
      workspace_folder = self._workspace.get_folder(workspace_path, workspace_root)
    except WorkspaceException:
      raise path_exception.PathException(u'Invalid folder')

    if self._is_readme_file([root_name]):
      return self._get_readme_file_attributes(workspace_path)

    # Now have all information required for gathering information about all the
    # objects in the workspace folder and dispatching to a controlled hierarchy
    # resolver.
    #workspace_folder = WorkspaceFolderObjects(self.workspace, workspace_folder)
    return self.resolvers[root_name].get_attributes(workspace_folder, controlled_path)

  def get_directory(self, workspace_root, path, preconfigured_query=None):
    # the directory will typically be in the cache. already retrieved by
    # get_attributes, since get_attributes() needs to know how many items
    # there are in the directory, in order to return that count.
    log.debug(u'get_directory: {0}'.format(util.string_from_path_elements(path)))

    # To determine where the path transitions from the workspace to the
    # controlled hierarchy, we check for the controlled hierarchy root names.
    # This means that those names are reserved. They can not be used as
    # workspace folder names by the user.

    try:
      workspace_folder = self._workspace.get_folder(path, workspace_root)
    except WorkspaceException:
      pass
    else:
      res = self._resolve_workspace_folder(workspace_folder)
      # All workspace folders have a readme.
      res.append(self._get_readme_directory_item())
      return res

    # If the path is not to a workspace folder root, a valid path must go to a
    # controlled hierarchy root or subfolder THROUGH a workspace folder root. In
    # that case, the first path element that matches the reserved name of one of
    # the controlled hierarchy roots becomes the separator between the two
    # sections and determines which resolver to use for the tail section of the
    # path.
    workspace_path, root_name, controlled_path = self._split_path_by_reserved_name(path)

    # If the workspace_path is not valid now, then the path is invalid.
    try:
      workspace_folder = self._workspace.get_folder(workspace_path, workspace_root)
    except WorkspaceException:
      raise path_exception.PathException(u'Invalid folder')

    log.debug('controlled path: {0}'.format(controlled_path))
    #log.debug('workspace folder: {0}'.format(workspace_folder))

    # Now have all information required for gathering information about all the
    # objects in the workspace folder and dispatching to a controlled hierarchy
    # resolver.
    return self.resolvers[root_name].get_directory(workspace_folder, controlled_path)

  def read_file(self, workspace_root, path, size, offset):
    log.debug(
      u'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(
          path
        ), size, offset
      )
    )

    try:
      workspace_folder = self._workspace.get_folder(path, workspace_root)
    except WorkspaceException:
      pass
    else:
      if len(path) > 0:
        if path[-1] == workspace_folder.get_help_name():
          return self.getFolderHelp(workspace_folder, size, offset)
          #return workspace_folder.get_help_text(size, offset)
      raise path_exception.PathException(u'Invalid file')

    workspace_path, root_name, controlled_path = self._split_path_by_reserved_name(path)

    try:
      workspace_folder = self._workspace.get_folder(workspace_path, workspace_root)
    except WorkspaceException:
      raise path_exception.PathException(u'Invalid folder')

    if self._is_readme_file([root_name]):
      return self._generate_readme_text(workspace_path)[offset:offset + size]

    return self.resolvers[root_name].read_file(
      workspace_folder, controlled_path, size, offset
    )

  #def load_workspace(self, workspace_xml):
  #  '''Loads the workspace XML document
  #  '''
  #  self._workspace = self._create_workspace_from_xml_doc(workspace_xml)
  #  #Additional processing to flush cache etc

  #def folderHelpSize(self, folder):
  #  '''Return the size of the help text for a folder
  #  '''
  #  try:
  #    return len(folder._helpText)
  #  except AttributeError:
  #    #Generate help text for folder
  #    self.getFolderHelp(folder)
  #    return len(folder._helpText)
  #  pass
  #
  #
  #def getFolderHelp(self, folder, size=None, offset=0):
  #  '''Return help text for specific folder. If not available, then the
  #  help text is generated by reviewing the folder attributes. The help text
  #  is then attached to the folder object for future use.
  #  #TODO: consider thread safety for this.
  #  '''
  #  try:
  #    test = folder._helpText
  #  except AttributeError:
  #    folder._helpText = util.os_format(generate_help_text(folder))
  #  res = folder._helpText[offset:offset + size]
  #  return res

  #
  # Private.
  #

  def _create_workspace_from_xml_doc(self, xml_doc_path):
    xml_doc = open(xml_doc_path, 'rb').read()
    return workspace_types.CreateFromDocument(xml_doc)

  def _split_path_by_reserved_name(self, path):
    '''Return: workspace_path, resolver, controlled_path
    '''
    for i, e in enumerate(path):
      if e in self.resolvers or e == self._get_readme_filename():
        return path[:i], path[i], path[i + 1:]
    raise path_exception.PathException(u'Invalid folder: %s' % str(path))

  def _resolve_workspace_folder(self, workspace_folder):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    self.append_folders(dir, workspace_folder)
    #if self.get_help_size() > 0:
    #  dir.append(self.get_help_directory_item())
    dir.extend([directory_item.DirectoryItem(name) for name in sorted(self.resolvers)])
    return dir

  def append_folders(self, d, workspace_folder):
    for k in workspace_folder['dirs']:
      d.append(directory_item.DirectoryItem(k))
    return d

  # Readme

  def _get_readme_file_attributes(self, workspace_path):
    return attributes.Attributes(
      size=len(self._generate_readme_text(workspace_path)),
      is_dir=False
    )

  def _generate_readme_text(self, workspace_path):
    '''Generate a human readable description of the folder in text format.
    '''

    wdef_folder = self._workspace.get_wdef_folder(workspace_path)

    res = StringIO()
    header = u'Workspace Folder "{0}"'.format(wdef_folder.name)
    res.write(header + '\n')
    res.write('{0}\n\n'.format('=' * len(header)))
    res.write(u'The content present in workspace folders is determined by a list\n')
    res.write(u'of specific identifiers and by queries applied against the DataONE\n')
    res.write(u'search index.\n\n')
    res.write(u'Queries:\n\n')
    if wdef_folder.query:
      for query in wdef_folder.query:
        res.write(u'- %s\n' % query)
    else:
      res.write(u'No queries specified at this level.\n')
    res.write(u'\n\n')
    res.write(u'Identifiers:\n\n')
    if wdef_folder.identifier:
      for pid in wdef_folder.identifier:
        res.write(u'- %s\n' % pid)
    else:
      res.write(u'No individual identifiers selected at this level.\n')
    res.write(u'\n\n')
    res.write(u'Sub-folders:\n\n')
    if wdef_folder.folder:
      for f in wdef_folder.folder:
        res.write(u'- %s\n' % f.name)
    else:
      res.write(u'No workspace sub-folders are specified at this level.\n')
    return res.getvalue().encode('utf8')
