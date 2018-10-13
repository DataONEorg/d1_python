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
"""Read and write HTTP Headers
"""

import d1_gmn.app
import d1_gmn.app.auth
import d1_gmn.app.db_filter
import d1_gmn.app.did
import d1_gmn.app.event_log
import d1_gmn.app.models
import d1_gmn.app.psycopg_adapter
import d1_gmn.app.revision
import d1_gmn.app.sysmeta
import d1_gmn.app.util
import d1_gmn.app.views.slice
import d1_gmn.app.views.util

import d1_common.const
import d1_common.date_time
import d1_common.type_conversions
import d1_common.types
import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.url
import d1_common.xml


def add_sciobj_properties_headers_to_response(response, sciobj):
  response['Content-Length'] = sciobj.size
  response['Content-Type'] = d1_gmn.app.views.util.content_type_from_format(
    sciobj.format.format
  )
  response['Last-Modified'] = d1_common.date_time.http_datetime_str_from_dt(
    d1_common.date_time.normalize_datetime_to_utc(sciobj.modified_timestamp)
  )
  response['DataONE-GMN'] = d1_gmn.__version__
  response['DataONE-FormatId'] = sciobj.format.format
  response['DataONE-Checksum'] = '{},{}'.format(
    sciobj.checksum_algorithm.checksum_algorithm, sciobj.checksum
  )
  response['DataONE-SerialVersion'] = sciobj.serial_version
  add_http_date_header_to_response(response)
  if d1_common.url.isHttpOrHttps(sciobj.url):
    response['DataONE-Proxy'] = sciobj.url
  if sciobj.obsoletes:
    response['DataONE-Obsoletes'] = sciobj.obsoletes.did
  if sciobj.obsoleted_by:
    response['DataONE-ObsoletedBy'] = sciobj.obsoleted_by.did
  sid = d1_gmn.app.revision.get_sid_by_pid(sciobj.pid.did)
  if sid:
    response['DataONE-SeriesId'] = sid


def add_http_date_header_to_response(response, date_time=None):
  response['Date'] = d1_common.date_time.http_datetime_str_from_dt(
    d1_common.date_time.normalize_datetime_to_utc(date_time)
    if date_time else d1_common.date_time.utc_now()
  )


def add_cors_headers_to_response(response, method_list):
  """Add Cross-Origin Resource Sharing (CORS) headers to response
  - {method_list} is a list of HTTP methods that are allowed for the endpoint
  that was called. It should not include "OPTIONS", which is included
  automatically since it's allowed for all endpoints.
  """
  opt_method_list = ','.join(method_list + ['OPTIONS'])
  response['Allow'] = opt_method_list
  response['Access-Control-Allow-Methods'] = opt_method_list
  response['Access-Control-Allow-Origin'] = '*'
  response['Access-Control-Allow-Headers'] = 'Authorization'
  response['Access-Control-Allow-Credentials'] = 'true'
