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
"""Source code aware filesystem iterator with filtering

A handy way to search for files in a Python source code tree.

See the file_iterator module for details on the arguments.
"""

import argparse
import logging
import sys

import d1_common.iter.dir
import d1_common.util


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
    '--no-default-excludes', dest='default_excludes', action='store_false',
    help='Don\'t add default glob exclude patterns'
  )
  parser.add_argument(
    '--debug', action='store_true', help='Debug level logging'
  )

  args = parser.parse_args()

  d1_common.util.log_setup(args.debug)

  for file_path in d1_common.iter.dir.dir_iter(
      path_list=args.path,
      include_glob_list=args.include,
      exclude_glob_list=args.exclude,
      recursive=args.recursive,
      ignore_invalid=args.ignore_invalid,
      default_excludes=args.default_excludes,
  ):
    with d1_common.util.print_logging():
      logging.info(file_path)


if __name__ == '__main__':
  sys.exit(main())
