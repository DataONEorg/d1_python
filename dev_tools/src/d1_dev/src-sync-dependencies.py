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
"""Synchronize the install_requires sections in all setup.py files with the
currently installed versions of all packages.

The two required params are the root to the DataONE Python software stack
and the new version number to use in the next release of the stack. We keep
the version numbers for all the packages in the d1_python repository in sync.
"""

import argparse
import logging
import os
import pkgutil
import re
import sys

import pkg_resources

import d1_dev.util

import d1_common.iter.dir
import d1_common.util


def main():
  parser = argparse.ArgumentParser(
    description='Sync the install_requires sections in setup.py files'
  )
  parser.add_argument('path', help='Root of Python source tree')
  parser.add_argument(
    'd1_version', help='Version to use for new D1 Py stack release'
  )
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
  parser.add_argument(
    '--diff', dest='show_diff', action='store_true',
    help='Show diff and do not modify any files'
  )
  parser.add_argument(
    '--dry-run', action='store_true',
    help='Perform a trial run without changing any files'
  )

  args = parser.parse_args()

  d1_common.util.log_setup(args.debug)

  for setup_path in d1_common.iter.dir.dir_iter(
      path_list=[args.path],
      include_glob_list=['setup.py'],
      exclude_glob_list=args.exclude,
      recursive=args.recursive,
      ignore_invalid=args.ignore_invalid,
      default_excludes=args.default_excludes,
  ):
    try:
      update_deps_on_file(args, setup_path, args.show_diff, args.d1_version)
    except Exception as e:
      logging.error(str(e))

  update_version_const(
    'd1_common', ['const.py'], args.d1_version, args.show_diff, args.dry_run
  )
  update_version_const(
    'd1_gmn', ['version.py'], args.d1_version, args.show_diff, args.dry_run
  )


def update_deps_on_file(args, setup_path, show_diff, d1_version):
  logging.info('Updating setup.py... path="{}"'.format(setup_path))
  try:
    r = d1_dev.util.redbaron_module_path_to_tree(setup_path)
    r = update_deps_on_tree(r, d1_version)
  except Exception as e:
    logging.error(
      'Update failed. error="{}" path="{}"'.format(str(e), setup_path)
    )
    if args.debug:
      raise
  else:
    d1_dev.util.update_module_file(
      r, setup_path, show_diff, dry_run=args.dry_run
    )


def update_deps_on_tree(r, d1_version):
  r = update_install_requires(r, d1_version)
  r = update_version(r, d1_version)
  return r


def update_install_requires(r, d1_version):
  dep_node = find_call_argument_node(r, 'install_requires')
  for str_node in dep_node.value:
    # logging.debug(str_node.help(True))
    update_dep_str(str_node, d1_version)
  return r


def update_version(r, d1_version):
  n = find_call_argument_node(r, 'version')
  n.value = '\'{}\''.format(d1_version)
  return r


def find_call_argument_node(r, value_str):
  node_list = r('CallArgumentNode')
  for n in node_list:
    if hasattr(n.target, 'value') and n.target.value == value_str:
      return n
  raise UpdateException(
    'CallArgumentNode not found. value="{}"'.format(value_str)
  )


def update_dep_str(str_node, d1_version):
  try:
    package_name, old_version_str = parse_dep_str(str_node.value)
  except UpdateException as e:
    logging.debug(
      'Dependency not updated. dep="{}" cause="{}"'.
      format(str_node.value, str(e))
    )
  else:
    new_version_str = get_package_version(package_name, d1_version)
    if old_version_str != new_version_str:
      str_node.value = '\'{} >= {}\''.format(package_name, new_version_str)
      logging.debug(
        'Dependency updated. package="{}" old="{}" new="{}"'.
        format(package_name, old_version_str, new_version_str)
      )
    else:
      logging.debug(
        'Dependency update not required. package="{}" version="{}"'.
        format(package_name, old_version_str)
      )


def parse_dep_str(dep_str):
  m = re.match(r'(.*)\s*>=\s*(.*)', dep_str)
  if not m:
    raise UpdateException('Dependency not set to ">="')
  return m.group(1).strip('\'" '), m.group(2).strip('\'" ')


def get_package_version(package_name, d1_version):
  if package_name.startswith('dataone.'):
    return d1_version
  else:
    return pkg_resources.get_distribution(package_name).version


def update_version_const(base_name, path_list, d1_version, only_diff, dry_run):
  module_path = get_module_path(base_name, path_list)
  logging.debug('Updating version in module. path="{}"'.format(module_path))
  r = d1_dev.util.redbaron_module_path_to_tree(module_path)
  for n in r('AssignmentNode'):
    if n.target.value in ('VERSION', '__version__'):
      n.value.value = "'{}'".format(d1_version)
      d1_dev.util.update_module_file(r, module_path, only_diff, dry_run)
      break


def get_module_path(base_str, path_list):
  return os.path.join(
    os.path.split(pkgutil.get_loader(base_str).path)[0], *path_list
  )


class UpdateException(Exception):
  pass


if __name__ == '__main__':
  sys.exit(main())
