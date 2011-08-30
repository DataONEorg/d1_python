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
'''
:mod:`tier_2_mn_auth_set_access_policy`
=======================================

:Created: 2011-08-09
:Author: DataONE (dahl)
:Dependencies:
  - python 2.6
'''

# Std.
import datetime
import os
import random
import sys
import StringIO
import threading
import time
import urllib
import uuid
import xml.sax.saxutils

# 3rd party.
import iso8601

# D1.
import d1_common.const
import d1_common.types.exceptions

# App.

# Path to modules shared between projects.
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
shared_path = _here('../../../projects/_shared/')
sys.path.append(shared_path)

import settings
import test_client
import test_utilities
import d1_test_case
import generate_random_sysmeta
import select_random_subject


class Transaction(object):
  '''listObjects, random subject, unfiltered, randomly distributed.
  '''

  def __init__(self, python_profile=False, sql_profile=False):
    self.python_profile = python_profile
    self.sql_profile = sql_profile

  def list_objects(self):
    # Select random subject to use in transaction.
    #subject = select_random_subject.select_random_subject()
    subject = 'santa=purposefully=3775'
    # Connect.
    client = test_client.TestClient(settings.BASEURL, subject)
    # Get page count.
    object_list = client.rest_call(client.listObjectsResponse, start=0, count=0)
    # Get number of pages. The last page will probably not be PAGESIZE long.
    print object_list.read()
    exit()
    self.n_pages, self.last_page_size = divmod(object_list.total, settings.PAGESIZE)
    if self.last_page_size:
      self.n_pages += 1
    #response = client.listObjectsResponse(
    #  start=page_idx*settings.PAGESIZE, count=settings.PAGESIZE,
    #  vendorSpecific=vendor_specific)
    #assert (response.status == 200), 'Exception returned by listObjectsResponse'
    #if self.profile:
    #  print response.read()
    #
    #
    #
    ## Connect to MN.
    #if settings.USE_CERTS:
    #  # When using certificates, the subject is passed in via a client side
    #  # certificate when creating the connection.
    #  subject_quoted = urllib.quote(subject)
    #  cert_path = os.path.join(shared_path, '{0}.crt'.format(subject_quoted))
    #  key_path = os.path.join(shared_path, '{0}.key'.format(subject_quoted))
    #  client = test_client.TestClient(settings.BASEURL,
    #                                  certfile=cert_path, keyfile=key_path)
    #else:
    #  # When not using certificates, the subject is passed in via a vendor
    #  # specific extension that is supported by all the REST calls in GMN.
    #  client = test_client.TestClient(settings.BASEURL)
    ## Select random page to retrieve.
    #page_idx = random.randint(0, self.n_pages)
    ## Enable profiling if requested.
    #if self.profile:
    #  vendor_specific = test_utilities.gmn_vse_enable_sql_profiling()
    #else:
    #  vendor_specific = {}
    ## If not using certificates, pass subject in via vendor specific extension.
    #if not settings.USE_CERTS:
    #response = client.listObjectsResponse(
    #  start=page_idx*settings.PAGESIZE, count=settings.PAGESIZE,
    #  vendorSpecific=vendor_specific)
    #assert (response.status == 200), 'Exception returned by listObjectsResponse'
    #if self.profile:
    #  print response.read()

  def run(self):
    self.list_objects()


if __name__ == '__main__':
  trans = Transaction(python_profile=False, sql_profile=False)
  trans.run()
