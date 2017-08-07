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

from __future__ import absolute_import

import datetime
import json
import logging
import os
import random
import StringIO
import sys
import tempfile
import traceback

import pytest
import requests

import d1_gmn.app
import d1_gmn.app.models
import d1_gmn.app.revision
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_client

import d1_common.checksum
import d1_common.types
import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.util
import d1_common.xml

import d1_test.d1_test_case
import d1_test.instance_generator.access_policy
import d1_test.instance_generator.identifier
import d1_test.instance_generator.random_data
import d1_test.instance_generator.sciobj
import d1_test.mock_api.create
import d1_test.mock_api.django_client
import d1_test.mock_api.get

import d1_client.mnclient
import d1_client.mnclient_1_1
import d1_client.mnclient_2_0
import d1_client.session

from django.db import connection

HTTPBIN_SERVER_STR = 'http://httpbin.org'
ENABLE_SQL_PROFILING = False


class GMNTestCase(
    d1_test.d1_test_case.D1TestCase,
):
  def setup_class(self):
    if ENABLE_SQL_PROFILING:
      connection.queries = []

  def teardown_class(self):
    GMNTestCase.capture_exception()
    if ENABLE_SQL_PROFILING:
      logging.debug('SQL queries by all methods:')
      map(logging.debug, connection.queries)

  def setup_method(self, method):
    d1_test.mock_api.django_client.add_callback(
      d1_test.d1_test_case.MOCK_BASE_URL
    )
    d1_test.mock_api.get.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
    self.client_v1 = d1_client.mnclient_1_1.MemberNodeClient_1_1(
      d1_test.d1_test_case.MOCK_BASE_URL
    )
    self.client_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      d1_test.d1_test_case.MOCK_BASE_URL
    )
    self.test_client = d1_gmn.tests.gmn_test_client.GMNTestClient(
      d1_test.d1_test_case.MOCK_BASE_URL
    )
    self.v1 = d1_common.types.dataoneTypes_v1_1
    self.v2 = d1_common.types.dataoneTypes_v2_0
    # Remove limit on max diff to show. This can cause debug output to
    # explode...
    self.maxDiff = None

  @property
  def mock(self):
    return d1_gmn.tests.gmn_mock

  @classmethod
  def capture_exception(cls):
    """If GMN responds with something that cannot be parsed by d1_client as
    a valid response for the particular call, d1_client raises a DataONE
    ServiceFailure exception with the response stored in the traceInformation
    member. The Django diagnostics page triggers this behavior, so, in order to
    access the diagnostics page, we check for unhandled DataONEExceptions here
    and write any provided traceInformation to temporary storage,
    typically /tmp.

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
    logging.exception('Test failed with exception:')
    if not isinstance(exc_value, d1_common.types.exceptions.DataONEException):
      return
    func_name_str = GMNTestCase.get_test_func_name()
    file_path = os.path.join(
      tempfile.gettempdir(), u'gmn_test_failed_{}.txt'.format(func_name_str)
    )
    # Dump the entire exception
    with open(file_path, 'w') as f:
      f.write(str(exc_value))
    logging.error('Wrote exception to file. path="{}"'.format(file_path))
    # Dump any HTML (typically from the Django diags page)
    if exc_value.traceInformation:
      ss = StringIO.StringIO()
      is_in_html = False
      for line_str in exc_value.traceInformation.splitlines():
        if '<!DOCTYPE' in line_str or '<html' in line_str:
          is_in_html = True
        if is_in_html:
          ss.write(line_str)
      if is_in_html:
        file_path = os.path.join(tempfile.gettempdir(), u'gmn_test_failed.html')
        with open(file_path, 'w') as f:
          f.write(str(ss.getvalue()))
        logging.error(
          'Wrote HTML from exception to file. path="{}"'.format(file_path)
        )

  @staticmethod
  def get_test_func_name():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    for stack_trace in traceback.extract_tb(exc_traceback):
      module_path = stack_trace[0]
      func_name = stack_trace[2]
      if func_name.startswith('test_'):
        return u'{}_{}'.format(os.path.split(module_path)[1][:-3], func_name)
    return u'<not a test>'

  # def disable_server_cert_validation(self):
  #   requests.packages.urllib3.disable_warnings()
  #   d1_client.session.DEFAULT_VERIFY_TLS = False

  #
  # assert
  #

  def assert_sysmeta_pid_and_sid(self, sysmeta_pyxb, pid, sid):
    self.assert_sysmeta_pid(sysmeta_pyxb, pid)
    self.assert_sysmeta_sid(sysmeta_pyxb, sid)

  def assert_sysmeta_pid(self, sysmeta_pyxb, pid):
    assert self.get_pyxb_value(sysmeta_pyxb, 'identifier') == pid

  def assert_sysmeta_sid(self, sysmeta_pyxb, sid):
    assert self.get_pyxb_value(sysmeta_pyxb, 'seriesId') == sid

  def assert_eq_sysmeta_sid(self, sysmeta_a_pyxb, sysmeta_b_pyxb):
    assert self.get_pyxb_value(sysmeta_a_pyxb, 'seriesId') == \
      self.get_pyxb_value(sysmeta_b_pyxb, 'seriesId')

  def assert_slice(self, slice_pyxb, start, count, total):
    """Check that slice matches the expected slice and that actual number of
    objects matches the slice count
    """
    assert slice_pyxb.start == start
    assert slice_pyxb.count == count
    assert slice_pyxb.total == total
    if hasattr(slice_pyxb, 'objectInfo'):
      assert len(slice_pyxb.objectInfo) == count
    elif hasattr(slice_pyxb, 'logEntry'):
      assert len(slice_pyxb.logEntry) == count

  def assert_required_response_headers_present(self, response):
    assert 'last-modified' in response.headers
    assert 'content-length' in response.headers
    assert 'content-type' in response.headers

  def assert_valid_date(self, date_str):
    assert datetime.datetime(*map(int, date_str.split('-')))

  def assert_sci_obj_size_matches_sysmeta(self, sciobj_str, sysmeta_pyxb):
    assert sysmeta_pyxb.size == len(sciobj_str)

  def assert_sci_obj_checksum_matches_sysmeta(self, sciobj_str, sysmeta_pyxb):
    checksum_pyxb = d1_common.checksum.create_checksum_object_from_string(
      sciobj_str, sysmeta_pyxb.checksum.algorithm
    )
    assert d1_common.checksum.are_checksums_equal(
      checksum_pyxb, sysmeta_pyxb.checksum
    )

  def assert_checksums_equal(self, a_pyxb, b_pyxb):
    assert d1_common.checksum.are_checksums_equal(a_pyxb, b_pyxb)

  def assert_valid_chain(self, client, pid_chain_list, sid):
    logging.debug('Chain: {}'.format(' - '.join(pid_chain_list)))
    pad_pid_chain_list = [None] + pid_chain_list + [None]
    i = 0
    for prev_pid, cur_pid, next_pid in zip(
        pad_pid_chain_list, pad_pid_chain_list[1:], pad_pid_chain_list[2:]
    ):
      logging.debug(
        'Link {}: {} <- {} -> {}'.format(i, prev_pid, cur_pid, next_pid)
      )
      obj_str, sysmeta_pyxb = self.get_obj(client, cur_pid)
      assert self.get_pyxb_value(sysmeta_pyxb, 'obsoletes') == prev_pid
      assert self.get_pyxb_value(sysmeta_pyxb, 'identifier') == cur_pid
      assert self.get_pyxb_value(sysmeta_pyxb, 'obsoletedBy') == next_pid
      assert self.get_pyxb_value(sysmeta_pyxb, 'seriesId') == sid
      i += 1

  #
  # CRUD
  #

  def create_revision_chain(self, client, chain_len, sid=None, *args, **kwargs):
    """Create a revision chain with a total of {chain_len} objects. If
    client is v2, can assign a SID to the chain. Return the SID (None for v1)
    and a list of the PIDs in the chain. The first PID in the list is the
    tail and the last is the head.
    """

    def did(idx, is_sid=False):
      return '#{:03d}_{}'.format(
        idx,
        d1_test.instance_generator.identifier.generate_sid()
        if is_sid else d1_test.instance_generator.identifier.generate_pid()
      )

    base_pid, sid, sciobj_str, sysmeta_pyxb = (
      self.create_obj(
        client, pid=did(0), sid=did(0, True) if sid else None, *args, **kwargs
      )
    )
    pid_chain_list = [base_pid]
    for i in range(1, chain_len):
      update_pid = did(i)
      base_pid, sid, sciobj_str, sysmeta_pyxb = (
        self.update_obj(
          client, old_pid=base_pid, new_pid=update_pid, sid=sid, *args, **kwargs
        )
      )
      pid_chain_list.append(update_pid)
      base_pid = update_pid
    return sid, pid_chain_list

  def convert_to_replica(self, pid):
    """Convert a local sciobj to a simulated replica by adding a LocalReplica
    model to it
    """
    replica_info_model = d1_gmn.app.models.replica_info(
      'completed', 'urn:node:testReplicaSource'
    )
    d1_gmn.app.models.local_replica(pid, replica_info_model)

  def call_d1_client(self, api_func, *arg_list, **arg_dict):
    """Issue d1_client calls under a mocked GMN authentication and authorization
    subsystem

    Mock GMN authn and authz so calls are detected as having been made with
    a specific set of active and trusted subjects. Then call GMN through
    d1_client, which itself is typically mocked to issue calls through the
    Django test client.

    By default, disable_auth=True, which disables GMN authn and authz
    altogether, making it irrelevant which active and trusted subjects are used.
    To get GMN to control access based on the provided active and trusted
    subjects, set disable_auth=False.

    Args:
      Optional args: active_subj_list, trusted_subj_list, disable_auth
      All other args are sent to the api function
    """
    # TODO: Handling the args manually like this was necessary to get the
    # signature I wanted, but it may be done better with
    # functools.partial(func[,*args][, **keywords]).
    active_subj_list = arg_dict.pop('active_subj_list', True)
    trusted_subj_list = arg_dict.pop('trusted_subj_list', True)
    disable_auth = arg_dict.pop('disable_auth', True)

    with d1_gmn.tests.gmn_mock.set_auth_context(
      ['active_subj_1', 'active_subj_2', 'active_subj_3']
        if active_subj_list is True else active_subj_list,
      ['trusted_subj_1', 'trusted_subj_2']
        if trusted_subj_list is True else trusted_subj_list,
        disable_auth,
    ):
      try:
        return api_func(*arg_list, **arg_dict)
      except requests.exceptions.ConnectionError as e:
        pytest.fail(
          'Check that the test function is decorated with '
          '"@responses.activate". error="{}"'.format(str(e))
        )
        # coercing to Unicode: need string or buffer, NoneType found:
        # Check that authentication has been disabled

  def create_obj(
      self, client, pid=True, sid=None, submitter=True, rights_holder=True,
      permission_list=True, active_subj_list=True, trusted_subj_list=True,
      disable_auth=True, vendor_dict=None, now_dt=True
  ):
    """Generate a test object and call MNStorage.create()
    Parameters:
      True: Use a default or generated value
      Other: Use the supplied value
    """
    pid, sid, sciobj_str, sysmeta_pyxb = self.generate_sciobj_with_defaults(
      client, pid, sid, submitter, rights_holder, permission_list, now_dt
    )
    with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
      self.call_d1_client(
        client.create, pid,
        StringIO.StringIO(sciobj_str), sysmeta_pyxb, vendor_dict,
        active_subj_list=active_subj_list, trusted_subj_list=trusted_subj_list,
        disable_auth=disable_auth
      )
    assert self.get_pyxb_value(sysmeta_pyxb, 'identifier') == pid
    return pid, sid, sciobj_str, sysmeta_pyxb

  def update_obj(
      self, client, old_pid, new_pid=True, sid=None, submitter=True,
      rights_holder=True, permission_list=True, active_subj_list=True,
      trusted_subj_list=True, disable_auth=True, vendor_dict=None, now_dt=True
  ):
    """Generate a test object and call MNStorage.update()
    Parameters:
      True: Use a default or generate a value
      Other: Use the supplied value
    """
    pid, sid, sciobj_str, sysmeta_pyxb = self.generate_sciobj_with_defaults(
      client, new_pid, sid, submitter, rights_holder, permission_list, now_dt
    )
    with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
      self.call_d1_client(
        client.update, old_pid,
        StringIO.StringIO(sciobj_str), pid, sysmeta_pyxb, vendor_dict,
        active_subj_list=active_subj_list, trusted_subj_list=trusted_subj_list,
        disable_auth=disable_auth
      )
    assert self.get_pyxb_value(sysmeta_pyxb, 'identifier') == pid
    return pid, sid, sciobj_str, sysmeta_pyxb

  def get_obj(
      self, client, did, active_subj_list=True, trusted_subj_list=True,
      disable_auth=True, vendor_dict=None
  ):
    sciobj_str = self.call_d1_client(
      client.get, did, vendor_dict, active_subj_list=active_subj_list,
      trusted_subj_list=trusted_subj_list, disable_auth=disable_auth
    ).content
    sysmeta_pyxb = self.call_d1_client(
      client.getSystemMetadata, did, vendor_dict,
      active_subj_list=active_subj_list, trusted_subj_list=trusted_subj_list,
      disable_auth=disable_auth
    )
    self.assert_sci_obj_size_matches_sysmeta(sciobj_str, sysmeta_pyxb)
    self.assert_sci_obj_checksum_matches_sysmeta(sciobj_str, sysmeta_pyxb)
    return sciobj_str, sysmeta_pyxb

  def generate_sciobj_with_defaults(
      self, client, pid=True, sid=None, submitter=True, rights_holder=True,
      permission_list=True, now_dt=True
  ):
    permission_list = (
      d1_test.d1_test_case.DEFAULT_PERMISSION_LIST
      if permission_list is True else permission_list
    )
    sid = d1_test.instance_generator.identifier.generate_sid() if sid is True else sid
    option_dict = {
      k: v
      for (k, v) in (('identifier', pid),
                     ('seriesId', sid),
                     ('submitter', submitter),
                     ('rightsHolder', rights_holder), (
                       'accessPolicy', d1_test.instance_generator.access_policy.
                       generate_from_permission_list(client, permission_list)
                     ),
                     ('dateUploaded', now_dt),
                     ('dateSysMetadataModified', now_dt),) if v is not True
    }
    pid, sid, sciobj_str, sysmeta_pyxb = \
      d1_test.instance_generator.sciobj.generate_reproducible(
        client, None if pid is True else pid, option_dict
      )
    return pid, sid, sciobj_str, sysmeta_pyxb

  #
  # Misc
  #

  def object_list_to_pid_list(self, object_list_pyxb):
    return sorted([v.identifier.value() for v in object_list_pyxb.objectInfo])

  def log_to_pid_list(self, log_record_list_pyxb):
    return sorted([v.identifier.value() for v in log_record_list_pyxb.logEntry])

  def vendor_proxy_mode(self, object_stream_url):
    return {'VENDOR-GMN-REMOTE-URL': object_stream_url}

  def dump_permissions(self):
    logging.debug('Permissions:')
    for s in d1_gmn.app.models.Permission.objects.order_by(
        'subject__subject', 'level', 'sciobj__pid__did'
    ):
      logging.debug(s.sciobj.pid.did)
      logging.debug(s.subject)
      logging.debug(s.level)
      logging.debug('')

  def dump_subjects(self):
    logging.debug('Subjects:')
    for s in d1_gmn.app.models.Subject.objects.order_by('subject'):
      logging.debug('  {}'.format(s.subject))

  def get_pid_list(self):
    """Get list of all PIDs in the DB fixture"""
    return json.loads(self.sample.load('db_fixture_pid.json', 'rb'))

  def get_sid_list(self):
    """Get list of all SIDs in the DB fixture"""
    return json.loads(self.sample.load('db_fixture_sid.json', 'rb'))

  def get_sid_with_min_chain_length(self, min_len=2):
    """Get list of all SIDs in the DB fixture"""
    sid_list = self.get_sid_list()
    random.shuffle(sid_list)
    for sid in sid_list:
      pid_list = d1_gmn.app.revision.get_all_pid_by_sid(sid)
      print pid_list
      if len(pid_list) >= min_len:
        return sid

  def get_total_log_records(self, client, **filters):
    return client.getLogRecords(start=0, count=0, **filters).total

  def get_total_objects(self, client, **filters):
    return client.listObjects(start=0, count=0, **filters).total

  def get_random_pid_sample(self, n_pids):
    # We select sample from ordered list since the prng seed may be locked for reproducability.
    return random.sample(
      [
        v.pid.did
        for v in d1_gmn.app.models.ScienceObject.objects.order_by('pid__did')
      ],
      n_pids,
    )
