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
"""FUSE based system to create filesystem mockups for ONEDrive
"""

import logging
import os

import fuse

import callbacks


def main():
  logging.getLogger().setLevel(logging.DEBUG)

  fuse_args = {
    'foreground': True,
    'fsname': 'ONEDrive',
    'nothreads': True,
    # Allow sharing the mount point with Samba / smb / smbd.
    # Requires user_allow_other in /etc/fuse.conf
    'allow_other': True,
  }
  if os.uname()[0] == 'Darwin':
    fuse_args['volicon'] = 'd1.icon'
    fuse_args['local'] = True
  else:
    fuse_args['nonempty'] = True

  fuse.FUSE(callbacks.FUSECallbacks(), 'fs', **fuse_args)


if __name__ == '__main__':
  main()
