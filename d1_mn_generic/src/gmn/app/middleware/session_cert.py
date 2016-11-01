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
"""Extract a list of subjects from a DataONE client side certificate

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
"""

# Stdlib.
import logging

# 3rd party
import pyxb

# D1.
import d1_certificate.certificate_extractor
import d1_common.const
import d1_common.types.dataoneTypes
import d1_common.types.exceptions


def get_subjects(request):
  """Get all subjects in the certificate.
  - Returns: primary_str (primary subject), equivalent_set (equivalent
  identities, groups and group memberships)
  - The primary subject is the certificate subject DN, serialized to a DataONE
  compliant subject string.
  """
  if _is_certificate_provided(request):
    return get_authenticated_subjects(request.META['SSL_CLIENT_CERT'])
  else:
    return d1_common.const.SUBJECT_PUBLIC, set()


def get_authenticated_subjects(cert_pem):
  primary_str, subject_info_pyxb = _get_subjects_from_certificate(cert_pem)
  equivalent_set = {
    d1_common.const.SUBJECT_PUBLIC,
    d1_common.const.SUBJECT_AUTHENTICATED,
  }
  if subject_info_pyxb is not None:
    equivalent_set |= _get_subject_info_sets(
      subject_info_pyxb, primary_str
    )
  return primary_str, equivalent_set


def _is_certificate_provided(request):
  return 'SSL_CLIENT_CERT' in request.META and \
    request.META['SSL_CLIENT_CERT'] != ''


def _get_subjects_from_certificate(cert_pem):
  subject, subject_info_xml = _extract_session_from_x509_v3_certificate(
    cert_pem
  )
  logging.debug(subject_info_xml)
  if subject_info_xml == '':
    return subject, None
  else:
    return subject, _deserialize_subject_info(subject_info_xml)


def _extract_session_from_x509_v3_certificate(cert_pem):
  try:
    return d1_certificate.certificate_extractor.extract(cert_pem)
  except Exception as e:
    raise d1_common.types.exceptions.InvalidToken(
      0,
      u'Error extracting session from certificate. error="{}"'.format(str(e))
    )


def _deserialize_subject_info(subject_info_xml):
  try:
    return d1_common.types.dataoneTypes.CreateFromDocument(subject_info_xml)
  except pyxb.ValidationError as e:
    err_str = e.details()
  except pyxb.PyXBException as e:
    err_str = str(e)
  raise d1_common.types.exceptions.InvalidToken(
    0, u'Could not deserialize SubjectInfo. subject_info="{}", error="{}"'
    .format(subject_info_xml, err_str)
  )

# SubjectInfo


def _get_subject_info_sets(subject_info_pyxb, primary_str):
  equivalent_set = set()
  _add_subject(equivalent_set, subject_info_pyxb, primary_str)
  return equivalent_set


def _add_subject(equivalent_set, subject_info_pyxb, subject_str):
  if subject_str in equivalent_set:
    return
  equivalent_set.add(subject_str)
  _add_person_subject(equivalent_set, subject_info_pyxb, subject_str)
  _add_group_subject(equivalent_set, subject_info_pyxb, subject_str)

# Person


def _add_person_subject(equivalent_set, subject_info_pyxb, subject_str):
  person_pyxb = _find_person_by_subject(subject_info_pyxb, subject_str)
  if not person_pyxb:
    return
  _if_person_is_verified_add_symbolic_subject(equivalent_set, person_pyxb)
  _add_person_is_member_of(equivalent_set, subject_info_pyxb, person_pyxb)
  _add_person_equivalent_identities(
    equivalent_set, subject_info_pyxb, person_pyxb
  )


def _find_person_by_subject(subject_info_pyxb, subject_str):
  print subject_info_pyxb, subject_str
  for person_pyxb in subject_info_pyxb.person:
    if person_pyxb.subject.value() == subject_str:
      return person_pyxb


def _add_person_is_member_of(equivalent_set, subject_info_pyxb, person_pyxb):
  for is_member_of in person_pyxb.isMemberOf:
    _add_subject(equivalent_set, subject_info_pyxb, is_member_of.value())


def _add_person_equivalent_identities(
  equivalent_set, subject_info_pyxb, person_pyxb
):
  for equivalent_pyxb in person_pyxb.equivalentIdentity:
    _add_subject(equivalent_set, subject_info_pyxb, equivalent_pyxb.value())


def _if_person_is_verified_add_symbolic_subject(equivalent_set, person_pyxb):
  if person_pyxb.verified:
    equivalent_set.add(d1_common.const.SUBJECT_VERIFIED)

# Group


def _add_group_subject(equivalent_set, subject_info_pyxb, subject_str):
  group_pyxb = _find_group_by_subject(subject_info_pyxb, subject_str)
  if group_pyxb:
    _add_members(equivalent_set, subject_info_pyxb, group_pyxb)


def _find_group_by_subject(subject_info_pyxb, subject_str):
  for group_pyxb in subject_info_pyxb.group:
    if group_pyxb.subject.value() == subject_str:
      return group_pyxb


def _add_members(equivalent_set, subject_info_pyxb, group_pyxb):
  for member_pyxb in group_pyxb.hasMember:
    _add_subject(equivalent_set, subject_info_pyxb, member_pyxb.value())
