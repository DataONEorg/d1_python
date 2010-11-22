#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
:mod:`config_util.py`
=====================

.. moduleauthor:: Roger Dahl
'''

# StdLib.
import os
import sys
import re
import subprocess


def run(cmd):
  print 'run: {0}'.format(cmd)
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = p.communicate()
  ret = p.returncode

  if ret != 0:
    print 'ret: {0}'.format(ret)
    print 'stdout: {0}'.format(stdout)
    print 'stderr: {0}'.format(stderr)

  return stdout


def get_svn_info():
  info = run(['svn', 'info'])
  info_map = {}
  for line in info.split('\n'):
    line_split = line.split(':', 2)
    if len(line_split) != 2:
      continue
    info_map[line_split[0].strip()] = line_split[1].strip()
  return info_map


def set_node_val(key, val):
  cur = os.getcwd()
  run(['./manage.py', 'set_node_val', key, val])
  os.chdir(cur)
