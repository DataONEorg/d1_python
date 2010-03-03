#!/usr/bin/env python
# -*- coding: utf-8 -*-
""":mod:`site_specific`
=======================

:module: site_specific
:platform: Linux
:synopsis: site_specific

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
from django.core.management.base import BaseCommand
from django.core.management.base import NoArgsCommand
from django.core.management.base import CommandError
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.http import Http404
from django.template import Context
from django.template import loader
from django.shortcuts import render_to_response
from django.utils.html import escape

# App
import settings
import mn_service.sys_log
import mn_service.util
import mn_service.sysmeta


def populate_db():
  # Loop through all the MN objects.
  for object_path in glob.glob(os.path.join(settings.REPOSITORY_DOC_PATH, '*', '*')):
    # Find type of object.
    if object_path.count(settings.REPOSITORY_DATA_PATH + os.sep):
      t = 'data'
    elif object_path.count(settings.REPOSITORY_METADATA_PATH + os.sep):
      t = 'metadata'
    else:
      # Skip sysmeta objects.
      continue

    # Create db entry for object.
    object_guid = os.path.basename(object_path)
    mn_service.util.insert_object(t, object_guid, object_path)

    # Create sysmeta for object.
    sysmeta_guid = str(uuid.uuid4())
    sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
    res = mn_service.sysmeta.generate(object_path, sysmeta_path)
    if not res:
      util.raise_sys_log_http_404(
        'System Metadata generation failed for object: %s' % object_path
      )

  # Create db entry for sysmeta object.
    mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)

    # Create association between sysmeta and regular object.
    mn_service.util.insert_association(object_guid, sysmeta_guid)

    # Successfully updated the db, so put current datetime in status.mtime.
  s = mn_service.models.Status()
  # Converted to auto_now = True
  # s.mtime = datetime.datetime.utcnow()
  s.status = 'update successful'
  s.save()

  return HttpResponse('ok')
