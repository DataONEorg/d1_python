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
import base64
import bz2
import contextlib
import logging
import os
import re
import subprocess
import tempfile
import textwrap
import traceback

import posix_ipc
import requests.structures
import requests_toolbelt.utils.dump

import d1_common
import d1_common.types
import d1_common.util
import d1_common.utils.filesystem
import d1_common.xml

import d1_test.pycharm
import d1_test.test_files
import d1_test.xml_normalize

import d1_client.d1client
import d1_client.util

import django
import django.core
import django.core.management

MAX_LINE_WIDTH = 130

# Options are populated by pytest.
options = {}

logger = logging.getLogger(__name__)


def start_tidy():
    """Call at start of test run to tidy the samples directory.

    Pytest will run regular session scope fixtures in parallel with test collection,
    while this function must complete before collection starts. The best place to call
    it from appears to be ./conftest.pytest_sessionstart().

    """
    logging.info("Moving files to tidy dir")
    sample_dir_path = get_abs_sample_file_path("")
    tidy_dir_path = get_abs_sample_tidy_file_path("")
    d1_common.utils.filesystem.create_missing_directories_for_dir(sample_dir_path)
    d1_common.utils.filesystem.create_missing_directories_for_dir(tidy_dir_path)
    i = 0
    for i, item_name in enumerate(os.listdir(sample_dir_path)):
        sample_path = os.path.join(sample_dir_path, item_name)
        tidy_path = os.path.join(tidy_dir_path, item_name)
        if os.path.exists(tidy_path):
            os.unlink(tidy_path)
        os.rename(sample_path, tidy_path)
    logging.info("Moved {} files".format(i))


def get_abs_sample_file_path(filename):
    return d1_test.test_files.get_abs_test_file_path(os.path.join("sample", filename))


def get_abs_sample_tidy_file_path(filename):
    return d1_test.test_files.get_abs_test_file_path(
        os.path.join("sample_tidy", filename)
    )


def assert_diff_equals(left_obj, right_obj, file_post_str, client=None):
    """Check that the difference between two objects, typically captured before and
    after some operation, is as expected."""
    file_ext_str, left_str = obj_to_pretty_str(left_obj)
    right_str = obj_to_pretty_str(right_obj)[1]
    diff_str = _get_sxs_diff_str(left_str, right_str)
    if diff_str is None:
        return
    return assert_equals(diff_str, file_post_str, client, ".sample")


def assert_equals(
    got_obj, file_post_str, client=None, sample_ext=".sample", no_wrap=False
):
    file_ext_str, got_str = obj_to_pretty_str(got_obj, no_wrap=no_wrap)
    filename = _format_file_name(client, file_post_str, sample_ext)
    logging.info('Using sample file. filename="{}"'.format(filename))
    exp_path = _get_or_create_path(filename)

    if options.get("review"):
        _review_interactive(got_str, exp_path, file_post_str, file_ext_str)
        return

    diff_str = _get_sxs_diff_file(got_str, exp_path)

    if diff_str is None:
        return

    logging.info(
        "\nSample file: {0}\n{1} Sample mismatch. GOT <-> EXPECTED {1}\n{2}".format(
            filename, "-" * 10, diff_str
        )
    )

    if options.get("update"):
        save(got_str, filename)
        return

    if options.get("ask"):
        _save_interactive(got_str, exp_path, file_post_str, file_ext_str)
        return

    raise AssertionError(
        "\nSample file: {0}\n{1} Sample mismatch. GOT <-> EXPECTED {1}\n{2}".format(
            filename, "-" * 10, diff_str
        )
    )


def get_path(filename):
    # When tidying, get_path_list() may move samples, which can cause concurrent calls
    # to receive different paths for the same file. This is resolved by
    # serializing calls to get_path_list(). Regular multiprocessing.Lock() does not
    # seem to work under pytest-xdist.
    # noinspection PyUnresolvedReferences
    with posix_ipc.Semaphore(
        "/{}".format(__name__), flags=posix_ipc.O_CREAT, initial_value=1
    ):
        path = get_abs_sample_file_path(filename)
        if os.path.isfile(path):
            return path
        tidy_file_path = get_abs_sample_tidy_file_path(filename)
        if os.path.isfile(tidy_file_path):
            os.rename(tidy_file_path, path)
        return path


def dump(o, log_func=logger.debug):
    map(log_func, d1_test.sample.obj_to_pretty_str(o, no_clobber=True)[1].splitlines())


def load(filename, mode_str="rb"):
    with open(_get_or_create_path(filename), mode_str) as f:
        return f.read()


def save_path(got_str, exp_path):
    assert isinstance(got_str, str)
    logging.info('Saving sample file. filename="{}"'.format(os.path.split(exp_path)[1]))
    with open(exp_path, "wb") as f:
        f.write(got_str.encode("utf-8"))


