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
"""OS specific escaping

Escape DataONE identifiers, so that they follow the filesystem conventions and
restrictions for valid file- and folder names on a given OS.

Unescape the escaped file- and folder names to arrive at the original DataONE
identifiers.

DataONE supports identifiers containing characters that cannot (or should not)
be represented directly within the file- and folder names in a filesystem, such
as the path separator character ("/" on *nix). This module contains functions
for converting between DataONE identifiers and names that are suitable for use
as file- and folder names on the operating systems that are supported by
ONEDrive.

It is necessary to be able to get the original DataONE identifier given an
escaped name, so the escaping must be reversible. This is because the filesystem
driver (e.g., FUSE), passes the escaped name back to ONEDrive when the user
interacts with the file or folder.

The current implementation simply uses URL percent-encoding of an utf-8 encoding
of the Unicode strings.

Quote and unquote are somewhat borrowed from python urllib standard library.
"""

import logging
import os
import urllib.error
import urllib.parse
import urllib.request

log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)
_hexdig = '0123456789ABCDEFabcdef'
_hextochr = dict((a + b, chr(int(a + b, 16))) for a in _hexdig for b in _hexdig)

LINUX = [
  "posix",
]

WINDOWS = [
  "nt",
]


def unquote(s):
  """unquote('abc%20def') -> 'abc def'."""
  res = s.split('%')
  # fastpath
  if len(res) == 1:
    return s
  s = res[0]
  for item in res[1:]:
    try:
      s += _hextochr[item[:2]] + item[2:]
    except KeyError:
      s += '%' + item
    except UnicodeDecodeError:
      s += chr(int(item[:2], 16)) + item[2:]
  return s


def quote(s, unsafe='/'):
  """Pass in a dictionary that has unsafe characters as the keys, and the
  percent encoded value as the value.
  """
  res = s.replace('%', '%25')
  for c in unsafe:
    res = res.replace(c, '%' + (hex(ord(c)).upper())[2:])
  return res


def posix_filename_from_identifier(identifier):
  return urllib.parse.quote(
    identifier.encode('utf8'), safe='`@#~!$^&*()-=<>,.: '
  )


def posix_identifier_from_filename(filename):
  return urllib.parse.unquote(filename)


def windows_filename_from_identifier(identifier):
  """On Windows, the following characters are not allowed:
  \ / :  * ? " < > |
  """
  return quote(identifier, '\\/:*?"<>|')


def windows_identifier_from_filename(filename):
  return urllib.parse.unquote(filename)


identifier_from_filename = (
  windows_identifier_from_filename
  if os.name in WINDOWS else posix_identifier_from_filename
)
filename_from_identifier = (
  windows_filename_from_identifier
  if os.name in WINDOWS else posix_filename_from_identifier
)
