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
"""System wide constants for the Python DataONE stack
"""

# Make contents of __init__ available.
import d1_common

# The root of all DataONE.  Used to perform introspection on the system when
# no other node information is provided.
DEFAULT_CN_PROTOCOL = 'https'
DEFAULT_CN_HOST = 'cn.dataone.org'
DEFAULT_CN_PATH = '/cn'
DEFAULT_MN_PROTOCOL = 'https'
DEFAULT_MN_HOST = 'localhost'
DEFAULT_MN_PATH = '/mn'
URL_DATAONE_ROOT = ''.join(
  (DEFAULT_CN_PROTOCOL, '://', DEFAULT_CN_HOST, DEFAULT_CN_PATH)
)
DEFAULT_MN_BASEURL = ''.join(
  (DEFAULT_MN_PROTOCOL, '://', DEFAULT_MN_HOST, DEFAULT_MN_PATH)
)

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

# MIME types.
CONTENT_TYPE_HTML = 'text/html'
CONTENT_TYPE_JSON = 'application/json'
CONTENT_TYPE_OCTETSTREAM = 'application/octet-stream'
CONTENT_TYPE_TEXT = 'text/plain'
CONTENT_TYPE_XHTML = 'text/html'
CONTENT_TYPE_XML = 'application/xml'
CONTENT_TYPE_XML_MEDIA_TYPES = 'application/xml', 'text/xml'

DATAONE_SCHEMA_ATTRIBUTE_BASE = 'http://ns.dataone.org/service/types/'
DEFAULT_CHARSET = 'utf-8'

# Designate characters which do not have to be percent-encoded in URLs. The
# character set is different for various URL sections, which is why "/" and "?"
# are listed as safe characters for URL query sections. DataONE uses a
# convention with key=value pairs in queries, so "=" has been omitted as well.
# More info in RFC3986.
URL_PATHELEMENT_SAFE_CHARS = ":@$!()',~*&="
URL_QUERYELEMENT_SAFE_CHARS = ":;@$!()',~*/?"

# Symbolic subjects.
SUBJECT_VERIFIED = 'verifiedUser'
SUBJECT_AUTHENTICATED = 'authenticatedUser'
SUBJECT_PUBLIC = 'public'

# Search
DEFAULT_SEARCH_ENGINE = 'solr'
