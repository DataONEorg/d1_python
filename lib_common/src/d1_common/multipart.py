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
"""Utilities for handling MIME Multipart documents
"""

import requests_toolbelt.multipart.decoder


def parse_response(response, encoding='utf-8'):
  """Parse a multipart Requests Response into a tuple of BodyPart objects
  - BodyPart members: headers (CaseInsensitiveDict), content (bytes), text
  (unicode), encoding (str).
  """
  return requests_toolbelt.multipart.decoder.MultipartDecoder.from_response(
    response, encoding
  ).parts


def parse_str(mmp_bytes, content_type, encoding='utf-8'):
  """Parse multipart document bytes into a tuple of BodyPart objects
  - {content_type} must be on the form, "multipart/form-data;
  boundary=<BOUNDARY>", where <BOUNDARY> is the string that separates the parts
  of the multipart document in {mmp_bytes}. In HTTP requests and responses, it
  is passed in the Content-Type header.
  - BodyPart members: headers (CaseInsensitiveDict), content (bytes), text
  (unicode), encoding (str).
  """
  return requests_toolbelt.multipart.decoder.MultipartDecoder(
    mmp_bytes, content_type, encoding
  ).parts


def normalize(
    body_part_tup,
):
  """Normalize a tuple of BodyPart objects to a string
  - Normalization is done by sorting the body_parts by the Content-Disposition
  headers, which is typically on the form, "form-data; name="name_of_part".
  """
  return '\n\n'.join([
    '{}\n\n{}'.format(
      str(p.headers[b'Content-Disposition'], p.encoding), p.text
    )
    for p in
    sorted(body_part_tup, key=lambda p: p.headers[b'Content-Disposition'])
  ])


def is_multipart(header_dict):
  """Return True if {header_dict} has a Content-Type key (case insensitive) with
  value that begins with 'multipart'
  """
  return {k.lower(): v for k, v in header_dict.items()
          }.get('content-type', '').startswith('multipart')
