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
:mod:`test_utilities`
=====================

:Synopsis: Testing utilities
:Created: 2011-04-22
:Author: DataONE (Dahl)
'''

import os
import sys
import hashlib


def log_setup():
  # Set up logging.
  # We output everything to both file and stdout.
  logging.getLogger('').setLevel(logging.DEBUG)
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  file_logger = logging.FileHandler(os.path.splitext(__file__)[0] + '.log', 'a')
  file_logging.setFormatter(formatter)
  logging.getLogger('').addHandler(file_logger)
  console_logger = logging.StreamHandler(sys.stdout)
  console_logging.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def calculate_checksum(flo, algorithm):
  '''Given a file like object and a ChecksumAlgorithm value,
  calculate the checksum.'''
  checksum_calculator_map = {
    'SHA-1': hashlib.sha1(),
    'SHA-224': hashlib.sha224(),
    # TODO: SHA-356 is supported by DataONE but is not in the hashlib. Will
    # probably need to get it from somewhere else.
    #'SHA-356': hashlib.sha356,
    'SHA-384': hashlib.sha384(),
    'SHA-512': hashlib.sha512(),
    'MD5': hashlib.md5(),
  }
  try:
    hash = checksum_calculator_map[algorithm]
  except LookupError:
    raise Exception('Not a valid DataONE Checksum Algorithm: '.format(algorithm))
  for chunk in iter(lambda: flo.read(1024 * hash.block_size), ''):
    hash.update(chunk)
  return hash.hexdigest()


def get_size(flo):
  '''Read an entire file like object to find its size.
  For use when the object does not support seek() or len().
  '''
  size = 0
  for chunk in iter(lambda: flo.read(1024**2), ''):
    size += len(chunk)
  return size


def find_random_existing_pid(client):
  object_list = client.listObjects(context.TOKEN)
  assertTrue(object_list.count > 0, 'No objects to perform test on')
  return object_list.objectInfo[0].identifier.value()


def get_object_info_by_identifer(pid):
  client = d1_client.client.DataOneClient(context.node['baseurl'])
  object_list = client.listObjects(context.TOKEN)
  for o in object_list['objectInfo']:
    if o["identifier"].value() == pid:
      return o
  assertTrue(False)
