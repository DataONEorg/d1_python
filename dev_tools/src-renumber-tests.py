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
"""
import argparse
import logging
import re

import d1_common.util
import redbaron
import redbaron.nodes

import file_iterator
import util


def main():
  parser = argparse.ArgumentParser(
    description='Renumber test functions to free up space for new tests'
  )
  parser.add_argument('path', help='Root of Python source tree')
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
  parser.add_argument(
    '--diff', dest='diff_only', action='store_true', default=False,
    help='Show diff and do not modify any files'
  )
  parser.add_argument(
    '--move', action='store_true', default=False,
    help='Move remaining part of test function name to the test\'s docstring'
  )

  args = parser.parse_args()

  d1_common.util.log_setup(args.debug)

  logging.debug('Args:')
  logging.debug('  paths: {}'.format(args.path))
  logging.debug('  exclude: {}'.format(args.exclude))
  logging.debug('  recursive: {}'.format(args.recursive))
  logging.debug('  ignore_invalid: {}'.format(args.ignore_invalid))
  logging.debug('  default_excludes: {}'.format(args.default_excludes))
  logging.debug('  debug: {}'.format(args.debug))
  logging.debug('')

  for module_path in file_iterator.file_iter(
      path_list=[args.path],
      include_glob_list=['test_*.py'],
      exclude_glob_list=args.exclude,
      recursive=args.recursive,
      ignore_invalid=args.ignore_invalid,
      default_excludes=args.default_excludes,
  ):
    try:
      reindex(module_path, args.diff_only, args.move)
    except Exception as e:
      print 'Operation failed. error="{}" path="{}"'.format(
        module_path, e.message
      )
      if args.debug:
        raise


def reindex(module_path, diff_only, do_move):
  print 'Reindexing: {}'.format(module_path)
  r = util.redbaron_module_path_to_tree(module_path)
  if not has_test_class(r):
    logging.info(
      'Skipped: No Test class in module. path="{}"'.format(module_path)
    )
    return False
  reindex_test_method(r, do_move)
  util.update_module_file(r, module_path, diff_only)


def reindex_test_method(r, do_move):
  test_idx = 0
  for node in r('DefNode'):
    if is_test_func(node.name):
      test_idx += 10
      rename_method(node, test_idx, do_move)


def rename_method(node, test_idx, do_move):
  print 'Method: {}'.format(node.name)
  test_name, test_trailing = split_func_name(node.name)
  if not do_move:
    node.name = u'test_{:04d}{}'.format(test_idx, test_trailing)
  else:
    node.name = u'test_{:04d}'.format(test_idx)
    old_doc_str = get_doc_str(node)
    new_doc_str = gen_doc_str(test_trailing, old_doc_str)
    if new_doc_str != u'""""""':
      if has_doc_str(node):
        node.value[0].value = new_doc_str
      else:
        node.value.insert(0, new_doc_str)
    else:
      if has_doc_str(node):
        node.value.pop(0)


def is_test_func(func_name):
  return re.match(r'^test', func_name)


def is_test_class(class_name):
  return re.match(r'^Test', class_name)


def has_doc_str(node):
  return (
    isinstance(node.value[0], redbaron.nodes.StringNode) or
    isinstance(node.value[0], redbaron.nodes.UnicodeStringNode)
  )


def has_test_class(r):
  for node in r('ClassNode'):
    if is_test_class(node.name):
      return True
  return False


def get_doc_str(node):
  return node.value[0].value if has_doc_str(node) else u''


def split_func_name(func_name):
  m = re.match(r'(test_\D*)\d*_?(.*)', func_name)
  return m.group(1), m.group(2)


def gen_doc_str(post_name_str, old_doc_str):
  return u'"""{}{}"""'.format(
    post_name_str.replace(u'_', u' ') + ': ' if post_name_str else u'',
    old_doc_str.strip("""\r\n"\'"""),
  )


if __name__ == '__main__':
  main()
