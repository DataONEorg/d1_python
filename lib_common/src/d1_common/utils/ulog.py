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
"""Utilities intended primarily for scripts that use logging to display output directly
to users.

In d1_python, this is used by GMN Management Commands and command line utilities and
examples.

"""
import contextlib
import importlib
import io
import logging
import logging.config
import sys

log = logging.getLogger(__name__)

LOGGER_NAME_MAX_WIDTH = 16


def setup(is_debug, disable_existing_loggers=False, format_str=None, datefmt_str=None):
    """Set up logging.

    This will output only to stdout. Simply writing to stdout and letting the user
    print, pipe or capture the stream as desired often seems to work best. To both view
    the log output and capture to a file, the ``tee`` command may be used.

    This modifies the configuration of the root logger in the current logging tree. As
    most loggers inherit everything from the root logger, they get the same
    configuration.

    Args:
        is_debug: bool

            - ``True``: Log level on the root logger is set to logging.DEBUG.
            - ``False``: Log level is set to logging.INFO.

        disable_existing_loggers: bool

            - ``True``: The ``disabled`` flag is set on all loggers that are currently
              in the logging tree, causing them to be unable to emit any log records. Only
              the root logger can emit log records. Any additional loggers must either be
              created or be re-enabled.
            - ``False``: The ``disabled`` flag is left as is on all existing loggers.

        datefmt_str: str (optional)
            Override the default date format string.

        format_str: str (optional)
            Override the default log format string.
    """
    level = logging.DEBUG if is_debug else logging.INFO
    logging.config.dictConfig(
        {
            "version": 1,
            "filters": {"last": {"()": LastLoggerFilter}},
            "disable_existing_loggers": disable_existing_loggers,
            "formatters": {
                "commandline": {
                    "class": "d1_common.utils.ulog.MultilineFormatter",
                    "format": (
                        format_str
                        or "%(asctime)s %(levelname)-5.5s %(last_name)s %(message)s"
                    ),
                    "datefmt": (datefmt_str or "%Y-%m-%d %H:%M:%S"),
                }
            },
            "loggers": {
                "": {
                    "handlers": ["stdout"],
                    "level": level,
                    "propagate": True,
                    "filters": ["last"],
                }
            },
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "commandline",
                    "filters": ["last"],
                    "stream": "ext://sys.stdout",
                }
            },
        }
    )


# ===============================================================================


@contextlib.contextmanager
def write_columns(
    col_space=2, indent=0, sort=False, newline=True, write_func=sys.stdout.write
):
    # Write columns as described in StreamWriter(). Use StreamWriter() directly if there
    # is more than one set of lines to write.
    __doc__ = StreamWriter.columns.__doc__
    with StreamWriter(write_func, indent, newline).columns(
        col_space, 0, sort
    ) as column_writer:
        yield column_writer


@contextlib.contextmanager
def write_section(
    header_str,
    col_space=2,
    header_indent=0,
    list_indent=2,
    count=True,
    sort=True,
    newline=True,
    write_func=sys.stdout.write,
):
    # Write list sections as described in StreamWriter(). Use StreamWriter() directly if
    # there is more than one list section to write.
    __doc__ = StreamWriter.section.__doc__
    with StreamWriter(write_func, 0, newline).section(
        header_str, col_space, header_indent, list_indent, count, sort
    ) as section_writer:
        yield section_writer


def string_io_writer(base_indent=0):
    string_io = io.StringIO()
    return string_io, StreamWriter(string_io.write, base_indent, newline=True)


def debug_logging_tree():
    """Investigate logging issues by printing the current tree of loggers.
    """
    try:
        logging_tree = importlib.import_module("logging_tree")
    except ModuleNotFoundError:
        raise AssertionError("logging_tree module is not installed as a dependency")
    logging_tree.printout()


