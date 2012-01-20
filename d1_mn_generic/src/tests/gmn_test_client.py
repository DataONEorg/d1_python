#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''Module d1_mn_generic.tests.gmn_test_client
=============================================

This module implements GMNTestClient, which extends
d1_client.mnclient.MemberNodeClient with GMN specific test functionality. The
REST interfaces on GMN that provide this functionality are prefixed with
"/test/" and are only enabled when GMN runs in debug mode. The interfaces are
not versioned, and so there is no version tag (such as "v1") in the URL for
these methods.

:Created: 2011-03-18
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging

import d1_client.mnclient
import d1_common.types.exceptions

# Constants.
GMN_TEST_SUBJECT_PUBLIC = 'public'
GMN_TEST_SUBJECT_TRUSTED = 'gmn_test_subject_trusted'


class GMNTestClient(d1_client.mnclient.MemberNodeClient):
  def __init__(
    self,
    base_url,
    timeout=d1_common.const.RESPONSE_TIMEOUT,
    defaultHeaders=None,
    cert_path=None,
    key_path=None,
    strict=True,
    capture_response_body=False,
    version='test'
  ):

    d1_client.mnclient.MemberNodeClient.__init__(
      self,
      base_url=base_url,
      timeout=timeout,
      defaultHeaders=defaultHeaders,
      cert_path=cert_path,
      key_path=key_path,
      strict=strict,
      capture_response_body=capture_response_body,
      version=version
    )

    self.logger = logging.getLogger('GMNTestClient')

    self.methodmap.update(
      {
        # Replication.
        'get_replication_queue': u'get_replication_queue',
        'clear_replication_queue': u'clear_replication_queue',
        # Access Policy.
        'set_access_policy': u'set_access_policy/%(pid)s',
        'delete_all_access_policies': u'delete_all_access_policies',
        # Misc.
        'slash': u'slash/%(arg1)s/%(arg2)s/%(arg3)s',
        'exception': u'exception/%(exception_type)s',
        'echo_request_object': u'echo_request_object',
        'clear_database': u'clear_database',
        'delete_all_objects': u'delete_all_objects',
        'delete_single_object': u'delete_single_object/%(pid)s',
        # Event Log.
        'delete_event_log': u'delete_event_log',
        'inject_fictional_event_log': u'inject_fictional_event_log',
        # Concurrency.
        'test_concurrency_clear': u'concurrency_clear',
        'test_concurrency_read_lock':
          u'concurrency_read_lock/%(key)s/%(sleep_before)s/%(sleep_after)s',
        'test_concurrency_write_lock':
          u'concurrency_write_lock/%(key)s/%(val)s/%(sleep_before)s/%(sleep_after)s',
        'test_concurrency_get_dictionary_id': u'concurrency_get_dictionary_id',
        'error': u'error',
        'system_metadata_changed': u'dirtySystemMetadata',
      }
    )

  # ----------------------------------------------------------------------------
  # Replication.
  # ----------------------------------------------------------------------------

  def get_replication_queue(self, headers=None):
    url = self._rest_url('get_replication_queue')
    response = self.GET(url, headers=headers)
    return response.read()

  def clear_replication_queue(self, headers=None):
    url = self._rest_url('clear_replication_queue')
    response = self.GET(url, headers=headers)
    return self._read_boolean_response(response)

  # ----------------------------------------------------------------------------
  # Access Policy.
  # ----------------------------------------------------------------------------

  def set_access_policy(self, pid, access_policy, headers=None):
    url = self._rest_url('set_access_policy', pid=pid)
    files = [('access_policy', 'access_policy', access_policy.toxml().encode('utf-8')), ]
    return self.POST(url, files=files, headers=headers)

  def delete_all_access_policies(self, headers=None):
    url = self._rest_url('delete_all_access_policies')
    response = self.GET(url, headers=headers)
    return self._read_boolean_response(response)

  # ----------------------------------------------------------------------------
  # Misc.
  # ----------------------------------------------------------------------------

  def slash(self, arg1, arg2, arg3, headers=None):
    url = self._rest_url('slash', arg1=arg1, arg2=arg2, arg3=arg3)
    response = self.GET(url, headers=headers)
    return response.read()

  def exception(self, exception_type):
    url = self._rest_url('exception', exception_type=exception_type)
    response = self.GET(url, headers=headers)
    return response.read()

  def echo_request_object(self, headers=None):
    url = self._rest_url('echo_request_object')
    response = self.GET(url, headers=headers)
    return response.read()

  def clear_database(self, headers=None):
    url = self._rest_url('clear_database')
    response = self.GET(url, headers=headers)
    return self._read_boolean_response(response)

  def delete_all_objects(self, headers=None):
    url = self._rest_url('delete_all_objects')
    response = self.GET(url, headers=headers)
    return self._read_boolean_response(response)

  def test_delete_single_object(self, pid, headers=None):
    url = self._rest_url('delete_single_object', pid=pid)
    response = self.GET(url, headers=headers)
    return self._read_boolean_response(response)

  # ----------------------------------------------------------------------------
  # Event Log.
  # ----------------------------------------------------------------------------

  def delete_event_log(self, headers=None):
    '''Delete event log for all objects.
    '''
    url = self._rest_url('delete_event_log')
    response = self.GET(url, headers=headers)
    return self._read_boolean_response(response)

  def inject_fictional_event_log(self, event_log_csv, headers=None):
    '''Inject a fake event log.
    '''
    files = [('csv', 'csv', event_log_csv)]
    url = self._rest_url('inject_fictional_event_log')
    response = self.POST(url, files=files, headers=headers)
    return self._read_boolean_response(response)

  # ----------------------------------------------------------------------------
  # Concurrency.
  # ----------------------------------------------------------------------------

  def test_concurrency_clear(self, headers=None):
    '''Clear test key/vals.
    '''
    url = self._rest_url('test_concurrency_clear')
    return self.GET(url, headers=headers)

  def test_concurrency_read_lock(self, key, sleep_before, sleep_after, headers=None):
    '''Test PID read locking.
    '''
    url = self._rest_url(
      'test_concurrency_read_lock',
      key=key,
      sleep_before=sleep_before,
      sleep_after=sleep_after
    )
    return self.GET(url, headers=headers)

  def test_concurrency_write_lock(
    self, key, val, sleep_before, sleep_after,
    headers=None
  ):
    '''Test PID write locking.
    '''
    url = self._rest_url(
      'test_concurrency_write_lock',
      key=key,
      val=val,
      sleep_before=sleep_before,
      sleep_after=sleep_after
    )
    return self.GET(url, headers=headers)

  def test_concurrency_get_dictionary_id(self, headers=None):
    '''Get dictionary ID.
    '''
    url = self._rest_url('test_concurrency_get_dictionary_id')
    return self.GET(url, headers=headers)
