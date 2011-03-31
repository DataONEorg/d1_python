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
:Author: DataONE (dahl)
:Dependencies:
  - python 2.6

'''
# Stdlib.
import logging

import d1_client.mnclient


class GMNTestClient(d1_client.mnclient.MemberNodeClient):
  def __init__(self, baseurl, defaultHeaders={}, timeout=1000, keyfile=None,
               certfile=None, strictHttps=True):

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
      }
    )

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
    response = self.POST(url, files=files, headers=self._getAuthHeader('<dummy token>'))
    return self.isHttpStatusOK(response.status)
