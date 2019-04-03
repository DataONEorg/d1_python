#!/usr/bin/env python

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
"""Local cache of the DataONE ObjectFormatList for a given DataONE environment.

The cache is stored in a file and is automatically updated periodically.

Simple methods for looking up elements of the ObjectFormatList are provided.

As part of the metadata for a science object, DataONE stores a type identifier called an
ObjectFormatID. The ObjectFormatList allows mapping ObjectFormatIDs to filename
extensions and content type.

Examples:

    Section of an ObjectFormatList:

        {
          '-//ecoinformatics.org//eml-access-2.0.0beta4//EN': {
            'extension': 'xml',
            'format_name': 'Ecological Metadata Language, Access module, version 2.0.0beta4',
            'format_type': 'METADATA',
            'media_type': {
              'name': 'text/xml',
              'property_list': []
            }
          },
          '-//ecoinformatics.org//eml-access-2.0.0beta6//EN': {
            'extension': 'xml',
            'format_name': 'Ecological Metadata Language, Access module, version 2.0.0beta6',
            'format_type': 'METADATA',
            'media_type': {
              'name': 'text/xml',
              'property_list': []}
            },
        }

"""
import contextlib
import datetime
import fcntl
import json
import logging
import time

import d1_common.const
import d1_common.date_time
import d1_common.env
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.util
import d1_common.utils.filesystem

import d1_client.cnclient_2_0

DEFAULT_OBJECT_FORMAT_CACHE_PATH = d1_common.utils.filesystem.abs_path(
    './object_format_cache.json'
)
DEFAULT_CACHE_REFRESH_PERIOD = datetime.timedelta(days=30)
DEFAULT_LOCK_FILE_PATH = '/tmp/object_format_cache.lock'

# ===============================================================================


class Singleton(object):
    _instances = {}

    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__new__(class_)
        return class_._instances[class_]


# ===============================================================================


class ObjectFormatListCache(Singleton):
    def __init__(
        self,
        cn_cn_base_url=d1_common.const.URL_DATAONE_ROOT,
        object_format_cache_path=DEFAULT_OBJECT_FORMAT_CACHE_PATH,
        cache_refresh_period=DEFAULT_CACHE_REFRESH_PERIOD,
        lock_file_path=DEFAULT_LOCK_FILE_PATH,
    ):
        """
        Args:
            cn_cn_base_url : str: 
                BaseURL for a CN in the DataONE Environment being targeted.

                This can usually be left at the production root, even if running in
                other environments.
                
            object_format_cache_path : str
                Path to a file in which the cached ObjectFormatList is or will be
                stored.

                By default, the path is set to a cache file that is distributed together
                with this module.

                The directories must exist. The file is created if it doesn't exist. The
                file is recreated whenever needed. Paths under "/tmp" will typically
                cause the file to have to be recreated after reboot while paths under
                "/var/tmp/" typically persist over reboot.

            cache_refresh_period: datetime.timedelta or None
                Period of time in which to use the cached ObjectFormatList before
                refreshing it by downloading a new copy from the CN. The
                ObjectFormatList does not change often, so a month is probably a
                sensible default.

                Set to None to disable refresh. When refresh is disabled,
                ``object_format_cache_path`` must point to an existing file.
        """
        self._logger = logging.getLogger(__name__)
        self._cn_base_url = cn_cn_base_url
        self._object_format_cache_path = object_format_cache_path
        self._cache_refresh_period = cache_refresh_period
        self._lock_file_path = lock_file_path
        self._format_dict = None
        self._load_and_refresh_cache()

    @property
    def object_format_dict(self):
        """Direct access to a native Python dict representing cached
        ObjectFormatList."""
        self._refresh_cache_if_expired()
        return self._format_dict

    def get_content_type(self, format_id, default=None):
        try:
            return self.object_format_dict[format_id]["media_type"]['name']
        except KeyError:
            return default

    def get_filename_extension(self, format_id, default=None):
        try:
            return self.object_format_dict[format_id]["extension"]
        except KeyError:
            return default

    def refresh_cache(self):
        """Force a refresh of the local cached version of the ObjectFormatList.

        This is typically not required, as the cache is refreshed automatically after
        the configured ``cache_expiration_period``.

        """
        self._refresh_cache()

    #
    # Private.
    #

    def _load_and_refresh_cache(self):
        with self._serialize_access():
            try:
                self._format_dict = d1_common.util.load_json(
                    self._object_format_cache_path
                )
            except (EnvironmentError, json.decoder.JSONDecodeError):
                self._refresh_cache()
            else:
                self._refresh_cache_if_expired()

    @contextlib.contextmanager
    def _serialize_access(self):
        with open(self._lock_file_path, "w") as lock_file:
            while True:
                try:
                    fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except IOError:
                    time.sleep(0.1)
                else:
                    break
            yield

    def _refresh_cache_if_expired(self):
        if self._is_cache_expired():
            self._refresh_cache()

    def _is_cache_expired(self):
        if self._cache_refresh_period is None:
            return False
        return (
            d1_common.date_time.dt_from_iso8601_str(
                self._format_dict["_last_refresh_timestamp"]
            )
            < d1_common.date_time.utc_now() - self._cache_refresh_period
        )

    def _refresh_cache(self):
        self._logger.debug("Refreshing ObjectFormatList cache...")
        self._download_format_dict_from_d1_env()
        d1_common.util.save_json(self._format_dict, self._object_format_cache_path)

    def _download_format_dict_from_d1_env(self):
        self._logger.debug(
            'Downloading ObjectFormatList from CN. base_url="{}"'.format(
                self._cn_base_url
            )
        )
        client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(self._cn_base_url)
        try:
            object_format_list_pyxb = client.listFormats()
        except d1_common.types.exceptions.DataONEException as e:
            raise d1_common.types.exceptions.ServiceFailure(
                0,
                'Unable to read ObjectFormatList from CN. base_url="{}" error="{}" '.format(
                    self._cn_base_url, str(e)
                ),
            )
        self._format_dict = self._pyxb_to_dict(object_format_list_pyxb)
        self._format_dict["_last_refresh_timestamp"] = str(
            d1_common.date_time.utc_now()
        )

    def _pyxb_to_dict(self, object_format_list_pyxb):
        return {
            o.formatId: {
                "format_name": o.formatName,
                "format_type": o.formatType,
                "extension": ".{}".format(getattr(o, "extension", "bin")),
                "media_type": {
                    "name": getattr(o.mediaType, 'name', None),
                    "property_list": list(getattr(o.mediaType, 'property_', [])),
                },
            }
            for o in object_format_list_pyxb.objectFormat
        }
