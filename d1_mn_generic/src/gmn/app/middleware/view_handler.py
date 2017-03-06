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
"""View handler middleware
"""

from __future__ import absolute_import

# Stdlib.
import StringIO
import d1_common
import logging

# Django.
import django.conf

# D1
import d1_common.const

# App.
import app.middleware.session_cert
import app.middleware.session_jwt


class ViewHandler(object):
  def process_view(self, request, view_func, view_args, view_kwargs):
    # Log which view is about the be called.
    logging.info(
      u'View: func_name="{}", method="{}", args="{}", kwargs="{}", url="{}"'
      .format(
        view_func.func_name, request.method, view_args, view_kwargs, request.path_info
      )
    )
    # logging.debug(request.headers)
    self.process_session(request)

  def process_session(self, request):
    # For simulating an HTTPS connection with client authentication when
    # debugging via regular HTTP, two mechanisms are supported. (1) A full
    # client side certificate can be included and (2) a list of subjects can be
    # included. Both use vendor specific extensions (HTTP headers that start
    # with the string "VENDOR_".) In some testing scenarios, it is convenient to
    # submit lists of subjects without having to generate certificates. In other
    # scenarios, it is desirable to simulate an HTTPS interaction as closely as
    # possible by providing a complete certificate.

    # Handle complete certificate in vendor specific extension.
    if django.conf.settings.DEBUG_GMN:
      if 'HTTP_VENDOR_INCLUDE_CERTIFICATE' in request.META:
        request.META['SSL_CLIENT_CERT'] = \
          self.pem_in_http_header_to_pem_in_string(
            request.META['HTTP_VENDOR_INCLUDE_CERTIFICATE'])

    # Add subjects from any provided certificate and JWT and store them in
    # the Django request obj.
    cert_primary_str, cert_equivalent_set = app.middleware.session_cert.get_subjects(
      request
    )
    jwt_subject_list = app.middleware.session_jwt.validate_jwt_and_get_subject_list(
      request
    )
    primary_subject_str = cert_primary_str
    all_subjects_set = cert_equivalent_set | {cert_primary_str
                                              } | set(jwt_subject_list)
    if len(jwt_subject_list) == 1:
      jwt_primary_str = jwt_subject_list[0]
      if jwt_primary_str != cert_primary_str:
        if cert_primary_str == d1_common.const.SUBJECT_PUBLIC:
          primary_subject_str = jwt_primary_str
        else:
          logging.warning(
            'Both a certificate and a JWT were provided and the primary '
            'subjects differ. Using the certificate for primary subject and'
            'the JWT as equivalent.'
          )
    logging.info(u'Primary subject: {}'.format(primary_subject_str))
    logging.info(
      u'All subjects: {}'.format(', '.join(sorted(all_subjects_set)))
    )
    request.primary_subject_str = primary_subject_str
    request.all_subjects_set = all_subjects_set

    # Handle list of subjects in vendor specific extension:
    if django.conf.settings.DEBUG_GMN:
      # This is added to any subjects obtained from cert and/or JWT.
      if 'HTTP_VENDOR_INCLUDE_SUBJECTS' in request.META:
        request.all_subjects_set.update(
          request.META['HTTP_VENDOR_INCLUDE_SUBJECTS'].split('\t')
        )

  def pem_in_http_header_to_pem_in_string(self, header_str):
    header = StringIO.StringIO(header_str)
    pem = StringIO.StringIO()
    pem.write('-----BEGIN CERTIFICATE-----\n')
    while True:
      pem_line = header.read(64)
      if len(pem_line) == 0:
        break
      pem.write(pem_line + '\n')
    pem.write('-----END CERTIFICATE-----\n')
    return pem.getvalue()