def save_obj(got_obj, filename):
    got_str = obj_to_pretty_str(got_obj)[1]
    save(got_str, filename)


def save(got_str, filename):
    path = _get_or_create_path(filename)
    save_path(got_str, path)


def get_sxs_diff(left_obj, right_obj):
    file_ext_str, left_str = obj_to_pretty_str(left_obj)
    right_str = obj_to_pretty_str(right_obj)[1]
    return _get_sxs_diff_str(left_str, right_str)


def gui_sxs_diff(left_obj, right_obj, file_post_str):
    file_ext_str, left_str = obj_to_pretty_str(left_obj)
    right_str = obj_to_pretty_str(right_obj)[1]
    return _gui_diff_str_str(left_str, right_str, file_post_str, file_ext_str)


def obj_to_pretty_str(o, no_clobber=False, no_wrap=False):
    """Serialize object to str.

    - Create a normalized string representation of the object that is suitable for
      using in a diff.
    - XML and PyXB is not normalized here, so the objects must be normalized before
      being passed in.
    - Serialization that breaks long lines into multiple lines is preferred, since
      multiple lines makes differences easier to spot in diffs.

    """

    # noinspection PyUnreachableCode
    def serialize(o_):
        logging.debug('Serializing object. type="{}"'.format(type(o_)))
        #
        # Special cases are ordered before general cases
        #
        # DOT Language (digraph str from ResourceMap)
        with ignore_exceptions():
            if "digraph" in o_:
                # We don't have a good way to normalize DOT, so we just sort the lines
                # and mask out node values.
                return (
                    ".txt",
                    "\n".join(
                        sorted(str(re.sub(r"node\d+", "nodeX", o_)).splitlines())
                    ),
                )
        # DataONEException
        if isinstance(o_, d1_common.types.exceptions.DataONEException):
            return (".txt", str(o_))

        # ResourceMap (rdflib.ConjunctiveGraph)
        with ignore_exceptions():
            return (
                ".xml.repr.txt",
                str(
                    # d1_test.xml_normalize.get_normalized_xml_representation(
                    o_.serialize_to_display("n3")
                    # )
                ),
            )
        # Dict returned from Requests
        if isinstance(o_, requests.structures.CaseInsensitiveDict):
            with ignore_exceptions():
                return (
                    ".json",
                    d1_common.util.serialize_to_normalized_pretty_json(dict(o_)),
                )
        # Requests Request / Response
        if isinstance(o_, (requests.Request, requests.Response)):
            if o_.reason is None:
                o_.reason = "<unknown>"
            return (
                ".txt",
                d1_client.util.normalize_request_response_dump(
                    requests_toolbelt.utils.dump.dump_response(o_)
                ),
            )
        # Valid UTF-8 bytes
        with ignore_exceptions():
            return ".txt", "VALID-UTF-8-BYTES:" + o_.decode("utf-8")
        # Bytes that are not valid UTF-8
        # - Sample files are always valid UTF-8, so binary is forced to UTF-8 by
        # removing any sequences that are not valid UTF-8. This makes diffs more
        # readable in case they contain some UTF-8.
        # - In addition, a Base64 encoded version is included in order to be able to
        # verify byte by byte equivalence.
        # - It would be better to use errors='replace' here, but kdiff3 interprets
        # the Unicode replacement char (�) as invalid Unicode.
        if isinstance(o_, (bytes, bytearray)):
            return (
                ".txt",
                "BINARY-BYTES-AS-UTF-8:{}\nBINARY-BYTES-AS-BASE64:{}".format(
                    o_.decode("utf-8", errors="ignore"),
                    base64.standard_b64encode(o_).decode("ascii"),
                ),
            )
        # Valid XML str
        with ignore_exceptions():
            return ".xml", d1_common.xml.reformat_to_pretty_xml(o_)
        # Valid JSON str
        with ignore_exceptions():
            return ".json", d1_common.util.format_json_to_normalized_pretty_json(o_)
        # Any str
        if isinstance(o_, str):
            return ".txt", o_
        # PyXB object
        with ignore_exceptions():
            return ".xml", d1_common.xml.serialize_to_xml_str(o_, pretty=True)
        # Any native object structure that can be serialized to JSON
        # This covers only basic types that can be sorted. E.g., of not covered:
        # datetime, mixed str and int keys.
        with ignore_exceptions():
            return ".json", d1_common.util.serialize_to_normalized_pretty_json(o_)
        # Anything that has a str representation
        with ignore_exceptions():
            return ".txt", str(o_)
        # Fallback to internal representation
        # Anything that looks like a memory address is clobbered later
        return ".txt", repr(o_)

    file_ext_str, obj_str = serialize(o)
    assert isinstance(obj_str, str)
    obj_str = obj_str.rstrip()

    # Replace '\n' with actual newlines since breaking text into multiple lines
    # when possible helps with diffs.
    obj_str = obj_str.replace("\\n", "\n")

    if not no_clobber:
        obj_str = _clobber_uncontrolled_volatiles(obj_str)

    if not no_wrap:
        obj_str = wrap_and_preserve_newlines(obj_str)

    return file_ext_str, obj_str


