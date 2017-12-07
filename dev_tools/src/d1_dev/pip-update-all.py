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
https://github.com/nschloe/pipdated
http://stackoverflow.com/a/3452888/353337
"""

from __future__ import absolute_import

import logging
import os
import subprocess
import sys

NO_UPGRADE_LIST = ['Django']


def main():
  try:
    os.utime('/usr/', None)
  except EnvironmentError:
    sys.exit('Must be root')

  freeze_str = subprocess.check_output(['pip', 'freeze'])

  for line_str in freeze_str.splitlines():
    pkg_str, ver_str = line_str.strip().split('==')
    if pkg_str in NO_UPGRADE_LIST:
      logging.warn(
        'Skipped package in NO_UPGRADE_LIST. pkg_str="{}"'.format(pkg_str)
      )
      continue
    print subprocess.check_output(['pip', 'install', '--upgrade', pkg_str])

  print subprocess.check_output(['pip', 'check'])


if __name__ == '__main__':
  main()
