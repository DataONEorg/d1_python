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

import os

import d1_common.url

import d1_test.d1_test_case
import d1_test.sample

HERE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))


class TestUrl(d1_test.d1_test_case.D1TestCase):
  unicode_str_list = d1_test.sample.load_utf8_to_str(
    'testUnicodeStrings.utf8.txt'
  )

  def test_1000(self):
    """encodePathElement()"""
    for row in self.unicode_str_list.splitlines():
      assert isinstance(row, str)
      parts = row.split('\t')
      if len(parts) > 1:
        v = parts[0]
        if v.startswith('common') or v.startswith('path'):
          e = parts[1].strip()
          assert e == d1_common.url.encodePathElement(v)

  def test_1010(self):
    """encodeQueryElement()"""
    for row in self.unicode_str_list.splitlines():
      parts = row.split('\t')
      if len(parts) > 1:
        v = parts[0]
        if v.startswith('common') or v.startswith('query'):
          e = parts[1].strip()
          assert e == d1_common.url.encodeQueryElement(v)

  def test_1020(self):
    """urlencode()"""
    data = [('a', '"#<>[]^`{}|'), ('b', '-&=&='),
            ('c', 'http://example.com/data/mydata?row=24')]
    expected = (
      'a=%22%23%3C%3E%5B%5D%5E%60%7B%7D%7C&b=-%26%3D%26%3D&c='
      'http://example.com/data/mydata?row%3D24'
    )
    test = d1_common.url.urlencode(data)
    assert test == expected

  def test_1030(self):
    """stripElementSlashes()"""
    assert 'element' == d1_common.url.stripElementSlashes('/element')
    assert 'element' == d1_common.url.stripElementSlashes('//element/')
    assert 'element' == d1_common.url.stripElementSlashes('element/')
    assert 'ele/ment' == d1_common.url.stripElementSlashes('/ele/ment/')
    assert 'ele//ment' == d1_common.url.stripElementSlashes('ele//ment')
    assert '' == d1_common.url.stripElementSlashes('/')
    assert '' == d1_common.url.stripElementSlashes('//')

  def test_1040(self):
    """joinPathElements()"""
    assert 'a/b' == d1_common.url.joinPathElements('a', 'b')
    assert 'a/b/c' == d1_common.url.joinPathElements('a/', '/b', 'c')

  def test_1060(self):
    """normalizeTarget()"""
    u0 = "http://some.server/base/mn/"
    u1 = "http://some.server/base/mn"
    u2 = "http://some.server/base/mn?"
    u3 = "http://some.server/base/mn/?"
    assert u0 == d1_common.url.normalizeTarget(u0)
    assert u0 == d1_common.url.normalizeTarget(u1)
    assert u0 == d1_common.url.normalizeTarget(u2)
    assert u0 == d1_common.url.normalizeTarget(u3)

  def test_1070(self):
    """makeCNBaseURL()"""
    assert d1_common.url.makeCNBaseURL('') == 'https://cn.dataone.org/cn'
    assert d1_common.url.makeCNBaseURL('test.com') == 'https://test.com/cn'
    assert d1_common.url.makeCNBaseURL('test.com/cn') == 'https://test.com/cn'
    assert d1_common.url.makeCNBaseURL(
      'test.com/a/cn'
    ) == 'https://test.com/a/cn'
    assert d1_common.url.makeCNBaseURL(
      'http://test.com'
    ) == 'http://test.com/cn'
    assert d1_common.url.makeCNBaseURL('http://test.com/') == 'http://test.com/'
    assert d1_common.url.makeCNBaseURL(
      'http://test.com/cn'
    ) == 'http://test.com/cn'
    assert d1_common.url.makeCNBaseURL('http://test.com/a/b/c/cn') == \
      'http://test.com/a/b/c/cn'

  def test_1080(self):
    """makeMNBaseURL()"""
    assert d1_common.url.makeMNBaseURL('') == 'https://localhost/mn'
    assert d1_common.url.makeMNBaseURL('test.com') == 'https://test.com/mn'
    assert d1_common.url.makeMNBaseURL('test.com/mn') == 'https://test.com/mn'
    assert d1_common.url.makeMNBaseURL(
      'test.com/a/mn'
    ) == 'https://test.com/a/mn'
    assert d1_common.url.makeMNBaseURL(
      'http://test.com'
    ) == 'http://test.com/mn'
    assert d1_common.url.makeMNBaseURL('http://test.com/') == 'http://test.com/'
    assert d1_common.url.makeMNBaseURL(
      'http://test.com/mn'
    ) == 'http://test.com/mn'
    assert d1_common.url.makeMNBaseURL('http://test.com/a/b/c/mn') == \
      'http://test.com/a/b/c/mn'

  def test_1090(self):
    """Equivalent"""
    a = "HTTP://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k1=11&k2=abc&k3=def#frag"
    b = "Http://www.SOME.host:999/a/b/c/;p3;p1;p2?k2=abc&k3=def&k1=10&k1=11#frag"
    url_diff_list = d1_common.url.find_url_mismatches(a, b)
    assert url_diff_list == []

  def test_1100(self):
    """Equivalent, k2 moved"""
    a = "HTTP://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k1=11&k2=abc&k3=def#frag"
    b = "HTTP://www.some.host:999/a/b/c/;p1;p2;p3?k2=abc&k3=def&k1=10&k1=11#frag"
    url_diff_list = d1_common.url.find_url_mismatches(a, b)
    assert url_diff_list == []

  def test_1110(self):
    """Different params, p1 replaced with p4"""
    a = "http://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k2=abc#frag"
    b = "http://www.some.host:999/a/b/c/;p2;p4;p3?k1=10&k2=abc#frag"
    url_diff_list = d1_common.url.find_url_mismatches(a, b)
    assert url_diff_list == ['Parameters differ. a="p1, p2, p3" b="p2, p3, p4"']

  def test_1120(self):
    """Different params, p3 missing"""
    a = "http://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k2=abc#frag"
    b = "http://www.some.host:999/a/b/c/;p1;p2?k1=10&k2=abc#frag"
    url_diff_list = d1_common.url.find_url_mismatches(a, b)
    assert url_diff_list == ['Parameters differ. a="p1, p2, p3" b="p1, p2"']

  def test_1130(self):
    """Different query, second k11 key missing"""
    a = "http://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k1=11&k2=abc&k3=def#frag"
    b = "http://www.some.host:999/a/b/c/;p3;p1;p2?k2=abc&k3=def&k1=10#frag"
    url_diff_list = d1_common.url.find_url_mismatches(a, b)
    assert url_diff_list == [
      'Query values differ. key="k1" a_value="[\'10\', \'11\']" b_value="[\'10\']"'
    ]

  def test_1140(self):
    """Different query, value for k2 different"""
    a = "HTTP://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k1=11&k2=abc&k3=def#frag"
    b = "HTTP://www.some.host:999/a/b/c/;p1;p2;p3?k3=dex&k1=10&k1=11&k2=abc#frag"
    url_diff_list = d1_common.url.find_url_mismatches(a, b)
    assert url_diff_list == [
      'Query values differ. key="k3" a_value="[\'def\']" b_value="[\'dex\']"'
    ]
