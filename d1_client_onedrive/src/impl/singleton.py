#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
''':mod:`singleton`
===================

:Synopsis:
 - Base class for singletons.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import os

# App.

# Set up logger for this module.
log = logging.getLogger(__name__)


# Note: This Singleton class does not prevent __init__() in the derived class
# from getting called each time the class is instantiated. I did not find
# a singleton class that prevented __init__() from getting called.
class Singleton(object):
  _instances = {}

  def __new__(class_, *args, **kwargs):
    if class_ not in class_._instances:
      class_._instances[class_] = super(Singleton, class_)\
        .__new__(class_, *args, **kwargs)
    return class_._instances[class_]
