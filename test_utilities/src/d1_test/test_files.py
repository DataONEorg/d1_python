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
"""Utilities for loading test files
"""
import codecs
import json
import logging
import os


# Path to the test document root, relative to this file
import d1_common
import d1_common.util
import d1_common.types
import d1_common.types.dataoneTypes


def get_abs_test_file_path(rel_path):
  return  os.path.join(d1_common.util.abs_path('./test_docs'), rel_path)


def load_bin(rel_path):
  bin_path = get_abs_test_file_path(rel_path)
  with open(bin_path, 'rb') as f:
    return f.read()

def load_utf8_to_str(rel_path, strip_xml_encoding_declaration=False):
  """Load file, decode from UTF-8 and return as str"""
  logging.debug('Loading test file. rel_path="{}"'.format(rel_path))
  utf8_path = get_abs_test_file_path(rel_path)
  with codecs.open(utf8_path, encoding='utf-8', mode='r') as f:
    unicode_str = f.read()
  # if strip_xml_encoding_declaration:
  #   unicode_str = re.sub(
  #     r'\s*encoding\s*=\s*"UTF-8"\s*', '', unicode_str, re.IGNORECASE
  #   )
  return unicode_str


def load_xml_to_pyxb(filename):
  return d1_common.types.dataoneTypes.CreateFromDocument(
    load_xml_to_str(filename)
  )

def load_xml_to_str(filename):
  return load_utf8_to_str(os.path.join('xml',  filename))


def load_json(filename):
  return json.loads(load_utf8_to_str(os.path.join('json',  filename)))


def load_cert(filename):
  return load_bin(os.path.join('cert',  filename))

def load_jwt(filename):
  return load_bin(os.path.join('jwt',  filename))


def _load_tricky_identifier_list():
  return [
    s.strip().split('\t') for s in
    # load_utf8_to_str('tricky_identifiers_unicode.utf8.txt').splitlines()
    load_utf8_to_str('combined_tricky_identifiers_unicode.utf8.txt').splitlines()
    if not s.startswith('#') and len(s) == 2
  ]

# List of Unicode identifiers that use various reserved characters and
# embedded URL segments. Each item in the list is a a 2-tuple where the first
# value is a Unicode identifier and the second is a URL escaped version of the
# identifier.
TRICKY_IDENTIFIER_LIST = _load_tricky_identifier_list()
