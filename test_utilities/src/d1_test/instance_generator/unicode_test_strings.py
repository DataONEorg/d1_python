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
"""A set of Unicode strings that are particularly likely to trip up the unwary
"""

UNICODE_TEST_STRINGS = [
  'common-unicode-ascii-safe-ABCDEFGHIJKLMNOPQRSTUVWXYZ',
  'common-unicode-ascii-safe-abcdefghijklmnopqrstuvwxyz',
  'common-unicode-ascii-safe-0123456789',
  'common-unicode-ascii-safe-:@$-_.!*()\',~',
  'common-unicode-ascii-safe-unreserved-._~',
  'common-unicode-ascii-safe-sub-delims-$!*()\',',
  'common-unicode-ascii-safe-gen-delims-:@',
  'common-unicode-ascii-escaped-"#<>[]^`{}|',
  'common-unicode-ascii-escaped-tomcatBlocked-\\',
  'common-unicode-ascii-escaped-tomcatBlocked-%5C',
  'common-unicode-ascii-semi-colon-test-%3B',
  'common-unicode-ascii-escaped-%',
  'common-unicode-ascii-escaped-space x x',
  'common-unicode-ascii-escape-anyway-+',
  'common-unicode-ascii-escape-space-v-plus-+ +%20 %20+',
  'path-unicode-ascii-safe-&=&=',
  'path-unicode-ascii-escaped-;',
  'path-unicode-ascii-escaped-?',
  'path-unicode-ascii-escaped-/',
  'path-unicode-ascii-escaped-%3F',
  'path-unicode-ascii-escaped-%2F',
  'path-unicode-ascii-escaped-double-//case',
  'path-unicode-ascii-escaped-double-trailing//',
  'path-unicode-ascii-escaped-double-%2F%2Fcase',
  'path-unicode-ascii-escaped-double-trailing%2F%2F',
  'query-unicode-ascii-safe-;',
  'query-unicode-ascii-safe-/?',
  'query-unicode-ascii-escaped-&=&=',
  'fragment-unicode-ascii-safe-;',
  'fragment-unicode-ascii-safe-&=&=/?',
  'common-unicode-bmp-1byte-escaped-¡¢£',
  'common-unicode-bmp-2byte-escaped-䦹䦺',
  'common-unicode-supplementary-escaped-𐌔𐌕𐌖𐌗',
  'query-unicode-ascii-escaped-this&that=theOther',
  'common-ascii-doc-example-urn:lsid:ubio.org:namebank:11815',
  'path-ascii-doc-example-10.1000/182',
  'query-ascii-doc-example-10.1000/182',
  'fragment-ascii-doc-example-10.1000/182',
  'path-ascii-doc-example-http://example.com/data/mydata?row=24',
  'query-ascii-doc-example-http://example.com/data/mydata?row=24',
  'fragment-ascii-doc-example-http://example.com/data/mydata?row=24',
  'path-ascii-doc-example-ldap://ldap1.example.net:6666/'
  'o=University%20of%20Michigan, c=US??sub?(cn=Babs%20Jensen)',
  'query-ascii-doc-example-ldap://ldap1.example.net:6666/'
  'o=University%20of%20Michigan, c=US??sub?(cn=Babs%20Jensen)',
  'fragment-ascii-doc-example-ldap://ldap1.example.net:6666/'
  'o=University%20of%20Michigan, c=US??sub?(cn=Babs%20Jensen)',
  'common-bmp-doc-example-ฉันกินกระจกได้',
  'common-bmp-doc-example-Is féidir liom ithe gloine',
  'decode-space-potential-error-unescaped-plus-+',
]
