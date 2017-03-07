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
"""High level object create.
"""
from __future__ import absolute_import

import d1_common.url

import django.core.files.move

import app.event_log
import app.sysmeta
import app.util
import app.views.asserts


def create(request, sysmeta_pyxb):
  """Create a new native object.

  Preconditions:
  - PID is verified not to be unused, E.g., with
  app.views.asserts.is_unused().

  Postconditions:
  - Files and database rows are added as necessary to add a new object.
  """
  # Proxy object vendor specific extension.
  if 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META:
    url = request.META['HTTP_VENDOR_GMN_REMOTE_URL']
    app.views.asserts.url_is_http_or_https(url)
    app.views.asserts.url_is_retrievable(url)
  else:
    # http://en.wikipedia.org/wiki/File_URI_scheme
    pid = sysmeta_pyxb.identifier.value()
    url = u'file:///{}'.format(d1_common.url.encodePathElement(pid))
    _object_pid_post_store_local(request, pid)
  app.sysmeta.create(sysmeta_pyxb, url)
  # Log the create event for this object.
  app.event_log.create(sysmeta_pyxb.identifier.value(), request)


def _object_pid_post_store_local(request, pid):
  """Django stores small uploads in memory and streams large uploads directly to
  disk. Uploads stored in memory are represented by UploadedFile and on disk,
  TemporaryUploadedFile. To store an UploadedFile on disk, it's iterated and
  saved in chunks. To store a TemporaryUploadedFile, it's moved from the
  temporary to the final location. Django automatically handles this when using
  the file related fields in the models.
  """
  sciobj_path = app.util.sciobj_file_path(pid)
  app.util.create_missing_directories(sciobj_path)
  try:
    django.core.files.move.file_move_safe(
      request.FILES['object'].temporary_file_path(), sciobj_path
    )
  except AttributeError:
    with open(sciobj_path, 'wb') as f:
      for chunk in request.FILES['object'].chunks():
        f.write(chunk)
