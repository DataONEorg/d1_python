#!/usr/bin/env python
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
"""
:mod:`date`
===========

:Synopsis: Generate random dates.
:Created: 2011-08-01
:Author: DataONE (Vieglais, Dahl)
"""

# Stdlib
import random
import datetime

# D1
import d1_common.date_time


def random_date(earliest=0, latest=1e10):
  """Generate a random date somewhere between earliest and latest.
  """
  tstamp = random.randrange(earliest, latest)
  dt = datetime.datetime.utcfromtimestamp(tstamp)
  return d1_common.date_time.create_utc_datetime(
    dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, random.randint(0, 1000)
  )


def now():
  """Generate a date with the current UTC date and time"""
  return datetime.datetime.utcnow()


def generate():
  """Generate a dataoneTypes.DateTime with a random datetime"""
  dt = dataoneTypes.DateTime(random_date())
