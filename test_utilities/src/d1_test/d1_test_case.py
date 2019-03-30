#!/usr/bin/env python

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
"""Utilities for unit- and integration tests."""
import collections
import contextlib
import datetime
import gc
import inspect
import io
import logging
import os
import random
import resource
import sys
import tempfile
import traceback
import xml

import decorator
import mock
import psutil
import psycopg2
import pyxb

import d1_common
import d1_common.cert.x509
import d1_common.const
import d1_common.date_time
import d1_common.types
import d1_common.types.dataoneErrors
import d1_common.types.dataoneTypes
import d1_common.xml

import d1_test.sample
import d1_test.test_files

CN_URL = d1_common.const.URL_DATAONE_ROOT

MOCK_MN_BASE_URL = 'http://mock.mn/node'
MOCK_CN_BASE_URL = 'http://mock.cn/node'
MOCK_CN_MN_BASE_URL = 'http://mock.cn.mn/node'

MOCK_REMOTE_BASE_URL = 'http://mock/remote'
MOCK_INVALID_BASE_URL = 'http://mock/invalid'

SOLR_QUERY_ENDPOINT = '/cn/v1/query/solr/'

DEFAULT_PERMISSION_LIST = [
    (['subj1'], ['read']),
    (['subj2', 'subj3', 'subj4'], ['read', 'write']),
    (['subj5', 'subj6', 'subj7', 'subj8'], ['read', 'changePermission']),
    (['subj9', 'subj10', 'subj11', 'subj12'], ['changePermission']),
]

SUBJ_DICT = {
    'trusted': 'gmn_test_subject_trusted',
    'submitter': 'gmn_test_subject_submitter',
}


@contextlib.contextmanager
def capture_std():
    """Capture stdout and stderr.

    - Does NOT capture logging.
    - Use the caplog fixture and get_caplog_text() for log capture.

    """
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def get_caplog_text(caplog, logger_name=None):
    """Return the log messages currently captured by the caplog fixture.

    - If ``logger_name`` is set, only messages from the given logger are returned.
    - This differs from `caplog.text` in that only the message part of the logs
    are retrieved, not the timestamps, loggers and log levels.

    """
    return '\n'.join(
        [
            r.getMessage()
            for r in caplog.records
            if (logger_name is None) or logger_name == r.name
        ]
    )


def clear_caplog(caplog):
    caplog.handler.records = []


@contextlib.contextmanager
def mock_input(answer_str):
    def _log(prompt_str):
        sys.stdout.write(prompt_str)
        return mock.DEFAULT

    with mock.patch('builtins.input', side_effect=_log, return_value=answer_str):
        yield


@contextlib.contextmanager
def disable_debug_level_logging():
    try:
        logging.disable(logging.DEBUG)
        yield
    finally:
        logging.disable(logging.NOTSET)


# reproducible_random

# TODO: When we move to Py3, move this over to the simple wrapper supported
# there. For now, this works, and it's probably not worth simplifying it with
# any decorator/context/class/function/parameterized wrappers.


def reproducible_random_decorator(seed):
    def reproducible_random_decorator_real(cls_or_func):
        if inspect.isclass(cls_or_func):
            return _reproducible_random_class_decorator(cls_or_func, seed)
        elif isinstance(cls_or_func, collections.Callable):
            return _reproducible_random_func_decorator(cls_or_func, seed)
        else:
            raise ValueError('Decorated object must be a class or callable (function)')

    return reproducible_random_decorator_real


def _reproducible_random_class_decorator(cls, seed):
    for test_name, test_func in list(cls.__dict__.items()):
        if test_name.startswith('test_'):
            # logging.debug(
            #   'Decorating: {}.{}: reproducible_random()'.
            #   format(cls.__name__, test_name)
            # )
            setattr(
                cls, test_name, _reproducible_random_func_decorator(test_func, seed)
            )
    return cls


def _reproducible_random_func_decorator(func, seed):
    def wrapper(func2, *args, **kwargs):
        # logging.debug(
        #   'Decorating: {}: reproducible_random()'.format(func2.__name__)
        # )
        with reproducible_random_context(seed):
            return func2(*args, **kwargs)

    return decorator.decorator(wrapper, func)


