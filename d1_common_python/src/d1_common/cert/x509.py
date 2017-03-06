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
"""Utilities for processing X.509 v3 certificates
"""

import logging
import re

# 3rd party
# pyasn1 is pulled in by cryptography
import pyasn1.codec.der
import cryptography.hazmat.backends
import cryptography.x509
import cryptography.x509.oid
"""Map OID to short names for use when creating DataONE compliant serialization
of the DN.

This is pulled from LDAPv3 RFCs (RFC 4510 TO RFC 4519).

The set of OIDs that can occur in RDNs seems to be poorly defined. RFC 4514
refers to a registry but, if the registry exists, it's probably too large to be
useful to us. So we pull in OIDs for a small set that can be expected in RDNs in
certs from CILogon and will just need to expand it if required.

RFC 4514 section 2: Converting DistinguishedName from ASN.1 to a String

If the AttributeType is defined to have a short name (descriptor) [RFC4512] and
that short name is known to be registered [REGISTRY] [RFC4520] as identifying
the AttributeType , that short name a <descr>, is used.  Otherwise the
AttributeType is encoded as the dotted-decimal encoding , a <numericoid> of its
OBJECT IDENTIFIER. The <descr> and <numericoid> are defined in [RFC4512].
"""
OID_TO_SHORT_NAME_DICT = {
  '0.9.2342.19200300.100.1.1': 'UID', # userId
  '0.9.2342.19200300.100.1.25': 'DC', # domainComponent
  '1.2.840.113549.1.9.1': 'email', # emailAddress
  '2.5.4.3': 'CN', # commonName
  '2.5.4.4': 'SN', # surname
  '2.5.4.6': 'C', # countryName
  '2.5.4.7': 'L', # localityName
  '2.5.4.8': 'ST', # stateOrProvinceName
  '2.5.4.9': 'STREET', # streetAddress
  '2.5.4.10': 'O', # organizationName
  '2.5.4.11': 'OU', # organizationalUnitName
}

CILOGON_DATAONE_SUBJECT_INFO_OID = '1.3.6.1.4.1.34998.2.1'


def extract(cert_pem):
  """Extract DataONE compliant serialization of the DN and SubjectInfo extension
  from PEM (base64) encoded X.509 v3 certificate.
  """
  cert_obj = _deserialize_pem(cert_pem)
  return (
    _extract_dataone_subject_from_dn(cert_obj), _extract_subject_info(cert_obj),
  )


def _deserialize_pem(cert_pem):
  return cryptography.x509.load_pem_x509_certificate(
    cert_pem,
    cryptography.hazmat.backends.default_backend(),
  )


def _extract_dataone_subject_from_dn(cert_obj):
  return (
    ','.join(
      reversed([
        '{}={}'.format(
          OID_TO_SHORT_NAME_DICT.get(v.oid.dotted_string, v.oid.dotted_string),
          _escape(v.value)
        ) for v in cert_obj.subject
      ])
    )
  )


def _escape(rdn_str):
  """The following chars must be escaped in RDNs: , = + < > # ; \ "
  """
  return re.sub(r'([,=+<>#;\\])', r'\\\1', rdn_str)


def _extract_subject_info(cert_obj):
  try:
    subject_info_der = cert_obj.extensions.get_extension_for_oid(
      cryptography.x509.oid.ObjectIdentifier(CILOGON_DATAONE_SUBJECT_INFO_OID)
    ).value.value
    return str(pyasn1.codec.der.decoder.decode(subject_info_der)[0])
  except Exception as e:
    logging.debug('Unable to extract SubjectInfo. error="{}"'.format(e))
    return None
