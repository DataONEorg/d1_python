#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`insert_test_log`
======================

:Synopsis:
  Insert fake access log for testing and unit tests.
  
.. moduleauthor:: Roger Dahl
"""

# Stdlib.
import datetime
import glob
import hashlib
import os
import random
import re
import stat
import sys
import time
import uuid

try:
  import cjson as json
except:
  import json

  # Django.
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.core.management.base import NoArgsCommand
from django.core.management.base import CommandError
from django.http import HttpResponse
from django.http import Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.utils.html import escape

# Add mn_service app path to the module search path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# MN API.
import d1common.exceptions

# App.
import mn_service.access_log
import mn_service.auth
import mn_service.models
import mn_service.sys_log
import mn_service.util
import settings
import site_specific


class Command(NoArgsCommand):
  help = 'Insert a fake access log into db for testing.'

  def handle_noargs(self, **options):
    mn_service.sys_log.info('Admin: insert_test_log')

    # Clear out existing log entries.
    mn_service.models.Access_log.objects.all().delete()
    mn_service.models.Access_log_operation_type.objects.all().delete()
    mn_service.models.Access_log_requestor_identity.objects.all().delete()

    # We use a fixed seed, so that the access log is the same each time to make
    # testing easier.
    random.seed(0)

    for requestor in ('1.1.1.1', '2.2.2.2', '3.3.3.3', '4.4.4.4'):
      query = mn_service.models.Object.objects.order_by('-object_mtime')
      for object in query:
        # Insert a "get bytes" access log entry for some objects for this
        # requestor.
        if random.random() > 0.3:
          mn_service.access_log.log(object.guid, 'get_bytes', requestor)
        # Insert a "get head" access log entry for some objects for this
        # requestor.
        if random.random() > 0.3:
          mn_service.access_log.log(object.guid, 'get_head', requestor)

        # Set up fixed datetimes.
    query = mn_service.models.Access_log.objects.all()
    for row in query:
      # We use auto_now_add for access_time so that we can modify it after it has
      # been added if necessary.
      row.access_time = datetime.datetime.fromtimestamp(random.random() * 10000000000)
      row.save()
