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
"""Test JSON Web Token parsing and validation"""

from __future__ import absolute_import

import unittest

import d1_client.mnclient_1_1
import d1_client.mnclient_2_0
import d1_test.mock_api.django_client as mock_django_client
import d1_test.util
import django.test
import gmn.app.middleware.session_jwt
import gmn.tests.gmn_test_case
import mock

BASE_URL = 'http://mock/mn'


@unittest.skip('TODO: Seems like mocking timegm is suddenly not working')
class TestJwt(gmn.tests.gmn_test_case.D1TestCase):
  # @classmethod
  # def setUpClass(cls):
  #   pass # d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    mock_django_client.add_callback(BASE_URL)
    self.client_v1 = d1_client.mnclient_1_1.MemberNodeClient_1_1(BASE_URL)
    self.client_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(BASE_URL)

  @django.test.override_settings(
    STAND_ALONE=False,
    DATAONE_ROOT='https://cn-stage.test.dataone.org/cn',
  )
  def test_0010(self):
    """_get_cn_cert() successfully retrieves CN server cert from cn-stage"""
    cert_obj = gmn.app.middleware.session_jwt._get_cn_cert()
    self.assertIn(
      u'cn-stage.test.dataone.org',
      [v.value for v in cert_obj.subject]
    )

  def _parse_test_token(self):
    jwt_base64 = d1_test.util.read_test_file('test_token_2.base64')
    return gmn.app.middleware.session_jwt._validate_jwt_and_get_subject_list(
      jwt_base64
    )

  @django.test.override_settings(
    STAND_ALONE=False,
    DATAONE_ROOT='https://cn-stage.test.dataone.org/cn',
  )
  def test_0020(self):
    """_validate_jwt_and_get_subject_list() silently returns an empty subject
    list when parsing the token fails to failed validation. The token expired on
    2016-10-06.
    """
    subject_list = self._parse_test_token()
    self.assertListEqual(subject_list, [])

  @django.test.tag("test")
  @django.test.override_settings(
    STAND_ALONE=False,
    DATAONE_ROOT='https://cn-stage.test.dataone.org/cn',
  )
  def test_0030(self):
    """_validate_jwt_and_get_subject_list() successfully returns the expected
    subject list when PyJWS' call to calendar.timegm() is mocked to return a
    time just before the token expired.
    """
    with mock.patch(
        'gmn.app.middleware.session_jwt.jwt.api_jwt.timegm'
    ) as mock_date:
      awt_exp_ts = 1475786896
      mock_date.return_value = awt_exp_ts - 1
      subject_list = self._parse_test_token()
      self.assertListEqual(
        subject_list, [u'CN=Roger Dahl A1779,O=Google,C=US,DC=cilogon,DC=org']
      )
