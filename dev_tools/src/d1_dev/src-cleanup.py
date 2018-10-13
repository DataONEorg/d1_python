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
"""Perform various small source cleanup tasks on modules

By default, files are NOT modified. After having verified that the modifications
are as expected with the `--diff` switch, run the script again with `--update`
to modify the files.

When files are updated, the original file is backed up by appending "~" to the
original name. Any earlier backups are overwritten. Use clean-tree.py to delete
the backups.
"""

import argparse
import lib2to3.main
import lib2to3.refactor
import logging
import os
import re
import sys

import d1_dev.util
import redbaron
import redbaron.nodes

import d1_common.iter.dir
import d1_common.util

# Single line comments containing these strings will not be removed.
KEEP_COMMENTS = ['noqa', 'noinspection']

COPYRIGHT_NOTICE = """\

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-{} DataONE
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

"""


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
    '--diff', dest='show_diff', action='store_true',
    help='Show diff and do not modify any files'
  )
  parser.add_argument(
    '--update', action='store_true',
    help='Apply the updates to the original files. By default, no files are '
    'changed.'
  )
  parser.add_argument(
    '--debug', action='store_true', help='Debug level logging'
  )

  args = parser.parse_args()

  d1_common.util.log_setup(args.debug)

  event_counter = d1_common.util.EventCounter()

  for module_path in d1_common.iter.dir.dir_iter(
      path_list=args.path,
      include_glob_list=['*.py'] if not args.include else args.include,
      exclude_glob_list=args.exclude,
      recursive=args.recursive,
      ignore_invalid=args.ignore_invalid,
      default_excludes=args.default_excludes,
  ):
    try:
      is_cleaned = clean_module(module_path, args.show_diff, args.update)
      if is_cleaned:
        event_counter.count('Cleaned files')

      # is_futurized = futurize_module(module_path, args.show_diff, args.update)
      # if is_futurized:
      #   event_counter.count('Futurized files')

    except Exception as e:
      logging.error(
        'Cleaning failed. error="{}" path="{}"'.format(module_path, str(e))
      )
      if args.debug:
        raise

  event_counter.dump_to_log()


def clean_module(module_path, show_diff, write_update):
  logging.info('Cleaning module... path="{}"'.format(module_path))
  r = d1_dev.util.redbaron_module_path_to_tree(module_path)
  r = clean_all(module_path, r)
  return d1_dev.util.update_module_file(r, module_path, show_diff, write_update)


def clean_all(module_path, r):
  # r = _remove_single_line_import_comments(r)
  # r = _remove_module_level_docstrs_in_unit_tests(r)
  # r = _add_absolute_import(r)
  # r = _update_init_all(module_path, r)
  # r = _remove_init_all(r)
  r = _insert_copyright_header(r)
  return r


def futurize_module(module_path, show_diff, write_update):
  """2to3 uses AST, not Baron"""
  logging.info('Futurizing module... path="{}"'.format(module_path))
  ast_tree = back_to_the_futurize(module_path)
  return d1_dev.util.update_module_file_ast(
    ast_tree, module_path, show_diff, write_update
  )


# remove_single_line_import_comments


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
      ) or _is_keep_comment(v):
        new_import_r.append(v)
    else:
      new_import_r.append(v)
  return new_import_r + remaining_r


def _is_keep_comment(r):
  return any([keep in r.value[0] for keep in KEEP_COMMENTS]) # maybe?
  # return any([keep in r.value for keep in KEEP_COMMENTS])


# remove_module_level_docstrs


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


# add_absolute_import


def _add_absolute_import(r):
  if has_future_absolute_import(r):
    return r

  new_r = redbaron.NodeList()
  first = True
  for v in r.node_list:
    if v.type == 'import' and first:
      first = False
      new_r.append(
        redbaron.RedBaron('from __future__ import absolute_import\n')
      )
    new_r.append(v)
  return new_r


def has_future_absolute_import(r):
  import_node_list = r('FromImportNode', recursive=False)
  return any([
    rr.value[0].value == '__future__' and
    'absolute_import' in [v.value for v in rr.targets]
    for rr in import_node_list if rr.value
  ])


