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
'''Module test_client
=====================

This module implements MemberNodeTestClient, which extends
d1_client.mnclient.MemberNodeClient with test functionality.

:Created: 2011-03-18
:Author: DataONE (dahl)
:Dependencies:
  - python 2.6

'''
# Stdlib.
import logging
import os
import urllib

# D1.
import d1_client.mnclient

# App.
import settings
import test_utilities

_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
test_subject_certs = _here('test_subject_certs')


class TestClient(d1_client.mnclient.MemberNodeClient):
  def __init__(self, baseurl, subject, defaultHeaders={}, timeout=1000, strictHttps=True):
    # When using certificates, the subject is passed in via a client side
    # certificate when creating the connection.
    if settings.USE_CERTS:
      cert_path = self._get_cert_path(subject, 'crt')
      key_path = self._get_cert_path(subject, 'key')
    else:
      cert_path = None
      key_path = None
    # Init d1_libclient and connect to MN.
    d1_client.mnclient.MemberNodeClient.__init__(
      self,
      baseurl,
      defaultHeaders=defaultHeaders,
      timeout=timeout,
      keyfile=key_path,
      certfile=cert_path,
      strictHttps=strictHttps
    )
    self.subject = subject
    self.logger = logging.getLogger('MemberNodeTestClient')
    self.methodmap.update(
      {
        'delete_all_objects': u'test_delete_all_objects',
        'delete_event_log': u'test_delete_event_log',
        'inject_event_log': u'test_inject_event_log',
      }
    )

  def _get_cert_path(self, subject, ext):
    subject_quoted = urllib.quote(subject)
    return os.path.abspath(
      os.path.join(
        os.path.dirname(__file__), test_subject_certs, '{0}.{1}'.format(subject_quoted,
                                                                        ext)
      )
    )

  def rest_call(self, func, python_profile=False, sql_profile=False, *args, **kwargs):
    '''Wrap a rest call up with automatic handling of vendor specific extensions
    for profiling and select subject.'''
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

  def delete_all_objects(self):
    '''Delete all the objects on an instance of GMN that is running in Debug
    mode.
    '''
    url = self.RESTResourceURL('delete_all_objects')
    response = self.GET(url)
    return self.isHttpStatusOK(response.status)

  def delete_event_log(self):
    '''Delete event log for all objects on an instance of GMN that is running
    in Debug mode.
    '''
    url = self.RESTResourceURL('delete_event_log')
    response = self.GET(url)
    return self.isHttpStatusOK(response.status)

  def inject_event_log(self, event_log_csv):
    '''Inject a fake event log for testing.
    '''
    files = [('csv', 'csv', event_log_csv)]
    url = self.RESTResourceURL('inject_event_log')
    response = self.POST(url, files=files, headers=self._getAuthHeader(context.TOKEN))
    return self.isHttpStatusOK(response.status)
