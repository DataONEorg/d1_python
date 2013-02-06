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
Module d1_common.const
======================

:Synopsis: Provides system wide constants for the Python DataONE stack.
:Created: 2010-01-20
:Author: DataONE (Vieglais, Dahl)
'''

# Make contents of __init__ available.
import d1_common

# The root of all DataONE.  Used to perform introspection on the system when
# no other node information is provided.
DEFAULT_CN_PROTOCOL = 'https'
DEFAULT_CN_HOST = 'cn.dataone.org'
DEFAULT_CN_PATH = '/cn'
DEFAULT_MN_PROTOCOL = 'https'
DEFAULT_MN_HOST = 'mn.dataone.org'
DEFAULT_MN_PATH = '/knb/d1/mn'
#
URL_DATAONE_ROOT = ''.join((DEFAULT_CN_PROTOCOL, '://',
                           DEFAULT_CN_HOST,
                           DEFAULT_CN_PATH))

# Version of this software.
VERSION = d1_common.__version__

# Maximum number of entries per list objects request.
MAX_LISTOBJECTS = 1000

# Default number of objects to retrieve in a list objects request.
DEFAULT_LISTOBJECTS = 100

# HTTP Response timeout in seconds, float.
RESPONSE_TIMEOUT = 30.0

# HTTP User Agent that this software is known as.
USER_AGENT = 'pyd1/%s +http://dataone.org/' % VERSION

# The system wide default checksum algorithm.
DEFAULT_CHECKSUM_ALGORITHM = 'SHA-1'

# Default number of replicas
DEFAULT_NUMBER_OF_REPLICAS = 3

# Mimetypes.
MIMETYPE_XML = 'application/xml'
MIMETYPE_XML_MEDIA_TYPES = 'application/xml', 'text/xml'
MIMETYPE_HTML = 'text/html'
MIMETYPE_XHTML = 'text/html'
MIMETYPE_TEXT = 'text/plain'
MIMETYPE_OCTETSTREAM = 'application/octet-stream'

DEFAULT_CHARSET = 'utf-8'

URL_PATHELEMENT_SAFE_CHARS = ":@$!()',~*&="
URL_QUERYELEMENT_SAFE_CHARS = ":;@$!()',~*/?"

# Symbolic subjects.
SUBJECT_VERIFIED = 'verifiedUser'
SUBJECT_AUTHENTICATED = 'authenticatedUser'
SUBJECT_PUBLIC = 'public'

# Search
DEFAULT_SEARCH_ENGINE = 'solr'
