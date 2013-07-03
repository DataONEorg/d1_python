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
import os
import urllib
import logging

# Set up logger for this module.
log = logging.getLogger(__name__)
#Set level specific for this module if specified
try:
  log.setLevel(logging.getLevelName( \
               getattr(logging,'ONEDRIVE_MODULES')[__name__]) )
except:
  pass


def posix_filename_from_identifier(identifier):
  #TODO: This method of encoding is bad because it downgrades unicode and so
  # presents readability issues. The only character that *really* needs to be
  # escaped on posix systems is "/"
  #
  # On Windows, the following characters are not allowed:
  # \ / :  * ? " < > |
  # Linux
  return urllib.quote(identifier.encode('utf8'), safe='`@#~!$^&*()-=<>,.: ')


def posix_identifier_from_filename(filename):
  return urllib.unquote(filename).decode('utf8')


def windows_filename_from_identifier(identifier):
  return urllib.quote(identifier.encode('utf8'), safe='`@#~!$^&()-=,. ')


def windows_identifier_from_filename(filename):
  return urllib.unquote(filename).decode('utf8')


LINUX = ["posix", ]
WINDOWS = ["nt", ]

filename_from_identifier = posix_filename_from_identifier
identifier_from_filename = posix_identifier_from_filename

if os.name in WINDOWS:
  filename_from_identifier = windows_filename_from_identifier
  identifier_from_filename = windows_identifier_from_filename
