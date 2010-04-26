#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`process_queue`
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

# Add mn_service app path to the module search path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# MN API.
import d1common.exceptions

# App.
import settings
import mn_service.models
import mn_service.auth
import mn_service.sys_log
import mn_service.util
import mn_service.access_log


def log_setup():
  # Set up logging.
  # We output everything to both file and stdout.
  logging.getLogger('').setLevel(logging.DEBUG)
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  file_logger = logging.FileHandler(os.path.splitext(__file__)[0] + '.log', 'a')
  file_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(file_logger)
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def register_object(obj):
  # Create database entry for this object.
  o = mn_service.models.Repository_object()
  o.guid = obj.identifier
  o.url = obj.url

  #TODO: Hack: Object type mapping.
  try:
    oc = {
      "DSPACE METS SIP Profile 1.0": 'scimeta',
      'Dataset': 'scidata',
    }[obj.format.format]
  except KeyError:
    logging.error('Invalid format: {0}'.format(obj.format.format))
    raise

  o.set_object_class(oc)
  o.hash = obj.checksum
  o.object_mtime = obj.timestamp
  o.size = obj.size
  o.save_unique()

  # Successfully updated the db, so put current datetime in status.mtime.
  s = mn_service.models.DB_update_status()
  s.status = 'update successful'
  s.save()

  # Set status to OK on registration object.
  obj.set_status('OK')
  obj.save()


class Command(NoArgsCommand):
  help = 'Process the object registration queue.'

  def handle_noargs(self, **options):
    mn_service.sys_log.info('Admin: process_queue')

    log_setup()

    # Loop through registration queue.
    for obj in mn_service.models.Registration_queue_work_queue.objects.filter(
      status__status='Queued'
    ):
      logging.info('Registering object: {0}'.format(obj.url))
      try:
        register_object(obj)
      except:
        # Something went wrong while processing queue.
        status = 'process_queue failed'
        logging.error(status)
        # Update db with failed status.
        s = mn_service.models.DB_update_status()
        s.status = status
        s.save()
        # Send exception on to framework for display.
        raise
