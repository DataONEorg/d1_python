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
:mod:`certificate`
==================

:Created: 2012-07-16
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

import os

from . import settings
from . import subject_dn


def check_path(path):
  """Because the authors of OpenSSL think that, "ssl.SSLError: [Errno 336445442]
  _ssl.c:365: error:140DC002:SSL
  routines:SSL_CTX_use_certificate_chain_file:system lib" is a good error message
  for "file not found", do explit checks of certificate paths.
  """
  if not os.path.exists(path):
    raise Exception('Certificate or key does not exist: {}'.format(path))


def get_certificate_path_for_subject(subject):
  """Get the path to the generated certificate for a given subject.
  """
  return os.path.join(
    settings.CLIENT_CERT_DIR, subject_dn.subject_to_filename(subject)
  )
