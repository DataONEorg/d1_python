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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# App
import models
import settings
import auth
import sys_log
import util
import sysmeta
import access_log

import site_specific


class Command(NoArgsCommand):
  help = 'Update the database with the contents of the member node filesystem.'

  def handle_noargs(self, **options):
    sys_log.info('Admin: update_db')

    # Clear out all data from the tables.
    models.associations.objects.all().delete()
    models.repository_object.objects.all().delete()
    models.repository_object_class.objects.all().delete()
    models.status.objects.all().delete()

    # We then remove the sysmeta objects.
    for sysmeta_path in glob.glob(os.path.join(settings.REPOSITORY_SYSMETA_PATH, '*')):
      os.remove(sysmeta_path)

    # Call the site specific db population.
    site_specific.populate_db()
