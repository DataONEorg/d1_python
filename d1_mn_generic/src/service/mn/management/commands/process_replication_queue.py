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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# MN API.
import d1_common.exceptions
import d1_client.client

# App.
import settings
import mn.models
import mn.auth
import mn.sys_log
import mn.util
import mn.sys_log


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


def replicate_object(identifier):
  # Find size of object.
  src = d1_client.client.DataOneClient('http://192.168.1.122/mn')
  sysmeta_obj = src.getSystemMetadata(identifier)
  obj_size = sysmeta_obj.size
  # Stream.
  object_file = src.get(identifier)
  sysmeta_str = src.getSystemMetadataResponse(identifier).read()
  dst = d1_client.client.DataOneClient('http://0.0.0.0:8000/')
  # Add the ability to do len() on object_file. Needed by mime_multipart.
  object_file.__len__ = lambda x=None: int(obj_size)
  dst.create(identifier, object_file, sysmeta_str, vendor_specific={})


class Command(NoArgsCommand):
  help = 'Process the object registration queue.'

  def handle_noargs(self, **options):
    log_setup()

    mn.sys_log.info('Admin: process_replication_queue')

    # Loop through registration queue.
    for obj in mn.models.Replication_work_queue.objects.filter(status__status='new'):
      logging.info('Replicating object: {0}'.format(obj.identifier))
      try:
        replicate_object(obj.identifier)
      except:
        # Something went wrong while processing queue.
        status = 'failed'
        logging.error(status)
        # Update queue with failed status.
        #obj.set_status(status)
        #obj.save()
        raise
