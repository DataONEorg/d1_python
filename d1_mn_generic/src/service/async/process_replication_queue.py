#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`process_replication_queue`
================================

:Synopsis: 
  Iterate over queue of objects registered for replication and attempt to
  replicate them.
:Created: 2011-01-01
:Author: DataONE (Dahl)
"""

# Stdlib.
import datetime
import glob
import hashlib
import httplib
import logging
import optparse
import os
import re
import shutil
import stat
import sys
import time
import tempfile
import urllib
import urlparse
import uuid

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.types.exceptions
import d1_common.util
import d1_common.date_time
import d1_common.url
import d1_client.mnclient
import d1_client.cnclient

# App.
sys.path.append('../types/generated')
import gmn_types


class ReplicateError(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return str(self.value)

# ==============================================================================


class GMNReplicationClient(d1_client.mnclient.MemberNodeClient):
  '''Extend the d1_client.MemberNodeClient class with wrappers for the internal
  GMN REST calls that support the replication process.
  '''

  def __init__(
    self,
    base_url,
    timeout=d1_common.const.RESPONSE_TIMEOUT,
    defaultHeaders=None,
    cert_path=None,
    key_path=None,
    strict=True,
    capture_response_body=False,
    version='internal',
    types=gmn_types
  ):

    d1_client.mnclient.MemberNodeClient.__init__(
      self,
      base_url=base_url,
      timeout=timeout,
      defaultHeaders=defaultHeaders,
      cert_path=cert_path,
      key_path=key_path,
      strict=strict,
      capture_response_body=capture_response_body,
      version=version,
      types=types
    )

    self.logger = logging.getLogger(self.__class__.__name__)

  def internal_replicate_task_get(self):
    url = self._rest_url('replicate/task_get')
    response = self.GET(url)
    return self._read_dataone_type_response(response)

  def update_replicate_task_status(self, task_id, status):
    url = self._rest_url(
      'replicate/task_update/%(task_id)s/%(status)s',
      task_id=str(task_id),
      status=status
    )
    response = self.GET(url)
    return self._read_boolean_response(response)

  #@util.utf8_to_unicode
  def internal_replicate_create(self, pid, sci_obj, sysmeta, vendorSpecific=None):
    '''Create replica of object on GMN'''
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('replicate/create/%(pid)s', pid=pid)
    mime_multipart_fields = [('pid', pid.encode('utf-8')), ]
    mime_multipart_files = [
      ('object', 'content.bin', sci_obj),
      ('sysmeta', 'sysmeta.xml', sysmeta),
    ]
    response = self.POST(
      url,
      fields=mime_multipart_fields,
      files=mime_multipart_files,
      headers=vendorSpecific
    )
    return self._read_boolean_response(response)

#===============================================================================


class ProcessReplicationQueue(object):
  def __init__(self, options):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.options = options
    self.gmn_client = GMNReplicationClient(self.options.gmn_url)
    self.cn_client = self._create_cn_client()
    self._process_replication_queue()

  def _create_cn_client(self):
    return d1_client.cnclient.CoordinatingNodeClient(
      cert_path='./urnnodemnDevGMN.crt',
      key_path='./privkey.pem'
    )

  def _process_replication_queue(self):
    while self._process_replication_task():
      pass

  def _process_replication_task(self):
    task = self._get_next_replication_task()
    if not task:
      return False
    self._replicate(task)
    return True

  def _get_next_replication_task(self):
    try:
      return self.gmn_client.internal_replicate_task_get()
    except d1_common.types.exceptions.NotFound:
      return None

  def _replicate(self, task):
    s = d1_common.types.exceptions.InvalidSystemMetadata(0, 'test')
    self._cn_replicate_task_update(task, 'requested', s)
    #self._update_replicate_task_status(task, 'in progress')
    try:
      sysmeta_tmp_file = self._get_system_metadata(task)
      science_data_tmp_file = self._get_science_data(task)
      self._gmn_replicate_create(task, science_data_tmp_file, sysmeta_tmp_file)
    except (d1_common.types.exceptions.DataONEException, ReplicateError) as e:
      self.logger.error(e)
      try:
        self._cn_replicate_task_update(task, 'failed')
      except Exception as e:
        self.logger.error(e)
      #self._update_replicate_task_status(task, 'completed')
    else:
      try:
        self._cn_replicate_task_update(task, 'completed')
      except Exception as e:
        self.logger.error(e)
      #self._update_replicate_task_status(task, 'completed')

  def _update_replicate_task_status(self, task, status):
    return self.gmn_client.update_replicate_task_status(task.taskId, status)

  def _get_system_metadata(self, task):
    sysmeta_stream = self._open_sysmeta_stream_on_coordinating_node(task.pid)
    return self._copy_stream_to_tmp_file(sysmeta_stream)

  def _open_sysmeta_stream_on_coordinating_node(self, pid):
    return self.cn_client.getSystemMetadataResponse(pid)

  def _get_science_data(self, task):
    source_node_base_url = self._resolve_source_node_id_to_base_url(task.sourceNode)
    mn_client = d1_client.mnclient.MemberNodeClient(base_url=source_node_base_url)
    sci_data_stream = self._open_sci_obj_stream_on_member_node(mn_client, task.pid)
    return self._copy_stream_to_tmp_file(sci_data_stream)

  def _copy_stream_to_tmp_file(self, stream):
    f = tempfile.TemporaryFile()
    shutil.copyfileobj(stream, f)
    f.seek(0)
    return f

  def _resolve_source_node_id_to_base_url(self, source_node):
    node_list = self._get_node_list()
    for node in node_list.node:
      if node.identifier.value() == source_node:
        return node.baseURL
    raise ReplicateError('Unable to resolve Source Node ID: {0}'.format(source_node))

  def _get_node_list(self):
    return self.cn_client.listNodes()

  def _open_sci_obj_stream_on_member_node(self, gmn_client, pid):
    return gmn_client.get(pid)

#  def _cn_get_system_metadata_serial_version(self, pid):
#    sysmeta = self.cn_client.getSystemMetadata(pid)
#    return sysmeta.serialVersion

  def _cn_replicate_task_update(self, task, status, dataone_error=None):
    #    serial_version = self._cn_get_system_metadata_serial_version(task.pid)
    self.cn_client.setReplicationStatus(task.pid, task.sourceNode, status, dataone_error)

  def _gmn_replicate_create(self, task, sci_obj, sysmeta):
    return self.gmn_client.internal_replicate_create(task.pid, sci_obj, sysmeta)

  # old streaming code 
  #  # Find size of sci_obj.
  #  src = GMNReplicationClient(base_url)
  #  sysmeta_obj = src.getSystemMetadata(replication_request.pid)
  #  obj_size = sysmeta_obj.size
  #  # Stream.
  #  object_file = src.get(replication_request.pid)
  #  sysmeta_xml = src.getSystemMetadataResponse(replication_request.pid).read()
  #  dst = GMNReplicationClient('http://0.0.0.0:8000/')
  #  # Add the ability to do len() on object_file. Needed by mime_multipart.
  #  object_file.__len__ = lambda x=None: int(obj_size)
  #  dst.create(replication_request.pid, object_file, sysmeta_xml)

  #===============================================================================


def log_setup():
  # Set up logging.
  # We output everything to both file and stdout.
  logging.getLogger('').setLevel(logging.DEBUG)
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(name)s '
    '%(message)s', '%y/%m/%d %H:%M:%S'
  )
  file_logger = logging.FileHandler(os.path.splitext(__file__)[0] + '.log', 'a')
  file_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(file_logger)
  # Stdout.
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  log_setup()

  # Command line options.
  parser = optparse.OptionParser()
  parser.add_option(
    '--gmn-url',
    dest='gmn_url',
    action='store',
    type='string',
    default='http://0.0.0.0:8000'
  )
  parser.add_option('--verbose', action='store_true', default=False, dest='verbose')

  (options, args) = parser.parse_args()

  #  if not options.verbose:
  #    logging.getLogger('').setLevel(logging.ERROR)

  logging.getLogger('').setLevel(logging.DEBUG)

  ProcessReplicationQueue(options)


if __name__ == '__main__':
  main()
