#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2014 DataONE
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
:mod:test_x509v3_certificate_generator`
=======================================

:platform:
  Linux
:Synopsis:
  Unit tests for DataONE X.509 v3 Certificate Generator.
:Author:
  DataONE (Dahl)
'''

# Stdlib.
import os
import re
import sys
import unittest

# D1.
import d1_x509v3_certificate_generator
import d1_common.types.generated.dataoneTypes as dataoneTypes

# ca_test.key passphrase is .

cert_out_path = './test_files/new_cert.pem'

ca_path = './test_files/ca_test.crt'
ca_key_path = './test_files/ca_test.key'
ca_key_pw = 'ca_test'

private_key_path = './test_files/new_cert_private_key.pem'
public_key_path = './test_files/new_cert_public_key.pem'

subject_info_path = './test_files/subject_info.xml'
subject_alt_name = 'DNS:dataone.org'

dn = (
  ('CN', 'Test Name'),
  ('O', 'testdomain'),
  ('C', 'US'),
  ('DC', 'test'),
  ('DC', 'com'),
)


class TestX509v3Generator(unittest.TestCase):
  def test_010(self):
    '''Test PEM formatted X.509 v3 certificate generation'''
    subject_info = open(subject_info_path).read()
    d1_x509v3_certificate_generator.generate(
      cert_out_path, ca_path, ca_key_path, ca_key_pw, public_key_path, subject_info,
      subject_alt_name, dn, 0
    )
    self.assertTrue(os.path.exists(cert_out_path))

  def test_020(self):
    '''Verify that new certificate contains expected information'''
    try:
      import d1_x509v3_certificate_extractor
    except ImportError:
      return
    cert = open(cert_out_path, 'rb').read()
    subject_info_correct = open(subject_info_path, 'rb').read()
    subject_extracted, subject_info_extracted = d1_x509v3_certificate_extractor.extract(
      cert
    )
    self.assertEqual(subject_extracted, 'DC=com,DC=test,C=US,O=testdomain,CN=Test Name')
    self.assertEqual(subject_info_correct, subject_info_extracted)

#===============================================================================

if __name__ == "__main__":
  argv = sys.argv
  if "--debug" in argv:
    logging.basicConfig(level=logging.DEBUG)
    argv.remove("--debug")
  if "--with-xunit" in argv:
    argv.remove("--with-xunit")
    unittest.main(argv=argv, testRunner=xmlrunner.XmlTestRunner(sys.stdout))
  else:
    unittest.main(argv=argv)
