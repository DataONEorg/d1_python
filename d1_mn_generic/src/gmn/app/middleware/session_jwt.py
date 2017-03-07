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
"""Validate Java Web Token (JWT) and extract subject
"""

from __future__ import absolute_import

# Stdlib
import httplib
import socket
import ssl
import urlparse

# Django
import django.conf
import django.core.cache
import logging

# 3rd party
import cryptography.hazmat.backends
import cryptography.x509
import jwt

# D1
import d1_common.const
import d1_common.types.exceptions

# App


def validate_jwt_and_get_subject_list(request):
  if not _has_jwt_header(request):
    return []
  if django.conf.settings.STAND_ALONE:
    logging.info(
      u'Running in stand-alone mode. Skipping certificate download and '
      u'ignoring included JWT.'
    )
    return []
  return _validate_jwt_and_get_subject_list(_get_jwt_header(request))


def get_subject_list_without_validate(jwt_base64):
  return _get_subject_list_without_validate(jwt_base64)


#
# Private
#


def _has_jwt_header(request):
  return 'Authorization' in request.META


def _get_jwt_header(request):
  return request.META['Authorization']


def _validate_jwt_and_get_subject_list(jwt_base64):
  """Validate any JWT in the request and return a list of authenticated
  subjects.

  The JWT is validated by checking that it was signed with a CN certificate.
  If validation fails for any reason, errors are logged and an empty list is
  returned. Possible errors include:

  - GMN is in stand-alone mode (settings_site.STAND_ALONE).
  - GMN could not establish a trusted (TLS/SSL) connection to the root CN in
  the env.
  - The certificate could not be retrieved from the root CN.
  - The JWT could not be decoded.
  - The JWT signature signature was invalid.
  - The JWT claim set contains invalid "Not Before" or "Expiration Time" claims.
  Currently, DataONE issues JWTs with only the primary subject. Equivalent
  identities and groups, as set up in the DataONE identity portal, are not
  represented. So the the list will contain either a single subject or be
  empty.
  """
  jwt_dict = _decode_and_validate_jwt(jwt_base64)
  subject_list = []
  if jwt_dict is not None:
    subject_list.append(jwt_dict['sub'])
  return subject_list


def _fix_base64_jwt(jwt_base64):
  header_json, payload_json, signature_str = jwt_base64.split('.')
  return '.'.join([
    _fix_base64_padding(_fix_base64_alphabet(header_json)),
    _fix_base64_padding(_fix_base64_alphabet(payload_json)),
    _fix_base64_padding(_fix_base64_alphabet(signature_str)),
  ]).strip()


def _fix_base64_padding(base64_str):
  padding = len(base64_str) % 4
  if padding:
    base64_str += '=' * (4 - padding)
  return base64_str


def _fix_base64_alphabet(base64_str):
  # jwt.decode() assumes a URL safe version of the base64 alphabet that uses
  # '-' instead of '+' and '_' instead of '/'.
  return base64_str.replace('+', '-').replace('/', '_')


def _decode_and_validate_jwt(jwt_base64):
  cn_cert_obj = _get_cn_cert()
  cn_public_key = cn_cert_obj.public_key()
  try:
    return jwt.decode(
      _fix_base64_jwt(jwt_base64), key=cn_public_key, algorithms=['RS256']
    )
  except jwt.InvalidTokenError as e:
    logging.warning(
      u'Ignoring JWT that failed to validate. error="{}"'.format(e.message)
    )
    return None


def _get_subject_list_without_validate(jwt_base64):
  jwt_dict = _decode_without_validate(jwt_base64)
  subject_list = []
  if jwt_dict is not None:
    subject_list.append(jwt_dict['sub'])
  return subject_list


def _decode_without_validate(jwt_base64):
  return jwt.decode(
    _fix_base64_jwt(jwt_base64), verify=False, algorithms=['RS256']
  )


def _get_cn_cert():
  """Get the public TLS/SSL X.509 certificate from the root CN of the DataONE
  environment. The certificate is used for validating the signature of the JWTs.

  If certificate retrieval fails, a new attempt to retrieve the certificate
  is performed after the cache expires (settings.CACHES.default.TIMEOUT).

  If successful, returns cryptography.Certificate().
  """
  try:
    return django.core.cache.cache.cn_cert_obj
  except AttributeError:
    cn_cert_obj = _download_and_decode_cert()
    django.core.cache.cache.cn_cert_obj = cn_cert_obj
    return cn_cert_obj


def _download_and_decode_cert():
  try:
    cert_der = _download_cn_cert()
  except (httplib.HTTPException, socket.error, ssl.SSLError) as e:
    logging.warn(
      u'Unable to get CN certificates from the DataONE environment. '
      u'If this server is being used for testing, see the STAND_ALONE setting. '
      u'error="{}" env="{}"'.format(str(e), django.conf.settings.DATAONE_ROOT)
    )
    return None
  else:
    logging.info(
      u'CN certificates successfully retrieved from the DataONE environment. '
      u'env="{}"'.format(django.conf.settings.DATAONE_ROOT)
    )
    return _decode_cert(cert_der)


def _download_cn_cert():
  """Download cert and return it as a DER encoded string"""
  # TODO: This requires Python 2.7.9 but is a better solution. Update the
  # code after upgrading to 2.7.9 or later.
  # ssl_context = ssl.create_default_context()
  # ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
  # ssl_socket = ssl_context.wrap_socket(
  #   socket.socket(),
  #   server_hostname=django.conf.settings.DATAONE_ROOT
  # )
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(d1_common.const.RESPONSE_TIMEOUT)
  ssl_socket = ssl.SSLSocket(sock)
  url_obj = urlparse.urlparse(django.conf.settings.DATAONE_ROOT)
  ssl_socket.connect((url_obj.netloc, 443))
  return ssl_socket.getpeercert(binary_form=True)


def _decode_cert(cert_der):
  """Decode cert DER string and return a cryptography.Certificate()"""
  return cryptography.x509.load_der_x509_certificate(
    cert_der,
    cryptography.hazmat.backends.default_backend(),
  )
