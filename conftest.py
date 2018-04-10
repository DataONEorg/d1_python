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

import datetime
import logging
import multiprocessing
import os
import shutil
import subprocess
import sys
import tempfile

import mock
import posix_ipc
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

DEFAULT_DEBUG_PYCHARM_BIN_PATH = os.path.expanduser(
  '~/bin/JetBrains/pycharm.sh'
)
D1_SKIP_LIST = 'skip_passed/list'
D1_SKIP_COUNT = 'skip_passed/count'

TEMPLATE_DB_KEY = 'template'
TEST_DB_KEY = 'default'

# Allow redefinition of functions. Pytest allows multiple hooks with the same
# name.
# flake8: noqa: F811

# template_db_lock = threading.Lock()
template_db_lock = multiprocessing.Lock()

# Hack to get access to print and logging output when running under pytest-xdist
# and pytest-catchlog. Without this, only output from failed tests is displayed.
sys.stdout = sys.stderr


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
    '--sample-update', action='store_true',
    help='Automatically update or write sample files on failures'
  )
  parser.addoption(
    '--sample-review', action='store_true',
    help='Review samples (use after --sample-update)'
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


# def pytest_configure(config):
#   """Allows plugins and conftest files to perform initial configuration.
#   This hook is called for every plugin and initial conftest file after command
#   line options have been parsed.
#   After that, the hook is called for other conftest files as they are imported.
#   """
#   logging.debug('pytest_configure()')
#   tmp_store_path = os.path.join(
#     tempfile.gettempdir(), 'gmn_test_obj_store_{}'.format(
#       d1_test.instance_generator.random_data.
#       random_lower_ascii(min_len=12, max_len=12)
#     )
#   )
#   logging.debug('Setting OBJECT_STORE_PATH = {}'.format(tmp_store_path))
#   django.conf.settings.OBJECT_STORE_PATH = tmp_store_path
#   d1_gmn.app.sciobj_store.create_clean_tmp_store()
#   mock.patch('d1_gmn.app.startup._create_sciobj_store_root')

# Hooks


def pytest_sessionstart(session):
  """Called by pytest before calling session.main()
  When running in parallel with xdist, this is called once for each worker.
  By default, the number of workers is the same as the number of CPU cores.
  """
  if pytest.config.getoption('--sample-tidy'):
    d1_test.sample.start_tidy()
    pytest.exit('Sample tidy started')

  if pytest.config.getoption('--fixture-refresh'):
    db_drop(TEMPLATE_DB_KEY)
    pytest.exit('Template refresh started')

  if pytest.config.getoption('--skip-clear'):
    _clear_skip_list()
    pytest.exit('Cleared list of passed tests')

  if pytest.config.getoption('--skip-print'):
    _print_skip_list()
    pytest.exit('Printed list of passed tests')


def pytest_sessionfinish(session, exitstatus):
  """Called by pytest after the test session ends"""
  # if exitstatus != 2:
  if pytest.config.getoption('--skip'):
    skipped_count = pytest.config.cache.get(D1_SKIP_COUNT, 0)
    if skipped_count:
      logging.warning(
        'Skipped {} previously passed tests'.format(skipped_count)
      )


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


# TODO: Implement side by side diff display for string compare failures
# def pytest_assertrepr_compare(config, op, left, right):
#   """Called by pytest on failed assert
#   - Return custom assert error message as a list of strings
#   - Return None to use pytest's default error message
#   """
#   if isinstance(left, str) and isinstance(right, str) and op == "==":
#     # print('{0}\n{1}\n{0}\n{2}\n{0}\n'.format('~'*80, left, right))
#     msg = d1_test.sample._get_sxs_diff_str(left, right)#.encode('utf-8')
#     # print(msg)
#     return msg.splitlines()


def _clear_skip_list():
  pytest.config.cache.set(D1_SKIP_LIST, [])
  pytest.config.cache.set(D1_SKIP_COUNT, 0)


def _print_skip_list():
  list(map(logging.info, sorted(pytest.config.cache.get(D1_SKIP_LIST, []))))


def _open_error_in_pycharm(call):
  """Attempt to open error locations in PyCharm. Use with --exitfirst (-x)"""
  # src_path, src_line, func_name = rep.location
  src_path = call.excinfo.traceback[-1].path
  src_line = call.excinfo.traceback[-1].lineno + 1
  logging.info('src_path="{}", src_line={}'.format(src_path, src_line))
  if src_path == '<string>':
    logging.debug('Unable to find location of error')
    return
  try:
    assert os.path.isfile(DEFAULT_DEBUG_PYCHARM_BIN_PATH), \
      'Path to PyCharm is incorrect'
    subprocess.call(
      [DEFAULT_DEBUG_PYCHARM_BIN_PATH, '--line', str(src_line), str(src_path)]
    )
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

# @pytest.fixture(scope='session', autouse=True)
# def set_unique_sciobj_store_path(request):
#   tmp_store_path = os.path.join(
#     tempfile.gettempdir(),
#     'gmn_test_obj_store_{}'.format(get_xdist_unique_suffix(request))
#   )
#   logging.debug('Setting OBJECT_STORE_PATH = {}'.format(tmp_store_path))
#   django.conf.settings.OBJECT_STORE_PATH = tmp_store_path
#   d1_gmn.app.sciobj_store.create_clean_tmp_store()


@pytest.yield_fixture(scope='session', autouse=True)
def django_sciobj_store_setup(request):
  tmp_store_path = os.path.join(
    tempfile.gettempdir(),
    'gmn_test_obj_store_{}'.format(get_xdist_unique_suffix(request))
  )
  mock.patch('d1_gmn.app.startup._create_sciobj_store_root')
  django.conf.settings.OBJECT_STORE_PATH = tmp_store_path
  logging.debug(
    'Creating sciobj store. tmp_store_path="{}"'.format(tmp_store_path)
  )
  d1_gmn.app.sciobj_store.create_clean_tmp_store()

  yield

  logging.debug(
    'Deleting sciobj store. tmp_store_path="{}"'.format(tmp_store_path)
  )
  shutil.rmtree(tmp_store_path)


# Database setup


@pytest.yield_fixture(scope='session')
def django_db_setup(request, django_db_blocker):
  """Set up DB fixture
  When running in parallel with xdist, this is called once for each worker.
  """
  logging.info('Setting up DB fixture')

  db_set_unique_db_name(request)

  with django_db_blocker.unblock():

    # if pytest.config.getoption('--fixture-regen'):
    #   db_drop(test_db_name)
    #   db_create_blank(test_db_key, test_db_name)
    #   django.db.connections[test_db_key].commit()
    #   pytest.exit('Database dropped and reinitialized. Now run mk_db_fixture')

    # Regular multiprocessing.Lock() context manager did not work here. Also
    # tried creating the lock at module scope, and also directly calling
    # acquire() and release(). It's probably related to how the worker processes
    # relate to each other when launched by pytest-xdist as compared to what the
    # multiprocessing module expects.
    with posix_ipc.Semaphore(
        '/{}'.format(__name__), flags=posix_ipc.O_CREAT, initial_value=1
    ):
      logging.warning(
        'LOCK BEGIN {} {}'.
        format(db_get_name_by_key(TEMPLATE_DB_KEY), datetime.datetime.now())
      )

      if not db_exists(TEMPLATE_DB_KEY):
        db_create_blank(TEMPLATE_DB_KEY)
        db_migrate(TEMPLATE_DB_KEY)
        db_populate_by_json(TEMPLATE_DB_KEY)
        db_migrate(TEMPLATE_DB_KEY)

      logging.warning(
        'LOCK END {} {}'.
        format(db_get_name_by_key(TEMPLATE_DB_KEY), datetime.datetime.now())
      )

    db_drop(TEST_DB_KEY)
    db_create_from_template()
    # db_migrate(TEST_DB_KEY)

    # # Haven't found out how to prevent transactions from being started, so
    # # closing the implicit transaction here so that template fixture remains
    # # available.
    # django.db.connections[test_db_key].commit()

    yield

    db_drop(TEST_DB_KEY)


def db_get_name_by_key(db_key):
  logging.debug('db_get_name_by_key() {}'.format(db_key))
  return django.conf.settings.DATABASES[db_key]['NAME']


def db_set_unique_db_name(request):
  logging.debug('db_set_unique_db_name()')
  db_name = '_'.join([
    db_get_name_by_key(TEST_DB_KEY),
    get_xdist_unique_suffix(request),
  ])
  django.conf.settings.DATABASES[TEST_DB_KEY]['NAME'] = db_name


def db_create_from_template():
  logging.debug('db_create_from_template()')
  new_db_name = db_get_name_by_key(TEST_DB_KEY)
  template_db_name = db_get_name_by_key(TEMPLATE_DB_KEY)
  logging.info(
    'Creating new db from template. new_db="{}" template_db="{}"'.
    format(new_db_name, template_db_name)
  )
  run_sql(
    'postgres',
    'create database {} template {};'.format(new_db_name, template_db_name)
  )


def db_populate_by_json(db_key):
  """Load DB fixture from compressed JSON file to template database"""
  logging.debug('db_populate_by_json() {}'.format(db_key))
  fixture_file_path = d1_test.sample.get_path('db_fixture.json.bz2')
  # loaddata used to have a 'commit' arg, but it appears to have been removed.
  django.core.management.call_command(
    'loaddata', fixture_file_path, database=db_key, commit=True
  )
  db_commit_and_close(db_key)


def db_migrate(db_key):
  logging.debug('db_migrate() {}'.format(db_key))
  django.core.management.call_command(
    'migrate', '--run-syncdb', database=db_key
  )
  db_commit_and_close(db_key)


def db_drop(db_key):
  logging.debug('db_drop() {}'.format(db_key))
  db_name = db_get_name_by_key(db_key)
  logging.debug('Dropping database: {}'.format(db_name))
  db_commit_and_close(db_key)
  run_sql('postgres', 'drop database if exists {};'.format(db_name))


def db_commit_and_close(db_key):
  logging.debug('db_commit_and_close() {}'.format(db_key))
  django.db.connections[db_key].commit()
  for connection in django.db.connections.all():
    connection.close()


def db_create_blank(db_key):
  logging.debug('db_create_blank() {}'.format(db_key))
  db_name = db_get_name_by_key(db_key)
  logging.debug('Creating blank database: {}'.format(db_name))
  run_sql('postgres', "create database {} encoding 'utf-8';".format(db_name))


def db_exists(db_key):
  logging.debug('db_exists() {}'.format(db_key))
  db_name = db_get_name_by_key(db_key)
  exists_bool = bool(
    run_sql(
      'postgres',
      "select 1 from pg_database WHERE datname='{}'".format(db_name)
    )
  )
  logging.debug('db_exists(): {}'.format(exists_bool))
  return exists_bool


def run_sql(db, sql):
  try:
    conn = psycopg2.connect(database=db)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
  except psycopg2.DatabaseError as e:
    logging.debug('SQL query error: {}'.format(str(e)))
    raise
  try:
    return cur.fetchall()
  except psycopg2.DatabaseError:
    return None
  finally:
    conn.close()
    for connection in django.db.connections.all():
      connection.close()


def get_xdist_unique_suffix(request):
  return '_'.join([get_random_ascii_string(), get_xdist_suffix(request)])


def get_random_ascii_string():
  return d1_test.instance_generator.random_data.random_lower_ascii(
    min_len=12, max_len=12
  )


def get_xdist_suffix(request):
  """Return a different string for each worker when running in parallel under
  pytest-xdist, else return an empty string. Returned strings are on the form,
  "gwN"."""
  s = getattr(request.config, 'slaveinput', {}).get('slaveid')
  return s if s is not None else ''
