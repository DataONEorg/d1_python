# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import logging
import os
import subprocess

import pytest

from d1_client.cnclient_1_1 import CoordinatingNodeClient_1_1 as cn_v1
from d1_client.cnclient_2_0 import CoordinatingNodeClient_2_0 as cn_v2
from d1_client.mnclient_1_1 import MemberNodeClient_1_1 as mn_v1
from d1_client.mnclient_2_0 import MemberNodeClient_2_0 as mn_v2

DEFAULT_DEBUG_PYCHARM_BIN_PATH = os.path.expanduser('~/bin/JetBrains/pycharm')


def pytest_addoption(parser):
  """Add a command line option to pytest that enables a mode that invokes
  `kdiff3` to display diffs and, after user confirmation, can automatically
  update or write new test sample documents on mismatches.

  The diff should be studied carefully before updating the sample since there is
  a risk of introducing errors.

  The implementation is in D1TestCase.assert_equals_sample()
  """
  parser.addoption(
    '--update-samples', action='store_true', default=False,
    help='Prompt to update or write new test sample files on failures'
  )
  parser.addoption(
    '--pycharm', action='store_true', default=False,
    help='Attempt to move the cursor in PyCharm to location of most recent test '
    'failure'
  )


def pytest_generate_tests(metafunc):
  """Parameterize test functions via parameterize_dict class member"""
  try:
    func_arg_list = metafunc.cls.parameterize_dict[metafunc.function.__name__]
  except (AttributeError, KeyError):
    return
  arg_names = sorted(func_arg_list[0])
  print arg_names
  metafunc.parametrize(
    arg_names,
    [[func_args[name] for name in arg_names] for func_args in func_arg_list]
  )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
  """Attempt to open error locations in PyCharm. Use with -x / --exitfirst"""
  outcome = yield
  if not pytest.config.getoption("--pycharm"):
    return
  rep = outcome.get_result()
  if rep.when == "call" and rep.failed:
    # src_path, src_line, func_name = rep.location
    src_path = call.excinfo.traceback[-1].path
    src_line = call.excinfo.traceback[-1].lineno + 1
    logging.info('src_path="{}", src_line={}'.format(src_path, src_line))
    # return
    if src_path == '<string>':
      logging.debug('Unable to find location of error')
      return
    try:
      subprocess.call([
        DEFAULT_DEBUG_PYCHARM_BIN_PATH, '--line', str(src_line), str(src_path)
      ])
    except subprocess.CalledProcessError as e:
      logging.warning(
        'Unable to open in PyCharm. error="{}" src_path="{}", src_line={}'.
        format(str(e), src_path, src_line)
      )
    else:
      logging.debug(
        'Opened in PyCharm. src_path="{}", src_line={}'.
        format(src_path, src_line)
      )


# Fixtures for parameterizing tests over CN/MN and v1/v2 clients.

MOCK_BASE_URL = 'http://mock/node'

# CN and MN (for baseclient)


@pytest.fixture(scope='function', params=[cn_v1, mn_v1])
def cn_mn_client_v1(request):
  yield request.param(MOCK_BASE_URL)


@pytest.fixture(scope='function', params=[cn_v2, mn_v2])
def cn_mn_client_v2(request):
  yield request.param(MOCK_BASE_URL)


@pytest.fixture(scope='function', params=[cn_v1, mn_v1, cn_v2, mn_v2])
def cn_mn_client_v1_v2(request):
  yield request.param(MOCK_BASE_URL)


# CN clients


@pytest.fixture(scope='function', params=[cn_v1])
def cn_client_v1(request):
  yield request.param(MOCK_BASE_URL)


@pytest.fixture(scope='function', params=[cn_v2])
def cn_client_v2(request):
  yield request.param(MOCK_BASE_URL)


@pytest.fixture(scope='function', params=[cn_v1, cn_v2])
def cn_client_v1_v2(request):
  yield request.param(MOCK_BASE_URL)


# MN clients


@pytest.fixture(scope='function', params=[mn_v1])
def mn_client_v1(request):
  yield request.param(MOCK_BASE_URL)


@pytest.fixture(scope='function', params=[mn_v2])
def mn_client_v2(request):
  yield request.param(MOCK_BASE_URL)


@pytest.fixture(scope='function', params=[mn_v1, mn_v2])
def mn_client_v1_v2(request):
  yield request.param(MOCK_BASE_URL)
