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
import os
import sys
import re
import glob
import time
import datetime
import stat
import hashlib
import uuid
import urllib
import logging
import urlparse
import httplib

try:
  import cjson as json
except:
  import json

  # 3rd party.
  # Lxml
try:
  from lxml import etree
except ImportError, e:
  sys.stderr.write('Import error: {0}'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-lxml')
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


def validate(sysmeta_etree):
  """
  Validate sysmeta etree against sysmeta xsd.
  """

  # Check for xsd file.
  try:
    xsd_file = open(settings.XSD_PATH, 'r')
  except IOError as (errno, strerror):
    logging.error('XSD could not be opened: {0}'.format(settings.XSD_PATH))
    logging.error('I/O error({0}): {1}'.format(errno, strerror))
    raise

  xmlschema_doc = etree.parse(settings.XSD_PATH)
  xmlschema = etree.XMLSchema(xmlschema_doc)
  try:
    xmlschema.assertValid(sysmeta_etree)
  except DocumentInvalid, e:
    logging.error('Invalid Sysmeta: {0}'.format(etree.tostring(sysmeta_etree)))
    raise

  # Create database entry for this object.
  o = mn_service.models.Repository_object()
  o.guid = item.identifier
  o.path = item.url
  o.set_object_class('data')
  o.hash = item.checksum
  o.object_mtime = item.timestamp
  o.size = item.size
  o.save_unique()

  # Successfully updated the db, so put current datetime in status.mtime.
  s = mn_service.models.DB_update_status()
  s.status = 'update successful'
  s.save()

  # Set status to OK on registration object.
  item.set_status('OK')
  item.save()


class Command(NoArgsCommand):
  help = 'Process the object registration queue.'

  def handle_noargs(self, **options):
    mn_service.sys_log.info('Admin: process_queue')

    log_setup()

    try:
      # Loop through registration queue.
      for item in mn_service.models.Registration_queue_work_queue.objects.filter(
        status__status='Queued'
      ):
        logging.info('Registering object: {0}'.format(item.url))
        register_object(item)
    except:
      # Something went wrong while processing queue.
      s = mn_service.models.DB_update_status()
      s.status = 'Process queue failed'
      s.save()
