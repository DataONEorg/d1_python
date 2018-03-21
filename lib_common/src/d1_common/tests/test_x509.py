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

import cryptography.hazmat.backends.openssl.x509
import freezegun

import d1_common.cert.subject_info
import d1_common.cert.subjects
import d1_common.cert.x509
import d1_common.xml

import d1_test.d1_test_case
import d1_test.sample


class TestCert(d1_test.d1_test_case.D1TestCase):
  cert_simple_subject_info_pem = d1_test.sample.load(
    'cert_with_simple_subject_info.pem'
  )
  cert_no_subject_info_pem = d1_test.sample.load(
    'cert_without_subject_info.pem'
  )

  def test_1000(self):
    """Deserialize PEM to cryptography.Certificate object"""
    cert_obj = d1_common.cert.x509.deserialize_pem(
      self.cert_simple_subject_info_pem
    )
    assert isinstance(
      cert_obj, cryptography.hazmat.backends.openssl.x509._Certificate
    )
    self.sample.assert_equals(cert_obj, 'deserialize_pem_to_crypt_cert')

  def test_1010(self):
    """Extract primary subject from certificate and returns as
    DataONE compliant serialization
    """
    cert_obj = d1_common.cert.x509.deserialize_pem(
      self.cert_simple_subject_info_pem
    )
    primary_str = d1_common.cert.x509.extract_subject_from_dn(cert_obj)
    self.sample.assert_equals(primary_str, 'extract_dn_to_d1_subject')

  def test_1020(self):
    """Extract SubjectInfo from certificate, SubjectInfo present"""
    cert_obj = d1_common.cert.x509.deserialize_pem(
      self.cert_simple_subject_info_pem
    )
    extracted_subject_info_xml = d1_common.cert.x509.extract_subject_info_extension(
      cert_obj
    )
    self.sample.assert_equals(
      extracted_subject_info_xml, 'cert_simple_subject_info'
    )

  def test_1030(self):
    """Extract SubjectInfo from certificate, SubjectInfo missing"""
    cert_obj = d1_common.cert.x509.deserialize_pem(
      self.cert_no_subject_info_pem
    )
    missing_subject_info = d1_common.cert.x509.extract_subject_info_extension(
      cert_obj
    )
    assert missing_subject_info is None

  def test_1040(self):
    """Extract primary and equivalent subjects from certificate, SubjectInfo
    present
    """
    primary_str, equivalent_set = d1_common.cert.subjects.extract_subjects(
      self.cert_simple_subject_info_pem
    )
    self.sample.assert_equals({
      'primary_str': primary_str,
      'equivalent_set': equivalent_set
    }, 'primary_and_equivalent_with_subject_info')

  def test_1050(self):
    """Extract primary and equivalent subjects from certificate, SubjectInfo
    missing
    """
    primary_str, equivalent_set = d1_common.cert.subjects.extract_subjects(
      self.cert_no_subject_info_pem
    )
    self.sample.assert_equals({
      'primary_str': primary_str,
      'equivalent_set': equivalent_set
    }, 'primary_and_equivalent_without_subject_info')

  @freezegun.freeze_time('2021-01-01')
  def test_1060(self, caplog):
    """log_cert_info(): Outputs expected log"""
    cert_obj = d1_common.cert.x509.deserialize_pem(
      self.cert_simple_subject_info_pem
    )
    with caplog.at_level(logging.WARN):
      d1_common.cert.x509.log_cert_info(logging.warn, 'test msg', cert_obj)
    self.sample.assert_equals(
      d1_test.d1_test_case.get_caplog_text(caplog), 'log_cert_info_expected'
    )
