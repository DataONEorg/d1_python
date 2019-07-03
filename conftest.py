# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
"""pytest setup and customization."""
import logging
import os
import sys
import tempfile

import mock
import pytest

import d1_client.cnclient_1_2
import d1_client.cnclient_2_0
import d1_client.mnclient_1_2
import d1_client.mnclient_2_0

import django.db

import d1_gmn.tests.gmn_test_case

import d1_test.d1_test_case
import d1_test.instance_generator.identifier
import d1_test.instance_generator.random_data
import d1_test.sample
import d1_test.test_files

if not "TRAVIS" in os.environ:
    import d1_test.pycharm

logger = logging.getLogger(__name__)

D1_SKIP_LIST = "skip_passed/list"
D1_SKIP_COUNT = "skip_passed/count"

# Allow redefinition of functions. Pytest allows multiple hooks with the same
# name.
# flake8: noqa: F811

# Hack to get access to print and logging output when running under pytest-xdist
# and pytest-catchlog. Without this, only output from failed tests is displayed.
# sys.stdout = sys.stderr


def pytest_addoption(parser):
    """Add command line switches for pytest customization.

    See README.md for info.

    """
    # Sample files

    parser.addoption(
        "--sample-ask",
        action="store_true",
        help="Prompt to update or write new test sample files on failures",
    )
    parser.addoption(
        "--sample-update",
        action="store_true",
        help="Automatically update or write sample files on failures",
    )
    parser.addoption(
        "--sample-review",
        action="store_true",
        help="Review samples (use after --sample-update)",
    )
    parser.addoption(
        "--sample-tidy",
        action="store_true",
        help="Move unused sample files to test_docs_tidy",
    )

    # PyCharm integration

    parser.addoption(
        "--pycharm",
        action="store_true",
        help="Attempt to move the cursor in PyCharm to location of most recent test "
        "failure",
    )

    # Skip passed tests

    parser.addoption(
        "--skip",
        action="store_true",
        help="Skip tests that are in the list of passed tests",
    )
    parser.addoption(
        "--skip-print", action="store_true", help="Print the list of passed tests"
    )


# Hooks


def pytest_configure(config):
    """Allow plugins and conftest files to perform initial configuration This hook is
    called for every plugin and initial conftest file after command line options have
    been parsed.

    After that, the hook is called for other conftest files as they are imported.

    """
    sys.is_running_under_travis = "TRAVIS" in os.environ
    sys.is_running_under_pytest = True

    d1_test.sample.options = {
        "ask": config.getoption("--sample-ask"),
        "review": config.getoption("--sample-review"),
        "update": config.getoption("--sample-update"),
    }


# noinspection PyUnresolvedReferences,PyUnusedLocal
def pytest_unconfigure(config):
    del sys.is_running_under_travis
    del sys.is_running_under_pytest


def pytest_sessionstart(session):
    """Called by pytest before calling session.main()

    - When running in parallel with xdist, this is called once for each worker. By
      default, the number of workers is the same as the number of CPU cores.

    """
    exit_if_switch_used_with_xdist(
        session,
        [
            # User input doesn't work well under xdist
            "--sample-ask",
            "--sample-review",
            "--pycharm",
            # Samples can be updated under xdist
            # '--sample-update',
            # Samples can be tidied under xdist
            # --sample-tidy
            # Recently passed tests cannot be skipped in parallel run since all xdist
            # workers must collect the same number of tests.
            "--skip",
            "--skip-print",
        ],
    )

    if session.config.getoption("--sample-tidy"):
        logger.info("Starting sample tidy")
        d1_test.sample.start_tidy()

    # Running the tests without either --skip-print or --skip always clears the passed
    # list, so that, if --skip is added on the next run, it will continue from the most
    # recent failed test.
    if session.config.getoption("--skip-print"):
        logger.info("Printing list of passed tests")
        _print_skip_list(session)
    elif not session.config.getoption("--skip"):
        logger.info("Clearing list of passed tests")
        _clear_skip_list(session)


