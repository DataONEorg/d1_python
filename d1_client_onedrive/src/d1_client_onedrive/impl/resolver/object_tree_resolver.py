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
""":mod:`resolver.object_tree`
============================

:Synopsis:
 - Resolve a filesystem path that points to a directory to the contents
   of the directory by querying the query engine.
:Author:
  DataONE (Dahl)
"""

# Stdlib
import pprint
import logging
import os
from StringIO import StringIO

# App
from ..onedrive_exceptions import ONEDriveException
from d1_client_onedrive.impl import attributes
from d1_client_onedrive.impl import cache_memory as cache
from d1_client_onedrive.impl import directory
from d1_client_onedrive.impl import onedrive_exceptions
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
  def __init__(self, options, object_tree):
    super(Resolver, self).__init__(options, object_tree)
    self._resource_map_resolver = resource_map.Resolver(options, object_tree)
    self._resolvers = {
      u'All': single.Resolver(options, object_tree),
      u'Authors': author.Resolver(options, object_tree),
      u'Regions': region.Resolver(options, object_tree),
      u'Taxa': taxa.Resolver(options, object_tree),
      u'TimePeriods': time_period.Resolver(options, object_tree),
    }

  def get_attributes(self, object_tree_root, path):
    log.debug(u'get_attributes: {0}'.format(util.string_from_path_elements(path)))

    # All items rendered by the ObjectTree Resolver are folders. Anything else is
    # deferred to one of the child resolvers.

    # To determine where the path transitions from the object_tree to the
    # controlled hierarchy, we check for the controlled hierarchy root names.
    # This means that those names are reserved. They can not be used as
    # object_tree folder names by the user.

    try:
      object_tree_folder = self._object_tree.get_folder(path, object_tree_root)
    except ONEDriveException:
      pass
    else:
      return attributes.Attributes(is_dir=True)

      #if len(path) > 0:
      #  if path[-1] == self._get_help_name():
      #    return attributes.Attributes(size=self._folderHelpSize(object_tree_folder),
      #                                 is_dir=False)

      # If the path is not to a object_tree folder root, a valid path must go to a
      # controlled hierarchy root or subfolder THROUGH a object_tree folder root. In
      # that case, the first path element that matches the reserved name of one of
      # the controlled hierarchy roots becomes the separator between the two
      # sections and determines which resolver to use for the tail section of the
      # path.
    object_tree_path, root_name, controlled_path = self._split_path_by_reserved_name(path)

    # If the object_tree_path is not valid now and is not the readme file, then
    # the path is invalid.
    try:
      object_tree_folder = self._object_tree.get_folder(
        object_tree_path, object_tree_root
      )
    except ONEDriveException:
      raise onedrive_exceptions.PathException(u'Invalid folder')

    if self._is_readme_file([root_name]):
      return self._get_readme_file_attributes(object_tree_path)

    # Now have all information required for gathering information about all the
    # objects in the object_tree folder and dispatching to a controlled hierarchy
    # resolver.
    #object_tree_folder = ObjectTreeFolderObjects(self._object_tree, object_tree_folder)
    return self._resolvers[root_name].get_attributes(object_tree_folder, controlled_path)

  def get_directory(self, object_tree_root, path, preconfigured_query=None):
    # the directory will typically be in the cache. already retrieved by
    # get_attributes, since get_attributes() needs to know how many items
    # there are in the directory, in order to return that count.
    log.debug(u'get_directory: {0}'.format(util.string_from_path_elements(path)))

    # To determine where the path transitions from the object_tree to the
    # controlled hierarchy, we check for the controlled hierarchy root names.
    # This means that those names are reserved. They can not be used as
    # object_tree folder names by the user.

    try:
      object_tree_folder = self._object_tree.get_folder(path, object_tree_root)
    except ONEDriveException:
      pass
    else:
      res = self._resolve_object_tree_folder(object_tree_folder)
      # All object_tree folders have a readme.
      res.append(self._get_readme_filename())
      return res

    # If the path is not to a object_tree folder root, a valid path must go to a
    # controlled hierarchy root or subfolder THROUGH a object_tree folder root. In
    # that case, the first path element that matches the reserved name of one of
    # the controlled hierarchy roots becomes the separator between the two
    # sections and determines which resolver to use for the tail section of the
    # path.
    object_tree_path, root_name, controlled_path = self._split_path_by_reserved_name(path)

    # If the object_tree_path is not valid now, then the path is invalid.
    try:
      object_tree_folder = self._object_tree.get_folder(
        object_tree_path, object_tree_root
      )
    except ONEDriveException:
      raise onedrive_exceptions.PathException(u'Invalid folder')

    log.debug('controlled path: {0}'.format(controlled_path))
    #log.debug('object_tree folder: {0}'.format(object_tree_folder))

    # Now have all information required for gathering information about all the
    # objects in the object_tree folder and dispatching to a controlled hierarchy
    # resolver.
    return self._resolvers[root_name].get_directory(object_tree_folder, controlled_path)

  def read_file(self, object_tree_root, path, size, offset):
    log.debug(
      u'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(
          path
        ), size, offset
      )
    )

    try:
      object_tree_folder = self._object_tree.get_folder(path, object_tree_root)
    except ONEDriveException:
      pass
    else:
      if len(path) > 0:
        if path[-1] == object_tree_folder.get_help_name():
          return self._getFolderHelp(object_tree_folder, size, offset)
          #return object_tree_folder.get_help_text(size, offset)
      raise onedrive_exceptions.PathException(u'Invalid file')

    object_tree_path, root_name, controlled_path = self._split_path_by_reserved_name(path)

    try:
      object_tree_folder = self._object_tree.get_folder(
        object_tree_path, object_tree_root
      )
    except ONEDriveException:
      raise onedrive_exceptions.PathException(u'Invalid folder')

    if self._is_readme_file([root_name]):
      return self._generate_readme_text(object_tree_path)[offset:offset + size]

    return self._resolvers[root_name].read_file(
      object_tree_folder, controlled_path, size, offset
    )

  #def load_object_tree(self, object_tree_xml):
  #  """Loads the object_tree XML document
  #  """
  #  self._object_tree = self._create_object_tree_from_xml_doc(object_tree_xml)
  #  #Additional processing to flush cache etc

  #def folderHelpSize(self, folder):
  #  """Return the size of the help text for a folder
  #  """
  #  try:
  #    return len(folder._helpText)
  #  except AttributeError:
  #    #Generate help text for folder
  #    self._getFolderHelp(folder)
  #    return len(folder._helpText)
  #  pass
  #
  #
  #def getFolderHelp(self, folder, size=None, offset=0):
  #  """Return help text for specific folder. If not available, then the
  #  help text is generated by reviewing the folder attributes. The help text
  #  is then attached to the folder object for future use.
  #  #TODO: consider thread safety for this.
  #  """
  #  try:
  #    test = folder._helpText
  #  except AttributeError:
  #    folder._helpText = util.os_format(generate_help_text(folder))
  #  res = folder._helpText[offset:offset + size]
  #  return res

  #
  # Private.
  #

  def _create_object_tree_from_xml_doc(self, xml_doc_path):
    xml_doc = open(xml_doc_path, 'rb').read()
    return object_tree_types.CreateFromDocument(xml_doc)

  def _split_path_by_reserved_name(self, path):
    """Return: object_tree_path, resolver, controlled_path
    """
    for i, e in enumerate(path):
      if e in self._resolvers or e == self._get_readme_filename():
        return path[:i], path[i], path[i + 1:]
    raise onedrive_exceptions.PathException(u'Invalid folder: %s' % str(path))

  def _resolve_object_tree_folder(self, object_tree_folder):
    dir = directory.Directory()
    self._append_folders(dir, object_tree_folder)
    dir.extend(self._resolvers.keys())
    return dir

  def _append_folders(self, d, object_tree_folder):
    for k in object_tree_folder['dirs']:
      d.append(k)
    return d

  # Readme

  def _get_readme_file_attributes(self, object_tree_path):
    return attributes.Attributes(
      size=len(self._generate_readme_text(object_tree_path)),
      is_dir=False
    )

  def _generate_readme_text(self, object_tree_path):
    """Generate a human readable description of the folder in text format.
    """

    wdef_folder = self._object_tree.get_source_tree_folder(object_tree_path)
    res = StringIO()
    if len(object_tree_path):
      folder_name = object_tree_path[-1]
    else:
      folder_name = 'root'
    header = u'ObjectTree Folder "{0}"'.format(folder_name)
    res.write(header + '\n')
    res.write('{0}\n\n'.format('=' * len(header)))
    res.write(u'The content present in object_tree folders is determined by a list\n')
    res.write(u'of specific identifiers and by queries applied against the DataONE\n')
    res.write(u'search index.\n\n')
    res.write(u'Queries:\n\n')
    if len(wdef_folder['queries']):
      for query in wdef_folder['queries']:
        res.write(u'- {}\n'.format(query))
    else:
      res.write(u'No queries specified at this level.\n')
    res.write(u'\n\n')
    res.write(u'Identifiers:\n\n')
    if len(wdef_folder['identifiers']):
      for pid in wdef_folder['identifiers']:
        res.write(u'- {}\n'.format(pid))
    else:
      res.write(u'No individual identifiers selected at this level.\n')
    res.write(u'\n\n')
    res.write(u'Sub-folders:\n\n')
    if len(wdef_folder['collections']):
      for f in wdef_folder['collections']:
        res.write(u'- {}\n'.format(f))
    else:
      res.write(u'No object_tree sub-folders are specified at this level.\n')
    return res.getvalue().encode('utf8')
