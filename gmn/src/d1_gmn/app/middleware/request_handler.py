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
"""Request handler middleware

This handler runs first and last in the middleware "onion".

If settings.DEBUG_ECHO_REQUEST is True, it will short circuit all other
processing in GMN and return an echo of the request. Also see the description in
settings.py.

CORS headers are added here as a final step before passing the response to
Django, which sends it to the client. By adding the headers as a final step,
CORS headers are also added to responses created by the other middleware layers,
such as the exception handler.
"""

import d1_gmn.app.util
import d1_gmn.app.views.headers

import django.conf
import django.http


class RequestHandler:
  def __init__(self, next_in_chain_func):
    self.next_in_chain_func = next_in_chain_func

  def __call__(self, request):
    if django.conf.settings.DEBUG_GMN:
      if django.conf.settings.DEBUG_ECHO_REQUEST or 'HTTP_VENDOR_GMN_ECHO_REQUEST' in request.META:
        return d1_gmn.app.util.create_http_echo_response(request)

    response = self.next_in_chain_func(request)

    if (
        isinstance(response, django.http.response.HttpResponseBase) and
        hasattr(request, 'allowed_method_list')
    ):
      d1_gmn.app.views.headers.add_cors_headers_to_response(
        response, request.allowed_method_list
      )

    return response
