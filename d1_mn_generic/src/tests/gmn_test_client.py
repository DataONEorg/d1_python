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
REST interfaces on GMN that provide this functionality are prefixed with "test_"
and are only enabled when GMN runs in debug mode.

:Created: 2011-03-18
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6

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
    baseurl,
    defaultHeaders=None,
    timeout=1000,
    keyfile=None,
    certfile=None,
    strictHttps=True
  ):

    d1_client.mnclient.MemberNodeClient.__init__(
      self,
      baseurl,
      defaultHeaders=defaultHeaders,
      timeout=timeout,
      keyfile=keyfile,
      certfile=certfile,
      strictHttps=strictHttps
    )

    self.logger = logging.getLogger('GMNTestClient')

    self.methodmap.update(
      {
        'delete_all_objects': u'test_delete_all_objects',
        'delete_event_log': u'test_delete_event_log',
        'inject_event_log': u'test_inject_event_log',
        'delete_single_object': u'test_delete_single_object/%(pid)s',
        'delete_all_access_rules': u'test_delete_all_access_rules',
        # Concurrency tests.
        'test_concurrency_clear': u'test_concurrency_clear',
        'test_concurrency_read_lock':
          u'test_concurrency_read_lock/%(key)s/%(sleep_before)s/%(sleep_after)s',
        'test_concurrency_write_lock':
          u'test_concurrency_write_lock/%(key)s/%(val)s/%(sleep_before)s/%(sleep_after)s',
        'test_concurrency_get_dictionary_id': u'test_concurrency_get_dictionary_id',
      }
    )

  def delete_all_objects(self, headers=None):
    '''Delete all the objects on an instance of GMN that is running in Debug
    mode.
    '''
    url = self.RESTResourceURL('delete_all_objects')
    response = self.GET(url, headers=headers)
    # TODO: Handle D1 exception.
    return self.isHttpStatusOK(response.status)

  def test_delete_single_object(self, pid, headers=None):
    url = self.RESTResourceURL('delete_single_object', pid=pid)
    try:
      response = self.GET(url, headers=headers)
    except d1_common.types.exceptions.DataONEException:
      return False
    return self.isHttpStatusOK(response.status)

  def delete_event_log(self, headers=None):
    '''Delete event log for all objects.
    '''
    url = self.RESTResourceURL('delete_event_log')
    response = self.GET(url, headers=headers)
    return self.isHttpStatusOK(response.status)

  def inject_event_log(self, event_log_csv, headers=None):
    '''Inject a fake event log.
    '''
    files = [('csv', 'csv', event_log_csv)]
    url = self.RESTResourceURL('inject_event_log')
    response = self.POST(url, files=files, headers=headers)
    return self.isHttpStatusOK(response.status)

  def delete_all_access_rules(self, headers=None):
    '''Delete all access rules.
    '''
    url = self.RESTResourceURL('delete_all_access_rules')
    response = self.GET(url, headers=headers)
    return self.isHttpStatusOK(response.status)

  # ----------------------------------------------------------------------------
  # Concurrency.
  # ----------------------------------------------------------------------------

  def test_concurrency_clear(self, headers=None):
    '''Clear test key/vals.
    '''
    url = self.RESTResourceURL('test_concurrency_clear')
    return self.GET(url, headers=headers)

  def test_concurrency_read_lock(self, key, sleep_before, sleep_after, headers=None):
    '''Test PID read locking.
    '''
    url = self.RESTResourceURL(
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
    url = self.RESTResourceURL(
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
    url = self.RESTResourceURL('test_concurrency_get_dictionary_id')
    return self.GET(url, headers=headers)