@contextlib.contextmanager
def reproducible_random_context(seed=None):
    """Start the PRNG at a fixed seed."""
    if seed is None:
        seed = get_test_module_name()
    state = random.getstate()
    random.seed(seed)
    yield
    random.setstate(state)


# ===============================================================================


@contextlib.contextmanager
def temp_sparse_file(gib=0, mib=0, kib=0, b=0):
    """Context manager providing a temporary file of size ``gib`` GiB + ``mib`` MiB +
    ``kib`` KiB + ``b`` bytes.

    - The file is created as a sparse empty file in tmp, so does not allocate
    actual space on disk.
    - Intended for use when large, empty (all zero), test files are needed.

    """
    with tempfile.TemporaryFile() as f:
        f.seek(gib * 1024 ** 3 + mib * 1024 ** 2 + kib * 1024 + b - 1)
        f.write(b'0')
        f.seek(0)
        yield f


@contextlib.contextmanager
def temp_file_name(suffix=None):
    """Provide a file path that can be used as the location of a temporary file, and
    delete any file written to the path on exit."""
    with tempfile.NamedTemporaryFile(suffix=suffix) as f:
        temp_file_path = f.name
    yield temp_file_path
    try:
        os.unlink(temp_file_path)
    except EnvironmentError:
        pass


@contextlib.contextmanager
def disable_garbage_collector():
    """Context manager that disables the garbage collector while in the context.

    Warnings:

      ``gc.collect()`` is called before entering the context in order to force Python to
      allocate new memory for objects that are created within the context. However, that
      does not seem to work reliably in the tested versions of Python 3.

    """
    gc.disable()
    gc.collect()
    try:
        yield
    finally:
        gc.enable()


@contextlib.contextmanager
def memory_limit(max_mem_bytes):
    """Raise MemoryError if code within the manager causes memory used by process to
    increase by more than ``max_mem_bytes``.

    This can be used for detecting excessive memory usage, for instance due to objects
    being buffered in memory instead of being streamed.

    This is implemented by setting a memory allocation limit at the process level and
    disabling garbage collection before entering the context and reversing that at
    exit.

    Warnings:

      This has turned out to not be very accurate. It may be due to Python holding on
      to memory after it has been garbage collected, though ``gc.collect()`` is called
      by the context manager in an attempt to avoid that.

      It's currently necessary to massively overshoot the limit specified by
      ``max_mem_bytes`` in order to reliably raise a MemoryError. Current values for a
      unit test for this context manager, is 10 MiB for ``max_mem_bytes`` and a
      combined 100 MiB of attempted allocations.

    """
    with disable_garbage_collector():
        process = psutil.Process(os.getpid())
        old_limit_tup = resource.getrlimit(resource.RLIMIT_AS)
        current_used_bytes = process.memory_info().vms
        limit_bytes = current_used_bytes + max_mem_bytes
        logging.debug(
            'Setting memory limit. current={:,} bytes, limit={:,} bytes'.format(
                current_used_bytes, limit_bytes
            )
        )
        resource.setrlimit(resource.RLIMIT_AS, (limit_bytes, resource.RLIM_INFINITY))

        yield

        logging.debug('Removing memory limit. limit={:,} bytes'.format(limit_bytes))
        resource.setrlimit(resource.RLIMIT_AS, old_limit_tup)


# ===============================================================================


