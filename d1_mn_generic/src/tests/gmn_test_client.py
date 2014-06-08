#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
    version='diag'
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

    self.logger = logging.getLogger(__name__)

  def gmn_vse_provide_subject(self, subject):
    '''GMN Vendor Specific Extension: Simulate subject.'''
    return {'VENDOR_INCLUDE_SUBJECTS': subject}

  def gmn_vse_enable_sql_profiling(self):
    '''GMN Vendor Specific Extension: Enable SQL profiling.'''
    return {'VENDOR_PROFILE_SQL': 1}

  def gmn_vse_enable_python_profiling(self):
    '''GMN Vendor Specific Extension: Enable Python profiling.'''
    return {'VENDOR_PROFILE_PYTHON': 1}

  def get_resource_path(self, path):
    '''Get path to test resources.'''
    resource_path = os.path.abspath(
      os.path.join(
        os.path.dirname(
          __file__
        ), '../../../../resources/'
      )
    )
    return os.path.join(resource_path, path)

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
    url = self._rest_url('set_access_policy/%(pid)s', pid=pid)
    files = [('access_policy', 'access_policy', access_policy.toxml().encode('utf-8')), ]
    return self.POST(url, files=files, headers=headers)

  def delete_all_access_policies(self, headers=None):
    url = self._rest_url('delete_all_access_policies')
    response = self.GET(url, headers=headers)
    return self._read_boolean_response(response)

  # ----------------------------------------------------------------------------
  # Authentication.
  # ----------------------------------------------------------------------------

  def echo_session(self, headers=None):
    url = self._rest_url('echo_session')
    response = self.GET(url, headers=headers)
    return response.read()

  # ----------------------------------------------------------------------------
  # Misc.
  # ----------------------------------------------------------------------------

  def create(self, pid, obj, sysmeta, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('create/%(pid)s', pid=pid)
    mime_multipart_fields = [('pid', pid.encode('utf-8')), ]
    mime_multipart_files = [
      ('object', 'content.bin', obj),
      ('sysmeta', 'sysmeta.xml', sysmeta.toxml().encode('utf-8')),
    ]
    response = self.POST(
      url,
      fields=mime_multipart_fields,
      files=mime_multipart_files,
      headers=vendorSpecific
    )
    return self._read_boolean_response(response)

  def slash(self, arg1, arg2, arg3, headers=None):
    url = self._rest_url(
      'slash/%(arg1)s/%(arg2)s/%(arg3)s',
      arg1=arg1, arg2=arg2,
      arg3=arg3
    )
    response = self.GET(url, headers=headers)
    return response.read()

  def exception(self, exception_type):
    url = self._rest_url('exception/%(exception_type)s', exception_type=exception_type)
    response = self.GET(url, headers=headers)
    return response.read()

  def echo_request_object(self, headers=None):
    url = self._rest_url('echo_request_object')
    response = self.GET(url, headers=headers)
    return response.read()

  def echo_raw_post_data(self, headers=None):
    url = self._rest_url('echo_raw_post_data')
    response = self.GET(url, headers=headers)
    return response.read()

  def delete_all_objects(self, headers=None):
    url = self._rest_url('delete_all_objects')
    response = self.GET(url, headers=headers)
    return self._read_boolean_response(response)

  def test_delete_single_object(self, pid, headers=None):
    url = self._rest_url('delete_single_object/%(pid)s', pid=pid)
    response = self.GET(url, headers=headers)
    return self._read_boolean_response(response)

  def get_setting(self, setting, headers=None):
    url = self._rest_url('get_setting/%(setting)s', setting=setting)
    response = self.GET(url, headers=headers)
    return response.read()

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

  def concurrency_clear(self, headers=None):
    '''Clear test key/vals.
    '''
    url = self._rest_url('concurrency_clear')
    return self.GET(url, headers=headers)

  def concurrency_read_lock(self, key, sleep_before, sleep_after, headers=None):
    '''Test PID read locking.
    '''
    url = self._rest_url(
      'concurrency_read_lock/%(key)s/%(sleep_before)s/%(sleep_after)s',
      key=key,
      sleep_before=sleep_before,
      sleep_after=sleep_after
    )
    return self.GET(url, headers=headers)

  def concurrency_write_lock(self, key, val, sleep_before, sleep_after, headers=None):
    '''Test PID write locking.
    '''
    url = self._rest_url(
      'concurrency_write_lock/%(key)s/%(val)s/%(sleep_before)s/%(sleep_after)s',
      key=key,
      val=val,
      sleep_before=sleep_before,
      sleep_after=sleep_after
    )
    return self.GET(url, headers=headers)

  def concurrency_get_dictionary_id(self, headers=None):
    '''Get dictionary ID.
    '''
    url = self._rest_url('concurrency_get_dictionary_id')
    return self.GET(url, headers=headers)

# ==============================================================================


def rest_call(self, func, python_profile=False, sql_profile=False, *args, **kwargs):
  '''Wrap a rest call up with automatic handling of vendor specific extensions
  for profiling and selecting subject.'''
  vendor_specific = {}
  # When not using certificates, the subject is passed in via a vendor
  # specific extension that is supported by all the REST calls in GMN.
  if not settings.USE_CERTS:
    vendor_specific.update(test_utilities.gmn_vse_provide_subject(self.subject))
  # Enable python profiling if requested.
  if python_profile:
    vendor_specific.update(test_utilities.gmn_vse_enable_python_profiling())
  if sql_profile:
    vendor_specific.update(test_utilities.gmn_vse_enable_sql_profiling())
  return func(vendorSpecific=vendor_specific, *args, **kwargs)
