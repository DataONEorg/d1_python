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
from __future__ import print_function

import logging
import os
import subprocess
import tempfile

import psycopg2
import psycopg2.extensions
import pytest

import d1_gmn.app.sciobj_store

import d1_test.instance_generator.random_data
import d1_test.sample

from d1_client.cnclient_1_2 import CoordinatingNodeClient_1_2 as cn_v1
from d1_client.cnclient_2_0 import CoordinatingNodeClient_2_0 as cn_v2
from d1_client.mnclient_1_2 import MemberNodeClient_1_2 as mn_v1
from d1_client.mnclient_2_0 import MemberNodeClient_2_0 as mn_v2

import django.conf
import django.core.management
import django.db
import django.db.utils

DEFAULT_DEBUG_PYCHARM_BIN_PATH = os.path.expanduser('~/bin/JetBrains/pycharm')
D1_SKIP_LIST = 'skip_passed/list'
D1_SKIP_COUNT = 'skip_passed/count'

# Allow redefinition of functions. Pytest allows multiple hooks with the same
# name.
# flake8: noqa: F811


def pytest_addoption(parser):
  """Add command line switches for pytest customization. See README.md for
  info.
  """
  # Sample files

  parser.addoption(
    '--sample-ask', action='store_true',
    help='Prompt to update or write new test sample files on failures'
  )
  parser.addoption(
    '--sample-write', action='store_true',
    help='Automatically update or write sample files on failures'
  )
  parser.addoption(
    '--sample-review', action='store_true',
    help='Review samples (use after --sample-write)'
  )
  parser.addoption(
    '--sample-tidy', action='store_true',
    help='Move unused sample files to test_docs_tidy'
  )

  # PyCharm

  parser.addoption(
    '--pycharm', action='store_true',
    help='Attempt to move the cursor in PyCharm to location of most recent test '
    'failure'
  )

  # GMN database fixture

  parser.addoption(
    '--fixture-refresh', action='store_true',
    help='Force reloading the template fixture'
  )
  parser.addoption(
    '--fixture-regen', action='store_true',
    help='Force regenerating the template fixture JSON files'
  )

  # Skip passed tests

  parser.addoption(
    '--skip', action='store_true',
    help='Skip tests that are in the list of passed tests'
  )
  parser.addoption(
    '--skip-clear', action='store_true', help='Clear the list of passed tests'
  )
  parser.addoption(
    '--skip-print', action='store_true', help='Print the list of passed tests'
  )


# Hooks


def pytest_sessionstart(session):
  """Called by pytest before calling session.main()"""
  if pytest.config.getoption('--sample-tidy'):
    d1_test.sample.start_tidy()
    pytest.exit('Tidy started. Run complete to complete')
  if pytest.config.getoption('--skip-clear'):
    _clear_skip_list()
  if pytest.config.getoption('--skip-print'):
    _print_skip_list()


def pytest_sessionfinish(session, exitstatus):
  """Called by pytest after the test session ends"""
  # if exitstatus != 2:
  if pytest.config.getoption('--skip'):
    skipped_count = pytest.config.cache.get(D1_SKIP_COUNT, 0)
    if skipped_count:
      logging.warn('Skipped {} previously passed tests'.format(skipped_count))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
  """Called by pytest after setup, after call and after teardown of each test"""
  outcome = yield
  rep = outcome.get_result()
  # Ignore setup and teardown
  if rep.when != 'call':
    return
  if rep.passed or rep.skipped:
    passed_set = set(pytest.config.cache.get(D1_SKIP_LIST, []))
    passed_set.add(item.nodeid)
    pytest.config.cache.set(D1_SKIP_LIST, list(passed_set))
  elif rep.failed:
    if pytest.config.getoption('--pycharm'):
      _open_error_in_pycharm(call)


def pytest_collection_modifyitems(session, config, items):
  """Called by pytest after collecting tests. The collected tests and the order
  in which they will be called are in {items}, which can be manipulated in place.
  """
  if not pytest.config.getoption('--skip'):
    return

  passed_set = set(pytest.config.cache.get(D1_SKIP_LIST, []))
  new_item_list = []
  for item in items:
    if item.nodeid not in passed_set:
      new_item_list.append(item)

  prev_skip_count = pytest.config.cache.get(D1_SKIP_COUNT, 0)
  cur_skip_count = len(items) - len(new_item_list)

  if prev_skip_count == cur_skip_count:
    logging.info(
      'No tests were run (--skip). Restarting with complete test set'
    )
    _clear_skip_list()
  else:
    pytest.config.cache.set(D1_SKIP_COUNT, cur_skip_count)
    logging.info(
      'Skipping {} previously passed tests (--skip)'.format(cur_skip_count)
    )
    items[:] = new_item_list


def _clear_skip_list():
  pytest.config.cache.set(D1_SKIP_LIST, [])
  pytest.config.cache.set(D1_SKIP_COUNT, 0)


def _print_skip_list():
  map(logging.info, sorted(pytest.config.cache.get(D1_SKIP_LIST, [])))


def _open_error_in_pycharm(call):
  """Attempt to open error locations in PyCharm. Use with -x / --exitfirst"""
  # src_path, src_line, func_name = rep.location
  src_path = call.excinfo.traceback[-1].path
  src_line = call.excinfo.traceback[-1].lineno + 1
  logging.info('src_path="{}", src_line={}'.format(src_path, src_line))
  if src_path == '<string>':
    logging.debug('Unable to find location of error')
    return
  try:
    subprocess.call(
      [DEFAULT_DEBUG_PYCHARM_BIN_PATH, '--line', str(src_line), str(src_path)]
    )
  except subprocess.CalledProcessError as e:
    logging.warn(
      'Unable to open in PyCharm. error="{}" src_path="{}", src_line={}'.
      format(str(e), src_path, src_line)
    )
  else:
    logging.debug(
      'Opened in PyCharm. src_path="{}", src_line={}'.
      format(src_path, src_line)
    )