def wrap_and_preserve_newlines(s):
    return "\n".join(
        [
            "\n".join(
                textwrap.wrap(
                    line,
                    MAX_LINE_WIDTH,
                    break_long_words=False,
                    replace_whitespace=False,
                )
            )
            for line in s.splitlines()
        ]
    )


def get_test_module_name():
    for module_path, line_num, func_name, line_str in traceback.extract_stack():
        module_name = os.path.splitext(os.path.split(module_path)[1])[0]
        if module_name.startswith("test_") and func_name.startswith("test_"):
            return module_name


def _clobber_uncontrolled_volatiles(o_str):
    """Some volatile values in results are not controlled by freezing the time and/or
    PRNG seed.

    We replace those with a fixed string here.

    """
    # requests-toolbelt is using another prng for mmp docs
    o_str = re.sub(r"(?<=boundary=)[0-9a-fA-F]+", "[BOUNDARY]", o_str)
    o_str = re.sub(r"--[0-9a-f]{32}", "[BOUNDARY]", o_str)
    # entryId is based on a db sequence type
    o_str = re.sub(r"(?<=<entryId>)\d+", "[ENTRY-ID]", o_str)
    # TODO: This shouldn't be needed...
    o_str = re.sub(r"(?<=Content-Type:).*", "[CONTENT-TYPE]", o_str)
    # The uuid module uses MAC address, etc
    o_str = re.sub(r"(?<=test_fragment_volatile_)[0-9a-fA-F]+", "[UUID]", o_str)
    # Version numbers
    o_str = re.sub(r"(?<=DataONE-Python/)\s*\d+\.\d+\.\d+", "[VERSION]", o_str)
    o_str = re.sub(r"(?<=DataONE-GMN:)\s*\d+\.\d+\.\d+", "[VERSION]", o_str)
    o_str = re.sub(r"(?<=Python ITK)\s*\d+\.\d+\.\d+", "[VERSION]", o_str)
    # ETA depends on how fast the computer is
    o_str = re.sub(r"\d{1,3}h\d{2}m\d{2}s", "[ETA-HMS]", o_str)
    # Disk space
    o_str = re.sub(r"[\s\d.]+GiB", "[DISK-SPACE]", o_str)
    # Memory address
    o_str = re.sub(r"0x[\da-fA-F]{8,}", "[MEMORY-ADDRESS]", o_str)
    return o_str


def _get_or_create_path(filename):
    """Get the path to a sample file and enable cleaning out unused sample files.

    See the test docs for usage.

    """
    path = get_path(filename)
    logging.debug("Sample path: {}".format(path))
    if not os.path.isfile(path):
        logging.info("Write new sample file: {}".format(path))
        with open(path, "w") as f:
            f.write("<new sample file>\n")
    return path


def _format_file_name(client, file_post_str, file_ext_str):
    section_list = [get_test_module_name(), file_post_str]
    if client:
        section_list.extend(
            [
                d1_client.d1client.get_client_type(client),
                d1_client.d1client.get_version_tag_by_d1_client(client),
            ]
        )
    return "{}{}".format(
        d1_common.utils.filesystem.gen_safe_path_element("_".join(section_list)),
        file_ext_str,
    )


def _get_sxs_diff_str(got_str, exp_str):
    with tempfile.NamedTemporaryFile(suffix="__EXPECTED") as exp_f:
        exp_f.write(exp_str.encode("utf-8"))
        exp_f.seek(0)
        return _get_sxs_diff_file(got_str, exp_f.name)


