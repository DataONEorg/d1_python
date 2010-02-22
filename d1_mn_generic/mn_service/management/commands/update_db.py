#!/usr/bin/env python
# -*- coding: utf-8 -*-
""":mod:`update_db` -- Admin Command
====================================

:module: update_db
:platform: Linux
:synopsis: update_db

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
  help = 'Update the database with the contents of the member node filesystem.'

  def handle_noargs(self, **options):
    mn_service.sys_log.info('Admin: update_db')

    # Clear out all data from the tables.
    mn_service.models.Access_log.objects.all().delete()
    mn_service.models.Associations.objects.all().delete()
    mn_service.models.Repository_object.objects.all().delete()
    mn_service.models.Repository_object_class.objects.all().delete()
    mn_service.models.Status.objects.all().delete()

    # We then remove the sysmeta objects.
    for sysmeta_path in glob.glob(os.path.join(settings.REPOSITORY_SYSMETA_PATH, '*')):
      os.remove(sysmeta_path)

    # Call the site specific db population.
    site_specific.populate_db()
