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
  u'common-unicode-ascii-safe-ABCDEFGHIJKLMNOPQRSTUVWXYZ',
  u'common-unicode-ascii-safe-abcdefghijklmnopqrstuvwxyz',
  u'common-unicode-ascii-safe-0123456789',
  u'common-unicode-ascii-safe-:@$-_.!*()\',~',
  u'common-unicode-ascii-safe-unreserved-._~',
  u'common-unicode-ascii-safe-sub-delims-$!*()\',',
  u'common-unicode-ascii-safe-gen-delims-:@',
  u'common-unicode-ascii-escaped-"#<>[]^`{}|',
  u'common-unicode-ascii-escaped-tomcatBlocked-\\',
  u'common-unicode-ascii-escaped-tomcatBlocked-%5C',
  u'common-unicode-ascii-semi-colon-test-%3B',
  u'common-unicode-ascii-escaped-%',
  u'common-unicode-ascii-escaped-space x x',
  u'common-unicode-ascii-escape-anyway-+',
  u'common-unicode-ascii-escape-space-v-plus-+ +%20 %20+',
  u'path-unicode-ascii-safe-&=&=',
  u'path-unicode-ascii-escaped-;',
  u'path-unicode-ascii-escaped-?',
  u'path-unicode-ascii-escaped-/',
  u'path-unicode-ascii-escaped-%3F',
  u'path-unicode-ascii-escaped-%2F',
  u'path-unicode-ascii-escaped-double-//case',
  u'path-unicode-ascii-escaped-double-trailing//',
  u'path-unicode-ascii-escaped-double-%2F%2Fcase',
  u'path-unicode-ascii-escaped-double-trailing%2F%2F',
  u'query-unicode-ascii-safe-;',
  u'query-unicode-ascii-safe-/?',
  u'query-unicode-ascii-escaped-&=&=',
  u'fragment-unicode-ascii-safe-;',
  u'fragment-unicode-ascii-safe-&=&=/?',
  u'common-unicode-bmp-1byte-escaped-¡¢£',
  u'common-unicode-bmp-2byte-escaped-䦹䦺',
  u'common-unicode-supplementary-escaped-𐌔𐌕𐌖𐌗',
  u'query-unicode-ascii-escaped-this&that=theOther',
  u'common-ascii-doc-example-urn:lsid:ubio.org:namebank:11815',
  u'path-ascii-doc-example-10.1000/182',
  u'query-ascii-doc-example-10.1000/182',
  u'fragment-ascii-doc-example-10.1000/182',
  u'path-ascii-doc-example-http://example.com/data/mydata?row=24',
  u'query-ascii-doc-example-http://example.com/data/mydata?row=24',
  u'fragment-ascii-doc-example-http://example.com/data/mydata?row=24',
  u'path-ascii-doc-example-ldap://ldap1.example.net:6666/'
  u'o=University%20of%20Michigan, c=US??sub?(cn=Babs%20Jensen)',
  u'query-ascii-doc-example-ldap://ldap1.example.net:6666/'
  u'o=University%20of%20Michigan, c=US??sub?(cn=Babs%20Jensen)',
  u'fragment-ascii-doc-example-ldap://ldap1.example.net:6666/'
  u'o=University%20of%20Michigan, c=US??sub?(cn=Babs%20Jensen)',
  u'common-bmp-doc-example-ฉันกินกระจกได้',
  u'common-bmp-doc-example-Is féidir liom ithe gloine',
  u'decode-space-potential-error-unescaped-plus-+',
]
