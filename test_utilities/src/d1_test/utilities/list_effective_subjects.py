#!/usr/bin/env python

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
"""Get active subjects from DataONE X.509 v3 Certificate

Given a DataONE X.509 v3 Certificate, list all subjects, equivalent identities
and groups for which the certificate holder is authenticated.
"""

import logging
import optparse
import sys

import d1_certificate.certificate_extractor

import d1_common.const
import d1_common.date_time
import d1_common.types.dataoneTypes_v1 as dataoneTypes_v1
import d1_common.types.exceptions
import d1_common.url
import d1_common.util


class get_subjects_from_certificate(object):
  def __init__(self):
    pass

  def get(self, cert):
    self.cert = cert
    self.subjects = set()
    self._get_subjects_from_certificate()
    return self.primary_subject, self.subjects

  def _get_subjects_from_certificate(self):
    self._add_symbolic_subject_public()
    self._process_authenticated_session()

  def _add_symbolic_subject_public(self):
    self.subjects.add(d1_common.const.SUBJECT_PUBLIC)

  def _process_authenticated_session(self):
    self.primary_subject, self.subject_info = self._get_session_from_certificate()
    self._add_symbolic_subject_authenticated()
    self._process_subject_info()

  def _add_symbolic_subject_authenticated(self):
    self.subjects.add(d1_common.const.SUBJECT_AUTHENTICATED)

  def _process_subject_info(self):
    if self.subject_info is None:
      return
    self._add_symbolic_subject_verified()
    self._add_subject_info()

  def _add_symbolic_subject_verified(self):
    person = self._find_person_by_subject(self.primary_subject)
    if person.verified:
      self.subjects.add(d1_common.const.SUBJECT_VERIFIED)

  def _add_subject_info(self):
    person = self._find_person_by_subject(self.primary_subject)
    self._add_person_is_member_of(person)
    self._add_equivalent_identities(person)
    for person in self.subject_info.person:
      self.subjects.add(person.subject.value())

  def _find_person_by_subject(self, subject):
    for person in self.subject_info.person:
      if person.subject.value() == subject:
        return person
    print((
      'SubjectInfo does not have any Person records matching Subject: {}'
      .format(person.subject.value())
    ))
    exit()

  def _add_person_is_member_of(self, person):
    for is_member_of in person.isMemberOf:
      self.subjects.add(is_member_of.value())

  def _add_equivalent_identities(self, person):
    for equivalent_identity in person.equivalentIdentity:
      subject = equivalent_identity.value()
      self.subjects.add(subject)
      person = self._find_person_by_subject(subject)
      self._add_person_is_member_of(person)

  def _get_session_from_certificate(self):
    subject, subject_info_xml = self._extract_session_from_x509_v3_certificate()
    if subject_info_xml == '':
      return subject, None
    else:
      return subject, self._deserialize_subject_info(subject_info_xml)

  def _extract_session_from_x509_v3_certificate(self):
    try:
      return d1_certificate.certificate_extractor.extract(self.cert)
    except Exception as e:
      print('Error processing certificate: {}'.format(str(e)))
      exit()

  def _deserialize_subject_info(self, subject_info_xml):
    try:
      return dataoneTypes_v1.CreateFromDocument(subject_info_xml)
    except Exception as e:
      print('Error deserializing SubjectInfo: {}'.format(str(e)))
      exit()


# ==============================================================================


def read_cert_from_file_and_print_subjects(options, cert_pem_path):
  cert = read_certificate_from_file(cert_pem_path)
  primary_subject, subjects = get_subjects_from_certificate().get(cert)
  print_effective_subjects(primary_subject, subjects)


def read_certificate_from_file(cert_pem_path):
  try:
    with open(cert_pem_path) as f:
      return f.read()
  except EnvironmentError as e:
    print('Error reading certificate file: {}'.format(str(e)))


def print_effective_subjects(primary_subject, subjects):
  print('Effective subjects for certificate:')
  print('{} (primary)'.format(primary_subject))
  for subject in sorted(list(subjects)):
    if subject != primary_subject:
      print('{}'.format(subject))


def main():
  parser = optparse.OptionParser()
  parser.add_option('--verbose', action='store_true')

  (options, args) = parser.parse_args()

  if len(args) != 1:
    print(
      'Need a single argument which must be the PEM formatted X.509 v3 '
      'DataONE certificate to examine'
    )
    exit()

  if options.verbose:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  cert_pem_path = args[0]
  read_cert_from_file_and_print_subjects(options, cert_pem_path)


if __name__ == '__main__':
  sys.exit(main())
