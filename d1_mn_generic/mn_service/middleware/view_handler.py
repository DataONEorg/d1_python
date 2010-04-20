#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`view_handler`
===================

:platform: Linux
:Synopsis:
  Sanity checking on system state before view is executed.

.. moduleauthor:: Roger Dahl
"""

# Stdlib.
import sys
import os
import csv
import StringIO
import types

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

import mimeparser

# Django.
from django.http import HttpResponse

# MN API.
import d1common.exceptions

# App.
import mn_service.sys_log as sys_log
import mn_service.models as models


class view_handler():
  def process_view(self, request, view_func, view_args, view_kwargs):
    # Log which view is about the be called.
    sys_log.info('View: {0}'.format(view_func.func_name))

    # If the view being called is one that returns data, verify that
    # DB_update_status is good.
    if view_func.func_name in [
      'object_collection',
      'object_contents',
      'object_sysmeta',
      'access_log_view',
      'register',
      'register_delete',
    ]:
      try:
        status_row = models.DB_update_status.objects.all()[0]
      except IndexError:
        raise d1common.exceptions.ServiceFailure(0, 'DB update status has not been set')
      else:
        if status_row.status != 'update successful':
          raise d1common.exceptions.ServiceFailure(
            0, 'Trying to read from DB, but last DB update was not successful'
          )

    # Returning None causes Django to continue processing by calling view_func.
    return None
