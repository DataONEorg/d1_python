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

# Stdlib
import datetime
import os
import sys

# Django
import django.test

# 3rd party
import cryptography
import cryptography.hazmat.backends

# D1
import d1_common.util

# App
import mn.middleware.session_jwt as session_jwt
import util


class TestJwt(django.test.TestCase):
  """Test JSON Web Tokens"""
  def setUp(self):
    pass

  def tearDown(self):
    pass


  @django.test.override_settings(
    STAND_ALONE=False,
    DATAONE_ROOT='https://cn-stage.test.dataone.org/cn',
  )
  def test_100(self):
    """_get_cn_cert()"""
    cert_obj = session_jwt.get_cn_cert()
    self.assertIn(u'*.test.dataone.org', [v.value for v in cert_obj.subject])


  @django.test.override_settings(
    STAND_ALONE=False,
    DATAONE_ROOT='https://cn-stage.test.dataone.org/cn',
  )
  def test_200(self):
    """_decode_and_validate_jwt()"""
    jwt_base64 = util.read_test_file('test_token_2.base64')
    subject_dict = session_jwt._decode_and_validate_jwt(jwt_base64)
    self.assertEqual(
      subject_dict['sub'],
      u'CN=Roger Dahl A1779,O=Google,C=US,DC=cilogon,DC=org'
    )


  @django.test.override_settings(
    STAND_ALONE=False,
    DATAONE_ROOT='https://cn-stage.test.dataone.org/cn',
  )
  def test_300(self):
    """_validate_jwt_and_get_subject_list()"""
    jwt_base64 = util.read_test_file('test_token_2.base64')
    subject_list = session_jwt.validate_jwt_and_get_subject_list(jwt_base64)
    self.assertEqual(
      subject_list,
      [u'CN=Roger Dahl A1779,O=Google,C=US,DC=cilogon,DC=org']
    )