class D1TestCase(object):
    @property
    def sample(self):
        return d1_test.sample

    @property
    def test_files(self):
        return d1_test.test_files

    @staticmethod
    def deserialize_and_check(doc, raises_pyxb_exc=False):
        try:
            d1_common.types.dataoneTypes.CreateFromDocument(doc)
        except (pyxb.PyXBException, xml.sax.SAXParseException):
            if raises_pyxb_exc:
                return
            else:
                raise
        if raises_pyxb_exc:
            raise Exception('Did not receive expected exception')

    @staticmethod
    def deserialize_exception_and_check(doc, raises_pyxb_exc=False):
        try:
            obj = d1_common.types.dataoneErrors.CreateFromDocument(doc)
        except (pyxb.PyXBException, xml.sax.SAXParseException):
            if raises_pyxb_exc:
                return
            else:
                raise
        if raises_pyxb_exc:
            raise Exception('Did not receive expected exception')
        return obj

    @staticmethod
    def get_total_number_of_objects(client):
        object_list = client.listObjects(
            count=1
        )  # TODO: Should be count=0 but there's currently a bug in CN.
        return object_list.total

    @staticmethod
    def get_pid_by_index(client, idx):
        object_list = client.listObjects(start=idx, count=1)
        try:
            return object_list.objectInfo[0].identifier.value()
        except IndexError:
            raise Exception('No objects')

    @staticmethod
    def get_random_valid_pid(client):
        total = D1TestCase.get_total_number_of_objects(client)
        return D1TestCase.get_pid_by_index(client, random.randint(0, total - 1))

    @staticmethod
    def touch(module_path, times=None):
        with open(module_path, 'a'):
            os.utime(module_path, times)

    #
    # Exception handling
    #

    # @staticmethod
    # def get_d1_test_case_location(exc_traceback=None):
    #   """Return the abs path and line number of the unit test that directly or
    #   indirectly triggered the exception
    #   - Use the exception currently being handled if exc_traceback is None,
    #   else use exc_traceback.
    #   - The unit test must be a method in a class that derives from D1TestCase.
    #   """
    #   tb_frame = D1TestCase.get_last_d1_test_case_frame(exc_traceback)
    #   return tb_frame.f_code.co_filename, tb_frame.f_lineno #+ 1

    # exc_traceback = D1TestCase.get_and_check_traceback(exc_traceback)
    # location_tup = None
    # while exc_traceback:
    #   if D1TestCase.frame_is_d1_test_case_method(exc_traceback):
    #     co = exc_traceback.tb_frame.f_code
    #     location_tup = co.co_filename, co.co_firstlineno + 1
    #   exc_traceback = exc_traceback.tb_next
    # if location_tup:
    #   return location_tup
    # raise Exception(
    #   "Exception was not triggered in a D1TestCase unit test method"
    # )

    @staticmethod
    def get_d1_test_case_location(exc_traceback=None):
        """Return the last stack frame that holds a D1TestCase unit test method.

        - Use the exception currently being handled if exc_traceback is None, else use
          exc_traceback.
        - The unit test must be a method in a class that derives from D1TestCase.

        """
        exc_traceback = D1TestCase.get_and_check_traceback(exc_traceback)
        location_tup = None
        while exc_traceback:
            if D1TestCase.frame_is_d1_test_case_method(exc_traceback):
                location_tup = (
                    exc_traceback.tb_frame.f_code.co_filename,
                    exc_traceback.tb_lineno,
                )

            exc_traceback = exc_traceback.tb_next
        if not location_tup:
            raise Exception(
                "Exception was not triggered in a D1TestCase unit test method"
            )
        return location_tup

    @staticmethod
    def frame_is_d1_test_case_method(exc_traceback):
        try:
            return isinstance(exc_traceback.tb_frame.f_locals['self'], D1TestCase)
        except KeyError:
            return False

    @staticmethod
    def get_and_check_traceback(tb):
        tb = tb or sys.exc_info()[2]
        assert hasattr(tb, "tb_next"), (
            "Not a valid traceback. Must be a native Python traceback, not a "
            "pytest.Traceback."
        )
        return tb

    #
    # Misc
    #

    @staticmethod
    @contextlib.contextmanager
    def mock_ssl_download(cert_obj):
        """Simulate successful cert download by catching call to
        ssl.SSLSocket.getpeercert() and returning {cert_obj} in DER format."""
        cert_der = d1_common.cert.x509.serialize_cert_to_der(cert_obj)
        with mock.patch('d1_common.cert.x509.ssl.SSLSocket.connect') as mock_connect:
            with mock.patch(
                'd1_common.cert.x509.ssl.SSLSocket.getpeercert'
            ) as mock_getpeercert:
                mock_getpeercert.return_value = cert_der
                yield mock_connect, mock_getpeercert

    def get_pyxb_value(self, inst_pyxb, inst_attr):
        try:
            return str(getattr(inst_pyxb, inst_attr).value())
        except (ValueError, AttributeError):
            return None

    def now_str(self):
        return d1_common.date_time.utc_now().strftime("%Y-%m-%d_%H:%M:%S")

    @staticmethod
    def dt_from_ts(ts, tz=None):
        """Convert POSIX timestamp to a datetime.

        - If ``tz`` supplied: The dt is adjusted to that tz before being returned.
        - If ``tz`` not supplied: the dt is returned as naive.
        - Keeping this function out of d1_common.date_time since naive datetimes are
          only needed for testing.

        """
        return datetime.datetime.fromtimestamp(ts, tz)

    # def random_str(self, num_chars=10):
    #   return ''.join([
    #     random.choice(string.ascii_lowercase) for _ in range(num_chars)
    #   ])

    # def random_id(self):
    #   return '{}_{}'.format(self.random_str(), self.now_str())
    #
    # def random_pid(self):
    #   return 'PID_{}'.format(self.random_id())
    #
    # def random_sid(self):
    #   return 'SID_{}'.format(self.random_id())
    #
    # def random_tag(self, tag_str):
    #   return '{}_{}'.format(tag_str, self.random_str())

    def format_pyxb(self, type_pyxb):
        ss = io.StringIO()
        ss.write('PyXB type instance:\n')
        ss.write(
            '\n'.join(
                [
                    '  {}'.format(s)
                    for s in d1_common.xml.serialize_to_xml_str(type_pyxb).splitlines()
                ]
            )
        )
        return ss.getvalue()

    # @staticmethod
    # def create_cursor(dsn):
    #   c = psycopg2.connect(dsn)
    #   return c.cursor(cursor_factory=psycopg2.extras.DictCursor)

    @staticmethod
    def run_sql(sql_str='', db_str=None, *args):
        """Run raw SQL using a separate DB connection."""
        try:
            conn = psycopg2.connect(database=db_str)
            # autocommit: Disable automatic transactions
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute(sql_str, args)
            return cur.fetchall()
        except psycopg2.DatabaseError as e:
            logging.error('SQL query error: ="{}"'.format(str(e)))
            raise
        finally:
            conn.close()

    #
    # SysMeta
    #

    @staticmethod
    def expand_subjects(subj):
        if isinstance(subj, str):
            subj = [subj]
        return {SUBJ_DICT[v] if v in SUBJ_DICT else v for v in subj or []}

    def prep_node_list(self, node_list, tag_str, num_nodes=5):
        if node_list is None:
            return None
        elif isinstance(node_list, list):
            return node_list
        elif node_list == 'random':
            return [
                'urn:node:{}'.format(self.random_tag(tag_str)) for _ in range(num_nodes)
            ]


