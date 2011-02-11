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

import cgi
import re
import urllib

import d1_common


class request_handler():
  def process_request(self, request):
    '''Django's view selection and argument parsing process is based on
     request.path_info. When Django is called through Apache and mod_wsgi,
     request.path_info is broken in two ways: Consecutive slashes are collapsed
     to a single slash and escaped slashes (%2f) are unescaped. This makes it
     impossible to use request.path_info to resolve REST calls where sections of
     the URL are variables that may contain escaped slashes. However, the
     REQUEST_URI contains the unmodified request URL, so we recreate
     request.path_info from it.
    
     When the service runs through the Django development server,
     request.path_info is still broken. Escaped slashes (%2f) are unescaped
     but, as opposed to when running through Apache, consecutive slashes are
     not collapsed to a single slash. However, when running through a standard
     version of the Django
     development server, there is no REQUEST_URI that can be used for fixing
     request.path_info. A one line patch to Django is required to bring the
     REQUEST_URI here, so that request.path_info can be repaired both when
     the service is run through Apache and when it's run through the Django
     development server.
    '''
    try:
      request_uri = request.environ['REQUEST_URI']
    except KeyError:
      patch_msg = '# Django must be patched #\n'
      patch_msg += 'In basehttp.py, around line 573, add:\n'
      patch_msg += 'env[\'REQUEST_URI\'] = path'
      raise d1_common.types.exceptions.ServiceFailure(0, patch_msg)

    # Strip parent path from path_info.
    parent_path_len = len(request.META['SCRIPT_NAME'])
    request.path_info = request.environ['REQUEST_URI'][parent_path_len:]
    # Strip any arguments from path_info.
    request.path_info = re.sub(r'\?.*', '', request.path_info)

    # Django ticket: http://code.djangoproject.com/ticket/12083. This is a hack
    # that is applied when the root of the app is requested without a trailing
    # backslash through Apache. Without this, Django 1.1.1 raises a KeyError
    # exception. The workaround was found by comparing working and non-working
    # requests. It should be removed for Django 1.2.
    if request.path_info == '':
      request.environ['REQUEST_URI'] = request.META['SCRIPT_NAME'] + '/'
      request.META['REQUEST_URI'] = request.META['SCRIPT_NAME'] + '/'
      request.path_info = '/'

    # Block access to the test functions if not in debug mode.
    if re.match(r'/test', request.path_info) and settings.GMN_DEBUG == False:
      #sys_log.info('client({0}): Attempted to access {0} while not in DEBUG mode'.format(request.path_info))
      # TODO: This exception is unhandled.
      raise d1_common.types.exceptions.InvalidRequest(0, 'Unsupported')

    if settings.GMN_DEBUG == False:
      return None

    # Print request.
    #    import pprint
    #    pp = pprint.PrettyPrinter(indent=2)
    #    return HttpResponse(cgi.escape('<pre>{0}</pre>'.format(pp.pformat(request))))

    return None
