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
'''
:mod:`models`
=============

:Synopsis:
  Database models.

.. moduleauthor:: Roger Dahl
'''

# App.
import settings

from django.db import models
from django.db.models import Q

# MN API.
import d1_common.types.exceptions

#class Object_replication_status(models.Model):
#  pid = models.CharField(max_length=200, db_index=True)
#  status = models.CharField(max_length=100)
#  mtime = models.DateTimeField(auto_now=True)
