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
"""High level object create
"""
from __future__ import absolute_import

import d1_gmn.app.event_log
import d1_gmn.app.revision
import d1_gmn.app.sysmeta
import d1_gmn.app.util
import d1_gmn.app.views.asserts

import d1_common.const
import d1_common.url
import d1_common.util
import d1_common.xml

import django.core.files.move


def create(request, sysmeta_pyxb):
  """Create a new native science object

  Preconditions:
  - PID is verified not to be unused, E.g., with
  d1_gmn.app.views.asserts.is_unused().

  Postconditions:
  - Files and database rows are added as necessary to add a new object.
  """
  # Proxy object vendor specific extension.
  if 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META:
    url = request.META['HTTP_VENDOR_GMN_REMOTE_URL']
    d1_gmn.app.views.asserts.url_is_http_or_https(url)
    d1_gmn.app.views.asserts.url_is_retrievable(url)
  else:
    # http://en.wikipedia.org/wiki/File_URI_scheme
    pid = d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
    url = u'file:///{}'.format(d1_common.url.encodePathElement(pid))
    _save_sciobj_bytes_from_request(request, pid)
  d1_gmn.app.sysmeta.create_or_update(sysmeta_pyxb, url)
  # Log the create event for this object.
  d1_gmn.app.event_log.create(
    d1_common.xml.get_req_val(sysmeta_pyxb.identifier), request,
    timestamp=sysmeta_pyxb.dateUploaded
  )


def create_native_sciobj(sysmeta_pyxb):
  """Create the db entries for a new native, locally stored (non-proxied)
  science object

  This assumes that the file containing the sciobj bytes has already been
  created.

  {sciobj_response} must be a Requests Response object that holds a stream
  (typically created via the d1_client wrapper for MNRead.get() with
  stream=True.)

  This method does not add any events to the event log.

  Preconditions:
  - PID is verified not to be unused, E.g., with
  d1_gmn.app.views.asserts.is_unused().
  - Sciobj bytes are saved to a file in the correct location.

  Postconditions:
  - A new file and new database entries are created.
  """
  pid = d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
  d1_gmn.app.sysmeta.create_or_update(
    sysmeta_pyxb, d1_gmn.app.util.get_sciobj_file_url(pid)
  )


def _save_sciobj_bytes_from_request(request, pid):
  """Django stores small uploads in memory and streams large uploads directly to
  disk. Uploads stored in memory are represented by UploadedFile and on disk,
  TemporaryUploadedFile. To store an UploadedFile on disk, it's iterated and
  saved in chunks. To store a TemporaryUploadedFile, it's moved from the
  temporary to the final location. Django automatically handles this when using
  the file related fields in the models.
  """
  sciobj_path = d1_gmn.app.util.get_sciobj_file_path(pid)
  d1_common.util.create_missing_directories_for_file(sciobj_path)
  try:
    django.core.files.move.file_move_safe(
      request.FILES['object'].temporary_file_path(), sciobj_path
    )
  except AttributeError:
    with open(sciobj_path, 'wb') as f:
      for chunk in request.FILES['object'].chunks():
        f.write(chunk)
