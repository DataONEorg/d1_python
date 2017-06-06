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
import hashlib
import logging
import os
import random
import string
import StringIO
import sys
import tempfile
import traceback

import pytest
import requests

import d1_common.checksum
import d1_common.types
import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.util
import d1_common.xml

import d1_test.d1_test_case
import d1_test.mock_api.create
import d1_test.mock_api.django_client
import d1_test.mock_api.get

import d1_client.mnclient
import d1_client.mnclient_1_1
import d1_client.mnclient_2_0
import d1_client.session

import gmn.app
import gmn.app.models
import gmn.tests.gmn_mock
import gmn.tests.gmn_test_client

DEFAULT_PERMISSION_LIST = [
  (['subj1'], ['read']),
  (['subj2', 'subj3', 'subj4'], ['read', 'write']),
  (['subj5', 'subj6', 'subj7', 'subj8'], ['read', 'changePermission']),
  (['subj9', 'subj10', 'subj11', 'subj12'], ['changePermission']),
]

HTTPBIN_SERVER_STR = 'http://httpbin.org'
GMN_TEST_SUBJECT_PUBLIC = 'public'

d1_common.util.log_setup(True)

# Setting DEBUG=True here is a workaround for pytest-django setting
# settings.DEBUG to False (in pytest_django/plugin.py)
# @django.test.override_settings(DEBUG=True)


