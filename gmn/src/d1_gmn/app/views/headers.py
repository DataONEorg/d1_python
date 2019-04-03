# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
"""Read and write HTTP Headers."""
import d1_gmn.app
import d1_gmn.app.object_format_cache
import d1_gmn.app.revision
import d1_gmn.app.views.util

import d1_common.const
import d1_common.date_time
import d1_common.url
import d1_common.utils.filesystem


def add_sciobj_properties_headers_to_response(response, sciobj_model):
    _add_standard_headers(response, sciobj_model)
    add_http_date_header(response)
    add_custom_dataone_headers(response, sciobj_model)
    add_content_disposition_header(response, sciobj_model)


def add_custom_dataone_headers(response, sciobj_model):
    response["DataONE-GMN"] = d1_gmn.__version__
    response["DataONE-FormatId"] = sciobj_model.format.format
    response["DataONE-Checksum"] = "{},{}".format(
        sciobj_model.checksum_algorithm.checksum_algorithm, sciobj_model.checksum
    )
    response["DataONE-SerialVersion"] = sciobj_model.serial_version
    if d1_common.url.isHttpOrHttps(sciobj_model.url):
        response["DataONE-Proxy"] = sciobj_model.url
    if sciobj_model.obsoletes:
        response["DataONE-Obsoletes"] = sciobj_model.obsoletes.did
    if sciobj_model.obsoleted_by:
        response["DataONE-ObsoletedBy"] = sciobj_model.obsoleted_by.did
    sid = d1_gmn.app.revision.get_sid_by_pid(sciobj_model.pid.did)
    if sid:
        response["DataONE-SeriesId"] = sid


def add_content_disposition_header(response, sciobj_model):
    response["Content-Disposition"] = 'attachment; filename="{}"'.format(
        d1_gmn.app.object_format_cache.get_filename(sciobj_model)
    )


def add_http_date_header(response, date_time=None):
    response["Date"] = d1_common.date_time.http_datetime_str_from_dt(
        d1_common.date_time.normalize_datetime_to_utc(date_time)
        if date_time
        else d1_common.date_time.utc_now()
    )


def add_cors_headers(response, request):
    """Add Cross-Origin Resource Sharing (CORS) headers to response.

    - ``method_list`` is a list of HTTP methods that are allowed for the endpoint that
      was called. It should not include "OPTIONS", which is included automatically
      since it's allowed for all endpoints.

    """
    opt_method_list = ",".join(request.allowed_method_list + ["OPTIONS"])
    response["Allow"] = opt_method_list
    response["Access-Control-Allow-Methods"] = opt_method_list
    response["Access-Control-Allow-Origin"] = request.META.get("Origin", "*")
    response["Access-Control-Allow-Headers"] = "Authorization"
    response["Access-Control-Allow-Credentials"] = "true"


def _add_standard_headers(response, sciobj_model):
    response["Content-Length"] = sciobj_model.size
    response["Content-Type"] = d1_gmn.app.object_format_cache.get_content_type(
        sciobj_model
    )
    response["Last-Modified"] = d1_common.date_time.http_datetime_str_from_dt(
        d1_common.date_time.normalize_datetime_to_utc(sciobj_model.modified_timestamp)
    )
