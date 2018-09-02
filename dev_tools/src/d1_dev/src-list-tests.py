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
"""List tests and their docstrings
"""

import argparse
import logging
import os
import sys

import d1_dev.util

import d1_common.iter.dir
import d1_common.util


def main():
  parser = argparse.ArgumentParser(
    description='List tests and their docstrings'
  )
  parser.add_argument('path', help='Root of Python source tree')
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

  event_counter = d1_common.util.EventCounter()

  for module_path in d1_common.iter.dir.dir_iter(
      path_list=[args.path],
      include_glob_list=['test_*.py'],
      exclude_glob_list=args.exclude,
      recursive=args.recursive,
      ignore_invalid=args.ignore_invalid,
      default_excludes=args.default_excludes,
  ):
    try:
      list_tests_module(module_path, event_counter)
    except Exception as e:
      logging.error(
        'Operation failed. error="{}" path="{}"'.format(module_path, str(e))
      )
      if args.debug:
        raise

  event_counter.dump_to_log()


def list_tests_module(module_path, event_counter):
  r = d1_dev.util.redbaron_module_path_to_tree(module_path)
  if d1_dev.util.has_test_class(r):
    event_counter.count('Test files')
    list_tests_tree(r, module_path, event_counter)
  else:
    logging.debug(
      'Skipped: No Test class in module. path="{}"'.format(module_path)
    )
    event_counter.count('Test files without test classes')


def list_tests_tree(r, module_path, event_counter):
  for node in r('DefNode'):
    if d1_dev.util.is_test_func(node.name):
      if d1_dev.util.has_doc_str(node):
        doc_str = d1_dev.util.get_doc_str(node)
      else:
        doc_str = '<missing>'
        event_counter.count('Missing docstrings')
      with d1_common.util.print_logging():
        logging.info(
          '{}.{}: {}'.
          format(os.path.split(module_path)[1][:-3], node.name, doc_str)
        )


if __name__ == '__main__':
  sys.exit(main())
