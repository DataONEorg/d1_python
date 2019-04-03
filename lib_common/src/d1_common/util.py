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
"""General utilities often needed by DataONE clients and servers."""
import collections
import contextlib
import datetime
import email.message
import json
import logging
import sys

import d1_common.date_time

logger = logging.getLogger(__name__)


def log_setup(is_debug=False, is_multiprocess=False):
    """Set up a standardized log format for the DataONE Python stack. All Python
    components should use this function. If ``is_multiprocess`` is True, include process
    ID in the log so that logs can be separated for each process.

    Output only to stdout and stderr.

    """
    format_str = (
        '%(asctime)s %(name)s %(module)s:%(lineno)d %(process)4d %(levelname)-8s %(message)s'
        if is_multiprocess
        else '%(asctime)s %(name)s %(module)s:%(lineno)d %(levelname)-8s %(message)s'
    )
    formatter = logging.Formatter(format_str, '%Y-%m-%d %H:%M:%S')
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setFormatter(formatter)
    logging.getLogger('').addHandler(console_logger)
    if is_debug:
        logging.getLogger('').setLevel(logging.DEBUG)
    else:
        logging.getLogger('').setLevel(logging.INFO)


def get_content_type(content_type):
    """Extract the MIME type value from a content type string.

    Removes any subtype and parameter values that may be present in the string.

    Args:
      content_type: str
        String with content type and optional subtype and parameter fields.

    Returns:
      str: String with only content type

    Example:

    ::

      Input:   multipart/form-data; boundary=aBoundaryString
      Returns: multipart/form-data

    """
    m = email.message.Message()
    m['Content-Type'] = content_type
    return m.get_content_type()


def nested_update(d, u):
    """Merge two nested dicts.

    Nested dicts are sometimes used for representing various recursive structures. When
    updating such a structure, it may be convenient to present the updated data as a
    corresponding recursive structure. This function will then apply the update.

    Args:
      d: dict
        dict that will be updated in-place. May or may not contain nested dicts.

      u: dict
        dict with contents that will be merged into ``d``. May or may not contain
        nested dicts.

    """
    for k, v in list(u.items()):
        if isinstance(v, collections.Mapping):
            r = nested_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


# ===============================================================================


class EventCounter(object):
    """Count events during a lengthy operation and write running totals and/or a summary
    to a logger when the operation has completed.

    The summary contains the name and total count of each event that was counted.

    Example:

      Summary written to the log:

    ::

      Events:
      Creating SciObj DB representations: 200
      Retrieving revision chains: 200
      Skipped Node registry update: 1
      Updating obsoletedBy: 42
      Whitelisted subject: 2

    """

    def __init__(self):
        self._event_dict = {}

    @property
    def event_dict(self):
        """Provide direct access to the underlying dict where events are recorded.

        Returns:   dict: Events and event counts.

        """
        return self._event_dict

    def count(self, event_str, inc_int=1):
        """Count an event.

        Args:
          event_str:
            The name of an event to count. Used as a key in the event dict. The same
            name will also be used in the summary.

          inc_int: int
            Optional argument to increase the count for the event by more than 1.

        """
        self._event_dict.setdefault(event_str, 0)
        self._event_dict[event_str] += inc_int

    def log_and_count(self, event_str, msg_str=None, inc_int=None):
        """Count an event and write a message to a logger.

        Args:
          event_str: str
            The name of an event to count. Used as a key in the event dict. The same
            name will be used in the summary. This also becomes a part of the message
            logged by this function.

          msg_str: str
            Optional message with details about the events. The message is only written
            to the log. While the ``event_str`` functions as a key and must remain the
            same for the same type of event, ``log_str`` may change between calls.

          inc_int: int
            Optional argument to increase the count for the event by more than 1.

        """
        logger.info(
            ' - '.join(map(str, [v for v in (event_str, msg_str, inc_int) if v]))
        )
        self.count(event_str, inc_int or 1)

    def dump_to_log(self):
        """Write summary to logger with the name and number of times each event has been
        counted.

        This function may be called at any point in the process. Counts are not zeroed.

        """
        if self._event_dict:
            logger.info('Events:')
            for event_str, count_int in sorted(self._event_dict.items()):
                logger.info('  {}: {}'.format(event_str, count_int))
        else:
            logger.info('No Events')


# ===============================================================================


