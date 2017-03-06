# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Startup handler middleware

This module contains code that should run once, after Django and GMN has been
fully loaded but before any requests have been serviced.
"""

from __future__ import absolute_import

# Django.
import django.core.exceptions


class StartupHandler(object):
  def __init__(self):
    # The startup_handler is currently just a placeholder.
    raise django.core.exceptions.MiddlewareNotUsed
