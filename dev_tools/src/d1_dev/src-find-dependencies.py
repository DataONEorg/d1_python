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
"""Find all pip packages that are imported by a set of scripts

Common forms of regular import and "from ... import" are supported but there
might be more obscure forms that are not.

Only packages managed by pip are included.

It's possible for a pip package to be included by mistake if there's a local
modules with matching package name which was imported with relative name.

The scripts can be directly specified and/or discovered through filtered
recursive searches.
"""

import argparse
import importlib
import logging
import sys

import pip

import d1_dev.util

import d1_common.iter.file as file_iterator
import d1_common.util


def main():
  parser = argparse.ArgumentParser(
    description='Find all pip packages that are imported by a set of scripts'
  )
  parser.add_argument('path', nargs='+', help='File or directory path')
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

  pkg_name_list = find_pkg_names(args)

  with d1_common.util.print_logging():
    logging.info('Dependent on packages:')
    for pkg_name_str in pkg_name_list:
      logging.info('  {}'.format(pkg_name_str))


def find_pkg_names(args):
  dep_set = set()
  for module_path in file_iterator.dir_iter(
      path_list=args.path,
      include_glob_list=['*.py'],
      exclude_glob_list=args.exclude,
      recursive=args.recursive,
      ignore_invalid=args.ignore_invalid,
      default_excludes=args.default_excludes,
  ):
    dep_set.update(find_deps_in_source(module_path))
  return sorted(get_external_deps(dep_set))


def find_deps_in_source(module_path):
  logging.info(
    'Searching module for dependencies... path="{}"'.format(module_path)
  )
  try:
    dep_list = find_deps_in_tree(
      d1_dev.util.redbaron_module_path_to_tree(module_path)
    )
    logging.debug('Deps: {}'.format(', '.join(dep_list)))
    return dep_list
  except Exception as e:
    logging.error(
      'Dependency search failed for module. error="{}" path="{}"'.
      format(str(e), module_path)
    )
    return []


def find_deps_in_tree(r):
  # logging.debug(r.help(True))
  regular_import_list = [
    v for n in r('ImportNode') for v in get_import_node_dotted_name_list(n)
  ]
  from_import_list = []
  for from_n in r('FromImportNode'):
    from_import_list.append('.'.join(v.value for v in from_n.value))
  return regular_import_list + from_import_list


def get_import_node_dotted_name_list(import_node):
  # Is there a simpler way?
  return [
    '.'.join([n.value for n in dotted_node.value])
    for dotted_node in import_node
  ]


def get_pkg_name_set(dep_set):
  dep_pkg_set = {v.split('.')[0] for v in dep_set}
  pip_pkg_set = {
    v.key.split('==')[0].strip() for v in pip.get_installed_distributions()
  }
  return dep_pkg_set & pip_pkg_set


def get_external_deps(dep_set):
  return {n.split('.')[0] for n in dep_set if is_external_library(n)}


def is_external_library(module_name):
  try:
    mod = importlib.import_module(module_name)
  except Exception:
    logging.error('Unable to import: {}'.format(module_name))
    return True
  try:
    return '/dist-packages/' in mod.__file__
  except AttributeError:
    return False


class DepSearchException(Exception):
  pass


if __name__ == '__main__':
  sys.exit(main())