@contextlib.contextmanager
def print_logging():
    """Context manager to temporarily suppress additional information such as timestamps
    when writing to loggers.

    This makes logging look like ``print()``. The main use case is in scripts that mix
    logging and ``print()``, as Python uses separate streams for those, and output can
    and does end up getting shuffled if ``print()`` and logging is used interchangeably.

    When entering the context, the logging levels on the current handlers are saved then
    modified to WARNING levels. A new DEBUG level handler with a formatter that does not
    write timestamps, etc, is then created.

    When leaving the context, the DEBUG handler is removed and existing loggers are
    restored to their previous levels.

    By modifying the log levels to WARNING instead of completely disabling the loggers,
    it is ensured that potentially serious issues can still be logged while the context
    manager is in effect.

    """
    root_logger = logging.getLogger()
    old_level_list = [h.level for h in root_logger.handlers]
    for h in root_logger.handlers:
        h.setLevel(logging.WARN)
    log_format = logging.Formatter('%(message)s')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_format)
    stream_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(stream_handler)
    yield
    root_logger.removeHandler(stream_handler)
    for h, level in zip(root_logger.handlers, old_level_list):
        h.setLevel(level)


def save_json(py_obj, json_path):
    """Serialize a native object to JSON and save it normalized, pretty printed to a
    file.

    The JSON string is normalized by sorting any dictionary keys.

    Args:
      py_obj: object
        Any object that can be represented in JSON. Some types, such as datetimes are
        automatically converted to strings.

      json_path: str
        File path to which to write the JSON file. E.g.: The path must exist. The
        filename will normally end with ".json".

    See Also:
      ToJsonCompatibleTypes()

    """
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(serialize_to_normalized_pretty_json(py_obj))


def load_json(json_path):
    """Load JSON file and parse it to a native object.

    Args:
      json_path: str
        File path from which to load the JSON file.

    Returns:
      object : Typically a nested structure of ``list`` and ``dict`` objects.

    """
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_json_to_normalized_pretty_json(json_str):
    """Normalize and pretty print a JSON string.

    The JSON string is normalized by sorting any dictionary keys.

    Args:
      json_str:
        A valid JSON string.

    Returns:
      str: normalized, pretty printed JSON string.

    """
    return serialize_to_normalized_pretty_json(json.loads(json_str))


def serialize_to_normalized_pretty_json(py_obj):
    """Serialize a native object to normalized, pretty printed JSON.

    The JSON string is normalized by sorting any dictionary keys.

    Args:
      py_obj: object
        Any object that can be represented in JSON. Some types, such as datetimes are
        automatically converted to strings.

    Returns:
      str: normalized, pretty printed JSON string.

    """
    return json.dumps(py_obj, sort_keys=True, indent=2, cls=ToJsonCompatibleTypes)


def serialize_to_normalized_compact_json(py_obj):
    """Serialize a native object to normalized, compact JSON.

    The JSON string is normalized by sorting any dictionary keys. It will be on a single
    line without whitespace between elements.

    Args:
      py_obj: object
        Any object that can be represented in JSON. Some types, such as datetimes are
        automatically converted to strings.

    Returns:
      str: normalized, compact JSON string.

    """
    return json.dumps(
        py_obj, sort_keys=True, separators=(',', ':'), cls=ToJsonCompatibleTypes
    )


class ToJsonCompatibleTypes(json.JSONEncoder):
    """Some native objects such as ``datetime.datetime`` are not automatically converted
    to strings for use as values in JSON.

    This helper adds such conversions for types that the DataONE Python stack encounters
    frequently in objects that are to be JSON encoded.

    """

    # noinspection PyMissingOrEmptyDocstring
    def default(self, o):
        # bytes -> str (assume UTF-8)
        if isinstance(o, bytes):
            return o.decode('utf-8', errors='replace')
        # set -> sorted list
        if isinstance(o, set):
            return sorted([v for v in o])
        # datetime -> ISO 8601 UTC
        if isinstance(o, datetime.datetime):
            return d1_common.date_time.to_iso8601_utc(o)
        return json.JSONEncoder.default(self, o)


def format_sec_to_dhm(sec):
    """Format seconds to days, hours, minutes.

    Args:
      sec: float or int
        Number of seconds in a period of time

    Returns:
      Period of time represented as a string on the form ``0d:00h:00m``.

    """
    rem_int, s_int = divmod(int(sec), 60)
    rem_int, m_int, = divmod(rem_int, 60)
    d_int, h_int, = divmod(rem_int, 24)
    return '{}d{:02d}h{:02d}m'.format(d_int, h_int, m_int)
