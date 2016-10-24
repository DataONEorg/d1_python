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
"""
:mod:`view_handler`
===================
"""

# Stdlib.
import logging
import StringIO
import inspect

# Django.
from django.conf import settings

# D1.
import d1_common.url

# App.
import session


class ViewHandler(object):
  def process_view(self, request, view_func, view_args, view_kwargs):
    # Log which view is about the be called.
    logging.info(
      u'View: func_name={}, method={}, args={}, kwargs={}'
      .format(view_func.func_name, request.method, view_args, view_kwargs)
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
    if settings.DEBUG_GMN:
      if 'HTTP_VENDOR_INCLUDE_CERTIFICATE' in request.META:
        request.META['SSL_CLIENT_CERT'] = \
          self.pem_in_http_header_to_pem_in_string(
            request.META['HTTP_VENDOR_INCLUDE_CERTIFICATE'])

    # Always run regular certificate processing.
    session.ProcessSession(request)

    # Handle list of subjects in vendor specific extension:
    if settings.DEBUG_GMN:
      # If this is used together with TLS, the list is added to the one derived
      # from any included client side certificate. The public symbolic principal
      # is always included in the subject list.
      if 'HTTP_VENDOR_INCLUDE_SUBJECTS' in request.META:
        request.subjects.update(request.META['HTTP_VENDOR_INCLUDE_SUBJECTS'].split('\t'))

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