@pytest.mark.django_db(transaction=True)
class GMNTestCase(
    # django.test.TransactionTestCase,
    d1_test.d1_test_case.D1TestCase,
):
  # def __init__(self, *args, **kwargs):
  #   super(GMNTestCase, self).__init__(*args, **kwargs)

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
    self.test_client = gmn.tests.gmn_test_client.GMNTestClient(
      d1_test.d1_test_case.MOCK_BASE_URL
    )
    self.v1 = d1_common.types.dataoneTypes_v1_1
    self.v2 = d1_common.types.dataoneTypes_v2_0
    # Remove limit on max diff to show. This can cause debug output to
    # explode...
    self.maxDiff = None

  def tearDown(self):
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
    if isinstance(exc_value, Exception):
      logging.exception('Test failed with exception:')
    if isinstance(exc_value, d1_common.types.exceptions.DataONEException):
      func_name_str = self.get_test_func_name()
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
          file_path = os.path.join(
            tempfile.gettempdir(), u'gmn_test_failed.html'
          )
          with open(file_path, 'w') as f:
            f.write(str(ss.getvalue()))
          logging.error(
            'Wrote HTML from exception to file. path="{}"'.format(file_path)
          )

  def get_test_func_name(self):
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

  def assert_object_list_slice(self, object_list, start, count, total):
    """Check that slice matches the expected slice and that actual number of
    objects matches the slice count
    """
    assert object_list.start == start
    assert object_list.count == count
    assert object_list.total == total
    assert len(object_list.objectInfo) == count

  def assert_log_slice(self, log, start, count, total):
    """Check that slice matches the expected slice and that actual number of
    objects matches the slice count
    """
    assert log.start == start
    assert log.count == count
    assert log.total == total
    # Check that the actual number of log records matches the count
    # provided in the slice.
    assert len(log.logEntry) == count

  def assert_required_response_headers_present(self, response):
    assert 'last-modified' in response.headers
    assert 'content-length' in response.headers
    assert 'content-type' in response.headers

  def assert_valid_date(self, date_str):
    assert datetime.datetime(*map(int, date_str.split('-')))

  def assert_sci_obj_size_matches_sysmeta(self, sciobj_str, sysmeta_pyxb):
    assert sysmeta_pyxb.size == len(sciobj_str)

  def assert_sci_obj_checksum_matches_sysmeta(self, sciobj_str, sysmeta_pyxb):
    assert d1_common.checksum. \
      is_checksum_correct_on_string(sysmeta_pyxb, sciobj_str)

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
    client is v2, assign a SID to the chain. Return the SID (None for v1)
    and a list of the PIDs in the chain. The first PID in the list is the
    tail and the last is the head.
    """

    def did(idx, is_sid=False):
      return '#{:03d}_{}'.format(
        idx, self.random_sid() if is_sid else self.random_pid()
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
    replica_info_model = gmn.app.models.replica_info(
      'completed', 'urn:node:testReplicaSource'
    )
    gmn.app.models.local_replica(pid, replica_info_model)

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

    with gmn.tests.gmn_mock.set_auth_context(
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

  #
  # SysMeta
  #

  def generate_sysmeta(
      self, client, pid, sid=None, sciobj_str=None, submitter=None,
      rights_holder=None, obsoletes=None, obsoleted_by=None,
      permission_list=None, now_dt=None
  ):
    sysmeta_pyxb = client.bindings.systemMetadata()
    sysmeta_pyxb.serialVersion = 1
    sysmeta_pyxb.identifier = pid
    sysmeta_pyxb.seriesId = sid
    sysmeta_pyxb.formatId = 'application/octet-stream'
    sysmeta_pyxb.size = len(sciobj_str)
    sysmeta_pyxb.submitter = submitter
    sysmeta_pyxb.rightsHolder = rights_holder
    sysmeta_pyxb.checksum = d1_common.types.dataoneTypes.checksum(
      hashlib.md5(sciobj_str).hexdigest()
    )
    sysmeta_pyxb.checksum.algorithm = 'MD5'
    sysmeta_pyxb.dateUploaded = now_dt
    sysmeta_pyxb.dateSysMetadataModified = now_dt
    sysmeta_pyxb.originMemberNode = 'urn:node:GMNUnitTestOrigin'
    sysmeta_pyxb.authoritativeMemberNode = 'urn:node:GMNUnitTestAuthoritative'
    sysmeta_pyxb.obsoletes = obsoletes
    sysmeta_pyxb.obsoletedBy = obsoleted_by
    sysmeta_pyxb.accessPolicy = self.generate_access_policy(
      client, permission_list
    )
    sysmeta_pyxb.replicationPolicy = self.create_replication_policy_pyxb(client)
    return sysmeta_pyxb

  def generate_access_policy(self, client, permission_list=None):
    if permission_list is None:
      return None
    elif permission_list == 'default':
      permission_list = DEFAULT_PERMISSION_LIST
    access_policy_pyxb = client.bindings.accessPolicy()
    for subject_list, action_list in permission_list:
      subject_list = gmn.tests.gmn_mock.expand_subjects(subject_list)
      action_list = list(action_list)
      access_rule_pyxb = client.bindings.AccessRule()
      for subject_str in subject_list:
        access_rule_pyxb.subject.append(subject_str)
      for action_str in action_list:
        permission_pyxb = client.bindings.Permission(action_str)
        access_rule_pyxb.permission.append(permission_pyxb)
      access_policy_pyxb.append(access_rule_pyxb)
    return access_policy_pyxb

  def create_replication_policy_pyxb(
      self, client, preferred_node_list=None, blocked_node_list=None,
      is_replication_allowed=True, num_replicas=None
  ):
    """{preferred_node_list} and {preferred_node_list}:
    None: No node list is generated
    A list of strings: A node list is generated using the strings as node URNs
    'random': A short node list is generated from random strings
    """
    preferred_node_list = self.prep_node_list(preferred_node_list, 'preferred')
    blocked_node_list = self.prep_node_list(blocked_node_list, 'blocked')
    rep_pyxb = client.bindings.ReplicationPolicy()
    rep_pyxb.preferredMemberNode = preferred_node_list
    rep_pyxb.blockedMemberNode = blocked_node_list
    rep_pyxb.replicationAllowed = is_replication_allowed
    rep_pyxb.numberReplicas = num_replicas or random.randint(10, 100)
    return rep_pyxb

  def generate_sciobj(
      self, client, pid, sid=None, submitter=None, rights_holder=None,
      obsoletes=None, obsoleted_by=None, permission_list=None, now_dt=None
  ):
    """Generate the object bytes and system metadata for a test object
    """
    sciobj_str = d1_test.d1_test_case.generate_reproducible_sciobj_str(pid)
    sysmeta_pyxb = self.generate_sysmeta(
      client, pid, sid, sciobj_str, submitter or GMN_TEST_SUBJECT_PUBLIC,
      rights_holder or GMN_TEST_SUBJECT_PUBLIC, obsoletes, obsoleted_by,
      permission_list, now_dt
    )
    return sciobj_str, sysmeta_pyxb

  def generate_sciobj_with_defaults(
      self, client, pid=True, sid=None, submitter=True, rights_holder=True,
      permission_list=True, now_dt=True
  ):
    """Generate the object bytes and system metadata for a test object
    Parameters:
      True: Use a default or generate a value
      Other: Use the supplied value
    """
    pid = self.random_pid() if pid is True else pid
    sid = self.random_sid() if sid is True else sid
    sciobj_str, sysmeta_pyxb = self.generate_sciobj(
      client, pid, sid,
      'submitter_subj' if submitter is True else submitter,
      'rights_holder_subj' if rights_holder is True else rights_holder,
      None, None,
      DEFAULT_PERMISSION_LIST if permission_list is True else permission_list,
      datetime.datetime.now() if now_dt is True else now_dt,
    ) # yapf: disable
    return pid, sid, sciobj_str, sysmeta_pyxb

  #
  # Misc
  #

  def now_str(self):
    return datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

  def random_str(self, num_chars=10):
    return ''.join([
      random.choice(string.ascii_lowercase) for _ in range(num_chars)
    ])

  def random_id(self):
    return '{}_{}'.format(self.random_str(), self.now_str())

  def random_pid(self):
    return 'PID_{}'.format(self.random_id())

  def random_sid(self):
    return 'SID_{}'.format(self.random_id())

  def random_tag(self, tag_str):
    return '{}_{}'.format(tag_str, self.random_str())

  def get_pyxb_value(self, inst_pyxb, inst_attr):
    try:
      return unicode(getattr(inst_pyxb, inst_attr).value())
    except (ValueError, AttributeError):
      return None

  def object_list_to_pid_list(self, object_list_pyxb):
    return sorted([v.identifier.value() for v in object_list_pyxb.objectInfo])

  def log_to_pid_list(self, log_record_list_pyxb):
    return sorted([v.identifier.value() for v in log_record_list_pyxb.logEntry])

  def vendor_trusted_subjects(self, active_subj_list):
    return {
      'VENDOR-INCLUDE-SUBJECTS':
        u'\t'.join(self.expand_subjects(active_subj_list))
    }

  def vendor_proxy_mode(self, object_stream_url):
    return {'VENDOR-GMN-REMOTE-URL': object_stream_url}

  def prep_node_list(self, node_list, tag_str, num_nodes=5):
    if node_list is None:
      return None
    elif isinstance(node_list, list):
      return node_list
    elif node_list == 'random':
      return [
        'urn:node:{}'.format(self.random_tag(tag_str))
        for _ in range(num_nodes)
      ]

  def dump_permissions(self):
    logging.debug('Permissions:')
    for s in gmn.app.models.Permission.objects.all():
      logging.debug(s.sciobj.pid.did)
      logging.debug(s.subject)
      logging.debug(s.level)
      logging.debug('')

  def dump_subjects(self):
    logging.debug('Subjects:')
    for s in gmn.app.models.Subject.objects.all():
      logging.debug('  {}'.format(s.subject))

  def dump_pyxb(self, type_pyxb):
    logging.debug('PyXB object:')
    for s in d1_common.xml.pretty_pyxb(type_pyxb).splitlines():
      logging.debug(u'  {}'.format(s))
