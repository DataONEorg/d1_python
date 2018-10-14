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
"""General utilities often needed by DataONE clients and servers.
"""
import collections
import contextlib
import datetime
import email.message
import email.utils
import errno
import json
import logging
import os
import sys

import d1_common.date_time


def log_setup(is_debug=False, is_multiprocess=False):
  """Set up a standardized log format for the DataONE Python stack. All Python
  components should use this function. If {is_multiprocess} is True, include
  process ID in the log so that logs can be separated for each process.

  Output only to stdout and stderr.
  """
  format_str = (
    '%(asctime)s %(name)s %(module)s:%(lineno)d %(process)4d %(levelname)-8s %(message)s'
    if is_multiprocess else
    '%(asctime)s %(name)s %(module)s:%(lineno)d %(levelname)-8s %(message)s'
  )
  formatter = logging.Formatter(format_str, '%Y-%m-%d %H:%M:%S')
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)
  if is_debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.INFO)


def abs_path(rel_path):
  """Convert a path that is relative to the module from which this function is
  called, to an absolute path.
  """
  return os.path.abspath(
    os.path.
    join(os.path.dirname(sys._getframe(1).f_code.co_filename), rel_path)
  )


def abs_path_from_base(base_path, rel_path):
  """Join {rel_path} to {base_path} and return an absolute path to the resulting
  location
  """
  return os.path.abspath(
    os.path.join(
      os.path.dirname(sys._getframe(1).f_code.co_filename), base_path, rel_path
    )
  )


def create_missing_directories_for_dir(dir_path):
  try:
    os.makedirs(dir_path)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise


def create_missing_directories_for_file(file_path):
  create_missing_directories_for_dir(os.path.dirname(file_path))


def get_content_type(content_type):
  m = email.message.Message()
  m['Content-Type'] = content_type
  return m.get_content_type()


def utf_8_bytes_to_str(b):
  assert isinstance(b, bytes)
  try:
    return b.decode('utf-8')
  except UnicodeDecodeError as e:
    logging.error(str(e))


def nested_update(d, u):
  for k, v in list(u.items()):
    if isinstance(v, collections.Mapping):
      r = nested_update(d.get(k, {}), v)
      d[k] = r
    else:
      d[k] = u[k]
  return d


#===============================================================================


class EventCounter(object):
  def __init__(self):
    self._event_dict = {}

  @property
  def event_dict(self):
    return self._event_dict

  def count(self, event_str, inc_int=1):
    self._event_dict.setdefault(event_str, 0)
    self._event_dict[event_str] += inc_int

  def log_and_count(self, event_str, msg_str=None, inc_int=None):
    """{event_str} is both a key for the count and part of the log message.
    {log_str} is a message with details that may change for each call
    """
    logging.info(
      ' - '.join(map(str,
                     [v for v in (event_str, msg_str, inc_int) if v]))
    )
    self.count(event_str, inc_int or 1)

  def dump_to_log(self):
    if self._event_dict:
      logging.info('Events:')
      for event_str, count_int in sorted(self._event_dict.items()):
        logging.info('  {}: {}'.format(event_str, count_int))
    else:
      logging.info('No Events')


#===============================================================================


@contextlib.contextmanager
def print_logging():
  """Temporarily remove all formatting from logging.

  Creates a logger that writes only the logged strings. This makes logging look
  like print(). The main use case is in scripts that mix logging and print(), as
  Python uses separate streams for those, and output can, and does, end up
  getting shuffled up. Also, it can be used as a "print with log level".

  This works by saving the logging levels on the current handlers, setting
  them to something high, so they don't interfere unless it's something
  serious. Then, adding a handler without formatting with debug level logging.
  When leaving the context, remove the old handler and restore the log levels.
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
  with open(json_path, 'w') as f:
    f.write(serialize_to_normalized_pretty_json(py_obj))


def load_json(json_path):
  with open(json_path, 'r') as f:
    return json.load(f)


def format_json_to_normalized_pretty_json(json_str):
  return serialize_to_normalized_pretty_json(json.loads(json_str))


def serialize_to_normalized_pretty_json(py_obj):
  return json.dumps(py_obj, sort_keys=True, indent=2, cls=ToJsonCompatibleTypes)


def serialize_to_normalized_compact_json(py_obj):
  return json.dumps(
    py_obj, sort_keys=True, separators=(',', ':'), cls=ToJsonCompatibleTypes
  )


class ToJsonCompatibleTypes(json.JSONEncoder):
  def default(self, o):
    # bytes -> str (assume UTF-8)
    if isinstance(o, bytes):
      return o.decode('utf-8', errors='replace')
    # set -> sorted list
    if isinstance(o, set):
      return sorted([v for v in o])
    # datetime -> ISO 8601 UTC
    if isinstance(o, datetime.datetime):
      return d1_common.date_time.date_utc(o)
    return json.JSONEncoder.default(self, o)


def format_sec_to_dhm(sec):
  """Format seconds to days-hours-minutes str"""
  rem_int, s_int = divmod(int(sec), 60)
  rem_int, m_int, = divmod(rem_int, 60)
  d_int, h_int, = divmod(rem_int, 24)
  return '{}d{:02d}h{:02d}m'.format(d_int, h_int, m_int)
