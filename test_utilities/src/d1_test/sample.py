# -*- coding: utf-8 -*-

import bz2
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
import requests.structures

import d1_common
import d1_common.types
import d1_common.types.dataoneTypes
import d1_common.util
import d1_common.xml

import d1_client.util

import django


def start_tidy():
  """Call at start of test run to tidy the samples directory.

  Pytest will run regular session scope fixtures in parallel with test
  collection, while this function must complete before collection starts. The
  best place to call it from appears to be ./conftest.pytest_sessionstart().
  """
  logging.info('Moving files to tidy dir')
  sample_dir_path = os.path.join(d1_common.util.abs_path('test_docs'))
  tidy_dir_path = os.path.join(d1_common.util.abs_path('test_docs_tidy'))
  d1_common.util.ensure_dir_exists(sample_dir_path)
  d1_common.util.ensure_dir_exists(tidy_dir_path)
  i = 0
  for i, item_name in enumerate(os.listdir(sample_dir_path)):
    sample_path = os.path.join(sample_dir_path, item_name)
    tidy_path = os.path.join(tidy_dir_path, item_name)
    if os.path.exists(tidy_path):
      os.unlink(tidy_path)
    os.rename(sample_path, tidy_path)
  logging.info('Moved {} files'.format(i))


def assert_equals(
    got_obj, name_postfix_str, client=None, extension_str='sample'
):
  filename = _format_file_name(client, name_postfix_str, extension_str)
  logging.info('Using sample file. filename="{}"'.format(filename))
  exp_path = _get_or_create_path(filename)
  got_str = obj_to_pretty_str(got_obj)

  if pytest.config.getoption('--sample-review'):
    _review_interactive(got_str, exp_path)
    return

  diff_str = _get_sxs_diff_file(got_str, exp_path)

  if diff_str is None:
    return

  if pytest.config.getoption('--sample-write'):
    save(got_str, filename)
    return

  if pytest.config.getoption('--sample-ask'):
    _save_interactive(got_str, exp_path)
    return

  raise AssertionError(
    '\nSample file: {0}\n{1} Sample mismatch. GOT <-> EXPECTED {1}\n{2}'.
    format(filename, '-' * 10, diff_str)
  )


def assert_no_diff(a_obj, b_obj):
  a_str = obj_to_pretty_str(a_obj)
  b_str = obj_to_pretty_str(b_obj)
  diff_str = _get_sxs_diff_str(a_str, b_str)
  if diff_str is None:
    return
  err_msg = '\n{0} Diff mismatch. A <-> B {0}\n{1}'.format('-' * 10, diff_str)
  if pytest.config.getoption('--sample-ask'):
    logging.error(err_msg)
    _diff_interactive(a_str, b_str)
  else:
    raise AssertionError(err_msg)


def get_path(filename):
  path = os.path.join(d1_common.util.abs_path('test_docs'), filename)
  if os.path.isfile(path):
    return path
  tidy_file_path = os.path.join(
    d1_common.util.abs_path('test_docs_tidy'), filename
  )
  if os.path.isfile(tidy_file_path):
    os.rename(tidy_file_path, path)
    logging.info('Moved from tidy: {} -> {}'.format(tidy_file_path, path))
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


def save(got_str, filename, mode_str='wb'):
  logging.info('Writing sample file. filename="{}"'.format(filename))
  with open(_get_or_create_path(filename), mode_str) as f:
    return f.write(got_str)


def save_obj(got_obj, filename, mode_str='wb'):
  got_str = obj_to_pretty_str(got_obj)
  save(got_str, filename, mode_str)


def save_path(got_str, exp_path, mode_str='wb'):
  logging.info(
    'Writing sample file. filename="{}"'.format(os.path.split(exp_path)[1])
  )
  with open(exp_path, mode_str) as f:
    return f.write(got_str)


def get_sxs_diff(a_obj, b_obj):
  return _get_sxs_diff_str(
    obj_to_pretty_str(a_obj),
    obj_to_pretty_str(b_obj),
  )


def gui_sxs_diff(a_obj, b_obj):
  return _gui_diff_str_str(
    obj_to_pretty_str(a_obj),
    obj_to_pretty_str(b_obj),
  )


def obj_to_pretty_str(o):
  # noinspection PyUnreachableCode
  def serialize(o):
    logging.debug('Serializing object. type="{}"'.format(type(o)))
    if isinstance(o, unicode):
      o = o.encode('utf-8')
    if isinstance(o, requests.structures.CaseInsensitiveDict):
      with ignore_exceptions():
        o = dict(o)
    with ignore_exceptions():
      return d1_common.xml.pretty_xml(o)
    with ignore_exceptions():
      return d1_common.xml.pretty_pyxb(o)
    with ignore_exceptions():
      return '\n'.join(sorted(o.serialize(doc_format='nt').splitlines()))
    with ignore_exceptions():
      if 'digraph' in o:
        return '\n'.join(
          sorted(str(re.sub(r'node\d+', 'nodeX', o)).splitlines())
        )
    with ignore_exceptions():
      if '\n' in str(o):
        return str(o)
    with ignore_exceptions():
      return json.dumps(o, sort_keys=True, indent=2, cls=SetToList)
    with ignore_exceptions():
      return str(o)
    return repr(o)

  return clobber_uncontrolled_volatiles(serialize(o)).rstrip() + '\n'


