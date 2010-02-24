#!/usr/bin/env python
# -*- coding: utf-8 -*-
""":mod:`insert_test_log` -- Admin Command
==========================================

:module: insert_test_log
:platform: Linux
:synopsis: insert_test_log

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
import json
import hashlib
import uuid
import random

# Django.
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, NoArgsCommand, CommandError
from django.http import HttpResponse, HttpResponseServerError
from django.http import Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.utils.html import escape

# Add mn_service app path to the module search path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# App
import settings
import mn_service.models
import mn_service.auth
import mn_service.sys_log
import mn_service.util
import mn_service.sysmeta
import mn_service.access_log

import site_specific


class Command(NoArgsCommand):
  help = 'Insert a fake access log into db for testing.'

  def handle_noargs(self, **options):
    mn_service.sys_log.info('Admin: insert_test_log')

    # Clear out existing log entries.
    mn_service.models.Access_log.objects.all().delete()

    # We use a fixed seed, so that the access log is the same each time to make
    # testing easier.
    random.seed(0)

    for requestor in ('1.1.1.1', '2.2.2.2', '3.3.3.3', '4.4.4.4'):
      query = mn_service.models.Repository_object.objects.order_by('-object_mtime')
      for repository_object in query:
        # Insert a "get bytes" access log entry for some objects for this
        # requestor.
        if random.random() > 0.3:
          mn_service.access_log.log(repository_object.guid, 'get_bytes', requestor)
        # Insert a "get head" access log entry for some objects for this
        # requestor.
        if random.random() > 0.3:
          mn_service.access_log.log(repository_object.guid, 'get_head', requestor)
        # Insert a "set_metadata" access log entry for some metadata objects for
        # this requestor.
        if random.random(
        ) > 0.3 and repository_object.repository_object_class.name == 'metadata':
          mn_service.access_log.log(repository_object.guid, 'set_metadata', requestor)

        # Set up fixed datetimes.
    query = mn_service.models.Access_log.objects.all()
    for row in query:
      # We use auto_now_add for access_time so that we can modify it after it has
      # been added if necessary.
      row.access_time = datetime.datetime.fromtimestamp(random.random() * 10000000000)
      row.save()
