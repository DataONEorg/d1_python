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
"""Local cache of the CN ObjectFormatList."""

import d1_common.const
import d1_common.object_format_cache
import d1_common.utils
import d1_common.utils.filesystem

import django.conf

if django.conf.settings.STAND_ALONE:
    object_format_list_cache = d1_common.object_format_cache.ObjectFormatListCache(
        cache_refresh_period=None
    )
else:
    object_format_list_cache = d1_common.object_format_cache.ObjectFormatListCache(
        django.conf.settings.DATAONE_ROOT,
        django.conf.settings.OBJECT_FORMAT_CACHE_PATH,
        django.conf.settings.OBJECT_FORMAT_CACHE_REFRESH_PERIOD,
    )


def get_filename(sciobj_model):
    return d1_common.utils.filesystem.gen_safe_path_element(
        sciobj_model.filename
        or (
            sciobj_model.pid.did
            + object_format_list_cache.get_filename_extension(
                sciobj_model.format.format, ".data"
            )
        )
    )


def get_content_type(format_id):
    return object_format_list_cache.get_content_type(
        format_id, d1_common.const.CONTENT_TYPE_OCTET_STREAM
    )
