#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`process_replication_queue`
====================

:Synopsis: 
  Iterate through queue of objects registered by client to be exposed by DataONE
  and create database entries for exposing them.
  
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

try:
  import cjson as json
except:
  import json

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
import d1_common.exceptions
import d1_common.types.identifier_serialization
import d1_client.client

# App.
import settings
import mn.models
import mn.auth
import mn.sys_log
import mn.util
import mn.sys_log


class DataOneClientWrapper(d1_client.client.DataOneClient):
  def getSetReplicationStatusUrl(self):
    '''Get the full URL to the setReplicationStatus target.
    :param: (None)
    :return: (string) url
    '''

    return urlparse.urljoin(self.client.target, 'setreplicationstatus/')

  def set_replication_status(self, status, node_ref, pid):
    '''
    :param:
    :return:
    '''
    url = urlparse.urljoin(
      self.getSetReplicationStatusUrl(), urllib.quote(status, '') + '/' + urllib.quote(
        node_ref, '') + '/' + urllib.quote(pid, '')
    )
    mn.sys_log.debug_(
      "status({0}) node_ref({1}) pid({2}) url({3})".format(
        status, node_ref, pid, url
      )
    )
    # Fetch.
    response = self.client.PUT(url, '')
    format = response.headers['content-type']
    deser = d1_common.types.identifier_serialization.Identifier()
    return deser.deserialize(response.read(), format)


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
  # Get MN baseURL by MN identifier.
  root = DataOneClientWrapper('http://0.0.0.0:8000/cn')
  nodes = root.node()
  base_url = ''
  for node in nodes.node:
    if obj.source_node.source_node == node.identifier:
      base_url = node.baseURL
      break
  if base_url == '':
    err_msg = 'Could not resolve source_node: {0}'.format(obj.source_node.source_node)
    mn.sys_log.error_(err_msg)
    # Update queue with failed message for current replication item.
    obj.set_status('Error: {0}'.format(err_msg))
    obj.save()
    # Abort handling of this replication item.
    raise d1_common.exceptions.ServiceFailure(0, err_msg)
  # Find size of object.
  src = d1_client.client.DataOneClient(base_url)
  sysmeta_obj = src.getSystemMetadata(obj.identifier)
  obj_size = sysmeta_obj.size
  # Stream.
  object_file = src.get(obj.identifier)
  sysmeta_str = src.getSystemMetadataResponse(obj.identifier).read()
  dst = d1_client.client.DataOneClient('http://0.0.0.0:8000/')
  # Add the ability to do len() on object_file. Needed by mime_multipart.
  object_file.__len__ = lambda x=None: int(obj_size)
  dst.create(obj.identifier, object_file, sysmeta_str)
  # Register the completed replication with the CN.
  root.set_replication_status('completed', obj.source_node.source_node, obj.identifier, )


class Command(NoArgsCommand):
  help = 'Process the object registration queue.'

  def handle_noargs(self, **options):
    log_setup()
    mn.sys_log.info_('Admin: process_replication_queue')

    verbosity = int(options.get('verbosity', 1))

    if verbosity <= 1:
      logging.getLogger('').setLevel(logging.ERROR)

    # Loop through registration queue.
    for obj in mn.models.Replication_work_queue.objects.filter(status__status='new'):
      #for obj in mn.models.Replication_work_queue.objects.all():
      mn.sys_log.info_('Replicating object: {0}'.format(obj.identifier))
      try:
        replicate_object(obj)
      except d1_common.exceptions.DataONEException as e:
        mn.sys_log.error_(e.serializeToXml())
      except Exception:
        err_msg = mn.util.traceback_to_detail_code()
        mn.sys_log.error_(err_msg)
      else:
        obj.set_status('completed')
        obj.save()
