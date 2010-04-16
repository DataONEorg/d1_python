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
  print('Import error: %s' % str(e))
  print('Try: sudo apt-get install python-lxml')
  sys.exit(1)

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

# XPaths for the possible locations of different items in EML.
eml_xpaths = {
  'identifier': [
    '//dataset[1]/dataTable[1]/entityName[1]',
    '//dataset[1]/dataTable[1]/physical[1]/objectName[1]'
  ],
}

# EML namespaces.
#
#<eml:eml
#xmlns:ds="eml://ecoinformatics.org/dataset-2.0.1"
#xmlns:xs="http://www.w3.org/2001/XMLSchema"
#xmlns:eml="eml://ecoinformatics.org/eml-2.0.1"
#xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#xmlns:res="eml://ecoinformatics.org/resource-2.0.1"
#xmlns:doc="eml://ecoinformatics.org/documentation-2.0.1"
#xmlns:stmml="http://www.xml-cml.org/schema/stmml"
#xmlns:sw="eml://ecoinformatics.org/software-2.0.1"
#xmlns:prot="eml://ecoinformatics.org/protocol-2.0.1"
#xmlns:cit="eml://ecoinformatics.org/literature-2.0.1"
#
#xsi:schemaLocation="eml://ecoinformatics.org/eml-2.0.1 eml.xsd"


def register_object(item):
  # Split URL into individual parts.
  try:
    url = urlparse.urlparse(item.url)
  except ValueError as e:
    err_msg = 'ValueError: {0}'.format(e)
    logging.error(err_msg)
    set_item_status(item, err_msg)
    return

  # Download object.
  try:
    conn = httplib.HTTPConnection(url.netloc)
    conn.connect()
    conn.request('GET', item.url)
    response = conn.getresponse()
    object_contents = response.read()
  except httplib.HTTPException as e:
    err_msg = 'HTTPException: {0}'.format(e)
    logging.error(err_msg)
    item.set_status('Error: %s' % err_msg)
    item.save()
    return
  if object_contents == '':
    err_msg = 'Downloaded object is empty'
    logging.error(err_msg)
    item.set_status('Error: %s' % err_msg)
    item.save()
    return

  # Parse to tree.
  try:
    object_tree = etree.fromstring(object_contents)
  except:
    err_msg = 'Couldn\'t parse object'
    logging.error(err_msg)
    item.set_status('Error: %s' % err_msg)
    item.save()
    return

    ## Validate EML
    #xmlschema = etree.XMLSchema(xmlschema_doc)
    #try:
    #  xmlschema.assertValid(object_tree)
    #except DocumentInvalid, e:
    #  logging.error('Invalid object: %s' % item.url)
    #  raise

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
        logging.info('Registering object: %s' % item.url)
        register_object(item)
    except:
      # Something went wrong while processing queue.
      s = mn_service.models.DB_update_status()
      s.status = 'Process queue failed'
      s.save()
