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
'''
:mod:`delete_all_objects_of_type`
=================================

:Synopsis:
  This is an example on how to use the DataONE Client Library for Python. It
  shows how to:

  - Retrieve a list of all objects with specific FormatID on a Member
    Node.
  - Delete all objects with a specific FormatID from a Member Node.

  Notes:

  - The objects are deleted with the MNStorage.delete() API method.
  - MNStorage.delete() should NOT be used on a node that is in DataONE's
    production environment except under specific circumstances.
  - Do not use this script to delete undesired objects from a production Member
    Node.
  - MNStorage.delete() is only available to subjects which have delete
    permission on the node.
  - To delete all the objects on the node, remove the formatId and replicaStatus
    parameters in the listObjects() call below.
  - The Member Node object list is retrieved in small sections, called pages.
    The objects on each page are processed before retrieving the next page.
  - The listObjects() Member Node API method may not be efficiently implemented
    by all Member Nodes as it is intended primarily for use by Coordinating
    Nodes.
  - The listObjects() method may miss objects that are created while the method
    is in use.

:Author:
  DataONE (Dahl)

:Created:
  2013-10-21

:Requires:
  - Python 2.6 or 2.7.
  - DataONE Common Library for Python (automatically installed as a dependency)
  - DataONE Client Library for Python (sudo pip install dataone.libclient)
'''

# Stdlib.
import codecs
import datetime
import hashlib
import logging
import os
import shutil
import sys
import urllib

# 3rd party.
import pyxb

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.types.exceptions
import d1_common.const
import d1_client.data_package
import d1_client.cnclient
import d1_client.mnclient

# Config.

# The Member Node from which objects are deleted.
MEMBER_NODE_BASE_URL = 'http://127.0.0.1:8000'

# Delete objects of this type. A complete list of valid formatIds can be
# found at https://cn.dataone.org/cn/v1/formats
LIST_OBJECTS_FORMAT_ID = 'eml://ecoinformatics.org/eml-2.1.1'

# The number of objects to list each time listObjects() is called.
LIST_OBJECTS_PAGE_SIZE = 100

# Paths to the certificate and key to use when deleting the objects. If the
# certificate has the key embedded, the _KEY setting should be set to None. The
# Member Node must trust the certificate and allow access to
# MNStorage.listObjects() and MNStorage.delete() for the certificate subject. If
# the target Member Node is a DataONE Generic Member Node (GMN) instance, see
# the "Using GMN" section in the documentation for GMN for information on how to
# create and use certificates. The information there may be relevant for other
# types of Member Nodes as well.
CERTIFICATE = 'client.crt'
CERTIFICATE_KEY = 'client.key'


def main():
  # Setting the default logger to level "DEBUG" causes the script to become
  # very verbose.
  logging.getLogger('').setLevel(logging.DEBUG)

  member_node_object_deleter = MemberNodeObjectDeleter(MEMBER_NODE_BASE_URL)
  member_node_object_deleter.delete_objects_from_member_node()

# ==============================================================================


class MemberNodeObjectDeleter(object):
  def __init__(self, base_url):
    self._base_url = base_url
    self._mn_client = d1_client.mnclient.MemberNodeClient(
      self._base_url, cert_path=CERTIFICATE,
      key_path=CERTIFICATE_KEY
    )

  def delete_objects_from_member_node(self):
    logging.info('Deleting objects from Member Node: {0}'.format(self._base_url))
    current_start = 0
    while True:
      try:
        object_list = self._mn_client.listObjects(
          start=current_start,
          count=LIST_OBJECTS_PAGE_SIZE,
          objectFormat=LIST_OBJECTS_FORMAT_ID,
          replicaStatus=False
        )
      except d1_common.types.exceptions.DataONEException as e:
        logging.exception('listObjects() failed with exception:')
        raise

      logging.info(
        'Retrieved page: {0}/{1} ({2} objects)'.format(
          current_start / LIST_OBJECTS_PAGE_SIZE + 1, object_list.total /
          LIST_OBJECTS_PAGE_SIZE + 1, object_list.count
        )
      )

      for d1_object in object_list.objectInfo:
        self._delete_object(d1_object)

      current_start += object_list.count
      if current_start >= object_list.total:
        break

  def _delete_object(self, d1_object):
    pid = d1_object.identifier.value()
    try:
      return self._mn_client.delete(pid)
    except d1_common.types.exceptions.DataONEException as e:
      logging.exception('getSystemMetadata() failed with exception:')
      raise


if __name__ == '__main__':
  main()
