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
"""Test JSON Web Token parsing and validation
"""

import freezegun

import d1_gmn.app.middleware.session_jwt
import d1_gmn.tests.gmn_test_case

import d1_common.cert.jwt
import d1_common.cert.x509
import d1_common.util

import django.core.cache


class TestSessionJwt(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def load_sample_cert_jwt_pair(self, cert_file_name, jwt_file_name):
    cert_pem = self.sample.load(cert_file_name)
    cert_obj = d1_common.cert.x509.deserialize_pem(cert_pem)
    # d1_common.cert.x509.log_cert_info(logging.info, 'CERT', cert_obj)
    jwt_bu64 = self.sample.load_utf8_to_str(jwt_file_name)
    # d1_common.cert.jwt.log_jwt_bu64_info(logging.info, 'JWT', jwt_bu64)
    return cert_obj, jwt_bu64

  @freezegun.freeze_time('2011-02-01')
  def test_1000(self):
    """_download_and_decode_cn_cert(): Successfully retrieves and decodes CN
    server cert"""
    cert_obj, jwt_bu64 = self.load_sample_cert_jwt_pair(
      'cert_cn_ucsb_1_dataone_org_20120604_191249.pem',
      'jwt_token_20170612_232523.base64',
    )
    with self.mock_ssl_download(cert_obj) as (mock_connect, mock_getpeercert):
      cert_obj = d1_gmn.app.middleware.session_jwt._download_and_decode_cn_cert()
      mock_connect.assert_called_with(('mock', 443))
      self.sample.assert_equals(cert_obj.subject, 'download_and_decode')

  @freezegun.freeze_time('2011-02-01')
  def test_1010(self):
    """_get_cn_cert(): Retrieves the cert from the CN on the first download and
    from the cache on the second"""
    cert_obj, jwt_bu64 = self.load_sample_cert_jwt_pair(
      'cert_cn_ucsb_1_dataone_org_20120604_191249.pem',
      'jwt_token_20170612_232523.base64',
    )
    with self.mock_ssl_download(cert_obj) as (mock_connect, mock_getpeercert):
      # Remote read
      cert_obj = d1_gmn.app.middleware.session_jwt._get_cn_cert()
      mock_connect.assert_called_with(('mock', 443))
      self.sample.assert_equals(cert_obj.subject, 'download_and_decode')
      assert len(mock_connect.mock_calls) == 1
      assert len(mock_getpeercert.mock_calls) == 1
      # Cache
      cert_obj = d1_gmn.app.middleware.session_jwt._get_cn_cert()
      mock_connect.assert_called_with(('mock', 443))
      self.sample.assert_equals(cert_obj.subject, 'download_and_decode')
      # Did not call connect() and getpeercert() again
      assert len(mock_connect.mock_calls) == 1
      assert len(mock_getpeercert.mock_calls) == 1
      # Object is in cache
      assert cert_obj == django.core.cache.cache.cn_cert_obj
