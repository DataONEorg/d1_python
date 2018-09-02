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
import socket
import ssl
import urllib.parse

import contextlib2
import cryptography.hazmat
import cryptography.hazmat.backends
import cryptography.hazmat.primitives.serialization
import cryptography.x509
import cryptography.x509.oid
import pyasn1.codec.der
import pyasn1.codec.der.decoder

# Map OID to short names for use when creating DataONE compliant serialization
# of the DN.
#
# This is pulled from LDAPv3 RFCs (RFC 4510 TO RFC 4519).
#
# The set of OIDs that can occur in RDNs seems to be poorly defined. RFC 4514
# refers to a registry but, if the registry exists, it's probably too large to be
# useful to us. So we pull in OIDs for a small set that can be expected in RDNs in
# certs from CILogon and will just need to expand it if required.
#
# RFC 4514 section 2: Converting DistinguishedName from ASN.1 to a String
#
# If the AttributeType is defined to have a short name (descriptor) [RFC4512] and
# that short name is known to be registered [REGISTRY] [RFC4520] as identifying
# the AttributeType , that short name a <descr>, is used.  Otherwise the
# AttributeType is encoded as the dotted-decimal encoding , a <numericoid> of its
# OBJECT IDENTIFIER. The <descr> and <numericoid> are defined in [RFC4512].
import d1_common.const

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
AUTHORITY_INFO_ACCESS_OID = '1.3.6.1.5.5.7.1.1' # authorityInfoAccess
CA_ISSUERS_OID = '1.3.6.1.5.5.7.48.2' # caIssuers
OCSP_OID = '1.3.6.1.5.5.7.48.1' # OCSP

UBUNTU_CA_BUNDLE_PATH = '/etc/ssl/certs/ca-certificates.crt'


def extract_subjects(cert_pem):
  """Extract from PEM (base64) encoded X.509 v3 certificate:
  - DataONE compliant serialization of the DN (str)
  - SubjectInfo extension (XML str)
  """
  cert_obj = deserialize_pem(cert_pem)
  return (
    extract_subject_from_dn(cert_obj), extract_subject_info_extension(cert_obj),
  )


def extract_subject_from_dn(cert_obj):
  """Serialize a DN to a DataONE subject string.
  E.g.: CN=Some Name A792,O=Harte Research Institute,C=US,DC=cilogon,DC=org
  If an RDN contains an unknown OID, the OID is serialized as a dotted string.
  """
  return (
    ','.join(
      '{}={}'.format(
        OID_TO_SHORT_NAME_DICT.get(v.oid.dotted_string, v.oid.dotted_string),
        rdn_escape(v.value)
      ) for v in reversed(list(cert_obj.subject))
    )
  )


def deserialize_pem(cert_pem):
  return cryptography.x509.load_pem_x509_certificate(
    cert_pem,
    cryptography.hazmat.backends.default_backend(),
  )


def deserialize_pem_file(cert_path):
  with open(cert_path, 'rb') as f:
    return deserialize_pem(f.read())


def rdn_escape(rdn_str):
  """The following chars must be escaped in RDNs: , = + < > # ; \ "
  """
  return re.sub(r'([,=+<>#;\\])', r'\\\1', rdn_str)


def extract_subject_info_extension(cert_obj):
  try:
    subject_info_der = cert_obj.extensions.get_extension_for_oid(
      cryptography.x509.oid.ObjectIdentifier(CILOGON_DATAONE_SUBJECT_INFO_OID)
    ).value.value
    return str(pyasn1.codec.der.decoder.decode(subject_info_der)[0])
  except Exception as e:
    logging.debug('SubjectInfo not extracted. reason="{}"'.format(e))


def download_as_der(
    base_url=d1_common.const.URL_DATAONE_ROOT,
    timeout_sec=d1_common.const.DEFAULT_HTTP_TIMEOUT,
):
  """Download certificate from the server at {base_url} and return it as a DER
  encoded string.

  {base_url} can be a full URL to a DataONE service endpoint or just a server
  hostname.

  In some cases, there's a need to download certificates in order to fix
  validation issues that prevent those certificates from being downloaded. To
  work around such chicken-and-egg problems, temporarily wrap calls to the
  download_* functions with the disable_cert_validation() context manager (also
  in this module).

  TODO: It is unclear which SSL and TLS protocols are supported by the method
  currently being used. The current method and the two commented out below
  should be compared to determine which has the best compatibility with current
  versions of Python and current best practices for protocol selection.
  """
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(timeout_sec)
  ssl_socket = ssl.SSLSocket(sock)
  url_obj = urllib.parse.urlparse(base_url)
  ssl_socket.connect((url_obj.netloc, 443))
  return ssl_socket.getpeercert(binary_form=True)

  # (1)
  # ssl_context = ssl.create_default_context()
  # ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
  # ssl_socket = ssl_context.wrap_socket(
  #   socket.socket(),
  #   server_hostname=django.conf.settings.DATAONE_ROOT
  # )
  #
  # (2)
  # ssl_protocol_list: PROTOCOL_SSLv2, PROTOCOL_SSLv3, PROTOCOL_SSLv23,
  # PROTOCOL_TLSv1, PROTOCOL_TLSv1_1,  PROTOCOL_TLSv1_2
  #
  # Check if protocols should be checked in order of preference or if the
  # function will do that.
  #
  # for ssl_protocol_str in ssl_protocol_list:
  #   print ssl_protocol_str
  #   try:
  #     return ssl.get_server_certificate(
  #       addr=(hostname_str, int(port_str)),
  #       ssl_version=getattr(ssl, ssl_protocol_str),
  #       ca_certs=UBUNTU_CA_BUNDLE_PATH,
  #     )
  #   except ssl.SSLError as e:
  #     logging.info('SSL: {}'.format(str(e)))
  #     if ssl_protocol_str is ssl_protocol_list[-1]:
  #       raise


