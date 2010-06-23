#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
:mod:`tests`
============

:Synopsis:
  Unit Tests.

.. moduleauthor:: Roger Dahl
'''

# Stdlib.
try:
  import cjson as json
except:
  import json

import StringIO

# Django.
from django.test import TestCase

# MN API.
import d1common.exceptions

# App.
import settings
import util
