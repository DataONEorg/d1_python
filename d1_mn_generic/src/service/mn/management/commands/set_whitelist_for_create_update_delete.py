#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`set_whitelist_for_create_update_delete`
=============================================

:Synopsis: 
  When running in production, GMN requires that subjects that wish to create,
  update or delete science objects are registered in a whitelist. This
  management command manages the whitelist.
:Created: 2012-3-5
:Author: DataONE (Dahl)
"""

# Stdlib.
import logging
import os
import sys
import urlparse

# Django.
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.core.management.base import NoArgsCommand
from django.core.management.base import CommandError
#from django.http import HttpResponse
#from django.http import Http404
#from django.template import Context
#from django.template import loader
#from django.shortcuts import render_to_response
#from django.utils.html import escape
import django.utils.log
import django.db.models

# D1.
import d1_common.const
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.types.exceptions
import d1_common.util
import d1_common.date_time
import d1_common.url
import d1_client.d1client

# App.
import settings
import mn.models


class Command(NoArgsCommand):
  help = 'Set the whitelist for create, update and delete operations'

  def handle(self, *args, **options):
    if len(args) != 1:
      print(
        'Must specify the path to a file that contains a list of subjects '
        'to whitelist'
      )
      exit()

    verbosity = int(options.get('verbosity', 1))

    if verbosity <= 1:
      logging.getLogger('').setLevel(logging.ERROR)

    self.set_whitelist(args[0])

  def set_whitelist(self, whitelist_path):
    with open(whitelist_path) as f:
      mn.models.WhitelistForCreateUpdateDelete.objects.all().delete()
      for subject in f:
        w = mn.models.WhitelistForCreateUpdateDelete()
        w.set(subject.strip())
        w.save()