def download_as_pem(
    base_url=d1_common.const.URL_DATAONE_ROOT,
    timeout_sec=d1_common.const.DEFAULT_HTTP_TIMEOUT,
):
  """Download certificate from the server at {base_url} and return it as a PEM
  encoded string.

  See download_as_der() for more info.
  """
  return ssl.DER_cert_to_PEM_cert(download_as_der(base_url, timeout_sec))


def download_as_obj(
    base_url=d1_common.const.URL_DATAONE_ROOT,
    timeout_sec=d1_common.const.DEFAULT_HTTP_TIMEOUT,
):
  """Download certificate from the server at {base_url} and return it as a
  cryptography.Certificate object.

  See download_as_der() for more info.
  """
  return decode_der(download_as_der(base_url, timeout_sec))


def decode_der(cert_der):
  """Decode cert DER string and return a cryptography.Certificate()"""
  return cryptography.x509.load_der_x509_certificate(
    cert_der,
    cryptography.hazmat.backends.default_backend(),
  )


# noinspection PyProtectedMember
@contextlib2.contextmanager
def disable_cert_validation():
  """Temporary disable certificate validation in the standard ssl library

  Note: This should not be used in production code but is sometimes necessary
  as a temporary workaround.
  """
  # By design, the standard ssl library does not provide a way to disable
  # verification of the server side cert. However, the ssl implementors do
  # mention this dangerous monkey patch as an alternative. Offered here as a
  # context manager to make it a bit safer.
  current_context = ssl._create_default_https_context
  ssl._create_default_https_context = ssl._create_unverified_context
  try:
    yield
  finally:
    ssl._create_default_https_context = current_context


def get_issuer_ca_cert_url(cert_obj):
  """Given {server_cert} as a cryptography.Certificate(), return a URL where the
  issuer's cert can be downloaded. The issuer cert can then be added to the
  trusted CA certs in order to trust {server_cert}.
  """
  for extension in cert_obj.extensions:
    if extension.oid.dotted_string == AUTHORITY_INFO_ACCESS_OID:
      authority_info_access = extension.value
      for access_description in authority_info_access:
        if access_description.access_method.dotted_string == CA_ISSUERS_OID:
          return access_description.access_location.value


# noinspection PyProtectedMember
def log_cert_info(log, msg_str, cert_obj):
  """Log information from {cert_obj} to {log}.
  """
  list(
    map(
      log, ['{}:'.format(msg_str)] + [
        '  {}'.format(v)
        for v in [
          'Subject: {}'.
          format(get_val_str(cert_obj, ['subject', 'value'], reverse=True)),
          'Issuer: {}'.
          format(get_val_str(cert_obj, ['issuer', 'value'], reverse=True)),
          'Not Valid Before: {}'.format(cert_obj.not_valid_before.isoformat()),
          'Not Valid After: {}'.format(cert_obj.not_valid_after.isoformat()),
          'Subject Alt Names: {}'.format(
            get_ext_val_str(
              cert_obj, 'SUBJECT_ALTERNATIVE_NAME', ['value', 'value']
            )
          ),
          'CRL Distribution Points: {}'.format(
            get_ext_val_str(
              cert_obj, 'CRL_DISTRIBUTION_POINTS',
              ['value', 'full_name', 'value', 'value']
            )
          ),
          'Authority Access Location: {}'
          .format(get_issuer_ca_cert_url(cert_obj) or '<not found>'),
        ]
      ]
    )
  )


def get_ext(cert_obj, n):
  try:
    return cert_obj.extensions.get_extension_for_oid(
      getattr(cryptography.x509.oid.ExtensionOID, n)
    )
  except cryptography.x509.ExtensionNotFound:
    pass


def get_val_list(n, path):
  """Return a list of the values in the innermost objects in a set of nested
  lists"""
  try:
    y = getattr(n, path[0])
  except AttributeError:
    return []
  if len(path) == 1:
    return [y]
  else:
    return [x for a in y for x in get_val_list(a, path[1:])]


def get_val_str(x, path=None, reverse=False):
  val_list = get_val_list(x, path or [])
  if reverse:
    val_list = reversed(val_list)
  return '<not found>' if x is None else ' / '.join(map(str, val_list))


def get_ext_val_str(cert_obj, e, path=None):
  return get_val_str(get_ext(cert_obj, e), path or [])


def get_cert_pem(cert_obj):
  return cert_obj.public_bytes(
    cryptography.hazmat.primitives.serialization.Encoding.PEM,
  )


def get_cert_der(cert_obj):
  return cert_obj.public_bytes(
    cryptography.hazmat.primitives.serialization.Encoding.DER,
  )


def get_public_key_pem(cert_obj):
  return cert_obj.public_key().public_bytes(
    cryptography.hazmat.primitives.serialization.Encoding.PEM,
    cryptography.hazmat.primitives.serialization.PublicFormat.PKCS1,
  )
