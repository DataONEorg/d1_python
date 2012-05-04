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
:mod:`extract`
==============

:Synopsis: Extract the subject and subject_info from a certificate.
:Created: 2012-05-01
:Author: DataONE (Dahl, Pippin)
'''

# This dance is required for Macintoshes.
import sys
try:
  orig = sys.getdlopenflags()
except AttributeError:
  from OpenSSL import crypto
else:
  try:
    import DLFCN
  except ImportError:
    try:
      import dl
    except ImportError:
      try:
        import ctypes
      except ImportError:
        flags = 2 | 256
      else:
        flags = 2 | ctypes.RTLD_GLOBAL
        del ctypes
    else:
      flags = dl.RTLD_NOW | dl.RTLD_GLOBAL
      del dl
  else:
    flags = DLFCN.RTLD_NOW | DLFCN.RTLD_GLOBAL
    del DLFCN

  sys.setdlopenflags(flags)
  from OpenSSL import crypto
  sys.setdlopenflags(orig)
  del orig, flags

import d1_x509v3_certificate_extractor


def extract_from_file(path):
  if os.path.exists(path):
    f = open(path, 'rb')
    read_buffer = f.read()
    f.close()
    return extract_from_buffer(read_buffer)
  else:
    return None


def extract_from_buffer(certificate_buffer):
  ''' Returns the tuple: (subject, subject_info) '''
  return d1_x509v3_certificate_extractor.extract(certificate_buffer)
