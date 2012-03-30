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
======================

:Synopsis: Django request handler middleware.
:Author: DataONE (Dahl)
'''

# Stdlib.
import cgi
import logging
import pprint
import re
import urllib

# Django.
from django.http import HttpResponse

# App.
import d1_common
import settings


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
    request.path_info is still broken. Escaped slashes (%2f) are unescaped but,
    as opposed to when running through Apache, consecutive slashes are not
    collapsed to a single slash. However, when running through a standard
    version of the Django development server, there is no REQUEST_URI that can
    be used for fixing request.path_info. A one line patch to Django is
    required to bring the REQUEST_URI here, so that request.path_info can be
    repaired both when the service is run through Apache and when it's run
    through the Django development server.
    '''
    try:
      request_uri = request.environ['REQUEST_URI']
    except KeyError:
      patch_msg = '# Django must be patched for debugging GMN with the Django '
      patch_msg += 'development server #\n'
      patch_msg += 'In basehttp.py, around line 573, add:\n'
      patch_msg += 'env[\'REQUEST_URI\'] = path'
      raise d1_common.types.exceptions.ServiceFailure(0, patch_msg)

    # Strip parent path from path_info.
    parent_path_len = len(request.META['SCRIPT_NAME'])
    request.path_info = request.environ['REQUEST_URI'][parent_path_len:]
    # Strip any arguments from path_info.
    request.path_info = re.sub(r'\?.*', '', request.path_info)

    if settings.GMN_DEBUG == True and settings.ECHO_REQUEST_OBJECT:
      pp = pprint.PrettyPrinter(indent=2)
      return HttpResponse(cgi.escape('<pre>{0}</pre>'.format(pp.pformat(request))))

    logging.info('REQUEST: {0}'.format(request_uri))

    return None
