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
:mod:`request_handler`
=========================

:platform: Linux
:Synopsis:
.. moduleauthor:: Roger Dahl
'''

from django.http import HttpResponse
import settings


class request_handler():
  def process_request(self, request):
    # Django's view selection and argument parsing process is based on
    # request.path_info. The default version of request.path_info is broken in
    # two ways: Consecutive slashes are collapsed to a single slash and escaped
    # slashes (%2f) are unescaped. This makes it impossible to use
    # request.path_info to resolve REST calls where sections of the URL are
    # variables that may contain escaped slashes. Because of that, we recreate
    # request.path_info from the REQUEST_URI, which contains the unmodified
    # request URL.
    try:
      parent_path_len = len(request.META['SCRIPT_NAME'])
      request.path_info = request.environ['REQUEST_URI'][parent_path_len:]
    except KeyError:
      pass

    if settings.GMN_DEBUG == False:
      return None

    ## Print request.
    #print '>'*80
    #print 'Request:'
    #print request
    #print '<'*80
    return None