class ColorStreamHandler(logging.StreamHandler):
    DEFAULT = "\x1b[0m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    CYAN = "\x1b[36m"

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


def getLogger(name, level=logging.DEBUG):
    current_logger = logging.getLoggerClass()
    try:
        logging.setLoggerClass(ULogger)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        return logger
    finally:
        logging.setLoggerClass(current_logger)


class ULogger(logging.getLoggerClass()):
    """Logger that adds log formatting and methods for writing log records intended for
    being viewed directly by an interactive user.
    """

    # Shortcuts
    N = logging.NOTSET
    D = logging.DEBUG
    I = logging.INFO
    E = logging.ERROR
    C = logging.CRITICAL

    def __init__(
        self,
        name,
        default_record_level=logging.INFO,
        default_logger_level=logging.DEBUG,
    ):
        super().__init__(name)
        self.setLevel(default_logger_level)
        self.default_record_level = default_record_level

        # self.default_logger_level = default_logger_level
        # if LastLoggerFilter not in logging.getLogger('').filters:
        #     setup(is_debug=True, disable_existing_loggers=False)

        self.setLevel(default_logger_level)

    def isatty(self):
        return hasattr(self._out, "isatty") and self._out.isatty()

    def w(self, s, level=None):
        """Write a log line"""
        print(s, level or self.default_record_level)
        self.log(level or self.level, s)

    @contextlib.contextmanager
    def columns(self, col_space=2, indent=0, sort=True, level=None):
        # Log column adjusted text as described in StreamWriter.
        __doc__ = StreamWriter.columns.__doc__
        with write_columns(
            col_space, indent, sort, False, lambda s: self.w(s, level)
        ) as writer:
            yield writer

    @contextlib.contextmanager
    def section(
        self,
        header_str,
        header_indent=0,
        list_indent=2,
        col_space=2,
        count=True,
        sort=True,
        level=None,
    ):
        # Log a list sections as described in StreamWriter.
        __doc__ = StreamWriter.section.__doc__
        with write_section(
            header_str,
            col_space,
            header_indent,
            list_indent,
            count,
            sort,
            lambda s: self.w(s, level),
        ) as writer:
            yield writer


class LastLoggerFilter(logging.Filter):
    """Add a last_name record to log formatters that contains only the last part of a
    logger name, trimmed to a fixed width. If the name is shorter than the trim width,
    it's right-justified and padded to the left.
    """

    def filter(self, record):
        record.last_name = record.name.rjust(LOGGER_NAME_MAX_WIDTH, " ")[
            -LOGGER_NAME_MAX_WIDTH:
        ]
        return True


class MultilineFormatter(logging.Formatter):
    """Write each line in multiline log records as a separate log record.

    Logs using this formatter is harder to parse since the timestamp and context
    information no longer appears only on first line of the multiline records. At the
    same time, logs using this method look much nicer when using logging for output in
    command line scripts.
    """

    def format(self, record: logging.LogRecord):
        msg_str = record.msg or "\n"
        fmt_list = []
        for s in msg_str.splitlines():
            record.msg = s
            fmt_list.append(super().format(record))
        record.msg = msg_str
        record.message = "\n".join(fmt_list)
        return record.message


class AltCustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno in (logging.WARNING, logging.ERROR, logging.CRITICAL):
            record.msg = "[%s] %s" % (record.levelname, record.msg)
        return super(AltCustomFormatter, self).format(record)


class StreamWriter:
    def __init__(self, write_func=sys.stdout.write, base_indent=0, newline=True):
        """Create a StreamWriter for a given stream.

        Args:
            write_func: Write function for a stream. Will be called with str.
            base_indent: Basic indentation level.

            newline: bool
                ``True``: Add a "\n" to the end of each write to the stream.
                
                Stream write methods differ in how they handle newlines. E.g, Log
                writers insert it automatically while regular IO writers do not.
        """
        self._write_func = write_func
        self._base_indent = base_indent
        self._newline = newline

    @contextlib.contextmanager
    def columns(self, col_space=2, indent=0, sort=False):
        """Write to a stream with column alignment between lines.

        While in the context manager, lines are added to a buffer. When exiting the
        context, the lines are written to the log with padding to align the
        columns.

        Any whitespace on either side of the pipe ("|") is stripped, so can be added in
        the strings as required to improve readability of the source.

        Args:

            col_space: int
                Minimum number of spaces between columns.
            indent: int
                Minimum number of spaces beyond base_indent to start writing header.
            sort: bool
                Sort the line before writing to stream.

        Example:

        .. highlight:: python

        ::

            with d1_common.utils.ulog.write_columns(col_space=2) as c:
                log("line with pipe | character marking column locations | columns")
                log("another line   |    with fewer, same or more column markers")
                log("| two columns")

        Writes to stream:

        .. highlight: none

        ::

            line with pipe    character marking column locations         columns
            another line      with fewer, same or more column markers
                              two columns

        """
        str_list = []
        max_list = []

        def k(sv):
            sv = str(sv)
            str_list.append([s.strip() for s in sv.split("|")])
            max_list.extend(0 for _ in range(len(max_list), len(str_list[-1])))
            for i, s in enumerate(str_list[-1]):
                max_list[i] = max(max_list[i], len(s))

        yield k

        if sort:
            str_list.sort()

        for v in str_list:
            self.write(
                (" " * col_space).join(
                    [f"{s.strip():<{max_list[i]}}" for i, s in enumerate(v)]
                ),
                indent,
            )

    @contextlib.contextmanager
    def section(
        self,
        header_str,
        col_space,
        header_indent=0,
        list_indent=2,
        count=True,
        sort=True,
    ):
        """Write a section consisting of a header and a list of strings, optionally column
         adjusted.

        Args:
            col_space:
            header_str (str):
                Header string to write.
            header_indent (int):
                Number of spaces beyond base_indent to start writing header.
            list_indent (int):
                Number of spaces beyond header to start writing each list item.
            count (bool):
                Add the number of items in the list in parens after the header.
            sort (bool):
                Write sorted list.

        See Also:
            ``write_columns()`` for how to add column markers to strings.

        Example output:

        .. highlight:: none

        ::

            Subjects known on this GMN (3):
              CN=urn:node:CNUCSB1,DC=dataone,DC=org 1
              uid=meacafdc=org                      2
              uid=uxdtzadc=org                      3
        """
        str_list = []
        yield lambda v: str_list.extend(v) if not isinstance(
            v, (str, int)
        ) else str_list.append(v)
        self.header(header_str, header_indent, len(str_list) if count else None)
        with self.columns(col_space, header_indent + list_indent, sort) as log_col:
            if not str_list:
                log_col("<none>")
            else:
                for s in str_list:
                    log_col(s)

    def header(self, header_str: str, indent: int = 0, count=None):
        self.write("")
        self.write(f'{header_str}{f" ({count})" if count is not None else ""}:', indent)

    def write(self, s, indent=0):
        """Write line to stream with optional indentation"""
        n = "\n" if self._newline else ""
        self._write_func(f'{" " * (self._base_indent + indent)}{s + n}')