def _get_sxs_diff_file(got_str, exp_path):
    """Return a minimal formatted side by side diff if there are any none- whitespace
    changes, else None.

    - Return: str

    """
    assert isinstance(got_str, str)
    try:
        sdiff_proc = subprocess.Popen(
            [
                "sdiff",
                "--ignore-blank-lines",
                "--ignore-all-space",
                "--minimal",
                "--width={}".format(MAX_LINE_WIDTH),
                "--tabsize=2",
                "--strip-trailing-cr",
                "--expand-tabs",
                "--text",
                "-",
                exp_path
                # '--suppress-common-lines'
            ],
            bufsize=-1,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out_bytes, err_str = sdiff_proc.communicate(got_str.encode("utf-8"))
    except OSError as e:
        raise AssertionError(
            'Unable to run sdiff. Is it installed? error="{}"'.format(str(e))
        )
    else:
        if not sdiff_proc.returncode:
            return
        if sdiff_proc.returncode == 1:
            return out_bytes.decode("utf-8")
        else:
            raise AssertionError(
                'sdiff returned error code. code={} error="{}"'.format(
                    sdiff_proc.returncode, err_str
                )
            )


def _gui_diff_str_path(got_str, exp_path, file_post_str, file_ext_str):
    exp_str = d1_test.test_files.load_utf8_to_str(exp_path)
    with _tmp_file_pair(got_str, exp_str, file_post_str, file_ext_str) as (
        got_f,
        exp_f,
    ):
        # subprocess.call(['kdiff3', got_f.name, exp_f.name])
        d1_test.pycharm.diff(got_f.name, exp_f.name)


def _gui_diff_str_str(left_str, right_str, file_post_str, file_ext_str):
    with _tmp_file_pair(left_str, right_str, file_post_str, file_ext_str) as (
        left_f,
        right_f,
    ):
        # subprocess.call(['kdiff3', left_f.name, right_f.name])
        d1_test.pycharm.diff(left_f.name, right_f.name)


def _save_interactive(got_str, exp_path, file_post_str, file_ext_str):
    _gui_diff_str_path(got_str, exp_path, file_post_str, file_ext_str)
    answer_str = ask_sample_file_update(exp_path)
    if answer_str == "y":
        save_path(got_str, exp_path)
    elif answer_str == "f":
        raise AssertionError("Failure triggered interactively")


def _diff_interactive(left_str, right_str, file_post_str, file_ext_str):
    _gui_diff_str_str(left_str, right_str, file_post_str, file_ext_str)
    answer_str = ask_diff_ignore()
    if answer_str == "f":
        raise AssertionError("Failure triggered interactively")


def _review_interactive(got_str, exp_path, file_post_str, file_ext_str):
    _gui_diff_str_path(got_str, exp_path, file_post_str, file_ext_str)
    # answer_str = ask_sample_file_update(exp_path)
    # if answer_str == 'y':
    #     save_path(got_str, exp_path)
    # elif answer_str == 'f':
    #     raise AssertionError('Failure triggered interactively')


@contextlib.contextmanager
def ignore_exceptions(*exception_list):
    exception_list = exception_list or (Exception,)
    try:
        yield
    except exception_list as e:
        if e is SyntaxError:
            raise
        # logging.debug('Ignoring exception: {}'.format(str(e)))


@contextlib.contextmanager
def _tmp_file_pair(got_str, exp_str, file_post_str, file_ext_str):
    def format_suffix(n):
        return "{}__{}__{}".format(
            "__{}".format(file_post_str.upper()) if file_post_str else "",
            n.upper(),
            file_ext_str,
        )

    with tempfile.NamedTemporaryFile(suffix=format_suffix("RECEIVED")) as got_f:
        with tempfile.NamedTemporaryFile(suffix=format_suffix("EXPECTED")) as exp_f:
            got_f.write(got_str.encode("utf-8"))
            exp_f.write(exp_str.encode("utf-8"))
            got_f.seek(0)
            exp_f.seek(0)
            yield got_f, exp_f


# def _guess_file_ext_strension(obj_str):
#     {
#         'text/plain': '.txt',
#         'application/octet-stream': '',
#
#
#     }
#     buffer = magic.from_buffer(obj_str, mime=True)
#     print('{}\n{}\n{}'.format('#'*100, obj_str, buffer))
#     return mimetypes.guess_extension(buffer) or '.txt'


def save_compressed_db_fixture(filename):
    fixture_file_path = get_path(filename)
    logging.info('Writing fixture sample. path="{}"'.format(fixture_file_path))
    with bz2.BZ2File(
        fixture_file_path, "w", buffering=1024, compresslevel=9
    ) as bz2_file:
        django.core.management.call_command("dumpdata", stdout=bz2_file)


def ask_sample_file_update(sample_path):
    answer_str = None
    while answer_str not in ("", "y", "n", "f"):
        answer_str = input_with_sigint_capture(
            'Update sample file "{}"? Yes/No/Fail [Enter/n/f] '.format(
                os.path.split(sample_path)[1]
            )
        )
    return answer_str


def ask_diff_ignore():
    answer_str = None
    while answer_str not in ("", "y", "f"):
        answer_str = input_with_sigint_capture("Ignore difference? Yes/Fail [Enter/f] ")
    return answer_str


def input_with_sigint_capture(question_str):
    """input() with SIGINT (Ctrl-C) capture and redirect to "Fail"."""
    try:
        answer_str = input(question_str).lower()
    except KeyboardInterrupt:
        return "f"
    if answer_str == "":
        answer_str = "y"
    return answer_str


# ==============================================================================


class SampleException(Exception):
    pass
