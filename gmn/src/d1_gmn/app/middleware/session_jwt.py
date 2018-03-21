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

import http.client
import logging
import socket
import ssl

import d1_common.cert.jwt
import d1_common.cert.x509
import d1_common.date_time

import django.conf
import django.core.cache


def validate_jwt_and_get_subject_list(request):
  if not _has_jwt_header(request):
    return []
  if django.conf.settings.STAND_ALONE:
    logging.info(
      'Running in stand-alone mode. Skipping certificate download and '
      'ignoring included JWT.'
    )
    return []
  return [
    d1_common.cert.jwt.
    get_subject_with_local_validation(_get_jwt_header(request))
  ]


def _has_jwt_header(request):
  return 'Authorization' in request.META


def _get_jwt_header(request):
  return request.META['Authorization']


def _get_cn_cert():
  """Get the public TLS/SSL X.509 certificate from the root CN of the DataONE
  environment. The certificate is used for validating the signature of the JWTs.

  If certificate retrieval fails, a new attempt to retrieve the certificate
  is performed after the cache expires (settings.CACHES.default.TIMEOUT).

  If successful, returns a cryptography.Certificate().
  """
  try:
    cert_obj = django.core.cache.cache.cn_cert_obj
    d1_common.cert.x509.log_cert_info(
      logging.debug, 'Using cached CN cert for JWT validation', cert_obj
    )
    return cert_obj
  except AttributeError:
    cn_cert_obj = _download_and_decode_cn_cert()
    django.core.cache.cache.cn_cert_obj = cn_cert_obj
    return cn_cert_obj


def _download_and_decode_cn_cert():
  try:
    cert_der = d1_common.cert.x509.download_as_der(
      django.conf.settings.DATAONE_ROOT
    )
  except (http.client.HTTPException, socket.error, ssl.SSLError) as e:
    logging.warning(
      'Unable to get CN certificates from the DataONE environment. '
      'If this server is being used for testing, see the STAND_ALONE setting. '
      'error="{}" env="{}"'.format(str(e), django.conf.settings.DATAONE_ROOT)
    )
    return None
  else:
    cert_obj = d1_common.cert.x509.decode_der(cert_der)
    d1_common.cert.x509.log_cert_info(
      logging.debug,
      'CN certificate successfully retrieved from the DataONE environment. '
      'env="{}"'.format(django.conf.settings.DATAONE_ROOT),
      cert_obj,
    )
    return cert_obj
