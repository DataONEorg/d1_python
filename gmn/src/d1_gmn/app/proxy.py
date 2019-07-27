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
"""Proxy mode."""
import base64
import urllib.parse

import requests

import d1_common.const
import d1_common.types
import d1_common.types.exceptions

import django.conf


def get_sciobj_iter_remote(url):
    try:
        response = requests.get(
            url,
            stream=True,
            headers=_mk_header_dict(),
            timeout=django.conf.settings.PROXY_MODE_STREAM_TIMEOUT,
        )
    except requests.RequestException as e:
        raise d1_common.types.exceptions.ServiceFailure(
            0, 'Unable to open proxy object for streaming. error="{}"'.format(str(e))
        )
    else:
        return response.iter_content(chunk_size=django.conf.settings.NUM_CHUNK_BYTES)


def is_proxy_url(url):
    return d1_common.url.isHttpOrHttps(url)


def _mk_header_dict():
    header_dict = {"User-Agent": d1_common.const.USER_AGENT}
    if django.conf.settings.PROXY_MODE_BASIC_AUTH_ENABLED:
        header_dict.update(_mk_http_basic_auth_header())
    return header_dict


def _mk_http_basic_auth_header():
    return {
        "Authorization": "Basic {}".format(
            base64.standard_b64encode(
                "{}:{}".format(
                    django.conf.settings.PROXY_MODE_BASIC_AUTH_USERNAME,
                    django.conf.settings.PROXY_MODE_BASIC_AUTH_PASSWORD,
                ).encode("utf-8")
            ).decode("utf-8")
        )
    }
