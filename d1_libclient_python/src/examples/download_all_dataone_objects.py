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
:mod:`download_all_dataone_objects`
===================================

:Synopsis:
  This is an example on how to use the DataONE Client Library for Python. It
  shows how to:

  - Retrieve a list of all DataONE Member Nodes
  - Retrieve a list of all objects of specific FormatID on each of those Member
    Nodes.
  - Retrieve and examine the System Metadata for each of the listed objects.
  - Based on information in the System Metadata, determine if the corresponding
    object should be downloaded.
  - Download the corresponding object.

  Notes:

  - This approach retrieves object lists directly from each Member Node and is
    mainly suitable in special situations where a 3rd party wishes to examine
    the overal state of objects in DataONE, for instance, for creating
    statistics or data quality reports.
  - This approach uses the listObjects() Member Node API method, which has very
    limited filtering facilities. The example shows how to use this filtering to
    list objects that are of a specific type (FormatID) and that are native to
    the Member Node (i.e., not replicas). If a more specific set of objects is
    desired, it is better to use DataONE's query interface, which offers much
    richer filtering facilities.
  - It is not possible to filter out non-public objects with listObjects().
    Instead, this script attempts to download the object's System Metadata and
    checks for NotAuthorized exceptions.
  - If a completely unfiltered object list is required, simply remove the
    formatId and replicaStatus parameters in the listObjects() call below.
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
  2013-05-30

:Requires:
  - Python 2.6 or 2.7.
  - DataONE Common Library for Python (automatically installed as a dependency)
  - DataONE Client Library for Python (sudo pip install dataone.libclient)
"""

# Stdlib
import logging
import os
import shutil
import urllib

# D1
import d1_common.types.exceptions
import d1_common.const
import d1_client.data_package
import d1_client.cnclient
import d1_client.mnclient

# Config.

# In addition to the default production environment, DataONE maintains several
# separate environments for use when developing and testing DataONE components.
# There are no connections between the environments. For instance, certificates,
# DataONE identities and science objects are exclusive to the environment in
# which they were created. This setting controls to which environment the CN
# client connects.

# Round-robin CN endpoints
DATAONE_ROOT = d1_common.const.URL_DATAONE_ROOT # (recommended, production)
#DATAONE_ROOT = 'https://cn-dev.test.dataone.org/cn'
#DATAONE_ROOT = 'https://cn-stage.test.dataone.org/cn'
#DATAONE_ROOT = 'https://cn-sandbox.dataone.org/cn'
#DATAONE_ROOT = 'https://cn-stage.dataone.org/cn/'
#DATAONE_ROOT = 'https://cn-stage.test.dataone.org/cn'

# Only retrieve objects of this type. A complete list of valid formatIds can be
# found at https://cn.dataone.org/cn/v1/formats
LIST_OBJECTS_FORMAT_ID = 'eml://ecoinformatics.org/eml-2.1.1'

# The number of objects to list each time listObjects() is called.
LIST_OBJECTS_PAGE_SIZE = 100

# The location in which to store downloaded objects.
DOWNLOAD_FOLDER = './d1_objects'

# Don't download objects larger than this size.
MAX_FILE_SIZE_TO_DOWNLOAD = 1024**2


def main():
  logging.basicConfig()
  # Setting the default logger to level "DEBUG" causes the script to become
  # very verbose.
  logging.getLogger('').setLevel(logging.DEBUG)

  try:
    os.makedirs(DOWNLOAD_FOLDER)
  except OSError:
    pass

  node_list = get_node_list_from_coordinating_node()
  for node in node_list.node:
    if is_member_node(node):
      member_node_object_downloader = MemberNodeObjectDownloader(node)
      member_node_object_downloader.download_objects_from_member_node()


def get_node_list_from_coordinating_node():
  cn_client = d1_client.cnclient.CoordinatingNodeClient(base_url=DATAONE_ROOT)
  try:
    return cn_client.listNodes()
  except d1_common.types.exceptions.DataONEException:
    logging.exception('listNodes() failed with exception:')
    raise


def is_member_node(node):
  return node.type == 'mn'


# ==============================================================================


class MemberNodeObjectDownloader(object):
  def __init__(self, node):
    self._node = node
    self._mn_client = d1_client.mnclient_2_0.MemberNodeClient_2_0(node.baseURL)

  def download_objects_from_member_node(self):
    logging.info(
      'Retrieving objects for Member Node: {0}'.format(self._node.name)
    )
    current_start = 0
    while True:
      try:
        object_list = self._mn_client.listObjects(
          start=current_start, count=LIST_OBJECTS_PAGE_SIZE,
          objectFormat=LIST_OBJECTS_FORMAT_ID, replicaStatus=False
        )
      except d1_common.types.exceptions.DataONEException:
        logging.exception('listObjects() failed with exception:')
        raise
      else:
        current_start += object_list.count
        if current_start >= object_list.total:
          break

        logging.info(
          'Retrieved page: {0}/{1}'.format(
            current_start / LIST_OBJECTS_PAGE_SIZE + 1, object_list.total /
            LIST_OBJECTS_PAGE_SIZE
          )
        )

        for d1_object in object_list.objectInfo:
          self._download_d1_object_if_public(d1_object)

  def _download_d1_object_if_public(self, d1_object):
    pid = d1_object.identifier.value()
    sys_meta = self._get_d1_object_system_metadata(pid)
    if sys_meta is not None:
      # The System Metadata object can be examined to determine system level
      # details about the corresponding object.
      if sys_meta.size < MAX_FILE_SIZE_TO_DOWNLOAD:
        self.download_d1_object(pid)

  def _get_d1_object_system_metadata(self, pid):
    try:
      return self._mn_client.getSystemMetadata(pid)
    except d1_common.types.exceptions.NotAuthorized:
      logging.info('Ignoring non-public object: {0}'.format(pid))
    except d1_common.types.exceptions.DataONEException:
      logging.exception('getSystemMetadata() failed with exception:')
      raise

  def download_d1_object(self, pid):
    try:
      object_stream = self._mn_client.get(pid)
    except d1_common.types.exceptions.DataONEException:
      logging.exception('get() failed with exception:')
      raise
    else:
      # The PID (DataONE Persistent Identifier) can contain characters that are
      # not valid for use as filenames (most commonly, slashes). A simple way to
      # make a PID safe for use as a filename is to "percent-encode" it.
      pid_filename = urllib.quote(pid, safe='')
      with open(os.path.join(DOWNLOAD_FOLDER, pid_filename), 'wb') as f:
        shutil.copyfileobj(object_stream, f)


if __name__ == '__main__':
  main()
