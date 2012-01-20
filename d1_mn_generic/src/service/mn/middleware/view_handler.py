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
:mod:`view_handler`
===================

:Synopsis: Sanity checking on system state before view is executed.
:Author: DataONE (Dahl)
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

# 3rd party.
# Lxml
try:
  from lxml import etree
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-lxml\n')
  raise

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
import mn.models as models
import settings
import mn.x509_extract_session


class view_handler():
  def subject_info_to_subject_list(self, subject_info):
    '''The DataONE SubjectInfo type contains a structure of person objects,
    each potentially containing equivalent identities and group memberships.
    "Flatten" this to a unique list of subjects.
    '''
    if subject_info is None:
      return set()
    subjects = set()
    for person in subject_info.person:
      subjects.add(person.subject.value())
      for equivalent_identity in person.equivalentIdentity:
        subjects.add(equivalent_identity.value())
      for is_member_of in person.isMemberOf:
        subjects.add(is_member_of.value())
    #print subjects
    return subjects

  def process_view(self, request, view_func, view_args, view_kwargs):
    # Log which view is about the be called.
    logging.info(
      'View: func_name({0}) method({1}) args({2}) kwargs({3})'
      .format(view_func.func_name, request.method, view_args, view_kwargs)
    )

    # If a session string was not passed in by either a certificate or by a
    # vendor specific extension, fall back to the Public principal.
    request.session = dataoneTypes.session()
    request.session.subject = dataoneTypes.subject(d1_common.const.SUBJECT_PUBLIC)

    # TODO: THE CODE BELOW IS WHAT WILL BE USED ONCE THE SESSION OBJECT
    # OFFICIALLY MOVES INTO A CERTIFICATE EXTENSION.
    # Extract the session object from the client side certificate and
    # store it in the request (for easy access).
    #    if 'SSL_CLIENT_CERT' in request.META:
    #      session_xml_str = x509_extract_session.extract(
    #        request.META['SSL_CLIENT_CERT'])
    #      try:
    #        request.session = dataoneTypes.CreateFromDocument(session_xml_str)
    #      except:
    #          raise d1_common.types.exceptions.NotAuthorized(0,
    #            'Invalid session: {0}'.format(
    #              request.META['HTTP_VENDOR_OVERRIDE_SESSION']))

    # For now, the principal is stored in the certificate subject. So just
    # create a session object from that.
    if 'SSL_CLIENT_S_DN' in request.META:
      request.session = dataoneTypes.session()
      request.session.subject = dataoneTypes.subject(request.META['SSL_CLIENT_S_DN'])

    if settings.DEBUG == True:
      # For simulating an HTTPS connection with client authentication when
      # debugging via regular HTTP, a serialized Session object can be passed in
      # by using a vendor specific extension.
      if 'HTTP_VENDOR_OVERRIDE_SESSION' in request.META:
        try:
          request.session = dataoneTypes.CreateFromDocument(
            request.META['HTTP_VENDOR_OVERRIDE_SESSION']
          )
        except:
          raise d1_common.types.exceptions.NotAuthorized(
            0, 'Invalid session: {0}'.format(request.META['HTTP_VENDOR_OVERRIDE_SESSION'])
          )

      # For debugging, simulate an accept header with a regular parameter.
      if 'accept' in request.REQUEST:
        request.META['HTTP_ACCEPT'] = request.REQUEST['accept']

    request.subjects = self.subject_info_to_subject_list(request.session.subjectInfo)

    # Decode view parameters. This is the counterpart to the changes made to
    # request.path_info detailed in request_handler.py.
    view_args_list = []
    for arg in view_args:
      view_args_list.append(d1_common.url.decodeQueryElement(arg))
    view_args = tuple(view_args_list)
    for key, arg in view_kwargs:
      view_kwargs[key] = d1_common.url.decodePathElement(arg)

    # Since copies of the view_args and view_kwargs were modified, the view must
    # be called directly with the modified arguments. This short circuits
    # Django's own processing, so the middleware functions must then be called
    # manually.
    try:
      response = view_func(request, *view_args, **view_kwargs)
    except Exception, e:
      # If the view raised an exception, run it through exception middleware,
      # and if the exception middleware returns a response, use that. Otherwise,
      # reraise the exception.
      for middleware_method in inspect.currentframe().f_back.f_locals['self']\
          ._exception_middleware:
        response = middleware_method(request, e)
        if response:
          return response
      raise

    return response
