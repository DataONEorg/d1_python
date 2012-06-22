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
''':mod:`generate_certificates_for_create`
==========================================

:Synopsis: Create set of test certificates signed by the local test CA, for
use by the stress tester for MNStorage.create().
:Author: DataONE (Dahl)
'''
# Stdlib.
import logging
import optparse
import os
import re
import sys
import unittest

# D1.
import d1_x509v3_certificate_generator
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_instance_generator.subject
import d1_instance_generator.random_data

# Get an instance of a logger.
logger = logging.getLogger()

# Config.
ca_key_path = './projects/_shared/certificates/local_test_ca.nopassword.key'
ca_cert_path = './projects/_shared/certificates/local_test_ca.crt'
cert_out_dir = './projects/_shared/certificates/certificates'

# Only required if the password has not been removed from the CA private key.
ca_key_pw = ''

public_key_path = './projects/_shared/certificates/local_test_client_cert.public.key'

subject_alt_name = 'DNS:dataone.org'

subjects_path = './projects/_shared/subjects.txt'

# A DN is created by inserting a randomly generated string in the CN field
# in this tuple. It is typically not necessary to change the other fields
# from their defaults.
dn = (
  ('CN', ''),
  ('O', 'd1-stress-tester'),
  ('C', 'US'),
  ('DC', 'd1-stress-tester'),
  ('DC', 'com'),
)

# The SubjectInfo to include in the certificate.
subject_info_template = \
'''<?xml version="1.0" encoding="UTF-8"?>
<d1:subjectInfo xmlns:d1="http://ns.dataone.org/service/types/v1">
  <person>
    <subject>%subject%</subject>
    <givenName>Test</givenName>
    <familyName>Subject</familyName>
    <email>testsubject@gmail.com</email>
    <verified>true</verified>
  </person>
</d1:subjectInfo>
'''


def main():
  log_setup()

  # Command line opts.
  parser = optparse.OptionParser('usage: %prog [options]')
  parser.add_option('--verbose', dest='verbose', action='store_true', default=False)
  (options, arguments) = parser.parse_args()

  if len(arguments) != 0:
    logging.error('No arguments are required')
    exit()

  create_certificates()


def create_certificates():
  subjects = get_subject_list()
  for subject in subjects:
    subject_dn = insert_subject_in_dn(subject)
    subject_dn_d1_serialization = dn_dataone_compliant_serialization(subject_dn)
    subject_info = create_subject_info(subject_dn_d1_serialization)
    create_certificate(subject, subject_dn, subject_info)


def get_subject_list():
  with open(subjects_path, 'r') as f:
    return filter(None, f.read().split('\n'))


def create_list_of_random_groups(n_groups):
  return d1_instance_generator.random_data.random_word_unique_list(n_groups)


def create_certificate(subject, subject_dn, subject_info):
  '''Test PEM formatted X.509 v3 certificate generation'''
  cert_out_path = os.path.join(cert_out_dir, subject_to_filename(subject))
  d1_x509v3_certificate_generator.generate(
    cert_out_path, ca_cert_path, ca_key_path, ca_key_pw, public_key_path, subject_info,
    subject_alt_name, subject_dn, 0
  )
  assert (os.path.exists(cert_out_path))


def insert_subject_in_dn(subject):
  return (('CN', subject), ) + dn[1:]


def create_subject_info(subject_dn):
  return subject_info_template.replace('%subject%', subject_dn)


def dn_dataone_compliant_serialization(subject_dn):
  return ','.join(map('='.join, subject_dn))


def subject_to_filename(subject):
  return re.sub('\W', '_', subject)


def log_setup():
  logging.getLogger('').setLevel(logging.INFO)
  formatter = logging.Formatter('%(levelname)-8s %(message)s')
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


if __name__ == '__main__':
  main()
