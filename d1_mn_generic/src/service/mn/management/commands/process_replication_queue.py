#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`process_replication_queue`
================================

:Synopsis: 
  Iterate through queue of objects registered for replication and attempt to
  replicate them.
  
.. moduleauthor:: Roger Dahl
"""

# Stdlib.
import datetime
import glob
import hashlib
import httplib
import logging
import os
import re
import stat
import sys
import time
import urllib
import urlparse
import uuid

# 3rd party.
# Lxml
try:
  from lxml import etree
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-lxml\n')
  raise

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

# Add mn app path to the module search path.
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# MN API.
import d1_common.types.exceptions
import d1_common.types.pid_serialization
import d1_client.client

# App.
import settings
import mn.models
import mn.auth
import mn.util

# Get an instance of a logger.
logger = logging.getLogger(__name__)


class DataOneClientWrapper(d1_client.client.DataOneClient):
  def getSetReplicationStatusUrl(self):
    '''Get the full URL to the setReplicationStatus target.
    :param: (None)
    :return: (string) url
    '''

    return urlparse.urljoin(self.client.target, 'setreplicationstatus/')

  def getReplicationStoreUrl(self):
    ''':param: (None)
    :return: (string) url
    '''

    return urlparse.urljoin(self.client.target, '_replicate_store/')

  def set_replication_status(self, status, node_ref, pid):
    '''
    :param:
    :return:
    '''
    url = urlparse.urljoin(
      self.getSetReplicationStatusUrl(), urllib.quote(status, '') + '/' + urllib.quote(
        node_ref, '') + '/' + urllib.quote(pid, '')
    )
    logger.debug(
      "status({0}) node_ref({1}) pid({2}) url({3})".format(
        status, node_ref, pid, url
      )
    )

    response = self.client.GET(url, {})
    format = response.headers['content-type']
    deser = d1_common.types.pid_serialization.Identifier()
    return deser.deserialize(response.read(), format)

  def replicate_store(self, pid, scidata):
    # Data to post.
    files.append(('systemmetadata', 'systemmetadata', sysmeta))

    # Send REST POST call to register object. The URL is the same as for /object/ GET.

    files = []
    files.append(('scidata', 'scidata', scidata))

    crud_create_url = urlparse.urljoin(
      self.getReplicationStoreUrl(), urllib.quote(
        pid.encode('utf-8'), '')
    )
    self.logger.debug_(u'url({0}) pid({1})'.format(crud_create_url, pid))

    multipart = mime_multipart.multipart([], files)
    try:
      status, reason, page = multipart.post(crud_create_url)
      if status != 200:
        raise Exception(page)
    except Exception as e:
      logging.error('REST call failed: {0}'.format(str(e)))
      raise


def log_setup():
  # Set up logging.
  # We output everything to both file and stdout.
  logging.getLogger('').setLevel(logging.DEBUG)
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  #file_logger = logging.FileHandler(os.path.splitext(__file__)[0] + '.log', 'a')
  #file_logger.setFormatter(formatter)
  #logging.getLogger('').addHandler(file_logger)
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def replicate_object(obj):
  root = DataOneClientWrapper('http://0.0.0.0:8000/cn')

  # Set replication status to 'requested' on CN.
  root.set_replication_status('requested', obj.source_node.source_node, obj.pid)

  # Get source MN baseURL by MN pid.
  nodes = root.node()
  base_url = ''
  for node in nodes.node:
    if obj.source_node.source_node == node.identifier:
      base_url = node.baseURL
      break
  if base_url == '':
    err_msg = 'Could not resolve source_node: {0}'.format(obj.source_node.source_node)
    logger.error(err_msg)
    # Update queue with failed message for current replication item.
    obj.set_status('Error: {0}'.format(err_msg))
    obj.save()
    # Abort handling of this replication item.
    raise d1_common.types.exceptions.ServiceFailure(0, err_msg)
  # Find size of scidata.
  src = DataOneClientWrapper(base_url)
  sysmeta_obj = src.getSystemMetadata(obj.pid)
  obj_size = sysmeta_obj.size
  # Stream.
  object_file = src.get(obj.pid)
  sysmeta_str = src.getSystemMetadataResponse(obj.pid).read()
  dst = DataOneClientWrapper('http://0.0.0.0:8000/')
  # Add the ability to do len() on object_file. Needed by mime_multipart.
  object_file.__len__ = lambda x=None: int(obj_size)
  dst.create(obj.pid, object_file, sysmeta_str)

  # Register the completed replication with the CN.
  root.set_replication_status('completed', obj.source_node.source_node, obj.pid)


class Command(NoArgsCommand):
  help = 'Process the object registration queue.'

  def handle_noargs(self, **options):
    log_setup()
    logger.info('Admin: process_replication_queue')

    verbosity = int(options.get('verbosity', 1))

    if verbosity <= 1:
      logging.getLogger('').setLevel(logging.ERROR)

    # Loop through registration queue.
    for obj in mn.models.Replication_work_queue.objects.filter(status__status='new'):
      #for obj in mn.models.Replication_work_queue.objects.all():
      logger.info('Replicating object: {0}'.format(obj.pid))
      try:
        replicate_object(obj)
      except d1_common.types.exceptions.DataONEException as e:
        logger.error(str(e))
      except Exception:
        err_msg = mn.util.traceback_to_detail_code()
        logger.error(err_msg)
      else:
        obj.set_status('completed')
        obj.save()
