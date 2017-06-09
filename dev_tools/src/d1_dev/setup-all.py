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

PKG_PATH_LIST = [
  'lib_common',
  'lib_client',
  'client_cli',
  'client_onedrive',
  'gmn',
  'test_utilities',
]


def main():
  logging.basicConfig()
  logging.getLogger('').setLevel(logging.DEBUG)

  parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
  )
  parser.add_argument(
    'root', action='store', default=None,
    help='path to the repository root (d1_python)'
  )
  parser.add_argument(
    'command', action='store', default=None,
    help='setup command (e.g., build, install, develop)'
  )
  args = parser.parse_args()

  for pkg_path in PKG_PATH_LIST:
    setup_dir_path = os.path.join(args.root, pkg_path, 'src')
    run_setup(setup_dir_path, args.command)


def run_setup(setup_dir_path, command_str):
  try:
    subprocess.check_call(
      ['python', 'setup.py', command_str],
      cwd=setup_dir_path,
    )
  except subprocess.CalledProcessError as e:
    logging.error('Setup failed. error="{}"'.format(str(e)))


if __name__ == '__main__':
  main()
