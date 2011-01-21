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

import email.message
from urllib import quote
import const


def get_content_type(content_type):
  m = email.message.Message()
  m['Content-Type'] = content_type
  return m.get_content_type()


def encodePathElement(element):
  '''Encodes a URL path element according to RFC3986.
  
  :param element: The path element to encode for transmission in a URL.
  :type element: Unicode
  :return: URL encoded path element
  :return type: UTF-8 encoded string. 
  '''
  return quote(element.encode('utf-8'), \
               safe=const.URL_PATHELEMENT_SAFE_CHARS)


def encodeQueryElement(element):
  '''Encodes a URL query element according to RFC3986.
  
  :param element: The query element to encode for transmission in a URL.
  :type element: Unicode
  :return: URL encoded query element
  :return type: UTF-8 encoded string. 
  '''
  return quote(element.encode('utf-8'), \
               safe=const.URL_QUERYELEMENT_SAFE_CHARS)
