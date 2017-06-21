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
import codecs
import contextlib
import json
import logging
import os
import re
import subprocess
import tempfile
import traceback

import pytest

import d1_common
import d1_common.types
import d1_common.types.dataoneTypes
import d1_common.util
import d1_common.xml

import d1_client.util


def assert_equals(
    got_obj, name_postfix_str, client=None, extension_str='sample'
):
  filename = _format_file_name(client, name_postfix_str, extension_str)
  logging.info('Using sample file. filename="{}"'.format(filename))
  got_str = _obj_to_pretty_str(got_obj)
  exp_path = _get_or_create_path(filename)
  diff_str = _get_sxs_diff(got_str, exp_path)
  if diff_str is None:
    return

  logging.error(
    '\n{0} Sample mismatch. GOT <-> EXPECTED {0}\n{1}'.
    format('#' * 10, diff_str)
  )

  if pytest.config.getoption('--update-samples'):

    _save_interactive(got_str, exp_path)
  else:
    raise AssertionError('Sample mismatch. filename="{}"'.format(filename))


def get_path(filename):
  tidy_file_path = os.path.join(
    d1_common.util.abs_path('test_docs_tidy'), filename
  )
  path = os.path.join(d1_common.util.abs_path('test_docs'), filename)
  if os.path.isfile(path):
    return path
  elif os.path.isfile(tidy_file_path):
    os.rename(tidy_file_path, path)
    return path
  return path


def load(filename, mode_str='rb'):
  with open(_get_or_create_path(filename), mode_str) as f:
    return f.read()


def load_utf8_to_unicode(filename):
  utf8_path = _get_or_create_path(filename)
  unicode_file = codecs.open(utf8_path, encoding='utf-8', mode='r')
  return unicode_file.read()


def load_xml_to_pyxb(filename, mode_str='r'):
  logging.debug('Reading sample XML file. filename="{}"'.format(filename))
  xml_str = load(filename, mode_str)
  return d1_common.types.dataoneTypes.CreateFromDocument(xml_str)


def save(filename, got_str, mode_str='wb'):
  logging.info('Writing sample file. filename="{}"'.format(filename))
  with open(_get_or_create_path(filename), mode_str) as f:
    return f.write(got_str)


def save_path(got_str, exp_path, mode_str='wb'):
  logging.info(
    'Writing sample file. filename="{}"'.format(os.path.split(exp_path)[1])
  )
  with open(exp_path, mode_str) as f:
    return f.write(got_str)


def _get_or_create_path(filename):
  """Get the path to a sample file

  Also provides a mechanism for cleaning out unused sample files. To clean, move
  all files from `test_docs` to `test_docs_tidy`, and run the tests. Any files
  that are used by the tests will be moved back to `test_docs`. Files that
  remain in `test_docs_tidy` can be untracked and deleted.

  This procedure moves files while pytest is running, which may confuse pytest.
  Fix by clearing out pytest's cache with clean-tree.py.
  """
  path = get_path(filename)
  if not os.path.isfile(path):
    with open(path, 'w') as f:
      f.write('<new sample file>\n')
  return path


def _format_file_name(client, name_postfix_str, extension_str):
  section_list = [
    _get_test_module_name(),
    name_postfix_str,
  ]
  if client:
    section_list.extend([
      d1_client.util.get_client_type(client),
      d1_client.util.get_version_tag_by_d1_client(client),
    ])
  return '{}.{}'.format('_'.join(section_list), extension_str)


def _get_test_module_name():
  for module_path, line_num, func_name, line_str in traceback.extract_stack():
    module_name = os.path.splitext(os.path.split(module_path)[1])[0]
    if module_name.startswith('test_') and func_name.startswith('test_'):
      return module_name


def _get_sxs_diff_str(got_str, exp_str):
  with tempfile.NamedTemporaryFile(suffix='__EXPECTED') as exp_f:
    exp_f.write(exp_str)
    exp_f.seek(0)
    return _get_sxs_diff(got_str, exp_f.name)


def _get_sxs_diff(got_str, exp_path):
  """Return a minimal formatted side by side diff if there are any
  none-whitespace changes, else None.
  """
  try:
    sdiff_proc = subprocess.Popen([
      'sdiff', '--ignore-blank-lines', '--ignore-all-space', '--minimal',
      '--width=160', '--tabsize=2', exp_path, '-'
    ], bufsize=-1, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    out_str, err_str = sdiff_proc.communicate(got_str)
  except OSError as e:
    raise AssertionError(
      'Unable to run sdiff. Is it installed? error="{}"'.format(str(e))
    )
  else:
    if not sdiff_proc.returncode:
      return
    if sdiff_proc.returncode == 1:
      return out_str
    else:
      raise AssertionError(
        'sdiff returned error code. code={} error="{}"'.
        format(sdiff_proc.returncode, err_str)
      )


def _display_diff_pyxb(got_pyxb, exp_pyxb):
  return _display_diff_str(
    d1_common.xml.pretty_pyxb(got_pyxb),
    d1_common.xml.pretty_pyxb(exp_pyxb),
  )


def _display_diff_xml(got_xml, exp_xml):
  return _display_diff_str(
    d1_common.xml.pretty_xml(got_xml),
    d1_common.xml.pretty_xml(exp_xml),
  )


def _display_diff_str(got_str, exp_path):
  with open(exp_path, 'rb') as exp_f:
    exp_str = exp_f.read()
  with _tmp_file_pair(got_str, exp_str) as (got_f, exp_f):
    subprocess.call(['kdiff3', got_f.name, exp_f.name])


def _save_interactive(got_str, exp_path):
  _display_diff_str(got_str, exp_path)
  answer_str = None
  while answer_str not in ('y', 'n', ''):
    answer_str = raw_input(
      'Update sample file "{}"? [Y/n] '.format(os.path.split(exp_path)[1])
    ).lower()
  if answer_str in ('y', ''):
    save_path(got_str, exp_path)


# noinspection PyUnreachableCode
def _obj_to_pretty_str(o):
  logging.debug('Serializing object. type="{}"'.format(type(o)))
  if isinstance(o, unicode):
    o = o.encode('utf-8')
  with ignore_exceptions():
    return d1_common.xml.pretty_xml(o)
  with ignore_exceptions():
    return d1_common.xml.pretty_pyxb(o)
  with ignore_exceptions():
    return '\n'.join(sorted(o.serialize(doc_format='nt').splitlines()))
  with ignore_exceptions():
    if 'digraph' in o:
      return '\n'.join(sorted(str(re.sub(r'node\d+', 'nodeX', o)).splitlines()))
  with ignore_exceptions():
    if '\n' in str(o):
      return str(o)
  with ignore_exceptions():
    return json.dumps(o, sort_keys=True, indent=2)
  with ignore_exceptions():
    return str(o)
  return repr(o)


@contextlib.contextmanager
def ignore_exceptions(*exception_list):
  exception_list = exception_list or (Exception,)
  try:
    yield
  except exception_list:
    pass


@contextlib.contextmanager
def _tmp_file_pair(got_str, exp_str):
  with tempfile.NamedTemporaryFile(suffix='__RECEIVED') as got_f:
    with tempfile.NamedTemporaryFile(suffix='__EXPECTED') as exp_f:
      got_f.write(got_str)
      exp_f.write(exp_str)
      got_f.seek(0)
      exp_f.seek(0)
      yield got_f, exp_f


class SampleException(Exception):
  pass
