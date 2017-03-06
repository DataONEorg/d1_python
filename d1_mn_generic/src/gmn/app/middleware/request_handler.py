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
"""

from __future__ import absolute_import

# Stdlib.
import logging
import pprint

# Django.
from django.http import HttpResponse
import django.conf

# D1.
import d1_common
import d1_common.const
import d1_common.types.exceptions


class RequestHandler(object):
  def process_request(self, request):
    if django.conf.settings.DEBUG_GMN and django.conf.settings.ECHO_REQUEST_OBJECT:
      logging.warning('django.conf.settings.ECHO_REQUEST_OBJECT=True')
      pp = pprint.PrettyPrinter(indent=2)
      return HttpResponse(
        pp.pformat(request.read()), d1_common.const.CONTENT_TYPE_TEXT
      )
    return None
