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

import logging

import freezegun
import pytest

import d1_common.cert.jwt
import d1_common.cert.x509
import d1_common.util

import d1_test.d1_test_case

TOKEN_FILE_NAME_LIST = [
  'jwt_token_20161004_092911.base64',
  'jwt_token_20161004_112502.base64',
  'jwt_token_20161005_204816.base64',
  'jwt_token_20170612_232523.base64',
  'jwt_token_20170613_125652.base64',
  'jwt_token_20170613_163157.base64',
]

CERT_FILE_NAME_LIST = [
  'cert_cn_dataone_org_20170517_122900.pem',
  'cert_cn_stage_test_dataone_org_20170522_155700.pem',
  'cert_cn_ucsb_1_dataone_org_20120604_191249.pem',
  'cert_cn_ucsb_1_dataone_org_20150709_180838.pem',
]

# The only cert/JWT combinations that successfully validate the JWT signature:
# cert_cn_dataone_org_20170517_122900.pem - jwt_token_20170612_232523.base64
# cert_cn_dataone_org_20170517_122900.pem - jwt_token_20170613_163157.base64
# cert_cn_stage_test_dataone_org_20170522_155700.pem - jwt_token_20170613_125652.base64


class TestJwt(d1_test.d1_test_case.D1TestCase):
  def load_sample_cert_jwt_pair(self, cert_file_name, jwt_file_name):
    cert_pem = self.sample.load(cert_file_name)
    cert_obj = d1_common.cert.x509.deserialize_pem(cert_pem)
    # d1_common.cert.x509.log_cert_info(logging.info, 'CERT', cert_obj)
    jwt_bu64 = self.sample.load(jwt_file_name)
    # d1_common.cert.jwt.log_jwt_bu64_info(logging.info, 'JWT', jwt_bu64)
    return cert_obj, jwt_bu64

  @freezegun.freeze_time('2030-01-01')
  def test_1000(self):
    """validate_and_decode(): Validation fails after JWT has expired"""
    cert_obj, jwt_bu64 = self.load_sample_cert_jwt_pair(
      'cert_cn_dataone_org_20170517_122900.pem',
      'jwt_token_20170612_232523.base64',
    )
    with pytest.raises(d1_common.cert.jwt.JwtException, match='expired'):
      d1_common.cert.jwt.validate_and_decode(jwt_bu64, cert_obj)

  @freezegun.freeze_time('2011-01-01')
  def test_1010(self):
    """validate_and_decode(): Validation succeeds before JWT has expired"""
    cert_obj, jwt_bu64 = self.load_sample_cert_jwt_pair(
      'cert_cn_dataone_org_20170517_122900.pem',
      'jwt_token_20170612_232523.base64',
    )
    d1_common.cert.jwt.validate_and_decode(jwt_bu64, cert_obj)

  @freezegun.freeze_time('2011-01-01')
  def test_1020(self):
    """validate_and_decode(): Decoded token matches expected"""
    cert_obj, jwt_bu64 = self.load_sample_cert_jwt_pair(
      'cert_cn_dataone_org_20170517_122900.pem',
      'jwt_token_20170612_232523.base64',
    )
    jwt_dict = d1_common.cert.jwt.validate_and_decode(jwt_bu64, cert_obj)
    self.sample.assert_equals(
      jwt_dict,
      'validate_and_decode_ok',
    )

  @freezegun.freeze_time('2011-01-01')
  def test_1030(self):
    """validate_and_decode(): Validation fails when signed with
    other cert"""
    cert_obj, jwt_bu64 = self.load_sample_cert_jwt_pair(
      'cert_cn_ucsb_1_dataone_org_20120604_191249.pem',
      'jwt_token_20170612_232523.base64',
    )
    with pytest.raises(d1_common.cert.jwt.JwtException):
      d1_common.cert.jwt.validate_and_decode(jwt_bu64, cert_obj)

  @freezegun.freeze_time('2011-01-01')
  def test_1040(self):
    """get_subject_with_local_validation(): After successful validation, returns
    subject from JWT"""
    cert_obj, jwt_bu64 = self.load_sample_cert_jwt_pair(
      'cert_cn_dataone_org_20170517_122900.pem',
      'jwt_token_20170612_232523.base64',
    )
    assert d1_common.cert.jwt.get_subject_with_local_validation(
      jwt_bu64, cert_obj
    ) == 'http://orcid.org/0000-0001-8849-7530'

  @freezegun.freeze_time('2011-01-01')
  def test_1050(self):
    """get_subject_with_remote_validation(): Receive expected call to
    getpeercert()"""
    cert_obj, jwt_bu64 = self.load_sample_cert_jwt_pair(
      'cert_cn_ucsb_1_dataone_org_20120604_191249.pem',
      'jwt_token_20170612_232523.base64',
    )
    with self.mock_ssl_download(cert_obj) as (mock_connect, mock_getpeercert):
      d1_common.cert.jwt.get_subject_with_remote_validation(
        jwt_bu64, 'https://bogus/node/'
      )
      mock_connect.assert_called_with(('bogus', 443))

  @freezegun.freeze_time('2011-01-01')
  def test_1060(self):
    """get_subject_with_file_validation(): After successful validation, returns
    subject from JWT"""
    cert_path = self.sample.get_path('cert_cn_dataone_org_20170517_122900.pem')
    jwt_bu64 = self.sample.load('jwt_token_20170612_232523.base64')
    assert d1_common.cert.jwt.get_subject_with_file_validation(
      jwt_bu64, cert_path
    ) == 'http://orcid.org/0000-0001-8849-7530'

  @freezegun.freeze_time('2020-01-01')
  def test_1070(self):
    """get_subject_with_file_validation(): Fails with expired token
    """
    cert_path = self.sample.get_path('cert_cn_dataone_org_20170517_122900.pem')
    jwt_bu64 = self.sample.load('jwt_token_20170612_232523.base64')
    assert d1_common.cert.jwt.get_subject_with_file_validation(
      jwt_bu64, cert_path
    ) is None

  @freezegun.freeze_time('2021-01-01')
  def test_1080(self, caplog):
    """log_jwt_bu64_info(): Outputs expected log"""
    jwt_bu64 = self.sample.load('jwt_token_20170612_232523.base64')
    with caplog.at_level(logging.INFO):
      d1_test.d1_test_case.clear_caplog(caplog)
      d1_common.cert.jwt.log_jwt_bu64_info(logging.info, "test msg", jwt_bu64)
    self.sample.assert_equals(
      d1_test.d1_test_case.get_caplog_text(caplog),
      'jwt_token_log_jwt_bu64_info_expected'
    )
