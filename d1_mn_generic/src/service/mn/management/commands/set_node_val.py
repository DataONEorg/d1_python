#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
"""
:mod:`set_node_val`
====================

:Synopsis: 
  Set a config value for the Member Node.

.. moduleauthor:: Roger Dahl
"""

# Stdlib.
import os
import sys

# Django.
from django.core.management.base import BaseCommand

# Add mn app path to the module search path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# App.
import settings
import mn.models


class Command(BaseCommand):
  args = '<key value ...>'
  help = 'Set a config value for the Member Node'

  def handle(self, *args, **options):
    mn.models.Node().set(args[0], args[1])
