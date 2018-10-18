#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
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
"""Run setup.py for each of the D1 Python packages

Note: Can't use any other D1 packages here. They may not be installed yet.
"""

import argparse
import logging
import os
import subprocess
import sys

try:
  import d1_dev.util
except ImportError:
  is_d1_dev_installed = False
  logging.info('d1_dev not yet installed')
else:
  is_d1_dev_installed = True

PKG_PATH_LIST = [
  'dev_tools',
  'lib_common',
  'lib_scimeta',
  'lib_client',
  'client_cli',
  'client_onedrive',
  'gmn',
  'test_utilities',
]


def main():
  if sys.version_info[0] != 3:
    raise Exception(
      'Python 3 required. Current version: {}'.format(sys.version)
    )

  logging.basicConfig(level=logging.DEBUG)

  parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
  )
  parser.add_argument(
    'command', nargs='+', help='Setup command (e.g., build sdist bdist_wheel)'
  )
  parser.add_argument(
    '--root', help='Repository root. for bootstrap install in Travis CI'
  )
  args = parser.parse_args()

  if args.root:
    repo_root_path = args.root
  else:
    assert is_d1_dev_installed, 'd1_dev not installed. Must use --root'
    repo_root_path = d1_dev.util.find_repo_root()

  for pkg_path in PKG_PATH_LIST:
    setup_dir_path = os.path.join(repo_root_path, pkg_path, 'src')
    run_setup(setup_dir_path, args.command)


def run_setup(setup_dir_path, command_list):
  try:
    subprocess.check_call(['python3', 'setup.py'] + command_list,
                          cwd=setup_dir_path)
  except subprocess.CalledProcessError as e:
    logging.error('Setup failed. error="{}"'.format(str(e)))
    raise


if __name__ == '__main__':
  sys.exit(main())
