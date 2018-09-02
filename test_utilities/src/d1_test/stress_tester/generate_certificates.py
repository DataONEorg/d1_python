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
"""Create set of test certificates signed by the local test CA

For use by the stress tester. A certificate is created for each subject in the
subject list and two certificates are created for test subjects with special
permissions.
"""

import codecs
import logging
import optparse
import os
import sys
import xml.sax.saxutils

import d1_x509v3_certificate_generator
import settings
import subject_dn

# Get an instance of a logger.
logger = logging.getLogger()

# The SubjectInfo to include in the certificate.
subject_info_template = (
  """<?xml version="1.0" encoding="utf-8"?>
  <d1:subjectInfo xmlns:d1="http://ns.dataone.org/service/types/v1">
    <person>
      <subject>%subject%</subject>
      <givenName>Test</givenName>
      <familyName>Subject</familyName>
      <email>testsubject@gmail.com</email>
      <verified>true</verified>
    </person>
  </d1:subjectInfo>
  """
)


def main():
  log_setup()

  # Command line opts.
  parser = optparse.OptionParser('usage: %prog [options]')
  parser.add_option(
    '--verbose',
    action='store_true',
  )
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
    subject_dn_tuple = subject_dn.dataone_compliant_dn_serialization_to_dn_tuple(
      subject
    )
    subject_info = create_subject_info(subject)
    create_certificate(subject, subject_dn_tuple, subject_info)
  print((
    'Created {} client side certificates in {}'.format(
      len(subjects), settings.CLIENT_CERT_DIR
    )
  ))


def get_subject_list():
  return codecs.open(settings.SUBJECTS_PATH, 'r', 'utf-8').read().splitlines()


def create_certificate(subject, subject_dn_tuple, subject_info):
  cert_out_path = os.path.join(
    settings.CLIENT_CERT_DIR, subject_dn.subject_to_filename(subject)
  )
  d1_x509v3_certificate_generator.generate(
    cert_out_path, settings.CA_CERT_PATH, settings.CA_KEY_PATH,
    settings.CA_KEY_PW, settings.CLIENT_CERT_PUBLIC_KEY_PATH, subject_info,
    settings.SUBJECT_ALT_NAME, subject_dn_tuple, 1
  )
  assert (os.path.exists(cert_out_path))


def create_subject_info(subject):
  return subject_info_template.replace(
    '%subject%', xml.sax.saxutils.escape(subject)
  )


def log_setup():
  logging.getLogger('').setLevel(logging.INFO)
  formatter = logging.Formatter('%(levelname)-8s %(message)s')
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


if __name__ == '__main__':
  sys.exit(main())