# noinspection PyUnusedLocal
def pytest_sessionfinish(session, exitstatus):
    """Called by pytest after the test session ends."""
    # if exitstatus != 2:
    if session.config.getoption("--skip"):
        skipped_count = session.config.cache.get(D1_SKIP_COUNT, 0)
        if skipped_count:
            logger.warning("Skipped {} previously passed tests".format(skipped_count))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Called by pytest after setup, after call and after teardown of each test."""
    outcome = yield
    rep = outcome.get_result()
    # Ignore setup and teardown
    if rep.when != "call":
        return
    if rep.passed or rep.skipped:
        passed_set = set(item.session.config.cache.get(D1_SKIP_LIST, []))
        passed_set.add(item.nodeid)
        item.session.config.cache.set(D1_SKIP_LIST, list(passed_set))
    elif rep.failed:
        if item.session.config.getoption("--pycharm"):
            _open_error_in_pycharm(call)


# noinspection PyUnusedLocal
def pytest_collection_modifyitems(session, config, items):
    """Called by pytest after collecting tests.

    The collected tests and the order in which they will be called are in ``items``,
    which can be manipulated in place.

    """
    if not session.config.getoption("--skip"):
        return

    passed_set = set(session.config.cache.get(D1_SKIP_LIST, []))
    new_item_list = []
    for item in items:
        if item.nodeid not in passed_set:
            new_item_list.append(item)

    prev_skip_count = session.config.cache.get(D1_SKIP_COUNT, 0)
    cur_skip_count = len(items) - len(new_item_list)

    if prev_skip_count == cur_skip_count:
        logger.info("No tests were run (--skip). Restarting with complete test set")
        _clear_skip_list(session)
    else:
        session.config.cache.set(D1_SKIP_COUNT, cur_skip_count)
        logger.info(
            "Skipping {} previously passed tests (--skip)".format(cur_skip_count)
        )
        items[:] = new_item_list


def _clear_skip_list(session):
    session.config.cache.set(D1_SKIP_LIST, [])
    session.config.cache.set(D1_SKIP_COUNT, 0)


def _print_skip_list(session):
    list(map(logger.info, sorted(session.config.cache.get(D1_SKIP_LIST, []))))


def _open_error_in_pycharm(call):
    """Attempt to open error locations in PyCharm.

    Use with --exitfirst (-x)

    """
    logger.error("Test raised exception: {}".format(call.excinfo.exconly()))
    test_path, test_lineno = d1_test.d1_test_case.D1TestCase.get_d1_test_case_location(
        call.excinfo.tb
    )
    logger.error("D1TestCase location: {}:{}".format(test_path, test_lineno))
    exc_frame = call.excinfo.traceback.getcrashentry()
    logger.error(
        "Exception location: {}({})".format(exc_frame.path, exc_frame.lineno + 1)
    )
    d1_test.pycharm.open_and_set_cursor(test_path, test_lineno)


# Fixtures


def pytest_generate_tests(metafunc):
    """Parameterize test functions via parameterize_dict class member."""
    try:
        func_arg_list = metafunc.cls.parameterize_dict[metafunc.function.__name__]
    except (AttributeError, KeyError):
        return
    arg_names = sorted(func_arg_list[0])
    metafunc.parametrize(
        arg_names,
        [[func_args[name] for name in arg_names] for func_args in func_arg_list],
    )


# Fixtures for parameterizing tests over CN/MN and v1/v2 clients.


@pytest.fixture(scope="function", params=[True, False])
def true_false(request):
    yield request.param


@pytest.fixture(scope="function", params=[None, True])
def none_true(request):
    yield request.param


@pytest.fixture(scope="function", params=["v1", "v2"])
def tag_v1_v2(request):
    yield request.param


# CN and MN (for baseclient)


@pytest.fixture(
    scope="function",
    params=[
        d1_client.cnclient_1_2.CoordinatingNodeClient_1_2,
        d1_client.mnclient_1_2.MemberNodeClient_1_2,
    ],
)
def cn_mn_client_v1(request):
    yield request.param(d1_test.d1_test_case.MOCK_CN_MN_BASE_URL)


@pytest.fixture(
    scope="function",
    params=[
        d1_client.cnclient_2_0.CoordinatingNodeClient_2_0,
        d1_client.mnclient_2_0.MemberNodeClient_2_0,
    ],
)
def cn_mn_client_v2(request):
    yield request.param(d1_test.d1_test_case.MOCK_CN_MN_BASE_URL)


@pytest.fixture(
    scope="function",
    params=[
        d1_client.cnclient_1_2.CoordinatingNodeClient_1_2,
        d1_client.mnclient_1_2.MemberNodeClient_1_2,
        d1_client.cnclient_2_0.CoordinatingNodeClient_2_0,
        d1_client.mnclient_2_0.MemberNodeClient_2_0,
    ],
)
def cn_mn_client_v1_v2(request):
    yield request.param(d1_test.d1_test_case.MOCK_CN_MN_BASE_URL)


# CN clients


@pytest.fixture(
    scope="function", params=[d1_client.cnclient_1_2.CoordinatingNodeClient_1_2]
)
def cn_client_v1(request):
    yield request.param(d1_test.d1_test_case.MOCK_CN_BASE_URL)


@pytest.fixture(
    scope="function", params=[d1_client.cnclient_2_0.CoordinatingNodeClient_2_0]
)
def cn_client_v2(request):
    yield request.param(d1_test.d1_test_case.MOCK_CN_BASE_URL)


@pytest.fixture(
    scope="function",
    params=[
        d1_client.cnclient_1_2.CoordinatingNodeClient_1_2,
        d1_client.cnclient_2_0.CoordinatingNodeClient_2_0,
    ],
)
def cn_client_v1_v2(request):
    yield request.param(d1_test.d1_test_case.MOCK_CN_BASE_URL)


# MN clients


@pytest.fixture(scope="function", params=[d1_client.mnclient_1_2.MemberNodeClient_1_2])
def mn_client_v1(request):
    yield request.param(d1_test.d1_test_case.MOCK_MN_BASE_URL)


@pytest.fixture(scope="function", params=[d1_client.mnclient_2_0.MemberNodeClient_2_0])
def mn_client_v2(request):
    yield request.param(d1_test.d1_test_case.MOCK_MN_BASE_URL)


@pytest.fixture(
    scope="function",
    params=[
        d1_client.mnclient_1_2.MemberNodeClient_1_2,
        d1_client.mnclient_2_0.MemberNodeClient_2_0,
    ],
)
def mn_client_v1_v2(request):
    yield request.param(d1_test.d1_test_case.MOCK_MN_BASE_URL)


# Misc


@pytest.fixture(
    scope="function",
    params=d1_test.test_files.load_json("combined_tricky_identifiers_unicode.json"),
)
def tricky_identifier_dict(request):
    """Unicode identifiers that use various reserved characters and embedded URL
    segments.

    Each value is a dict with keys, 'unescaped', 'path_escaped', 'query_escaped'.

    """
    yield request.param


@pytest.fixture(
    scope="function",
    params=[d1_test.instance_generator.identifier.generate_pid("DID_")],
)
def did(request):
    """Return a random identifier."""
    yield request.param


# Settings


@pytest.fixture(scope="session", autouse=True)
def django_sciobj_store_setup(request):
    """Create a unique SciObj store dir under /tmp for each worker.

    This overrides the path set in settings_test.OBJECT_STORE_PATH.

    """
    tmp_store_path = os.path.join(
        tempfile.gettempdir(), "gmn_test_obj_store", get_xdist_worker_id(request)
    )
    mock.patch("d1_gmn.app.startup._create_sciobj_store_root")
    with d1_gmn.tests.gmn_test_case.unique_sciobj_store(tmp_store_path):
        yield


# Database

# @pytest.fixture(scope="function", autouse=True)
# def enable_db_access(db):
#     # No current connection:
#     # django.db.connection.(.connection).set_isolation_level(
#     #   psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
#     # )
#     #
#     # Force the process to create new DB connections by closing the current ones.
#     # Not allowed in atomic block: django.db.connections.close_all()
#     pass


@pytest.fixture(scope="function")
def profile_sql(db):
    django.db.connection.queries = []
    yield
    logging.info("SQL queries by all methods:")
    list(map(logging.info, django.db.connection.queries))


@pytest.fixture(scope="function", autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(scope="session", autouse=True)
@pytest.mark.django_db
def django_db_setup(request, django_db_blocker):
    """Set up DB fixture from template.

    By default, pytest-django will set up empty test DBs. GMN tests need to run in
    context of a populated DB in order to be realistic. Using a populated DB also allows
    writing tests without having to set up preconditions from scratch in each test.

    This fixture overrides the default behavior to create test DBs from a template,
    providing populated DBs to GMN tests. Using a template DB is much faster than
    creating the DBs directly from JSON fixture files.

    When running in parallel with xdist, each worker is handled as a separate session,
    so session scoped fixtures are called for each worker, causing a separate database
    to be set up for each worker.

    """
    logger.debug("Setting up GMN test DB from template")

    template_db_name = d1_gmn.tests.gmn_test_case.django_get_db_name_by_key()
    unique_db_name = get_unique_db_name(request)
    d1_gmn.tests.gmn_test_case.django_set_db_name_by_key(unique_db_name)

    with django_db_blocker.unblock():
        postgres_create_from_template(unique_db_name, template_db_name)
        d1_gmn.tests.gmn_test_case.django_migrate()
        d1_gmn.tests.gmn_test_case.django_dump_db_stats()

    try:
        yield
    finally:
        d1_gmn.tests.gmn_test_case.django_close_all_connections()
        d1_gmn.tests.gmn_test_case.postgres_drop_if_exists(unique_db_name)


def get_unique_db_name(request):
    return "_".join(
        [
            d1_gmn.tests.gmn_test_case.django_get_db_name_by_key(),
            get_unique_suffix(request),
        ]
    )


def postgres_create_from_template(new_db_name, template_db_name):
    logger.debug(
        'Creating new db from template. new_db="{}" template_db="{}"'.format(
            new_db_name, template_db_name
        )
    )
    d1_gmn.tests.gmn_test_case.run_postgres_sql(
        "postgres",
        "create database {} template {};".format(new_db_name, template_db_name),
    )


def get_unique_suffix(request):
    return "_".join(
        [
            d1_test.instance_generator.random_data.random_lower_ascii(fixed_len=10),
            get_xdist_worker_id(request),
        ]
    ).strip("_")


def get_xdist_worker_id(request):
    """Return a different string for each worker when running in parallel under pytest-
    xdist, else return an empty string.

    Returned strings are on the form, "gwN".

    """
    s = getattr(request.config, "slaveinput", {}).get("slaveid")
    return s if s is not None else ""


def exit_if_switch_used_with_xdist(session, switch_list):
    if hasattr(session.config, "slaveinput"):
        for switch_str in switch_list:
            if session.config.getoption(switch_str):
                pytest.exit(
                    "Cannot use {} when running in parallel under pytest-xdist "
                    "(e.g., -n, --dist, --tx)".format(switch_str)
                )
