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
"""Resolve a list of file and dir paths to a list of file paths with optional
filtering and client feedback.

This function is intended for use on a list of paths passed to a script on the
command line.

:param path_list: List of file- and dir paths. File paths are used directly and
dirs are searched for files.

:param include_glob_list: :param exclude_glob_list: Patterns ending with "/" are
matched only against dir names. All other patterns are matched only against file
names. If the include list contains any file patterns, files must match one or
more of the patterns in order to be returned. If the include list contains any
dir patterns, dirs must match one or more of the patterns in order for the
recursive search to descend into them. The exclude list works in the same way
except that matching files and dirs are excluded instead of included. If both
include and exclude lists are specified, files and dirs must both match the
include and not match the exclude patterns in order to be returned or descended
into.

:param recursive: Set to false to prevent subdirectories from being searched.
Each dir to search must then be specified directly in path_list.

:param ignore_invalid: True: Invalid paths in path_list are ignored. False
(default): EnvironmentError is raised if any of the paths in {path_list} do not
reference an existing file or dir.

:param default_excludes: True: A list of glob patterns for files and dirs that
should typically be ignored is added to any exclude patterns passed to the
function. These include dirs such as .git and backup files, such as files
appended with "~". False: No files or dirs are excluded by default.

:param return_dir_paths: False: Only file paths are returned. True: Directories
paths are also returned.

:return: File path iterator

Notes:

During iteration, the iterator can be prevented from descending into a directory
by sending a "skip" flag when the iterator yields the directory path. This
allows the client to determine if directories should be iterated by, for
instance, which files are present in the directory. This can be used in
conjunction with the include and exclude glob lists. Note that, in order to
receive directory paths that can be skipped, the return_dir_paths must be set to
True. The regular "for...in" syntax does not support sending the "skip" flag
back to the iterator. Instead, use a pattern like:

itr = file_iterator.file_iter(..., return_dir_paths=True) try: path = itr.next()
while True: skip_dir = determine_if_dir_should_be_skipped(path) file_path =
itr.send(skip_dir) except KeyboardInterrupt: raise StopIteration except
StopIteration: pass

{path_list} does not accept glob patterns, as it's more convenient to let the
shell expand glob patterns to directly specified files and dirs. E.g., to use a
glob to select all .py files in a subdir, the command may be called with
sub/dir/*.py, which the shell expands to a list of files, which are then passed
to this function. The paths should be Unicode or utf-8 strings. Tilde ("~") to
home expansion is performed on the paths.

The shell can also expand glob patterns to dir paths or a mix of file and dir
paths.

{include_glob_list} and {exclude_glob_list} are handy for filtering the files
found in dir searches.

Glob patterns are matched only against file and directory names, not the full
paths.

Paths passed directly in {path_list} are not filtered.

The same file can be returned multiple times if {path_list} contains duplicated
file paths or dir paths, or dir paths that implicitly include the same subdirs.

Remember to escape the include and exclude glob patterns on the command line so
that they're not expanded by the shell.
"""

# TODO: Update code and docstr for Py3

import fnmatch
import logging
import os

DEFAULT_EXCLUDE_GLOB_LIST = [
  # Dirs
  'build/', 'dist/', '*egg-info/', 'generated/', '.git/', 'doc/',
  '.idea/', 'migrations/', '__pycache__/',
  # Files
  '*~', '*.bak', '*.tmp', '*.pyc'
] # yapf: disable


