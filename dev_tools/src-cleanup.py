#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2013 DataONE
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

from __future__ import absolute_import

import argparse
import logging

import file_iterator
import redbaron
import redbaron.nodes
import util

import d1_common.util


def main():
  parser = argparse.ArgumentParser(
    description='Perform various small source cleanup tasks on modules'
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
    '--diff', dest='diff_only', action='store_false', default=True,
    help='Show diff and do not modify any files'
  )
  parser.add_argument(
    '--debug', action='store_true', default=False, help='Debug level logging'
  )

  args = parser.parse_args()

  d1_common.util.log_setup(args.debug)

  for module_path in file_iterator.file_iter(
      path_list=args.path,
      include_glob_list=['*.py'] if not args.include else args.include,
      exclude_glob_list=args.exclude,
      recursive=args.recursive,
      ignore_invalid=args.ignore_invalid,
      default_excludes=args.default_excludes,
  ):
    modified_cnt = 0
    try:
      is_modified = clean_module(module_path, args.diff_only)
      if is_modified:
        modified_cnt += 1
    except Exception as e:
      logging.error(
        'Cleaning failed. error="{}" path="{}"'.format(module_path, str(e))
      )
      if args.debug:
        raise

  logging.info('Files modified: {}'.format(modified_cnt))


def clean_module(module_path, diff_only):
  logging.info('Cleaning module... path="{}"'.format(module_path))
  r = util.redbaron_module_path_to_tree(module_path)
  r = clean_all(r)
  return util.update_module_file(r, module_path, diff_only)


def clean_all(r):
  r = _remove_single_line_import_comments(r)
  r = _remove_module_level_docstrs_in_unit_tests(r)
  return r


def _remove_single_line_import_comments(r):
  """We previously used more groups for the import statements and named each
  group"""
  logging.info('Removing single line import comments')
  import_r, remaining_r = split_by_last_import(r)
  new_import_r = redbaron.NodeList()
  for i, v in enumerate(import_r):
    if 1 < i < len(import_r) - 2:
      if not (
          import_r[i - 2].type != 'comment' and v.type == 'comment' and
          import_r[i + 2].type != 'comment'
      ):
        new_import_r.append(v)
    else:
      new_import_r.append(v)
  return new_import_r + remaining_r


def _remove_module_level_docstrs_in_unit_tests(r):
  """We previously used more groups for the import statements and named each
  group"""
  logging.info('Removing module level docstrs in tests')
  new_r = redbaron.NodeList()
  first = True
  for v in r.node_list:
    if v.type == 'string' and first:
      first = False
    else:
      new_r.append(v)
  return new_r


def split_by_last_import(r):
  import_node_list = r('ImportNode', recursive=False)
  if not import_node_list:
    return redbaron.RedBaron('').node_list, r.node_list
  last_import_n = import_node_list[-1]
  import_r = r.node_list[:last_import_n.index_on_parent_raw + 1]
  remaining_r = r.node_list[last_import_n.index_on_parent_raw + 1:]
  return import_r, remaining_r


if __name__ == '__main__':
  main()
