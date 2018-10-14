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
"""SciObj create for view methods
"""

import d1_gmn.app.event_log
import d1_gmn.app.resource_map
import d1_gmn.app.revision
import d1_gmn.app.scimeta
import d1_gmn.app.sciobj_store
import d1_gmn.app.sysmeta
import d1_gmn.app.util
import d1_gmn.app.views.assert_db
import d1_gmn.app.views.assert_sysmeta
import d1_gmn.app.views.util

import d1_common.const
import d1_common.date_time
import d1_common.types
import d1_common.types.exceptions
import d1_common.url
import d1_common.util
import d1_common.xml

import django.conf
import django.core.files.move


def create_sciobj(request, sysmeta_pyxb):
  """Create object file and database entries for a new native locally stored
  (non-proxied) science object

  This method takes a request object and is only called from the views that
  handle:

  - MNStorage.create()
  - MNStorage.update()

  Various sanity checking is performed. Raises D1 exceptions that are returned
  directly to the client. Adds create event to the event log.

  Preconditions:
  - None. This method should check everything.

  Postconditions:
  - A new file containing sciobj bytes, and models (database rows) for the newly
  added object.
  """
  pid = d1_common.xml.get_req_val(sysmeta_pyxb.identifier)

  _set_mn_controlled_values(request, sysmeta_pyxb)
  d1_gmn.app.views.assert_db.is_valid_pid_for_create(pid)
  d1_gmn.app.views.assert_sysmeta.sanity(request, sysmeta_pyxb)

  abs_sciobj_path = d1_gmn.app.sciobj_store.get_abs_sciobj_file_path_by_pid(pid)

  if _is_proxy_sciobj(request):
    sciobj_url = _get_sciobj_proxy_url(request)
    _sanity_check_proxy_url(sciobj_url)
  else:
    sciobj_url = d1_gmn.app.sciobj_store.get_rel_sciobj_file_url_by_pid(pid)

  if not _is_proxy_sciobj(request):
    if d1_gmn.app.resource_map.is_resource_map_sysmeta_pyxb(sysmeta_pyxb):
      _create_resource_map(
        pid, request, abs_sciobj_path, sysmeta_pyxb, sciobj_url
      )
    else:
      _save_sciobj_bytes_from_request(request, abs_sciobj_path)
      d1_gmn.app.scimeta.assert_valid(sysmeta_pyxb, abs_sciobj_path)

  d1_gmn.app.sysmeta.create_or_update(sysmeta_pyxb, sciobj_url)

  d1_gmn.app.event_log.create(
    d1_common.xml.get_req_val(sysmeta_pyxb.identifier), request,
    timestamp=d1_common.date_time.
    normalize_datetime_to_utc(sysmeta_pyxb.dateUploaded)
  )


def _create_resource_map(pid, request, sciobj_path, sysmeta_pyxb, sciobj_url):
  map_xml = _read_sciobj_bytes_from_request(request)
  resource_map = d1_gmn.app.resource_map.parse_resource_map_from_str(map_xml)
  d1_gmn.app.resource_map.assert_map_is_valid_for_create(resource_map)
  d1_common.util.create_missing_directories_for_file(sciobj_path)
  _save_sciobj_bytes_from_str(map_xml, sciobj_path)
  d1_gmn.app.sysmeta.create_or_update(sysmeta_pyxb, sciobj_url)
  d1_gmn.app.resource_map.create_or_update(pid, resource_map)


def _is_proxy_sciobj(request):
  """Return True if sciobj is being created with the proxy vendor specific
  extension
  """
  return 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META


def _sanity_check_proxy_url(url):
  d1_gmn.app.views.assert_db.url_is_http_or_https(url)
  d1_gmn.app.views.assert_db.url_is_retrievable(url)


def _get_sciobj_proxy_url(request):
  return request.META['HTTP_VENDOR_GMN_REMOTE_URL']


def _read_sciobj_bytes_from_request(request):
  request.FILES['object'].seek(0)
  sciobj_bytes = request.FILES['object'].read()
  return sciobj_bytes


def _save_sciobj_bytes_from_request(request, sciobj_path):
  """Django stores small uploads in memory and streams large uploads directly to
  disk. Uploads stored in memory are represented by UploadedFile and on disk,
  TemporaryUploadedFile. To store an UploadedFile on disk, it's iterated and
  saved in chunks. To store a TemporaryUploadedFile, it's moved from the
  temporary to the final location. Django automatically handles this when using
  the file related fields in the models, but GMN is not using those, so has to
  do it manually here.
  """
  d1_common.util.create_missing_directories_for_file(sciobj_path)
  try:
    django.core.files.move.file_move_safe(
      request.FILES['object'].temporary_file_path(), sciobj_path
    )
  except AttributeError:
    with open(sciobj_path, 'wb') as f:
      for chunk in request.FILES['object'].chunks():
        f.write(chunk)


def _save_sciobj_bytes_from_str(map_xml, sciobj_path):
  d1_common.util.create_missing_directories_for_file(sciobj_path)
  with open(sciobj_path, 'wb') as f:
    f.write(map_xml)


def _set_mn_controlled_values(request, sysmeta_pyxb, update_submitter=True):
  """See the description of TRUST_CLIENT_* in settings.py.
  """
  now_datetime = d1_common.date_time.utc_now()

  default_value_list = [
    ('originMemberNode', django.conf.settings.NODE_IDENTIFIER, True),
    ('authoritativeMemberNode', django.conf.settings.NODE_IDENTIFIER, True),
    ('dateSysMetadataModified', now_datetime, False),
    ('serialVersion', 1, False),
    ('dateUploaded', now_datetime, False),
  ]

  if update_submitter:
    default_value_list.append(('submitter', request.primary_subject_str, True))
  else:
    sysmeta_pyxb.submitter = None

  for attr_str, default_value, is_simple_content in default_value_list:
    is_trusted_from_client = getattr(
      django.conf.settings, 'TRUST_CLIENT_{}'.format(attr_str.upper()), False
    )
    override_value = None
    if is_trusted_from_client:
      override_value = (
        d1_common.xml.get_opt_val(sysmeta_pyxb, attr_str)
        if is_simple_content else getattr(sysmeta_pyxb, attr_str, None)
      )
    setattr(sysmeta_pyxb, attr_str, override_value or default_value)
