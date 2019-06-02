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
import os

import d1_gmn.app
import d1_gmn.app.object_format_cache
import d1_gmn.app.revision
import d1_gmn.app.views.util

import d1_common.const
import d1_common.date_time
import d1_common.url
import d1_common.utils.filesystem

import django.conf


def add_sciobj_properties_headers_to_response(response, sciobj_model):
    """Add headers for SciObj to response."""
    _add_standard(response, sciobj_model)
    _add_sciobj_standard(response, sciobj_model)
    _add_custom_dataone(response, sciobj_model)
    _add_sciobj_custom_dataone(response, sciobj_model)


def add_bagit_zip_properties_headers_to_response(response, sciobj_model):
    """Add headers for dynamically generated BagIt ZIP files to response.

    - ``sciobj_model`` will hold the underlying ORE RDF SciObj.
    - Since the BagIt ZIP file is generated on the fly, there are some headers that
    cannot be provided. Among these are ``Content-Length``, so the browser will not be
    able to display an ETA or progress bar during download.

    """
    _add_standard(response, sciobj_model)
    _add_bagit_standard(response, sciobj_model)
    _add_custom_dataone(response, sciobj_model)
    _add_bagit_custom_dataone(response)


def add_cors(response, request):
    """Add Cross-Origin Resource Sharing (CORS) headers to response.

    - ``allowed_method_list`` is a list of HTTP methods that are allowed for the
    endpoint that was called. It should not include "OPTIONS", which is included
    automatically since it's allowed for all endpoints.

    """
    opt_method_list = ",".join(request.allowed_method_list + ["OPTIONS"])
    response["Allow"] = opt_method_list
    response["Access-Control-Allow-Methods"] = opt_method_list
    response["Access-Control-Allow-Origin"] = request.META.get(
        "HTTP_ORIGIN", django.conf.settings.CORS_DEFAULT_ORIGIN
    )
    response["Access-Control-Allow-Headers"] = "Authorization"
    response["Access-Control-Allow-Credentials"] = "true"


def add_http_date(response, date_time=None):
    response["Date"] = d1_common.date_time.http_datetime_str_from_dt(
        d1_common.date_time.normalize_datetime_to_utc(date_time)
        if date_time
        else d1_common.date_time.utc_now()
    )


def _add_standard(response, sciobj_model):
    add_http_date(response)
    response["Last-Modified"] = d1_common.date_time.http_datetime_str_from_dt(
        d1_common.date_time.normalize_datetime_to_utc(sciobj_model.modified_timestamp)
    )


def _add_sciobj_standard(response, sciobj_model):
    response["Content-Length"] = sciobj_model.size
    response["Content-Type"] = d1_gmn.app.object_format_cache.get_content_type(
        sciobj_model
    )
    response["Content-Disposition"] = 'attachment; filename="{}"'.format(
        d1_gmn.app.object_format_cache.get_filename(sciobj_model)
    )


def _add_bagit_standard(response, sciobj_model):
    """Use the base of any name provided in the SysMeta for the underlying ORE RDF
    SciObj and change any provided extension (typically .rdf) to .zip."""
    response["Content-Type"] = "application/zip"
    rdf_file_name = d1_gmn.app.object_format_cache.get_filename(sciobj_model)
    zip_file_name = os.path.splitext(rdf_file_name)[0] + ".zip"
    response["Content-Disposition"] = 'attachment; filename="{}"'.format(zip_file_name)


def _add_custom_dataone(response, sciobj_model):
    response["DataONE-GMN"] = d1_gmn.__version__
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


def _add_sciobj_custom_dataone(response, sciobj_model):
    response["DataONE-FormatId"] = sciobj_model.format.format
    response["DataONE-Checksum"] = "{},{}".format(
        sciobj_model.checksum_algorithm.checksum_algorithm, sciobj_model.checksum
    )


def _add_bagit_custom_dataone(response):
    response["DataONE-FormatId"] = d1_common.const.DEFAULT_DATA_PACKAGE_FORMAT_ID
