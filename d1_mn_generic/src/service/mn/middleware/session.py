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
'''
:mod:`session`
==============

:Synopsis: Session handling
:Author: DataONE (Dahl)

The DataONE infrastructure uses X.509 v3 certificates to represent sessions.
A session contains assertions about the identity of the caller. In particular,
the session contains a list of equivalent identities and group memberships
of the caller.

A user can connect without providing a certificate (and so, without providing a
session). This limits the user's access to data that is publicly available.

A user can connect with a certificate that does not contain a list of
equivalent identities and group memberships (no SubjectInfo). This limits the
user's access to data that is publicly available and that is available directly
to that user (as designated in the Subject DN). 

The list of subjects to use for access control is created with the following
algorithm:

1. Start with empty list of subjects
2. Add the symbolic subject, "public"
3. Get the DN from the Subject and serialize it to a standardized string. This string is called Subject below.
4. Add Subject
5. If the connection was not made with a certificate, stop here.
6. Add the symbolic subject, "authenticatedUser"
7. If the certificate does not have a SubjectInfo extension, stop here.
8. Find the Person that has a subject that matches the Subject.
9. If the Person has the verified flag set, add the symbolic subject, "verifiedUser"
10. Iterate over the Person's isMemberOf and add those subjects
11. Iterate over the Person's equivalentIdentity and for each of them:
  - Add its subject
  - Find the corresponding Person
  - Iterate over that Person's isMemberOf and add those subjects
'''

# Stdlib.
import csv
import logging
import os
import StringIO
import sys
import types
import urllib
import inspect
import json

import d1_common.ext.mimeparser

# Django.
from django.http import HttpResponse

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.types.exceptions
import d1_common.util
import d1_common.date_time
import d1_common.url
import d1_common.const

# App.
import settings
import x509_extract_session


class process_session(object):
  def __init__(self, request):
    '''Process the session in the certificate and store the result in the
    request object.
    - The SubjectInfo is stored unprocessed in request.subject_info.
    - The processed SubjectInfo is stored in request.subjects (as a list of
      subjects).
    - The certificate subject DN is stored in request.primary_subject.
    '''
    self.request = request
    self.request.subjects = set()
    self.subjects = self.request.subjects
    self._process_session()
    self.request.primary_subject = self.primary_subject

  def _process_session(self):
    self._add_symbolic_subject_public()
    if self._is_certificate_provided():
      self._process_authenticated_session()
    else:
      self._process_unauthenticated_session()

  def _add_symbolic_subject_public(self):
    self.subjects.add(d1_common.const.SUBJECT_PUBLIC)

  def _process_unauthenticated_session(self):
    self.primary_subject = d1_common.const.SUBJECT_PUBLIC
    self.subject_info = None

  def _process_authenticated_session(self):
    self.primary_subject, self.subject_info = self._get_session_from_certificate()
    self._add_symbolic_subject_authenticated()
    self._add_symbolic_subject_verified()
    self._add_subject()
    self._add_subject_info()

  def _add_symbolic_subject_authenticated(self):
    self.subjects.add(d1_common.const.SUBJECT_AUTHENTICATED)

  def _add_symbolic_subject_verified(self):
    person = self._find_person_by_subject(self.subject)
    if person.verified:
      self.subjects.add(d1_common.const.SUBJECT_VERIFIED)

  def _add_primary_subject(self):
    self.subjects.add(self.primary_subject)

  def _add_subject_info(self):
    if self.subject_info is None:
      return
    person = self._find_person_by_subject(self.primary_subject)
    self._add_person_is_member_of(person)
    self._add_equivalent_identities(person)

    subjects = self.subjects
    for person in self.subject_info.person:
      subjects.add(person.subject.value())

  def _find_person_by_subject(self, subject):
    for person in self.subject_info.person:
      # TODO: lower() ?
      if person.subject.value().lower() == subject.lower():
        return person
    raise d1_common.types.exceptions.InvalidToken(0,
      'SubjectInfo does not have any Person records matching Subject: {0}'\
      .format(person.subject.value()))

  def _add_person_is_member_of(self, person):
    for is_member_of in person.isMemberOf:
      self.subjects.add(is_member_of.value())

  def _add_equivalent_identities(self, person):
    for equivalent_identity in person.equivalentIdentity:
      subject = equivalent_identity.value()
      self.subjects.add(subject)
      person = self._find_person_by_subject(subject)
      self._add_person_is_member_of(person)

  def _is_certificate_provided(self):
    return 'SSL_CLIENT_CERT' in self.request.META and \
      self.request.META['SSL_CLIENT_CERT'] != ''

  def _get_session_from_certificate(self):
    subject, subject_info_xml = self._extract_session_from_x509_v3_certificate()
    if subject_info_xml == '':
      return subject, None
    else:
      return subject, self._deserialize_subject_info(subject_info_xml)

  def _extract_session_from_x509_v3_certificate(self):
    try:
      return x509_extract_session.extract(self.request.META['SSL_CLIENT_CERT'])
    except Exception as e:
      raise d1_common.types.exceptions.InvalidToken(
        0, 'Error extracting session from certificate: {0}'.format(str(e))
      )

  def _deserialize_subject_info(self, subject_info_xml):
    try:
      return dataoneTypes.CreateFromDocument(subject_info_xml)
    except Exception as e:
      raise d1_common.types.exceptions.InvalidToken(
        0, 'Error deserializing SubjectInfo: {0}'.format(str(e))
      )
