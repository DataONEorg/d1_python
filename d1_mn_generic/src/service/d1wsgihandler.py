#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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

from django import http
from django.utils import datastructures
import django.core.handlers.wsgi

# class D1WSGIRequest(django.core.handlers.wsgi.WSGIRequest):
#   '''Overrides the _load_post_and_files method of the standard Django WSGI
#   handler to ensure that PUT message bodies are parsed the same was as POST.
#   '''
#
#   def _load_post_and_files(self):
#       # Populates self._post and self._files
#       if self.method in ('POST', 'PUT'):
#           if self.environ.get('CONTENT_TYPE', '').startswith('multipart'):
#               self._raw_post_data = ''
#               try:
#                   self._post, self._files = self.parse_file_upload(self.META, self.environ['wsgi.input'])
#               except:
#                   # An error occured while parsing POST data.  Since when
#                   # formatting the error the request handler might access
#                   # self.POST, set self._post and self._file to prevent
#                   # attempts to parse POST data again.
#                   self._post = http.QueryDict('')
#                   self._files = datastructures.MultiValueDict()
#                   # Mark that an error occured.  This allows self.__repr__ to
#                   # be explicit about it instead of simply representing an
#                   # empty POST
#                   self._post_parse_error = True
#                   raise
#           else:
#               self._post, self._files = http.QueryDict(self.raw_post_data, encoding=self._encoding), datastructures.MultiValueDict()
#       else:
#           self._post, self._files = http.QueryDict('', encoding=self._encoding), datastructures.MultiValueDict()
#
# class D1WSGIHandler(django.core.handlers.wsgi.WSGIHandler):
#     request_class = D1WSGIRequest
