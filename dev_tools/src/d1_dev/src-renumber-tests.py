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
"""Renumber test functions to free up space for new tests

By default, files are NOT modified. After having verified that the modifications
are as expected with the `--diff` switch, run the script again with `--update`
to modify the files.

When files are updated, the original file is backed up by appending "~" to the
original name. Any earlier backups are overwritten. Use clean-tree.py to delete
the backups.
"""

import argparse
import logging
import sys

import d1_dev.util

import d1_common.iter.dir
import d1_common.util


def main():
  parser = argparse.ArgumentParser(
    description='Renumber test functions to free up space for new tests'
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
    '--move', action='store_true',
    help='Move remaining part of test function name to the test\'s docstring'
  )
  parser.add_argument(
    '--diff', dest='show_diff', action='store_true',
    help='Show diff and do not modify any files'
  )
  parser.add_argument(
    '--dry-run', action='store_true',
    help='Process files but do not write results'
  )
  parser.add_argument(
    '--debug', action='store_true', help='Debug level logging'
  )

  args = parser.parse_args()

  d1_common.util.log_setup(args.debug)

  for module_path in d1_common.iter.dir.dir_iter(
      path_list=[args.path],
      include_glob_list=['test_*.py'],
      exclude_glob_list=args.exclude,
      recursive=args.recursive,
      ignore_invalid=args.ignore_invalid,
      default_excludes=args.default_excludes,
  ):
    try:
      renumber_module(module_path, args.move, args.show_diff, args.dry_run)
    except Exception as e:
      logging.error(
        'Operation failed. error="{}" path="{}"'.format(str(e), module_path)
      )
      if args.debug:
        raise


def renumber_module(module_path, do_move, show_diff, dry_run):
  logging.info('Renumbering: {}'.format(module_path))
  r = d1_dev.util.redbaron_module_path_to_tree(module_path)
  if not d1_dev.util.has_test_class(r):
    logging.info(
      'Skipped: No Test class in module. path="{}"'.format(module_path)
    )
    return False
  renumber_all(r, do_move)
  d1_dev.util.update_module_file(r, module_path, show_diff, dry_run)


def renumber_all(r, do_move):
  test_idx = 1000
  for node in r('DefNode'):
    if d1_dev.util.is_test_func(node.name):
      renumber_method(node, test_idx, do_move)
      test_idx += 10


def renumber_method(node, test_idx, do_move):
  new_name = 'test_{:04d}'.format(test_idx)
  if node.name != new_name:
    with d1_common.util.print_logging():
      logging.info('Method: {} -> {}'.format(node.name, new_name))
  node.name = new_name
  if not do_move:
    return
  test_name, test_trailing = d1_dev.util.split_func_name(node.name)
  old_doc_str = d1_dev.util.get_doc_str(node)
  new_doc_str = d1_dev.util.gen_doc_str(test_trailing, old_doc_str)
  if new_doc_str != '""""""':
    if d1_dev.util.has_doc_str(node):
      node.value[0].value = new_doc_str
    else:
      node.value.insert(0, new_doc_str)
  else:
    if d1_dev.util.has_doc_str(node):
      node.value.pop(0)


if __name__ == '__main__':
  sys.exit(main())
