# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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

# The Django init needs to occur before the django and gmn_test_case imports, so we're
# stuck with a bit of a messy import section that isort and flake8 don't like.
# isort:skip_file

import requests.exceptions
import d1_gmn.tests.gmn_test_case
import bz2
import contextlib
import copy
import datetime
import io
import logging
import os
import random
import shutil
import sys
import tempfile
import traceback

import django
import django.conf
import django.core.management
import django.db
import django.test

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d1_gmn.settings_test")
django.setup()

import d1_test.test_files
import psycopg2
import psycopg2.extensions
import requests

import pytest

import d1_gmn.app
import d1_gmn.app.models
import d1_gmn.app.revision
import d1_gmn.app.sciobj_store
import d1_gmn.app.views.internal
import d1_gmn.tests
import d1_gmn.tests.gmn_mock

import d1_common.checksum
import d1_common.const
import d1_common.resource_map
import d1_common.types
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions

import d1_common.xml

import d1_test.d1_test_case
import d1_test.instance_generator.access_policy
import d1_test.instance_generator.identifier
import d1_test.instance_generator.random_data
import d1_test.instance_generator.sciobj
import d1_test.instance_generator.system_metadata
import d1_test.mock_api.django_client

import d1_client.mnclient_1_2
import d1_client.mnclient_2_0

ENABLE_SQL_PROFILING = False

MOCK_GMN_BASE_URL = "http://gmn.client/node"
REL_DB_FIXTURE_PATH = "json/db_fixture.json.bz2"
DEFAULT_DB_KEY = "default"

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def unique_sciobj_store(store_root_path):
    # TODO: Turn into a fixture. Current solution leaves temp upload dirs.
    root_path = os.path.join(
        store_root_path,
        d1_test.instance_generator.random_data.random_lower_ascii(fixed_len=10),
    )
    store_path = os.path.join(root_path, "store")
    upload_path = os.path.join(root_path, "upload")
    with django.test.override_settings(
        OBJECT_STORE_PATH=store_path, FILE_UPLOAD_TEMP_DIR=upload_path
    ):
        try:
            logger.debug('Creating sciobj store. store_path="{}"'.format(store_path))
            # d1_common.utils.filesystem.create_missing_directories_for_dir(store_path)
            d1_gmn.app.sciobj_store.create_store()
            logger.debug(
                'Creating tmp upload dir. upload_path="{}"'.format(upload_path)
            )
            yield
        finally:
            logger.debug('Deleting sciobj store. store_path="{}"'.format(root_path))
            shutil.rmtree(root_path)


# Postgres DB


def postgres_drop_if_exists(db_name):
    logger.debug("Dropping DB if exists: db_name={}".format(db_name))
    run_postgres_sql("postgres", "drop database if exists {};".format(db_name))


def postgres_create_blank(db_name):
    logger.debug("Creating blank DB. db_name={}".format(db_name))
    run_postgres_sql("postgres", "create database {} encoding 'utf-8';".format(db_name))


def postgres_db_exists(db_name):
    logger.debug("Checking if DB exists. db_name={}".format(db_name))
    exists_bool = bool(
        run_postgres_sql(
            "postgres", "select 1 from pg_database WHERE datname='{}'".format(db_name)
        )
    )
    if exists_bool:
        logger.debug("DB exists")
    else:
        logger.debug("DB does not exist")
    return exists_bool


def run_postgres_sql(db, sql):
    try:
        conn = psycopg2.connect(database=db)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(sql)
    except psycopg2.DatabaseError as e:
        logger.debug("SQL query error: {}".format(str(e)))
        raise
    try:
        return cur.fetchall()
    except psycopg2.DatabaseError:
        return None
    finally:
        conn.close()
        d1_gmn.tests.gmn_test_case.django_close_all_connections()


# Django DB


def django_get_db_name_by_key(db_key=DEFAULT_DB_KEY):
    return django.conf.settings.DATABASES[db_key]["NAME"]


def django_set_db_name_by_key(db_name, db_key=DEFAULT_DB_KEY):
    django.conf.settings.DATABASES[db_key]["NAME"] = db_name


