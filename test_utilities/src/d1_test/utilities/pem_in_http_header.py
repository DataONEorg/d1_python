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
"""Convert PEM formatted certificates to and from HTTP header compatible values

For debugging certificate processing logic, it is sometimes convenient to pass
the certificates via HTTP headers instead of HTTPS.
"""

import io


def pem_in_string_to_pem_in_http_header(pem_str):
  pem = io.StringIO(pem_str)
  header = io.StringIO()
  for pem_line in pem:
    pem_line = pem_line.strip()
    if pem_line.startswith('-'):
      continue
    header.write(pem_line)
  pem_header = header.getvalue()
  if len(pem_header) > 8190:
    raise Exception('PEM certificate is too large for HTTP header')
  return pem_header


def pem_in_http_header_to_pem_in_string(header_str):
  header = io.StringIO(header_str)
  pem = io.StringIO()
  pem.write('-----BEGIN CERTIFICATE-----\n')
  while True:
    pem_line = header.read(64)
    if len(pem_line) == 0:
      break
    pem.write(pem_line + '\n')
  pem.write('-----END CERTIFICATE-----\n')
  return pem.getvalue()
