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

import d1_common.util

import file_iterator


def main():
  parser = argparse.ArgumentParser(
    description='Find files in dir tree with filtering'
  )
  parser.add_argument('path', nargs='+', help='File or directory path')
  parser.add_argument('--include', nargs='+', help='Include glob patterns')
  parser.add_argument('--exclude', nargs='+', help='Exclude glob patterns')
  parser.add_argument(
    '--no-recursive', dest='recursive', action='store_false', default=True,
    help='Search directories recursively'
  )
  parser.add_argument(
    '--ignore-invalid', action='store_true', default=False,
    help='Ignore invalid paths'
  )
  parser.add_argument(
    '--no-default-excludes', dest='default_excludes', action='store_false',
    default=True, help='Don\'t add default glob exclude patterns'
  )
  parser.add_argument(
    '--debug', action='store_true', default=False, help='Debug level logging'
  )

  args = parser.parse_args()

  d1_common.util.log_setup(args.debug)

  logging.debug('Args:')
  logging.debug('  paths: {}'.format(args.path))
  logging.debug('  include: {}'.format(args.include))
  logging.debug('  exclude: {}'.format(args.exclude))
  logging.debug('  recursive: {}'.format(args.recursive))
  logging.debug('  ignore_invalid: {}'.format(args.ignore_invalid))
  logging.debug('  default_excludes: {}'.format(args.default_excludes))
  logging.debug('  debug: {}'.format(args.debug))
  logging.debug('')

  for file_path in file_iterator.file_iter(
      path_list=args.path,
      include_glob_list=args.include,
      exclude_glob_list=args.exclude,
      recursive=args.recursive,
      ignore_invalid=args.ignore_invalid,
      default_excludes=args.default_excludes,
  ):
    print file_path


if __name__ == '__main__':
  main()
