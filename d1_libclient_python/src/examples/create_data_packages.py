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
"""
:mod:`create_data_package`
==========================

:Synopsis:
  This is an example on how to use the DataONE Client Library for Python. It
  shows how to:

  - Automatically create data packages from local objects.
  - Generate the system metadata for a local file.
  - Generate an access policy for public access.
  - Upload the local files to a Member Node as science Science Object.
  - Create the data packages on the Member Node.

:Author:
  DataONE (Dahl)

:Created:
  2013-02-27

:Requires:
  - Python 2.6 or 2.7.
  - DataONE Common Library for Python (automatically installed as a dependency)
  - DataONE Client Library for Python (sudo pip install dataone.libclient)
  - A client side certificate that is trusted by the target Member Node.

:Operation:
  Data packages are created from files in a folder provided by the user.
  Files with the same basename are combined into a package, with the basename
  being the name of the package.

  Example:

  The files

    myfile.1.txt
    myfile.2.txt
    myfile.jpg

  would be grouped into a package because they share the same basename. First,
  each of the files would be uploaded to the Member Node separately. The full
  filename is used as the PID.

  For each file, a system metadata file is generated, based on information
  from the file and from a set of fixed settings.

  Then, a package for all the files is generated. System metadata is generated
  for the package, and the package is uploaded to the Member Node.
"""

# Stdlib
import datetime
import hashlib
import logging
import os
import StringIO

# D1
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.const
import d1_client.data_package
import d1_client.mnclient

# Config.

# The path to the files that will be uploaded as science objects.
SCIENCE_OBJECTS_DIR_PATH = './testfiles'

# The identifier (PID) to use for the Science Object.
SCIENCE_OBJECT_PID = 'dataone_test_object_pid'

# The formatId to use for the Science Object. It should be the ID of an Object
# Format that is registered in the DataONE Object Format Vocabulary. A list of
# valid IDs can be retrieved from https://cn.dataone.org/cn/v1/formats.
SYSMETA_FORMATID = 'application/octet-stream'

# The DataONE subject to set as the rights holder of the created objects. The
# rights holder must be a subject that is registered with DataONE. Subjects are
# created in the DataONE identity manager at https://cn.dataone.org/cn/portal.
#
# By default, only the rights holder has access to the object, so access to the
# uploaded object may be lost if the rights holder subject is set to a
# non-existing subject or to a subject that is not prepared to handle the
# object.
SYSMETA_RIGHTSHOLDER = 'CN=First Last,O=Google,C=US,DC=cilogon,DC=org'

# BaseURL for the Member Node. If the script is run on the same server as the
# Member Node, this can be localhost.
MN_BASE_URL = 'http://localhost:8000'
#MN_BASE_URL = 'https://localhost/mn'

# Paths to the certificate and key to use when creating the object. If the
# certificate has the key embedded, the _KEY setting should be set to None. The
# Member Node must trust the certificate and allow access to MNStorage.create()
# for the certificate subject. If the target Member Node is a DataONE Generic
# Member Node (GMN) instance, see the "Using GMN" section in the documentation
# for GMN for information on how to create and use certificates. The information
# there may be relevant for other types of Member Nodes as well.
CERTIFICATE_FOR_CREATE = 'client.crt'
CERTIFICATE_FOR_CREATE_KEY = 'client.key'

# Constants.

RESOURCE_MAP_FORMAT_ID = 'http://www.openarchives.org/ore/terms'


def main():
  logging.basicConfig()
  logging.getLogger('').setLevel(logging.DEBUG)

  # Create a Member Node client that can be used for running commands against
  # a specific Member Node.
  client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
    MN_BASE_URL, cert_path=CERTIFICATE_FOR_CREATE,
    key_path=CERTIFICATE_FOR_CREATE_KEY
  )
  # Iterate over the object groups and create them and their resource maps
  # on the Member Node.
  for group in find_file_groups(SCIENCE_OBJECTS_DIR_PATH):
    print 'Group: {0}'.format(group)
    files_in_group = find_files_in_group(SCIENCE_OBJECTS_DIR_PATH, group)
    if len(files_in_group) < 2:
      raise Exception('Each group must have at least 2 files')
    for file_path in files_in_group:
      print '  File: {0}'.format(file_path)
      create_science_object_on_member_node(client, file_path)
    create_package_on_member_node(client, files_in_group)

  print 'Objects created successfully'