def django_save_db_fixture(db_key=DEFAULT_DB_KEY):
    fixture_file_path = d1_test.test_files.get_abs_test_file_path(REL_DB_FIXTURE_PATH)
    logging.info('Writing fixture. path="{}"'.format(fixture_file_path))
    buf = io.StringIO()
    django.core.management.call_command(
        "dumpdata",
        exclude=["auth.permission", "contenttypes"],
        database=db_key,
        stdout=buf,
    )
    with bz2.BZ2File(
        fixture_file_path, "w", buffering=1024 ** 2, compresslevel=9
    ) as bz2_file:
        bz2_file.write(buf.getvalue().encode("utf-8"))


def django_load_db_fixture(rel_json_fixture_path, db_key=DEFAULT_DB_KEY):
    logger.debug(
        "Populating DB from compressed JSON fixture file. db_key={}".format(db_key)
    )
    fixture_file_path = d1_test.test_files.get_abs_test_file_path(rel_json_fixture_path)
    django.core.management.call_command("loaddata", fixture_file_path, database=db_key)
    django_commit_and_close(db_key)


def django_migrate(db_key=DEFAULT_DB_KEY):
    logger.debug("Applying DB migrations. db_key={}".format(db_key))
    django.core.management.call_command("migrate", "--run-syncdb", database=db_key)
    django_commit_and_close(db_key)


def django_dump_db_stats():
    logger.debug("Database:")
    logger.debug(
        "  db_name={}".format(django.conf.settings.DATABASES["default"]["NAME"])
    )
    logger.debug(
        "  total_sciobj_count={}".format(
            d1_gmn.app.views.internal.get_total_sciobj_count()
        )
    )
    logger.debug(
        "  unique_subject_count={}".format(
            d1_gmn.app.views.internal.get_unique_subject_count()
        )
    )
    logger.debug(
        "  total_permissions_count={}".format(
            d1_gmn.app.views.internal.get_total_permissions_count()
        )
    )
    logger.debug(
        "  total_event_count={}".format(
            d1_gmn.app.views.internal.get_total_event_count()
        )
    )
    logger.debug(
        "  total_format_count={}".format(
            d1_gmn.app.views.internal.get_total_format_count()
        )
    )
    logger.debug(
        "  avg_sci_data_size_bytes={}".format(
            d1_gmn.app.views.internal.get_avg_sci_data_size_bytes()
        )
    )
    logger.debug(
        "  sciobj_storage_used_bytes={}".format(
            d1_gmn.app.views.internal.get_sciobj_storage_used_bytes()
        )
    )
    logger.debug(
        "  last_hour_event_count={}".format(
            d1_gmn.app.views.internal.get_last_hour_event_count()
        )
    )


def django_clear_db(db_key=DEFAULT_DB_KEY):
    django.core.management.call_command("flush", interactive=False, database=db_key)


def django_commit_and_close(db_key=DEFAULT_DB_KEY):
    django_commit(db_key)
    django_close_all_connections()


def django_commit(db_key=DEFAULT_DB_KEY):
    django.db.connections[db_key].commit()


def django_close_all_connections():
    for connection in django.db.connections.all():
        connection.close()
    # TODO: Needed?
    django.db.connections.close_all()


# =============================================================================


