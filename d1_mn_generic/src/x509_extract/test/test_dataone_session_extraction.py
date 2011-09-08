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
:mod:test_dataone_session_extraction`
=====================================

:platform:
  Linux
:Synopsis:
  Test DataONE Session object extraction from PEM formatted X.509 v3
  certificate.
:Author:
  DataONE (dahl)
'''

import os
import re
import sys

sys.path.append('../build/lib.linux-x86_64-2.6/')
import x509_extract_session

import d1_common.types.generated.dataoneTypes as dataoneTypes

cert_file = open('./test_cert_dataone_session.pem', 'rb')
cert_str = cert_file.read()
session_str = x509_extract_session.extract(cert_str)

print 'Extracted: {0}'.format(session_str)

try:
  session = dataoneTypes.CreateFromDocument(session_str)
except:
  raise Exception("Extracted Session object is invalid")
else:
  print "Session OK"
