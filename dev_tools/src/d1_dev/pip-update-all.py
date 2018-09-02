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

# 3rd party source
"""Upgrade all pip managed packages to latest PyPI release
- https://github.com/nschloe/pipdated
- http://stackoverflow.com/a/3452888/353337
"""

import logging
import subprocess
import sys

NO_UPGRADE_LIST = [
  # 'Django', # We're on the last version that supports Python 2.
  # 'pygobject', # build error
  # 'zope.interface', # build error
  'urllib3', # requests 2.18.4 has requirement urllib3<1.23,>=1.21.1
]


def main():
  freeze_str = run_pip('freeze')

  for line_str in freeze_str.splitlines():
    print('#### {}'.format(line_str))
    try:
      pkg_str, ver_str = line_str.strip().split('==')
    except ValueError:
      print('Skipped')
      continue
    if pkg_str in NO_UPGRADE_LIST:
      logging.warning(
        'Skipped package in NO_UPGRADE_LIST. pkg_str="{}"'.format(pkg_str)
      )
      continue
    print(run_pip('install', '--upgrade', pkg_str))

  print(run_pip('check'))


def run_pip(*pip_arg_list):
  print('pip {}'.format(' '.join(pip_arg_list)))
  try:
    return subprocess.check_output(['pip'] + list(pip_arg_list)).decode('utf-8')
  except subprocess.CalledProcessError as e:
    logging.error('Setup failed. error="{}"'.format(str(e)))
    raise


if __name__ == '__main__':
  sys.exit(main())
