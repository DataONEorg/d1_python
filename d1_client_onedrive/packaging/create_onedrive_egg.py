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

'''
Created on Jan 11, 2013

@author: brumgard
'''
import sys

from setuptools import setup, find_packages

sys.argv = [sys.argv[0], 'bdist_egg']

setup(
    name = "Onedrive",
    version = "0.1",
    py_modules = ['main', '__main__', 'onedrive', 'settings'],
    package_dir = {'impl':'../src/impl', 'onedrive':'../src/' },
    packages = ['onedrive', 'impl', 'impl.drivers', 'impl.drivers.fuse', 
                'impl.resolver'],
    
    entry_points = {
        'setuptools.installation': [
            'eggsecutable = main:entrypoint0',
        ]
    }
)
