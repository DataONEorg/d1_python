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
"""Test URL utilities
"""

# Stdlib
import os
import unittest

# D1
import d1_common.url

# App
import util

HERE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))


class TestUrl(unittest.TestCase):
  def setUp(self):
    self._unicode_strings = util.read_utf8_to_unicode(
      'testUnicodeStrings.utf8.txt'
    )

  def test_010(self):
    """encodePathElement()"""
    for row in self._unicode_strings.splitlines():
      self.assertTrue(isinstance(row, unicode))
      parts = row.split('\t')
      if len(parts) > 1:
        v = parts[0]
        if v.startswith('common') or v.startswith('path'):
          e = parts[1].strip()
          self.assertEqual(e, d1_common.url.encodePathElement(v))

  def test_020(self):
    """encodeQueryElement()"""
    for row in self._unicode_strings.splitlines():
      parts = row.split('\t')
      if len(parts) > 1:
        v = parts[0]
        if v.startswith('common') or v.startswith('query'):
          e = parts[1].strip()
          self.assertEqual(e, d1_common.url.encodeQueryElement(v))

  def test_030(self):
    """urlencode()"""
    data = [('a', '"#<>[]^`{}|'), ('b', '-&=&='),
            ('c', 'http://example.com/data/mydata?row=24')]
    expected = (
      'a=%22%23%3C%3E%5B%5D%5E%60%7B%7D%7C&b=-%26%3D%26%3D&c='
      'http://example.com/data/mydata?row%3D24'
    )
    test = d1_common.url.urlencode(data)
    self.assertEqual(test, expected)

  def test_040(self):
    """stripElementSlashes()"""
    self.assertEqual('element', d1_common.url.stripElementSlashes('/element'))
    self.assertEqual('element', d1_common.url.stripElementSlashes('//element/'))
    self.assertEqual('element', d1_common.url.stripElementSlashes('element/'))
    self.assertEqual(
      'ele/ment', d1_common.url.stripElementSlashes('/ele/ment/')
    )
    self.assertEqual(
      'ele//ment', d1_common.url.stripElementSlashes('ele//ment')
    )
    self.assertEqual('', d1_common.url.stripElementSlashes('/'))
    self.assertEqual('', d1_common.url.stripElementSlashes('//'))

  def test_050(self):
    """joinPathElements()"""
    self.assertEqual('a/b', d1_common.url.joinPathElements('a', 'b'))
    self.assertEqual('a/b/c', d1_common.url.joinPathElements('a/', '/b', 'c'))

  def test_055(self):
    """joinPathElementsNoStrip()"""
    self.assertEqual('', d1_common.url.joinPathElementsNoStrip(''))
    self.assertEqual('/', d1_common.url.joinPathElementsNoStrip('/'))
    self.assertEqual('//', d1_common.url.joinPathElementsNoStrip('//'))
    self.assertEqual('ab', d1_common.url.joinPathElementsNoStrip('ab'))
    self.assertEqual('a/b', d1_common.url.joinPathElementsNoStrip('a/b'))
    self.assertEqual('a/b', d1_common.url.joinPathElementsNoStrip('a', 'b'))
    self.assertEqual(
      'a/b/c', d1_common.url.joinPathElementsNoStrip('a', 'b', 'c')
    )
    self.assertEqual('a/b', d1_common.url.joinPathElementsNoStrip('a/', 'b'))
    self.assertEqual('a//b', d1_common.url.joinPathElementsNoStrip('a//', 'b'))
    self.assertEqual('a/b/', d1_common.url.joinPathElementsNoStrip('a/', 'b/'))
    self.assertEqual(
      'a//b///c', d1_common.url.joinPathElementsNoStrip('a//', 'b', '///c')
    )

  def test_060(self):
    """normalizeTarget()"""
    u0 = "http://some.server/base/mn/"
    u1 = "http://some.server/base/mn"
    u2 = "http://some.server/base/mn?"
    u3 = "http://some.server/base/mn/?"
    self.assertEqual(u0, d1_common.url.normalizeTarget(u0))
    self.assertEqual(u0, d1_common.url.normalizeTarget(u1))
    self.assertEqual(u0, d1_common.url.normalizeTarget(u2))
    self.assertEqual(u0, d1_common.url.normalizeTarget(u3))

  def test_070(self):
    """makeCNBaseURL()"""
    self.assertEqual(
      d1_common.url.makeCNBaseURL(''), 'https://cn.dataone.org/cn'
    )
    self.assertEqual(
      d1_common.url.makeCNBaseURL('test.com'), 'https://test.com/cn'
    )
    self.assertEqual(
      d1_common.url.makeCNBaseURL('test.com/cn'), 'https://test.com/cn'
    )
    self.assertEqual(
      d1_common.url.makeCNBaseURL('test.com/a/cn'), 'https://test.com/a/cn'
    )
    self.assertEqual(
      d1_common.url.makeCNBaseURL('http://test.com'), 'http://test.com/cn'
    )
    self.assertEqual(
      d1_common.url.makeCNBaseURL('http://test.com/'), 'http://test.com/'
    )
    self.assertEqual(
      d1_common.url.makeCNBaseURL('http://test.com/cn'), 'http://test.com/cn'
    )
    self.assertEqual(
      d1_common.url.makeCNBaseURL('http://test.com/a/b/c/cn'),
      'http://test.com/a/b/c/cn'
    )

  def test_080(self):
    """makeMNBaseURL()"""
    self.assertEqual(d1_common.url.makeMNBaseURL(''), 'https://localhost/mn')
    self.assertEqual(
      d1_common.url.makeMNBaseURL('test.com'), 'https://test.com/mn'
    )
    self.assertEqual(
      d1_common.url.makeMNBaseURL('test.com/mn'), 'https://test.com/mn'
    )
    self.assertEqual(
      d1_common.url.makeMNBaseURL('test.com/a/mn'), 'https://test.com/a/mn'
    )
    self.assertEqual(
      d1_common.url.makeMNBaseURL('http://test.com'), 'http://test.com/mn'
    )
    self.assertEqual(
      d1_common.url.makeMNBaseURL('http://test.com/'), 'http://test.com/'
    )
    self.assertEqual(
      d1_common.url.makeMNBaseURL('http://test.com/mn'), 'http://test.com/mn'
    )
    self.assertEqual(
      d1_common.url.makeMNBaseURL('http://test.com/a/b/c/mn'),
      'http://test.com/a/b/c/mn'
    )
