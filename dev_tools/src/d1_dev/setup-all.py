#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run setup.py for each of the D1 Python packages
"""
from __future__ import absolute_import
from __future__ import print_function

import argparse
import logging
import os
import subprocess

import d1_dev.util

import d1_common
import d1_common.util

PKG_PATH_LIST = [
  'lib_common',
  'lib_client',
  'client_cli',
  'client_onedrive',
  'gmn',
  'test_utilities',
]


def main():
  d1_common.util.log_setup()

  parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
  )
  parser.add_argument(
    'command', nargs='+', help='setup command (e.g., build sdist bdist_wheel)'
  )
  args = parser.parse_args()

  repo_root_path = d1_dev.util.find_repo_root()

  for pkg_path in PKG_PATH_LIST:
    setup_dir_path = os.path.join(repo_root_path, pkg_path, 'src')
    run_setup(setup_dir_path, args.command)


def run_setup(setup_dir_path, command_list):
  try:
    subprocess.check_call(
      ['python', 'setup.py'] + command_list,
      cwd=setup_dir_path,
    )
  except subprocess.CalledProcessError as e:
    logging.error('Setup failed. error="{}"'.format(str(e)))
    raise


if __name__ == '__main__':
  main()
