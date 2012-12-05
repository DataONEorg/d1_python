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
''':mod:`os_escape`
===================

:Synopsis:
 - Escape DataONE identifiers, so that they follow the filesystem conventions
   and restrictions for valid file- and folder names on a given OS.
 - Unescape the escaped file- and folder names to arrive at the original DataONE
  identifiers. 
:Author: DataONE (Dahl)

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

The current implementation simply uses URL percent-encoding of an UTF-8
encoding of the Unicode strings.
'''

# Stdlib.
import urllib


def filename_from_identifier(identifier):
  # "%" is not safe because it causes the URL "percent-encoding" to become
  # non-reversible.
  #
  # TODO: "@" and "#" are reserved as decorators for facet names and values.
  # They are only reserved as the first character. For now, they are allowed in
  # all positions because it allows escaping to be performed in a single
  # location (the root resolver), instead of individually by each resolver.
  #
  # On Windows, the following characters are not allowed:
  # \ / :  * ? " < > |
  return urllib.quote(identifier.encode('utf8'), safe='`@#~!$^&*()-=<>,.: ')


def identifier_from_filename(filename):
  return urllib.unquote(filename).decode('utf8')
