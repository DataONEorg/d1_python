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

# Django.
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.core.management.base import NoArgsCommand
from django.core.management.base import CommandError
from django.http import HttpResponse
from django.http import Http404
from django.template import Context
from django.template import loader
from django.shortcuts import render_to_response
from django.utils.html import escape

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.types.exceptions
import d1_common.util
import d1_common.date_time
import d1_common.url
import d1_client.d1client

# App.
import gmn_types
import mn.models
import mn.auth
import mn.util
import settings


class GMNReplicationClient(d1_client.mnclient.MemberNodeClient):
  '''Extend the d1_client.MemberNodeClient class with wrappers for the internal
  GMN REST calls that support the replication process.
  '''
  def __init__(self,
               baseurl=settings.LOCAL_BASE_URL,
               defaultHeaders=None,
               timeout=1000,
               keyfile=settings.CLIENT_SIDE_KEY,
               certfile=settings.CLIENT_SIDE_CERT,
               strictHttps=True):

    d1_client.mnclient.MemberNodeClient.__init__(self, baseurl,
                                           defaultHeaders=defaultHeaders,
                                           timeout=timeout,
                                           keyfile=keyfile,
                                           certfile=certfile,
                                           strictHttps=strictHttps)

    self.logger = logging.getLogger(__name__)

    self.methodmap.update({
      'replicate_task_get': u'internal_replicate_task_get',
      'replicate_task_update': \
        u'internal_replicate_task_update/%(task_id)s/%(status)s',
      'replicate_create': u'internal_replicate_create/%(pid)s',
    })


  def internal_replicate_task_get(self):
    url = self._rest_url('replicate_task_get')

    response = self.GET(url)

    return gmn_types.CreateFromDocument(response.read())


  def internal_replicate_task_update(self, task_id, status):
    url = self._rest_url('replicate_task_update', task_id=str(task_id),
                               status=status)
    response = self.GET(url)
    return self._read_boolean_response(response)


  #@util.str_to_unicode
  def internal_replicate_create(self, pid, scidata, sysmeta,
                                vendorSpecific=None):
    '''Create replicate of object on GMN'''
    url = self._rest_url('replicate_create', pid=pid)
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    mime_multipart_files = [
      ('object', 'content.bin', scidata),
      ('sysmeta', 'sysmeta.xml', sysmeta),
    ]
    return self.POST(url, files=mime_multipart_files, headers=headers)

#===============================================================================

class Command(NoArgsCommand):
  help = 'Process the replication queue.'


  def handle_noargs(self, **options):
    self.log_setup()

    logging.info('Running management command: process_replication_queue')

    verbosity = int(options.get('verbosity', 1))

    if verbosity <= 1:
      logging.getLogger('').setLevel(logging.INFO)

    self.process_replication_queue()


  def internal_replicate_task_get(self):
    client = GMNReplicationClient()
    return client.internal_replicate_task_get()


  def internal_replicate_task_update(self, task, status):
    client = GMNReplicationClient()
    return client.internal_replicate_task_update(task.taskId, status)


  def cn_get_system_metadata_serial_version(self, task):
    client = d1_client.cnclient.CoordinatingNodeClient(
      baseurl='https://cn-dev-2.dataone.org/cn/v1')
    sysmeta = client.getSystemMetadata(task.pid)
    return sysmeta.serialVersion


  def cn_replicate_task_update(self, task, status):
    serial_version = self.cn_get_system_metadata_serial_version(task)
    client = d1_client.cnclient.CoordinatingNodeClient(
      baseurl='https://cn-dev-2.dataone.org/cn/v1')
    return client.setReplicationStatusResponse(task.pid,
      task.sourceNode, status, serial_version)


  def cn_get_node_registry(self):
    client = d1_client.cnclient.CoordinatingNodeClient(
      baseurl='https://cn-dev-2.dataone.org/cn/v1')
    return client.listNodesResponse()


  def resolve_source_node(self, task):
    nodes = self.cn_get_node_registry()
    base_url = ''
    for node in nodes.node:
      if replication_request.source_node.source_node == node.identifier:
        base_url = node.baseURL
        break
    if base_url == '':
      err_msg = 'Could not resolve source_node: {0}'.format(
        replication_request.source_node.source_node)
      logging.error(err_msg)
      # Update queue with failed message for current replication item.
      replication_request.set_status('Error: {0}'.format(err_msg))
      replication_request.save()
      # Abort handling of this replication item.
      raise d1_common.types.exceptions.ServiceFailure(0, err_msg)


  def gmn_replicate_create(self, task, scidata, sysmeta):
    client = GMNReplicationClient()
    return client.internal_replicate_create(task.pid, scidata, sysmeta)


  def process_replication_queue(self):
    while self.process_replication_task():
      continue


  def process_replication_task(self):
    try:
      task = self.internal_replicate_task_get()
    except d1_common.types.exceptions.DataONEException as e:
      logging.error(e)
      return False
    self.replicate(task)

    return True


  def get_science_data_from_member_node(self, client, pid):
    try:
      return client.get(pid)
    except d1_common.types.exceptions.DataONEException as e:
      raise Exception(
        'Unable to get Science Object from Member Node.\n{0}'.format(e))


  def get_system_metadata_from_coordinating_node(self, client, pid):
    try:
      return client.getSystemMetadataResponse(pid)
    except d1_common.types.exceptions.DataONEException as e:
      raise Exception(
        'Unable to get System Metadata from Coordinating Node.\n{0}'.format(e))


  def get_science_data(self, task):
    client = d1_client.mnclient.MemberNodeClient(
      baseurl='https://cn-dev-2.dataone.org/cn/v1')
    scidata = self.get_science_data_from_member_node(client, task.pid)
    tmp_file = tempfile.TemporaryFile()
    shutil.copyfileobj(scidata, tmp_file)
    return tmp_file


  def get_system_metadata(self, task):
    client = d1_client.cnclient.CoordinatingNodeClient(
      baseurl='https://cn-dev-2.dataone.org/cn/v1')
    sysmeta = self.get_system_metadata_from_coordinating_node(client, task.pid)
    tmp_file = tempfile.TemporaryFile()
    shutil.copyfileobj(sysmeta, tmp_file)
    return tmp_file


  def replicate(self, task):
    self.internal_replicate_task_update(task, 'in progress')

    sysmeta_tmp_file = self.get_system_metadata(task)
    science_data_tmp_file = self.get_science_data(task)

    sysmeta_tmp_file.seek(0)
    science_data_tmp_file.seek(0)

    self.gmn_replicate_create(task, science_data_tmp_file, sysmeta_tmp_file)

    #self.cn_replicate_task_update(task, 'test')

    self.internal_replicate_task_update(task, 'completed')



  # old streaming code 
  #  # Find size of scidata.
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


  def log_setup(self):
    # Set up logging.
    # We output everything to both file and stdout.
    logging.getLogger('').setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)s %(message)s',
                                  '%y/%m/%d %H:%M:%S')
    file_logger = logging.FileHandler(os.path.splitext(__file__)[0] + '.log',
                                      'a')
    file_logger.setFormatter(formatter)
    logging.getLogger('').addHandler(file_logger)
    # Stdout.
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setFormatter(formatter)
    logging.getLogger('').addHandler(console_logger)
    # Set logging level on the django.db.backends logger to "WARNING" to
    # suppress logging of SQL statements.
    logging.getLogger('django.db.backends').setLevel(logging.WARNING)


