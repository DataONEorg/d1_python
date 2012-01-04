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


def gmn_vse_provide_subject(subject):
  '''GMN Vendor Specific Extension: Simulate subject.'''
  return {'VENDOR_OVERRIDE_SESSION': subject}


def gmn_vse_enable_sql_profiling():
  '''GMN Vendor Specific Extension: Enable SQL profiling.'''
  return {'VENDOR_PROFILE_SQL': 1}


def gmn_vse_enable_python_profiling():
  '''GMN Vendor Specific Extension: Enable Python profiling.'''
  return {'VENDOR_PROFILE_PYTHON': 1}


def get_resource_path(path):
  '''Get path to test resources.'''
  resource_path = os.path.abspath(
    os.path.join(
      os.path.dirname(
        __file__
      ), '../../../../resources/'
    )
  )
  return os.path.join(resource_path, path)


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


def find_valid_pid(client):
  '''Find the PID of an object that exists on the server.
  '''
  # Verify that there's at least one object on server.
  object_list = client.listObjects(context.TOKEN)
  assertTrue(object_list.count > 0, 'No objects to perform test on')
  # Get the first PID listed. The list is in random order.
  return object_list.objectInfo[0].identifier.value()


def get_object_info_by_identifer(pid):
  client = d1_client.client.DataOneClient(context.node['baseurl'])

  # Get object collection.
  object_list = client.listObjects(context.TOKEN)

  for o in object_list['objectInfo']:
    if o["identifier"].value() == pid:
      return o

  # Object not found
  assertTrue(False)


def gen_sysmeta(pid, size, md5, now):
  return u'''<?xml version="1.0" encoding="UTF-8"?>
    <D1:systemMetadata xmlns:D1="http://dataone.org/service/types/0.5.1">
    <identifier>{0}</identifier>
    <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
    <size>{1}</size>
    <submitter>test</submitter>
    <rightsHolder>test</rightsHolder>
    <checksum algorithm="MD5">{2}</checksum>
    <dateUploaded>{3}</dateUploaded>
    <dateSysMetadataModified>{3}</dateSysMetadataModified>
    <originMemberNode>MN1</originMemberNode>
    <authoritativeMemberNode>MN1</authoritativeMemberNode>
    </D1:systemMetadata>
    '''.format(
    escape(pid), size, md5, datetime.datetime.isoformat(now))


def unicode_test_1():
  '''GMN and libraries handle Unicode correctly.
  '''
  client = test_client.TestClient(context.node['baseurl'])

  test_doc_path = os.path.join(
    opts.int_path, 'src', 'test', 'resources', 'd1_testdocs', 'encodingTestSet'
  )
  test_ascii_strings_path = os.path.join(test_doc_path, 'testAsciiStrings.utf8.txt')

  file_obj = codecs.open(test_ascii_strings_path, 'r', 'utf-8')
  for line in file_obj:
    line = line.strip()
    try:
      pid_unescaped, pid_escaped = line.split('\t')
    except ValueError:
      pass

    # Create a small test object containing only the pid.
    scidata = pid_unescaped.encode('utf-8')

    # Create corresponding System Metadata for the test object.
    size = len(scidata)
    # hashlib.md5 can't hash a unicode string. If it did, we would get a hash
    # of the internal Python encoding for the string. So we maintain scidata as a utf-8 string.
    md5 = hashlib.md5(scidata).hexdigest()
    now = datetime.datetime.now()
    sysmeta_xml = gen_sysmeta(pid_unescaped, size, md5, now)

    # Create the object on GMN.
    client.create(pid_unescaped, StringIO.StringIO(scidata), StringIO.StringIO(sysmeta_xml), {})

    # Retrieve the object from GMN.
    scidata_retrieved = client.get(pid_unescaped).read()
    sysmeta_obj_retrieved = client.getSystemMetadata(pid_unescaped)

    # Round-trip validation.
    assertEqual(scidata_retrieved, scidata)
    assertEqual(sysmeta_obj_retrieved.identifier.value(), scidata)
