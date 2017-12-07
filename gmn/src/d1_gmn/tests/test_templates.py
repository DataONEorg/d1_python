#!/usr/bin/env python
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
"""Basic tests for the template based pages
"""

from __future__ import absolute_import

import freezegun
import responses

import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_test_client

import d1_test.mock_api.get_system_metadata

import django
import django.conf
import django.core.management
import django.test


@d1_test.d1_test_case.reproducible_random_decorator('TestTemplates')
@freezegun.freeze_time('1961-11-22')
class TestTemplates(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self):
    """home: Returns expected HTML document and status 200"""
    response = django.test.Client().get('/home')
    assert response.status_code == 200
    self.sample.assert_equals(response.content, 'home_html_doc')
