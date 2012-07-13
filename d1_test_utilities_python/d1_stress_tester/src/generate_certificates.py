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

# App.
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
sys.path.append(_here('./shared/'))
import settings
import subject_dn

# Get an instance of a logger.
logger = logging.getLogger()

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
  subjects.append(settings.SUBJECT_WITH_CREATE_PERMISSIONS)
  subjects.append(settings.SUBJECT_WITH_CN_PERMISSIONS)
  for subject in subjects:
    subject_dn_serialized = subject_dn.get_dataone_compliant_dn_serialization_by_subject(
      subject
    )
    subject_dn_tuple = subject_dn.get_dn_by_subject(subject)
    subject_info = create_subject_info(subject)
    create_certificate(subject, subject_dn_tuple, subject_info)


def get_subject_list():
  with open(settings.SUBJECTS_PATH, 'r') as f:
    return filter(None, f.read().split('\n'))


def create_list_of_random_groups(n_groups):
  return d1_instance_generator.random_data.random_word_unique_list(n_groups)


def create_certificate(subject, subject_dn_tuple, subject_info):
  cert_out_path = os.path.join(
    settings.CLIENT_CERT_DIR, subject_dn.subject_to_filename(subject)
  )
  d1_x509v3_certificate_generator.generate(
    cert_out_path, settings.CA_CERT_PATH, settings.CA_KEY_PATH, settings.CA_KEY_PW,
    settings.CLIENT_CERT_PUBLIC_KEY_PATH, subject_info, settings.SUBJECT_ALT_NAME,
    subject_dn_tuple, 1
  )
  assert (os.path.exists(cert_out_path))


def create_subject_info(subject):
  return subject_info_template.replace(
    '%subject%', subject_dn.get_dataone_compliant_dn_serialization_by_subject(subject)
  )


def log_setup():
  logging.getLogger('').setLevel(logging.INFO)
  formatter = logging.Formatter('%(levelname)-8s %(message)s')
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


if __name__ == '__main__':
  main()