# Create the object on the Member Node. The create() call takes an open
# file-like object for the Science Object. Since we already have the data in a
# string, we use StringIO. Another way would be to open the file again, with "f
# = open(filename, 'rb')", and then pass "f". The StringIO method is more
# efficient if the file fits in memory, as it already had to be read from disk
# once, for the MD5 checksum calculation.
def create_science_object_on_member_node(client, file_path):
  pid = os.path.basename(file_path)
  sci_obj = open(file_path, 'rb').read()
  sys_meta = generate_system_metadata_for_science_object(
    pid, SYSMETA_FORMATID, sci_obj
  )
  client.create(pid, StringIO.StringIO(sci_obj), sys_meta)


def create_package_on_member_node(client, files_in_group):
  package_pid = group_name(files_in_group[0])
  pids = [os.path.basename(p) for p in files_in_group]
  resource_map = create_resource_map_for_pids(package_pid, pids)
  sys_meta = generate_system_metadata_for_science_object(
    package_pid, RESOURCE_MAP_FORMAT_ID, resource_map
  )
  client.create(package_pid, StringIO.StringIO(resource_map), sys_meta)


def create_resource_map_for_pids(package_pid, pids):
  # Create a resource map generator that will generate resource maps that, by
  # default, use the DataONE production environment for resolving the object
  # URIs. To use the resource map generator in a test environment, pass the base
  # url to the root CN in that environment in the dataone_root parameter.
  resource_map_generator = d1_client.data_package.ResourceMapGenerator()
  return resource_map_generator.simple_generate_resource_map(
    package_pid, pids[0], pids[1:]
  )


# Create the System Metadata for the object that is to be uploaded. The System
# Metadata contains information about the object, such as its format, access
# control list and size.
def generate_system_metadata_for_science_object(pid, format_id, science_object):
  size = len(science_object)
  md5 = hashlib.md5(science_object).hexdigest()
  now = datetime.datetime.now()
  sys_meta = generate_sys_meta(pid, format_id, size, md5, now)
  return sys_meta


def generate_sys_meta(pid, format_id, size, md5, now):
  sys_meta = dataoneTypes.systemMetadata()
  sys_meta.identifier = pid
  sys_meta.formatId = format_id
  sys_meta.size = size
  sys_meta.rightsHolder = SYSMETA_RIGHTSHOLDER
  sys_meta.checksum = dataoneTypes.checksum(md5)
  sys_meta.checksum.algorithm = 'MD5'
  sys_meta.dateUploaded = now
  sys_meta.dateSysMetadataModified = now
  sys_meta.accessPolicy = generate_public_access_policy()
  return sys_meta


def generate_public_access_policy():
  accessPolicy = dataoneTypes.accessPolicy()
  accessRule = dataoneTypes.AccessRule()
  accessRule.subject.append(d1_common.const.SUBJECT_PUBLIC)
  permission = dataoneTypes.Permission('read')
  accessRule.permission.append(permission)
  accessPolicy.append(accessRule)
  return accessPolicy


def find_file_groups(directory_path):
  groups = set()
  for file_name in os.listdir(directory_path):
    groups.add(group_name(file_name))
  return sorted(list(groups))


def find_files_in_group(directory_path, group):
  return sorted([
    os.path.join(directory_path, p)
    for p in os.listdir(directory_path) if p.startswith(group)
  ])


def group_name(file_path):
  n = os.path.basename(file_path)
  return n[:n.find('.')]


def base_name_without_extension(file_path):
  return os.path.splitext(os.path.basename(file_path))[0]


if __name__ == '__main__':
  main()
