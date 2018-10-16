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

"""
PyCharm support in the test framework
# - This sets up the path to the PyCharm binary. It is required and used only if pytest is started with the --pycharm switch. Otherwise it is ignored.
# - When active, the test framework will:
# - Automatically open files where errors occur and move the cursor to the line of the error
# - Show syntax highlighted diffs for scripts and data files using PyCharm's powerful diff viewer
"""
import logging
import os
import subprocess
import sys
import d1_dev.util

# Set this path to the binary that launches PyCharm. If an environment variable
# of the same name exists, it is used instead of this setting.
PYCHARM_BIN_PATH = os.path.expanduser(
  '~/bin/JetBrains/pycharm.sh'
)


def open_and_set_cursor(src_path, src_line=1):
  """Attempt to open the file at {src_path} in the PyCharm IDE and move the
  cursor to line {src_line}
  - {src_path} can be an absolute path, or a path relative to the root of the
  DataONE Git repository.
  """
  if src_path == '<string>':
    logging.debug('Unable to find location of error')
    return
  # Handle LocalPath from pytest
  src_path = str(src_path)
  src_path = get_abs_path(src_path)
  call_pycharm('--line', src_line, src_path)


def diff(left_path, right_path):
  """Attempt to open a diff of the two files in the PyCharm Diff & Merge tool"""
  call_pycharm('diff', str(left_path), str(right_path))


def get_abs_path(src_path):
  if not os.path.isabs(src_path):
    src_path = os.path.join(
      d1_dev.util.find_repo_root_by_path(__file__),
      src_path
    )
  return src_path


def get_exception_location(exc_traceback=None):
  """Return the abs path and line number of the line of the location where
  exception was triggered
  """
  exc_traceback = exc_traceback or sys.exc_info()[2]
  return exc_traceback[-1].path, exc_traceback[-1].lineno + 1


def get_d1_exception_location(exc_traceback=None):
  """Return the abs path and line number of the line of project code that is
  closest to location where exception was triggered
  - If an exception is triggered within a 3rd party package, this will provide
  the location within the DataONE source code that passed control down to the
  dependencies.
  - If exception was triggered directly in the DataONE source code, gives the
  exact location, like get_exception_location().
  """
  exc_traceback = exc_traceback or sys.exc_info()[2]
  location_tup = ()
  while exc_traceback:
    co = exc_traceback.tb_frame.f_code
    # if co.co_filename.startswith(django.conf.settings.BASE_DIR):
    if 'd1_' in co.co_filename:
      # location_tup = co.co_filename, str(exc_traceback.tb_lineno)
      location_tup = co.path, co.lineno + 1
    exc_traceback = exc_traceback.tb_next
  return location_tup


def call_pycharm(*arg_list):
  pycharm_bin_path = os.environ.get('PYCHARM_BIN_PATH', PYCHARM_BIN_PATH)
  try:
    assert os.path.isfile(pycharm_bin_path), (
      'PyCharm IDE integration has been enabled but the path to the PyCharm '
      'binary is incorrect. Please set the correct path in {}, PYCHARM_BIN_PATH'
      'or set the PYCHARM_BIN_PATH environment variable. If PyCharm is not '
      'available, try starting again without the --pycharm '
      'switch.'.format(__file__)
    )
    subprocess.call([PYCHARM_BIN_PATH] + [str(v) for v in arg_list])
  except subprocess.CalledProcessError as e:
    logging.warning(
      'PyCharm call failed. error="{}" args="{}"'.
        format(str(e), ', '.join(arg_list))
    )
  else:
    logging.debug(
      'PyCharm call. args="{}"'. format(', '.join(arg_list))
    )