# The following fixers are "safe": they convert Python 2 code to more
# modern Python 2 code. They should be uncontroversial to apply to most
# projects that are happy to drop support for Py2.5 and below. Applying
# them first will reduce the size of the patch set for the real porting.
lib2to3_fix_names_stage1 = {
  'lib2to3.fixes.fix_apply',
  'lib2to3.fixes.fix_except',
  'lib2to3.fixes.fix_exec',
  'lib2to3.fixes.fix_exitfunc',
  'lib2to3.fixes.fix_funcattrs',
  'lib2to3.fixes.fix_has_key',
  'lib2to3.fixes.fix_idioms',
  'lib2to3.fixes.fix_intern',
  'lib2to3.fixes.fix_isinstance',
  'lib2to3.fixes.fix_methodattrs',
  'lib2to3.fixes.fix_ne',
  'lib2to3.fixes.fix_numliterals',
  'lib2to3.fixes.fix_paren',
  'lib2to3.fixes.fix_reduce',
  'lib2to3.fixes.fix_renames',
  'lib2to3.fixes.fix_repr',
  'lib2to3.fixes.fix_standarderror',
  'lib2to3.fixes.fix_sys_exc',
  'lib2to3.fixes.fix_throw',
  'lib2to3.fixes.fix_tuple_params',
  'lib2to3.fixes.fix_types',
  'lib2to3.fixes.fix_ws_comma',
  'lib2to3.fixes.fix_xreadlines',
}

libfuturize_fix_names_stage1 = {
  'libfuturize.fixes.fix_absolute_import',
  'libfuturize.fixes.fix_next_call',
  'libfuturize.fixes.fix_print_with_import',
  'libfuturize.fixes.fix_raise',
}


def back_to_the_futurize(module_path):
  fixer_names_set = lib2to3_fix_names_stage1 | libfuturize_fix_names_stage1
  mt = lib2to3.refactor.MultiprocessRefactoringTool(
    fixer_names=sorted(fixer_names_set)
  )
  with open(module_path, 'rb') as f:
    module_str = f.read()
  tree = mt.refactor_string(module_str, 'urk')
  if mt.errors:
    raise ValueError('lib2to3 refactor error')
  # mt.summarize()
  return tree


def _update_init_all(module_path, r):
  """Add or update __all__ in __init__.py file"""
  module_dir_path = os.path.split(module_path)[0]
  module_list = []
  for item_name in os.listdir(module_dir_path):
    item_path = os.path.join(module_dir_path, item_name)
    if os.path.isfile(item_path) and item_name in ('__init__.py', 'setup.py'):
      continue
    if os.path.isfile(item_path) and not item_name.endswith('.py'):
      continue
    # if os.path.isdir(item_path) and not os.path.isfile(
    #     os.path.join(item_path, '__init__.py')
    # ):
    #   continue
    if os.path.isdir(item_path):
      continue
    module_list.append(re.sub(r'.py$', '', item_name).encode('utf-8'))
  module_literal_str = str(sorted(module_list))

  assignment_node_list = r('AssignmentNode', recursive=False)
  for n in assignment_node_list:
    if n.type == 'assignment' and n.target.value == '__all__':
      n.value = module_literal_str
      break
  else:
    r.node_list.append(
      redbaron.RedBaron('__all__ = {}\n'.format(module_literal_str))
    )
  return r


def _remove_init_all(r):
  """Remove any __all__ in __init__.py file"""
  new_r = redbaron.NodeList()
  for n in r.node_list:
    if n.type == 'assignment' and n.target.value == '__all__':
      pass
    else:
      new_r.append(n)
  return new_r


def _insert_copyright_header(r):
  for i, n in enumerate(r.node_list):
    if n.type == 'comment' and re.search(r'Copyright.*DataONE', n.value):
      return r
  logging.info('Adding copyright header')
  i = 0
  for n in r('CommentNode', recursive=False)[:3]:
    if n.value.startswith('#!') or 'coding' in n.value:
      # Skip endl node.
      i = n.index_on_parent_raw + 2
  r.node_list.insert(
    i,
    redbaron.
    RedBaron(COPYRIGHT_NOTICE.format(d1_common.date_time.utc_now().year))
  )
  return r


if __name__ == '__main__':
  sys.exit(main())