# Fixtures


def pytest_generate_tests(metafunc):
  """Parameterize test functions via parameterize_dict class member"""
  try:
    func_arg_list = metafunc.cls.parameterize_dict[metafunc.function.__name__]
  except (AttributeError, KeyError):
    return
  arg_names = sorted(func_arg_list[0])
  metafunc.parametrize(
    arg_names,
    [[func_args[name] for name in arg_names] for func_args in func_arg_list]
  )


@pytest.fixture(autouse=True)
# @pytest.mark.django_db(transaction=True)
def enable_db_access(db):
  pass


# Fixtures for parameterizing tests over CN/MN and v1/v2 clients.

MOCK_BASE_URL = 'http://mock/node'


@pytest.fixture(scope='function', params=[True, False])
def true_false(request):
  yield request.param


@pytest.fixture(scope='function', params=['v1', 'v2'])
def tag_v1_v2(request):
  yield request.param


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


# Settings


@pytest.fixture(scope='session', autouse=True)
def set_unique_sciobj_store_path(request):
  tmp_store_path = os.path.join(
    tempfile.gettempdir(), 'gmn_test_obj_store_{}{}'.format(
      d1_test.instance_generator.random_data.random_lower_ascii(
        min_len=12, max_len=12
      ), get_xdist_suffix(request)
    )
  )
  django.conf.settings.OBJECT_STORE_PATH = tmp_store_path
  d1_gmn.app.sciobj_store.create_clean_tmp_store()


# DB fixtures


@pytest.yield_fixture(scope='session')
def django_db_setup(request, django_db_blocker):
  """Set up DB fixture
  """
  logging.info('Setting up DB fixture')

  test_db_key = 'default'
  test_db_name = django.conf.settings.DATABASES[test_db_key]['NAME']
  test_db_name += get_xdist_suffix(request)
  django.conf.settings.DATABASES[test_db_key]['NAME'] = test_db_name

  template_db_key = 'template'
  template_db_name = django.conf.settings.DATABASES[template_db_key]['NAME']

  with django_db_blocker.unblock():
    if pytest.config.getoption('--fixture-regen'):
      drop_database(test_db_name)
      create_blank_db(test_db_key, test_db_name)
      django.db.connections[test_db_key].commit()
      pytest.exit('Database dropped and reinitialized. Now run mk_db_fixture')

    try:
      load_template_fixture(template_db_key, template_db_name)
    except psycopg2.DatabaseError as e:
      logging.error(str(e))
    drop_database(test_db_name)
    create_db_from_template(test_db_name, template_db_name)
    # Haven't found out how to prevent transactions from being started, so
    # closing the implicit transaction here so that template fixture remains
    # available.
    django.db.connections[test_db_key].commit()
    migrate_db(test_db_key)
    logging.debug('Test DB ready')
    yield


def get_xdist_suffix(request):
  """When running in parallel with xdist, each thread gets a different suffix.
  - In parallel run, return '_gw1', etc.
  - In single run, return ''.
  """
  s = getattr(request.config, 'slaveinput', {}).get('slaveid')
  return '_{}'.format(s) if s is not None else ''


def create_db_from_template(test_db_name, template_db_name):
  logging.info(
    'Creating test DB from template. test_db="{}" template_db="{}"'.
    format(test_db_name, template_db_name)
  )
  run_sql(
    'postgres',
    'create database {} template {};'.format(test_db_name, template_db_name)
  )


def load_template_fixture(template_db_key, template_db_name):
  """Load DB fixture from compressed JSON file to template database"""
  logging.info('Loading template DB fixture')
  fixture_file_path = d1_test.sample.get_path('db_fixture.json.bz2')
  if pytest.config.getoption('--fixture-refresh'):
    # django.core.management.call_command('flush', database=template_db_key)
    drop_database(template_db_name)
  create_blank_db(template_db_key, template_db_name)
  logging.debug('Populating tables with fixture data')
  django.core.management.call_command(
    'loaddata', fixture_file_path, database=template_db_key, commit=True
  )
  django.db.connections[template_db_key].commit()
  for connection in django.db.connections.all():
    connection.close()


def migrate_db(test_db_key):
  django.core.management.call_command(
    'migrate', database=test_db_key, commit=True
  )
  django.db.connections[test_db_key].commit()
  for connection in django.db.connections.all():
    connection.close()


def drop_database(db_name):
  logging.debug('Dropping database: {}'.format(db_name))
  run_sql('postgres', 'drop database if exists {};'.format(db_name))


def create_blank_db(db_key, db_name):
  logging.debug('Creating blank DB: {}'.format(db_name))
  run_sql('postgres', "create database {} encoding 'utf-8';".format(db_name))
  logging.debug('Creating GMN tables')
  django.core.management.call_command(
    'migrate', '--run-syncdb', database=db_key
  )


def run_sql(db, sql):
  try:
    conn = psycopg2.connect(database=db)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
  except psycopg2.DatabaseError as e:
    logging.debug('SQL query result="{}"'.format(str(e)))
    raise
  try:
    return cur.fetchall()
  except psycopg2.DatabaseError:
    return None
  finally:
    conn.close()
    for connection in django.db.connections.all():
      connection.close()
