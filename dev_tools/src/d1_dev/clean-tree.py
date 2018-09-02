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
"""Delete generated files in a Python source code tree.

See the file_iterator module for details on the arguments.

TODO: Matching directories in the root directory are not deleted.
"""

import argparse
import fnmatch
import logging
import os
import shutil
import sys

import d1_common.iter.dir
import d1_common.util

# Files and directories to delete
JUNK_GLOB_LIST = [
  # Dirs
  'build/', 'dist/', '*egg-info/', '__pycache__/', 'cover/', 'htmlcov/',
  '.cache/',
  # Files
  '*~', '*.bak', '*.tmp', '*.pyc', '.coverage', 'coverage.xml',
  'pip_freeze_*.txt',
] # yapf: disable


def main():
  parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
  )
  parser.add_argument('path', nargs='+', help='File or directory path')
  parser.add_argument('--include', nargs='+', help='Include glob patterns')
  parser.add_argument('--exclude', nargs='+', help='Exclude glob patterns')
  parser.add_argument(
    '--no-recursive', dest='recursive', action='store_false',
    help='Search directories recursively'
  )
  parser.add_argument(
    '--ignore-invalid', action='store_true', help='Ignore invalid paths'
  )
  parser.add_argument(
    '--debug', action='store_true', help='Debug level logging'
  )

  args = parser.parse_args()
  d1_common.util.log_setup(args.debug)

  itr = d1_common.iter.dir.dir_iter(
    path_list=args.path,
    include_glob_list=args.include,
    exclude_glob_list=args.exclude,
    recursive=args.recursive,
    ignore_invalid=args.ignore_invalid,
    default_excludes=False,
    return_dir_paths=True,
  )

  try:
    item_path = next(itr)
    while True:
      logging.debug('item_path="{}"'.format(item_path))
      is_junk_bool = is_junk(item_path)
      logging.debug('is_junk={} path="{}"'.format(is_junk_bool, item_path))
      if is_junk_bool:
        if os.path.isfile(item_path):
          logging.info('Deleting file: {}'.format(item_path))
          os.unlink(item_path)
        else:
          logging.info('Deleting dir:  {}'.format(item_path))
          shutil.rmtree(item_path)
      item_path = itr.send(is_junk_bool)
  except KeyboardInterrupt:
    logging.info('Interrupted')
    raise StopIteration
  except StopIteration:
    sys.exit()


def is_junk(path):
  junk_file_glob_list = [
    p for p in JUNK_GLOB_LIST if not p.endswith(os.path.sep)
  ]
  junk_dir_glob_list = [p for p in JUNK_GLOB_LIST if p.endswith(os.path.sep)]
  if os.path.isfile(path):
    return any(
      fnmatch.fnmatch(os.path.split(path)[1], g) for g in junk_file_glob_list
    )
  elif os.path.isdir(path):
    return any(
      fnmatch.fnmatch(os.path.split(path)[1] + '/', g)
      for g in junk_dir_glob_list
    )
  return False


if __name__ == '__main__':
  sys.exit(main())
