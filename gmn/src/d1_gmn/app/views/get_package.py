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
"""MNPackage.getPackage(session, packageType, id) → OctetStream."""
import d1_gmn.app.model_util
import d1_gmn.app.object_format_cache
import d1_gmn.app.resource_map
import d1_gmn.app.sciobj_store
import d1_gmn.app.views.decorators
import d1_gmn.app.views.headers
import d1_gmn.app.views.util

import d1_common.bagit
import d1_common.checksum
import d1_common.const
import d1_common.iter.bytes
import d1_common.types.exceptions

import django.http


def get_package(request, pid, package_type):
    # Convert args from keyword to positional
    return _get_package(request, pid, package_type)


@d1_gmn.app.views.decorators.decode_did
@d1_gmn.app.views.decorators.resolve_sid
@d1_gmn.app.views.decorators.read_permission
def _get_package(request, pid, package_type):
    package_type = d1_gmn.app.views.decorators.decode_path_segment(package_type)
    if package_type != d1_common.const.DEFAULT_DATA_PACKAGE_FORMAT_ID:
        raise d1_common.types.exceptions.InvalidRequest(
            0,
            "Unsupported Data Package format. "
            "Currently, only BagIt (formatId={}) is supported".format(
                d1_common.const.DEFAULT_DATA_PACKAGE_FORMAT_ID
            ),
        )
    pid_list = d1_gmn.app.resource_map.get_resource_map_members(pid)
    sciobj_info_list = _create_sciobj_info_list(request, pid_list)
    bagit_file = d1_common.bagit.create_bagit_stream(pid, sciobj_info_list)
    response = django.http.StreamingHttpResponse(
        bagit_file, content_type="application/zip"
    )
    sciobj_model = d1_gmn.app.model_util.get_sci_model(pid)
    d1_gmn.app.views.headers.add_sciobj_properties_headers_to_response(
        response, sciobj_model
    )
    return response


def _create_sciobj_info_list(request, pid_list):
    sciobj_info_list = []
    for pid in pid_list:
        # Skip any sciobj which are aggregated by the package but do not exist locally.
        # TODO: Handle proxied sciobj.
        if not d1_gmn.app.sciobj_store.is_existing_sciobj_file(pid):
            continue
        sciobj_model = d1_gmn.app.model_util.get_sci_model(pid)
        sciobj_info_list.append(_create_sciobj_info_dict(sciobj_model))
        sciobj_info_list.append(_create_sysmeta_info_dict(request, sciobj_model))
    return sciobj_info_list


def _create_sciobj_info_dict(sciobj_model):
    return {
        "pid": sciobj_model.pid.did,
        "filename": d1_gmn.app.object_format_cache.get_filename(sciobj_model),
        "iter": d1_gmn.app.sciobj_store.get_sciobj_iter_by_pid(sciobj_model.pid.did),
        "checksum": sciobj_model.checksum,
        "checksum_algorithm": sciobj_model.checksum_algorithm.checksum_algorithm,
    }


def _create_sysmeta_info_dict(request, sciobj_model):
    sysmeta_iter = _create_sysmeta_iterator(request, sciobj_model.pid.did)
    return {
        "pid": sciobj_model.pid.did,
        "filename": "{}.sysmeta.xml".format(
            d1_gmn.app.object_format_cache.get_filename(sciobj_model)
        ),
        "iter": sysmeta_iter,
        "checksum": d1_common.checksum.calculate_checksum_on_iterator(sysmeta_iter),
        "checksum_algorithm": d1_common.const.DEFAULT_CHECKSUM_ALGORITHM,
    }


def _create_sysmeta_iterator(request, pid):
    return d1_common.iter.bytes.BytesIterator(
        d1_gmn.app.views.util.generate_sysmeta_xml_matching_api_version(request, pid)
    )
