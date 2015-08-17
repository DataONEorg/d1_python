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
'''
:mod:`session`
==============

:Synopsis: Session handling
:Author: DataONE (Dahl)

The DataONE infrastructure uses X.509 v3 certificates to represent sessions. A
session contains assertions about the identity of the caller. In particular, the
session contains the primary identity, a list of equivalent identities and group
memberships of the caller.

A user can connect without providing a certificate (and so, without providing a
session). This limits the user's access to data that is publicly available.

A user can connect with a certificate that does not contain a list of
equivalent identities and group memberships (no SubjectInfo). This limits the
user's access to data that is publicly available and that is available directly
to that user (as designated in the Subject DN).

If a certificate was provided, it has been validated by Apache before being
passed to GMN. So it is known to signed by a trusted CA and to be unexpired.

The list of subjects to use for access control is created with the following
algorithm:

- Start with empty list of subjects
- Add the symbolic subject, "public"
- If the connection was made without a certificate:
  - Stop.
- Add the symbolic subject, "authenticatedUser"
- Get the DN from the Subject and serialize it to a standardized string. This
  string is called Subject below.
- If the certificate does not have a SubjectInfo extension:
  - Add Subject
  - Stop.
- Perform recursive search with detection of circular dependencies, starting
  with Subject.
  - If subject is not in list of subjects:
    - Add subject to list of subjects.
    - Search for Person with subject.
      - If Person is found:
        - If the Person has the verified flag set and if "verifiedUser" has not
          already been added, add it.
        - Iterate over isMemberOf and equivalentIdentity:
          - Recursively add those subjects.
    - Search for Group with Subject.
      - If Group is found:
        - Iterate over hasMember:
          - Recursively add those subjects.
'''

# Stdlib.
import logging

# D1.
import d1_common.const
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.types.exceptions
import d1_x509v3_certificate_extractor


class process_session(object):
  def __init__(self, request):
    '''Process the session in the certificate and store the result in the
    request object.
    - The primary subject is the certificate subject DN, serialized to a
      DataONE compliant subject string.
    - The SubjectInfo is stored unprocessed in request.subject_info.
    - The entire list of subjects (primary subject, equivalent identities and
      group memberships) is stored in request.subjects.
    - In addition, the primary subject is stored separately in
      request.primary_subject.
    '''
    self.request = request
    self.request.subjects = set()
    self.subjects = self.request.subjects
    self._process_session()
    self.request.primary_subject = self.primary_subject
    self._log_session()

  def _process_session(self):
    self._add_symbolic_subject_public()
    if self._is_certificate_provided():
      self._process_authenticated_session()
    else:
      self._process_unauthenticated_session()

  def _is_certificate_provided(self):
    return 'SSL_CLIENT_CERT' in self.request.META and \
      self.request.META['SSL_CLIENT_CERT'] != ''

  def _add_symbolic_subject_public(self):
    self.subjects.add(d1_common.const.SUBJECT_PUBLIC)

  def _process_unauthenticated_session(self):
    self.primary_subject = d1_common.const.SUBJECT_PUBLIC
    self.subject_info = None

  def _process_authenticated_session(self):
    self.primary_subject, self.subject_info = self._get_session_from_certificate()
    self._add_symbolic_subject_authenticated()
    self._process_subject_info()

  def _get_session_from_certificate(self):
    subject, subject_info_xml = self._extract_session_from_x509_v3_certificate()
    if subject_info_xml == '':
      return subject, None
    else:
      return subject, self._deserialize_subject_info(subject_info_xml)

  def _extract_session_from_x509_v3_certificate(self):
    try:
      return d1_x509v3_certificate_extractor.extract(self.request.META['SSL_CLIENT_CERT'])
    except Exception as e:
      raise d1_common.types.exceptions.InvalidToken(
        0, 'Error extracting session from certificate: {0}'.format(str(e))
      )

  def _deserialize_subject_info(self, subject_info_xml):
    try:
      return dataoneTypes.CreateFromDocument(subject_info_xml)
    except Exception as e:
      raise d1_common.types.exceptions.InvalidToken(
        0, 'Error deserializing SubjectInfo: {0}\n{1}'.format(
          str(e), subject_info_xml)
      )

  def _add_symbolic_subject_authenticated(self):
    self.subjects.add(d1_common.const.SUBJECT_AUTHENTICATED)

  def _process_subject_info(self):
    if self.subject_info is None:
      self._add_primary_subject()
      return
    self._add_subject_info()

  def _add_symbolic_subject_verified(self):
    self.subjects.add(d1_common.const.SUBJECT_VERIFIED)

  def _add_primary_subject(self):
    self.subjects.add(self.primary_subject)

  # Process SubjectInfo.

  def _add_subject_info(self):
    self._add_subject(self.primary_subject)

  def _add_subject(self, subject):
    if subject in self.subjects:
      return
    self.subjects.add(subject)
    self._add_person_subject(subject)
    self._add_group_subject(subject)

  # Person

  def _add_person_subject(self, subject):
    person = self._find_person_by_subject(subject)
    if not person:
      return
    self._if_person_is_verified_add_symbolic_subject(person)
    self._add_person_is_member_of(person)
    self._add_person_equivalent_identities(person)

  def _find_person_by_subject(self, subject):
    for person in self.subject_info.person:
      if person.subject.value() == subject:
        return person

  def _add_person_is_member_of(self, person):
    for is_member_of in person.isMemberOf:
      self._add_subject(is_member_of.value())

  def _add_person_equivalent_identities(self, person):
    for equivalent_identity in person.equivalentIdentity:
      self._add_subject(equivalent_identity.value())

  def _if_person_is_verified_add_symbolic_subject(self, person):
    if person.verified:
      self.subjects.add(d1_common.const.SUBJECT_VERIFIED)

  # Group

  def _add_group_subject(self, subject):
    group = self._find_group_by_subject(subject)
    if not group:
      return
    self._add_members(group)

  def _find_group_by_subject(self, subject):
    for group in self.subject_info.group:
      if group.subject.value() == subject:
        return group

  def _add_members(self, group):
    for member in group.hasMember:
      self._add_subject(member.value())

  def _log_session(self):
    logging.info('Session:')
    logging.info('  {0} (primary)'.format(self.request.primary_subject))
    for subject in self.request.subjects:
      logging.info('  {0}'.format(subject))
    logging.debug('SubjectInfo:')
    if self.subject_info:
      logging.debug(u'  {0}'.format(self.subject_info.toxml()))
    else:
      logging.debug(u'  <none>')