def clobber_uncontrolled_volatiles(o_str):
  """Some volatile values in results are not controlled by freezing the time
  and PRNG seed. We replace those with a fixed string here.
  """
  # requests-toolbelt is using another prng for mmp docs
  o_str = re.sub(r'(?<=boundary=)[0-9a-fA-F]+', '[volatile]', o_str)
  # entryId is based on a db sequence type
  o_str = re.sub(r'(?<=<entryId>)\d+', '[volatile]', o_str)
  # TODO: This shouldn't be needed...
  o_str = re.sub(r'(?<=Content-Type:).*', '[volatile]', o_str)
  return o_str


def _get_or_create_path(filename):
  """Get the path to a sample file and enable cleaning out unused sample files.
  See the test docs for usage.
  """
  path = get_path(filename)
  logging.info('Sample path: {}'.format(path))
  if not os.path.isfile(path):
    logging.info('Write new blank file: {}'.format(path))
    with open(path, 'w') as f:
      f.write('<new sample file>\n')
  return path


def _format_file_name(client, name_postfix_str, extension_str):
  section_list = [
    get_test_module_name(),
    name_postfix_str,
  ]
  if client:
    section_list.extend([
      d1_client.util.get_client_type(client),
      d1_client.util.get_version_tag_by_d1_client(client),
    ])
  return '{}.{}'.format('_'.join(section_list), extension_str)


def get_test_module_name():
  for module_path, line_num, func_name, line_str in traceback.extract_stack():
    module_name = os.path.splitext(os.path.split(module_path)[1])[0]
    if module_name.startswith('test_') and func_name.startswith('test_'):
      return module_name


def _get_sxs_diff_str(got_str, exp_str):
  with tempfile.NamedTemporaryFile(suffix='__EXPECTED') as exp_f:
    exp_f.write(exp_str)
    exp_f.seek(0)
    return _get_sxs_diff_file(got_str, exp_f.name)


def _get_sxs_diff_file(got_str, exp_path):
  """Return a minimal formatted side by side diff if there are any
  none-whitespace changes, else None.
  """
  try:
    sdiff_proc = subprocess.Popen(
      [
        'sdiff', '--ignore-blank-lines', '--ignore-all-space', '--minimal',
        '--width=130', '--tabsize=2', '--strip-trailing-cr', '--expand-tabs',
        '--text', '-', exp_path
        # '--suppress-common-lines'
      ],
      bufsize=-1,
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
    )
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


def _gui_diff_str_path(got_str, exp_path):
  with open(exp_path, 'rb') as exp_f:
    exp_str = exp_f.read()
  with _tmp_file_pair(got_str, exp_str) as (got_f, exp_f):
    subprocess.call(['kdiff3', got_f.name, exp_f.name])


def _gui_diff_str_str(a_str, b_str, a_name='received', b_name='expected'):
  with _tmp_file_pair(a_str, b_str, a_name, b_name) as (a_f, b_f):
    subprocess.call(['kdiff3', a_f.name, b_f.name])


def _save_interactive(got_str, exp_path):
  _gui_diff_str_path(got_str, exp_path)
  answer_str = None
  while answer_str not in ('', 'n', 'f'):
    answer_str = raw_input(
      'Update sample file "{}"? Yes/No/Fail [Enter/n/f] '.
      format(os.path.split(exp_path)[1])
    ).lower()
  if answer_str == '':
    save_path(got_str, exp_path)
  elif answer_str == 'f':
    raise AssertionError('Failure triggered interactively')


def _diff_interactive(a_str, b_str):
  _gui_diff_str_str(a_str, b_str, 'a' * 10, 'b' * 10)
  answer_str = None
  while answer_str not in ('', 'n'):
    answer_str = raw_input('Fail? Yes/No [Enter/n] ').lower()
  if answer_str == '':
    raise AssertionError('Failure triggered interactively')


def _review_interactive(got_str, exp_path):
  _gui_diff_str_path(got_str, exp_path)
  answer_str = None
  while answer_str not in ('', 'n', 'f'):
    answer_str = raw_input(
      'Update sample file "{}"? Yes/No/Fail [Enter/n/f] '.
      format(os.path.split(exp_path)[1])
    ).lower()
  if answer_str == '':
    save_path(got_str, exp_path)
  elif answer_str == 'f':
    raise AssertionError('Failure triggered interactively')


@contextlib.contextmanager
def ignore_exceptions(*exception_list):
  exception_list = exception_list or (Exception,)
  try:
    yield
  except exception_list:
    pass


@contextlib.contextmanager
def _tmp_file_pair(got_str, exp_str, a_name='a', b_name='b'):
  with tempfile.NamedTemporaryFile(suffix='__{}'.format(a_name.upper())
                                   ) as got_f:
    with tempfile.NamedTemporaryFile(suffix='__{}'.format(b_name.upper())
                                     ) as exp_f:
      got_f.write(got_str)
      exp_f.write(exp_str)
      got_f.seek(0)
      exp_f.seek(0)
      yield got_f, exp_f


def save_compressed_db_fixture(filename):
  fixture_file_path = get_path(filename)
  logging.info('Writing fixture sample. path="{}"'.format(fixture_file_path))
  with bz2.BZ2File(
      fixture_file_path, 'w', buffering=1024, compresslevel=9
  ) as bz2_file:
    django.core.management.call_command('dumpdata', stdout=bz2_file)


# ==============================================================================


class SampleException(Exception):
  pass


# ==============================================================================


class SetToList(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, set):
      return sorted(list(obj))
    return json.JSONEncoder.default(self, obj)