def dir_iter(
    path_list,
    include_glob_list=None,
    exclude_glob_list=None,
    recursive=True,
    ignore_invalid=False,
    default_excludes=True,
    return_dir_paths=False,
):
  include_glob_list = include_glob_list or []
  exclude_glob_list = exclude_glob_list or []

  if default_excludes:
    exclude_glob_list += DEFAULT_EXCLUDE_GLOB_LIST

  logging.debug('file_iter():')
  logging.debug('  paths: {}'.format(', '.join(path_list)))
  logging.debug('  include: {}'.format(', '.join(include_glob_list)))
  logging.debug('  exclude: {}'.format(', '.join(exclude_glob_list)))
  logging.debug('  recursive: {}'.format(recursive))
  logging.debug('  ignore_invalid: {}'.format(ignore_invalid))
  logging.debug('  default_excludes: {}'.format(default_excludes))
  logging.debug('  return_dir_paths: {}'.format(return_dir_paths))
  logging.debug('')

  include_file_glob_list = [
    p for p in include_glob_list if not p.endswith(os.path.sep)
  ]
  exclude_file_glob_list = [
    p for p in exclude_glob_list if not p.endswith(os.path.sep)
  ]
  include_dir_glob_list = [
    p for p in include_glob_list if p.endswith(os.path.sep)
  ]
  exclude_dir_glob_list = [
    p for p in exclude_glob_list if p.endswith(os.path.sep)
  ]

  for path in path_list:
    path = os.path.expanduser(path)
    # if not isinstance(path, str):
    #   path = path.decode('utf-8')
    if not ignore_invalid:
      if not (os.path.isfile(path) or os.path.isdir(path)):
        raise EnvironmentError(0, 'Not a valid file or dir path', path)
    # Return file
    if os.path.isfile(path):
      file_name = os.path.split(path)[1]
      if not _is_filtered(
          file_name, include_file_glob_list, exclude_file_glob_list
      ):
        yield path
    # Search directory
    if os.path.isdir(path):
      if recursive:
        # Recursive directory search
        file_path_iter = _filtered_walk(
          path, include_dir_glob_list, exclude_dir_glob_list, return_dir_paths
        )
      else:
        # Single directory search
        file_path_iter = os.listdir(path)

      skip_dir = None

      while True:
        file_or_dir_path = file_path_iter.send(skip_dir)
        file_or_dir_name = os.path.split(file_or_dir_path)[1]
        skip_dir = False
        if not _is_filtered(
            file_or_dir_name, include_file_glob_list, exclude_file_glob_list
        ):
          skip_dir = yield file_or_dir_path

      # skip_dir = yield next(file_path_iter)
      # while True:
      #   file_or_dir_path = file_path_iter.send(skip_dir)
      #   file_or_dir_name = os.path.split(file_or_dir_path)[1]
      #   if not _is_filtered(
      #       file_or_dir_name, include_file_glob_list, exclude_file_glob_list
      #   ):
      #     skip_dir = yield file_or_dir_path
      #   else:
      #     skip_dir = False


def _is_filtered(name, include_glob_list, exclude_glob_list):
  return (
    include_glob_list and
    not any(fnmatch.fnmatch(name, g)
            for g in include_glob_list) or exclude_glob_list and
    any(fnmatch.fnmatch(name, g) for g in exclude_glob_list)
  )


def _filtered_walk(
    root_dir_path, include_dir_glob_list, exclude_dir_glob_list,
    return_dir_paths
):
  skip_dir_path_list = []
  for dir_path, dir_list, file_list in os.walk(root_dir_path):
    if any(dir_path.startswith(d) for d in skip_dir_path_list):
      logging.debug('Skipped dir tree. root="{}"'.format(dir_path))
      continue
    dir_list[:] = [
      d for d in dir_list
      if not _is_filtered(
        os.path.split(d)[1] + '/', include_dir_glob_list, exclude_dir_glob_list
      )
    ]
    if return_dir_paths:
      for dir_name in dir_list:
        this_dir_path = os.path.join(dir_path, dir_name)
        skip_dir = yield this_dir_path
        if skip_dir:
          logging.debug(
            'Client requested skip. root="{}"'.format(this_dir_path)
          )
          skip_dir_path_list.append(this_dir_path)
    for file_name in file_list:
      yield os.path.join(dir_path, file_name)