class GMNTestCase(d1_test.d1_test_case.D1TestCase):
    def setup_method(self, method):
        """Run for each test method that derives from GMNTestCase."""
        # logger.error('GMNTestCase.setup_method()')
        d1_test.mock_api.django_client.add_callback(MOCK_GMN_BASE_URL)
        # d1_test.mock_api.get.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
        self.client_v1 = d1_client.mnclient_1_2.MemberNodeClient_1_2(MOCK_GMN_BASE_URL)
        self.client_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(MOCK_GMN_BASE_URL)
        # self.test_client = d1_gmn.tests.gmn_test_client.GMNTestClient(
        #   d1_test.d1_test_case.MOCK_BASE_URL
        # )
        self.v1 = d1_common.types.dataoneTypes_v1_1
        self.v2 = d1_common.types.dataoneTypes_v2_0
        # Remove limit on max diff to show. This can cause debug output to
        # explode...
        # TODO
        # self.maxDiff = None

    @property
    def mock(self):
        return d1_gmn.tests.gmn_mock

    @classmethod
    def capture_exception(cls):
        """If GMN responds with something that cannot be parsed by d1_client as a valid
        response for the particular call, d1_client raises a DataONE ServiceFailure
        exception with the response stored in the traceInformation member. The Django
        diagnostics page triggers this behavior, so, in order to access the diagnostics
        page, we check for unhandled DataONEExceptions here and write any provided
        traceInformation to temporary storage, typically.

        /tmp.

        For convenience, we also maintain a link to the latest traceInformation.
        Together with the "--exitfirst" parameter for pytest, it allows just
        refreshing the browser to view new Django diagnostics pages.

        When serializing a DataONEException to a string, traceInformation is
        truncated to 1024 characters, but the files written here will always contain
        the complete traceInformation.

        """
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if not isinstance(exc_value, Exception):
            return
        logger.exception("Test failed with exception:")
        if not isinstance(exc_value, d1_common.types.exceptions.DataONEException):
            return
        func_name_str = GMNTestCase.get_test_func_name()
        file_path = os.path.join(
            tempfile.gettempdir(), "gmn_test_failed_{}.txt".format(func_name_str)
        )
        # Dump the entire exception
        with open(file_path, "w") as f:
            f.write(str(exc_value))
        logger.error('Wrote exception to file. path="{}"'.format(file_path))
        # Dump any HTML (typically from the Django diags page)
        if exc_value.traceInformation:
            ss = io.StringIO()
            is_in_html = False
            for line_str in exc_value.traceInformation.splitlines():
                if "<!DOCTYPE" in line_str or "<html" in line_str:
                    is_in_html = True
                if is_in_html:
                    ss.write(line_str)
            if is_in_html:
                file_path = os.path.join(tempfile.gettempdir(), "gmn_test_failed.html")
                with open(file_path, "w") as f:
                    f.write(str(ss.getvalue()))
                logger.error(
                    'Wrote HTML from exception to file. path="{}"'.format(file_path)
                )

    @staticmethod
    def get_test_func_name():
        exc_type, exc_value, exc_traceback = sys.exc_info()
        for stack_trace in traceback.extract_tb(exc_traceback):
            module_path = stack_trace[0]
            func_name = stack_trace[2]
            if func_name.startswith("test_"):
                return "{}_{}".format(os.path.split(module_path)[1][:-3], func_name)
        return "<not a test>"

    # def disable_server_cert_validation(self):
    #   requests.packages.urllib3.disable_warnings()
    #   d1_client.session.DEFAULT_VERIFY_TLS = False

    #
    # assert
    #

    # TODO: Move the "assert" keyword over to the calling code. It's easier to
    # find the errors when they're asserted in the caller.

    def assert_sysmeta_pid_and_sid(self, sysmeta_pyxb, pid, sid):
        self.assert_sysmeta_pid(sysmeta_pyxb, pid)
        self.assert_sysmeta_sid(sysmeta_pyxb, sid)

    def assert_sysmeta_pid(self, sysmeta_pyxb, pid):
        assert self.get_pyxb_value(sysmeta_pyxb, "identifier") == pid

    def assert_sysmeta_sid(self, sysmeta_pyxb, sid):
        assert self.get_pyxb_value(sysmeta_pyxb, "seriesId") == sid

    def assert_eq_sysmeta_sid(self, sysmeta_a_pyxb, sysmeta_b_pyxb):
        assert self.get_pyxb_value(sysmeta_a_pyxb, "seriesId") == self.get_pyxb_value(
            sysmeta_b_pyxb, "seriesId"
        )

    def assert_slice(self, slice_pyxb, start, count, total):
        """Check that slice matches the expected slice and that actual number of objects
        matches the slice count."""
        assert slice_pyxb.start == start
        assert slice_pyxb.count == count
        assert slice_pyxb.total == total
        if hasattr(slice_pyxb, "objectInfo"):
            assert len(slice_pyxb.objectInfo) == count
        elif hasattr(slice_pyxb, "logEntry"):
            assert len(slice_pyxb.logEntry) == count

    def assert_required_response_headers_present(self, response):
        assert "last-modified" in response.headers
        assert "content-length" in response.headers
        assert "content-type" in response.headers

    def assert_valid_date(self, date_str):
        assert datetime.datetime(*list(map(int, date_str.split("-"))))

    def assert_sci_obj_size_matches_sysmeta(self, sciobj_bytes, sysmeta_pyxb):
        assert sysmeta_pyxb.size == len(sciobj_bytes)

    def assert_sci_obj_checksum_matches_sysmeta(self, sciobj_bytes, sysmeta_pyxb):
        checksum_pyxb = d1_common.checksum.create_checksum_object_from_bytes(
            sciobj_bytes, sysmeta_pyxb.checksum.algorithm
        )
        assert d1_common.checksum.are_checksums_equal(
            checksum_pyxb, sysmeta_pyxb.checksum
        )

    def assert_checksums_equal(self, a_pyxb, b_pyxb):
        assert d1_common.checksum.are_checksums_equal(a_pyxb, b_pyxb)

    def assert_valid_chain(self, client, pid_chain_list, sid):
        logger.debug("Chain: {}".format(" - ".join(pid_chain_list)))
        pad_pid_chain_list = [None] + pid_chain_list + [None]
        i = 0
        for prev_pid, cur_pid, next_pid in zip(
            pad_pid_chain_list, pad_pid_chain_list[1:], pad_pid_chain_list[2:]
        ):
            logger.debug(
                "Link {}: {} <- {} -> {}".format(i, prev_pid, cur_pid, next_pid)
            )
            obj_str, sysmeta_pyxb = self.get_obj(client, cur_pid)
            assert self.get_pyxb_value(sysmeta_pyxb, "obsoletes") == prev_pid
            assert self.get_pyxb_value(sysmeta_pyxb, "identifier") == cur_pid
            assert self.get_pyxb_value(sysmeta_pyxb, "obsoletedBy") == next_pid
            assert self.get_pyxb_value(sysmeta_pyxb, "seriesId") == sid
            i += 1

    def are_equivalent_pyxb(self, a_pyxb, b_pyxb):
        a_xml = d1_common.xml.serialize_pretty(a_pyxb)
        b_xml = d1_common.xml.serialize_pretty(b_pyxb)
        if not d1_common.xml.are_equivalent(a_xml, b_xml):
            self.dump(
                'PyXB type instances are not equivalent.\na_xml="{}"\nb_xml="{}"\n'.format(
                    a_xml, b_xml
                )
            )
            return False
        return True

    #
    # CRUD
    #

    def create_revision_chain(self, client, chain_len, sid=None, *args, **kwargs):
        """Create a revision chain with a total of ``chain_len`` objects.

        If client is v2, can assign a SID to the chain. Return the SID (None for v1) and
        a list of the PIDs in the chain. The first PID in the list is the tail and the
        last is the head.

        """

        def did(idx):
            return "#{:03d}_{}".format(
                idx, d1_test.instance_generator.identifier.generate_pid()
            )

        base_pid, base_sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
            client, pid=did(0), sid=sid, *args, **kwargs
        )

        pid_chain_list = [base_pid]
        for i in range(1, chain_len):
            update_pid = did(i)
            self.update_obj(
                client,
                old_pid=base_pid,
                new_pid=update_pid,
                sid=base_sid,
                *args,
                **kwargs,
            )
            pid_chain_list.append(update_pid)
            base_pid = update_pid

        return base_sid, pid_chain_list

    def convert_to_replica(self, pid):
        """Convert a local sciobj to a simulated replica by adding a LocalReplica model
        to it."""
        replica_info_model = d1_gmn.app.models.replica_info(
            "completed", "urn:node:testReplicaSource"
        )
        d1_gmn.app.models.local_replica(pid, replica_info_model)

    def call_d1_client(self, api_func, *arg_list, **arg_dict):
        """Issue d1_client calls under a mocked GMN authentication and authorization
        subsystem.

        Mock GMN authn and authz so calls are detected as having been made with a
        specific set of active and trusted subjects. Then call GMN through
        d1_client, which itself is typically mocked to issue calls through the
        Django test client.

        By default, disable_auth=True, which disables GMN authn and authz
        altogether, making it irrelevant which active and trusted subjects are used.
        To get GMN to control access based on the provided active and trusted
        subjects, set disable_auth=False.

        Args:
          Optional args: session_subj_list, trusted_subj_list, disable_auth
          All other args are sent to the api function

        """
        # TODO: Handling the args manually like this was necessary to get the
        # signature I wanted, but it may be done better with
        # functools.partial(func[,*args][, **keywords]).
        session_subj_list = arg_dict.pop("session_subj_list", True)
        trusted_subj_list = arg_dict.pop("trusted_subj_list", True)
        whitelisted_subj_list = arg_dict.pop("whitelisted_subj_list", True)
        disable_auth = arg_dict.pop("disable_auth", True)

        with d1_gmn.tests.gmn_mock.set_auth_context(
            ["session_subj_1", "session_subj_2", "session_subj_3"]
            if session_subj_list is True
            else session_subj_list,
            ["trusted_subj_1", "trusted_subj_2"]
            if trusted_subj_list is True
            else trusted_subj_list,
            ["whitelisted_subj_1", "whitelisted_subj_2"]
            if whitelisted_subj_list is True
            else whitelisted_subj_list,
            disable_auth,
        ):
            try:
                return api_func(*arg_list, **arg_dict)
            except requests.exceptions.ConnectionError as e:
                pytest.fail(
                    'Make sure: Test function is decorated with "@responses.activate", '
                    "class derives from GMNTestCase, "
                    "The correct client fixture is used (mn_client / gmn_client), "
                    "class setup_method() calls super(). "
                    'error="{}"'.format(str(e))
                )
                # coercing to Unicode: need string or buffer, NoneType found:
                # Check that authentication has been disabled

    def create_obj(
        self,
        client,
        pid=True,
        sid=None,
        submitter=True,
        rights_holder=True,
        permission_list=True,
        session_subj_list=True,
        trusted_subj_list=True,
        disable_auth=True,
        vendor_dict=None,
        now_dt=True,
        **sysmeta_generator_option_dict,
    ):
        """Generate a test object and call MNStorage.create() Parameters:

        True: Use a default or generated value Other: Use the supplied value

        """
        pid, sid, sciobj_bytes, sysmeta_pyxb = self.generate_sciobj_with_defaults(
            client,
            pid,
            sid,
            submitter,
            rights_holder,
            permission_list,
            now_dt,
            **sysmeta_generator_option_dict,
        )
        with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
            self.call_d1_client(
                client.create,
                pid,
                io.BytesIO(sciobj_bytes),
                sysmeta_pyxb,
                vendor_dict,
                session_subj_list=session_subj_list,
                trusted_subj_list=trusted_subj_list,
                disable_auth=disable_auth,
            )
        assert self.get_pyxb_value(sysmeta_pyxb, "identifier") == pid
        return pid, sid, sciobj_bytes, sysmeta_pyxb

    def update_obj(
        self,
        client,
        old_pid,
        new_pid=True,
        sid=None,
        submitter=True,
        rights_holder=True,
        permission_list=True,
        session_subj_list=True,
        trusted_subj_list=True,
        disable_auth=True,
        vendor_dict=None,
        now_dt=True,
    ):
        """Generate a test object and call MNStorage.update() Parameters:

        True: Use a default or generate a value Other: Use the supplied value

        """
        pid, sid, sciobj_bytes, sysmeta_pyxb = self.generate_sciobj_with_defaults(
            client, new_pid, sid, submitter, rights_holder, permission_list, now_dt
        )
        with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
            self.call_d1_client(
                client.update,
                old_pid,
                io.BytesIO(sciobj_bytes),
                pid,
                sysmeta_pyxb,
                vendor_dict,
                session_subj_list=session_subj_list,
                trusted_subj_list=trusted_subj_list,
                disable_auth=disable_auth,
            )
        assert self.get_pyxb_value(sysmeta_pyxb, "identifier") == pid
        return pid, sid, sciobj_bytes, sysmeta_pyxb

    def get_obj(
        self,
        client,
        did,
        session_subj_list=True,
        trusted_subj_list=True,
        disable_auth=True,
        vendor_dict=None,
    ):
        """Combined MNRead.get() and MNRead.getSystemMetadata() Parameters:

        True: Use a default or generate a value Other: Use the supplied value

        """
        sciobj_bytes = self.call_d1_client(
            client.get,
            did,
            vendor_dict,
            session_subj_list=session_subj_list,
            trusted_subj_list=trusted_subj_list,
            disable_auth=disable_auth,
        ).content
        sysmeta_pyxb = self.call_d1_client(
            client.getSystemMetadata,
            did,
            vendor_dict,
            session_subj_list=session_subj_list,
            trusted_subj_list=trusted_subj_list,
            disable_auth=disable_auth,
        )
        self.assert_sci_obj_size_matches_sysmeta(sciobj_bytes, sysmeta_pyxb)
        self.assert_sci_obj_checksum_matches_sysmeta(sciobj_bytes, sysmeta_pyxb)
        return sciobj_bytes, sysmeta_pyxb

    # create(), update(), get() with provided sysmeta

    def create_obj_by_sysmeta(
        self,
        client,
        sysmeta_pyxb,
        session_subj_list=True,
        trusted_subj_list=True,
        disable_auth=True,
        vendor_dict=None,
    ):
        """Generate a test object and call MNStorage.create() Parameters:

        True: Use a default or generated value Other: Use the supplied value

        """
        pid = d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
        send_sciobj_bytes = d1_test.instance_generator.sciobj.generate_reproducible_sciobj_bytes(
            pid
        )
        send_sysmeta_pyxb = copy.deepcopy(sysmeta_pyxb)
        send_sysmeta_pyxb.checksum = d1_common.checksum.create_checksum_object_from_bytes(
            send_sciobj_bytes, sysmeta_pyxb.checksum.algorithm
        )
        send_sysmeta_pyxb.size = len(send_sciobj_bytes)
        send_sysmeta_pyxb.obsoletes = None
        send_sysmeta_pyxb.obsoletedBy = None
        with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
            self.call_d1_client(
                client.create,
                pid,
                io.BytesIO(send_sciobj_bytes),
                send_sysmeta_pyxb,
                vendor_dict,
                session_subj_list=session_subj_list,
                trusted_subj_list=trusted_subj_list,
                disable_auth=disable_auth,
            )
        return send_sciobj_bytes, send_sysmeta_pyxb

    # create multiple objects

    def create_multiple_objects(self, client, object_count=10):
        with d1_gmn.tests.gmn_mock.disable_auth():
            pid_list = []
            for i in range(object_count):
                pid, sid, send_sciobj_bytes, send_sysmeta_pyxb = self.create_obj(client)
                pid_list.append(pid)
        return pid_list

    def create_objects_by_list(self, client, pid_list):
        with d1_gmn.tests.gmn_mock.disable_auth():
            for pid in pid_list:
                self.create_obj(client, pid, sid=None)

    #

    def generate_sciobj_with_defaults(
        self,
        client,
        pid=True,
        sid=None,
        submitter=True,
        rights_holder=True,
        permission_list=True,
        now_dt=True,
        **sysmeta_generator_option_dict,
    ):
        permission_list = (
            d1_test.d1_test_case.DEFAULT_PERMISSION_LIST
            if permission_list is True
            else permission_list
        )
        sid = (
            d1_test.instance_generator.identifier.generate_sid() if sid is True else sid
        )
        option_dict = {
            k: v
            for (k, v) in (
                ("identifier", pid),
                ("seriesId", sid),
                ("submitter", submitter),
                ("rightsHolder", rights_holder),
                (
                    "accessPolicy",
                    d1_test.instance_generator.access_policy.generate_from_permission_list(
                        client, permission_list
                    ),
                ),
                ("dateUploaded", now_dt),
                ("dateSysMetadataModified", now_dt),
            )
            if v is not True
        }
        option_dict.update(sysmeta_generator_option_dict)
        pid, sid, sciobj_bytes, sysmeta_pyxb = d1_test.instance_generator.sciobj.generate_reproducible_sciobj_with_sysmeta(
            client, None if pid is True else pid, option_dict
        )
        return pid, sid, sciobj_bytes, sysmeta_pyxb

    # Resource maps

    def create_resource_map(self, client, pid_list, ore_pid=None):
        ore_pid = ore_pid or d1_test.instance_generator.identifier.generate_pid(
            "PID_ORE_"
        )
        ore = d1_common.resource_map.createSimpleResourceMap(
            ore_pid, scimeta_pid=pid_list[0], sciobj_pid_list=pid_list[1:]
        )
        ore_xml = ore.serialize_to_transport()
        sysmeta_pyxb = d1_test.instance_generator.system_metadata.generate_from_file(
            client,
            io.BytesIO(ore_xml),
            {
                "identifier": ore_pid,
                "formatId": d1_common.const.ORE_FORMAT_ID,
                "replica": None,
            },
        )
        self.call_d1_client(client.create, ore_pid, io.BytesIO(ore_xml), sysmeta_pyxb)
        return ore_pid

    #
    # Misc
    #

    def object_list_to_pid_list(self, object_list_pyxb):
        return sorted([v.identifier.value() for v in object_list_pyxb.objectInfo])

    def log_to_pid_list(self, log_record_list_pyxb):
        return sorted([v.identifier.value() for v in log_record_list_pyxb.logEntry])

    def vendor_proxy_mode(self, object_stream_url):
        return {"VENDOR-GMN-REMOTE-URL": object_stream_url}

    def dump_permissions(self):
        logger.debug("Permissions:")
        for s in d1_gmn.app.models.Permission.objects.order_by(
            "subject__subject", "level", "sciobj__pid__did"
        ):
            logger.debug(s.sciobj.pid.did)
            logger.debug(s.subject)
            logger.debug(s.level)
            logger.debug("")

    def dump_subjects(self):
        logger.debug("Subjects:")
        for s in d1_gmn.app.models.Subject.objects.order_by("subject"):
            logger.debug("  {}".format(s.subject))

    def get_sid_with_min_chain_length(self, min_len=2):
        """Get list of all SIDs in the DB fixture."""
        sid_list = self.get_sid_list()
        random.shuffle(sid_list)
        for sid in sid_list:
            pid_list = d1_gmn.app.revision.get_all_pid_by_sid(sid)
            if len(pid_list) >= min_len:
                return sid

    def get_sid_list(self):
        """Get list of all SIDs in the DB."""
        return [
            o.sid.did for o in d1_gmn.app.models.Chain.objects.filter(sid__isnull=False)
        ]

    def get_pid_list(self):
        """Get list of all PIDs in the DB."""
        return [o.pid.did for o in d1_gmn.app.models.ScienceObject.objects.all()]

    def get_total_log_records(self, client, **filters):
        return client.getLogRecords(start=0, count=0, **filters).total

    def get_total_objects(self, client, **filters):
        return client.listObjects(start=0, count=0, **filters).total

    def get_random_pid_sample(self, n_pids):
        # We select sample from ordered list since the prng seed may be locked for reproducability.
        return random.sample(
            [
                v.pid.did
                for v in d1_gmn.app.models.ScienceObject.objects.order_by("pid__did")
            ],
            n_pids,
        )

    def call_management_command(self, *args, **kwargs):
        with self.mock.disable_management_command_logging_setup():
            with self.mock.disable_management_command_concurrent_instance_check():
                django.core.management.call_command(*args, **kwargs)

    def run_django_sql(self, sql_str, dump=True, *sql_arg_list):
        """Run raw SQL in the current Django database context and return any results as
        a list of dicts, where they keys are the column names.

        - By default, also dump the result with logging.debug(). Disable with
          dump=False.
        - This can be used for checking the state of a database within the implicit
          transactions that wrap the unit tests.

        """

        def dict_fetchall(c):
            return [
                dict(zip([d[0] for d in c.description], row)) for row in c.fetchall()
            ]

        try:
            with django.db.connection.cursor() as cursor:
                logger.debug("Running SQL query: {}".format(sql_str.strip()))
                logger.debug("SQL query args: {}".format(", ".join(sql_arg_list)))
                cursor.execute(sql_str, sql_arg_list)
                row_dict = dict_fetchall(cursor)
                logger.debug("SQL query result:")
                if dump:
                    self.sample.dump(row_dict)
        except Exception as e:
            logger.error("SQL query error: {}".format(str(e)))
            raise