# ===============================================================================

# import logging, logging.config, colorstreamhandler
#
# _LOGCONFIG = {
#     "version": 1,
#     "disable_existing_loggers": False,
#
#     "handlers": {
#         "console": {
#             "class": "colorstreamhandler.ColorStreamHandler",
#             "stream": "ext://sys.stderr",
#             "level": "INFO"
#         }
#     },
#
#     "root": {
#         "level": "INFO",
#         "handlers": ["console"]
#     }
# }
#
# logging.config.dictConfig(_LOGCONFIG)
# mylogger = logging.getLogger("mylogger")
# mylogger.warning("foobar")


class ColorStreamHandler(logging.StreamHandler):
    DEFAULT = '\x1b[0m'
    RED = '\x1b[31m'
    GREEN = '\x1b[32m'
    YELLOW = '\x1b[33m'
    CYAN = '\x1b[36m'

    CRITICAL = RED
    ERROR = RED
    WARNING = YELLOW
    INFO = GREEN
    DEBUG = CYAN

    @classmethod
    def _get_color(cls, level):
        if level >= logging.CRITICAL:
            return cls.CRITICAL
        elif level >= logging.ERROR:
            return cls.ERROR
        elif level >= logging.WARNING:
            return cls.WARNING
        elif level >= logging.INFO:
            return cls.INFO
        elif level >= logging.DEBUG:
            return cls.DEBUG
        else:
            return cls.DEFAULT

    def __init__(self, stream=None):
        logging.StreamHandler.__init__(self, stream)

    def format(self, record):
        text = logging.StreamHandler.format(self, record)
        color = self._get_color(record.levelno)
        return color + text + self.DEFAULT


def get_test_module_name():
    for module_path, line_num, func_name, line_str in traceback.extract_stack():
        module_name = os.path.splitext(os.path.split(module_path)[1])[0]
        if module_name.startswith('test_') and func_name.startswith('test_'):
            return module_name
