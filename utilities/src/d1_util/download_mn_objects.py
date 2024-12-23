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
"""Download Science Objects from a Member Node.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Retrieve a list of all objects on a MN
- Retrieve the bytes and System Metadata for each object

Operation:

- Configure the script in the Config section below

"""
import argparse
import logging
import os
import sys
import urllib.parse

import d1_common.const
import d1_common.env
# D1
# import d1_common.types.generated.dataoneTypes as v2
import d1_common.types.exceptions
import d1_common.xml

# Config

# In addition to the default production environment, DataONE maintains several
# separate environments for use when developing and testing DataONE components.
# There are no connections between the environments. For instance, certificates,
# DataONE identities and science objects are exclusive to the environment in
# which they were created. This setting controls to which environment the CN
# client connects.

# Round-robin CN endpoints
DATAONE_ROOT = d1_common.const.URL_DATAONE_ROOT  # (recommended, production)
# DATAONE_ROOT = 'https://cn-dev.test.dataone.org/cn'
# DATAONE_ROOT = 'https://cn-stage.test.dataone.org/cn'
# DATAONE_ROOT = 'https://cn-sandbox.dataone.org/cn'
# DATAONE_ROOT = 'https://cn-stage.dataone.org/cn/'
# DATAONE_ROOT = 'https://cn-stage.test.dataone.org/cn'

# The number of objects to list each time listObjects() is called.
LIST_OBJECTS_PAGE_SIZE = 100

# The location in which to store downloaded objects.
DOWNLOAD_FOLDER = "./d1_objects"

# Don't download objects larger than this size.
MAX_FILE_SIZE_TO_DOWNLOAD = 1024 ** 3


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--debug", action="store_true", help="Debug level logging")
    parser.add_argument(
        "--env",
        type=str,
        default="prod",
        help="Environment, one of {}".format(", ".join(d1_common.env.D1_ENV_DICT)),
    )
    parser.add_argument(
        "--cert-pub",
        dest="cert_pem_path",
        action="store",
        help="Path to PEM formatted public key of certificate",
    )
    parser.add_argument(
        "--cert-key",
        dest="cert_key_path",
        action="store",
        help="Path to PEM formatted private key of certificate",
    )
    parser.add_argument(
        "--timeout",
        action="store",
        default=d1_common.const.DEFAULT_HTTP_TIMEOUT,
        help="Amount of time to wait for calls to complete (seconds)",
    )

    logging.basicConfig()
    # Setting the default logger to level "DEBUG" causes the script to become
    # very verbose.
    logging.getLogger("").setLevel(logging.DEBUG)

    try:
        os.makedirs(DOWNLOAD_FOLDER)
    except OSError:
        pass

    base_url = "https://mynpn.usanpn.org/knb/d1/mn"

    member_node_object_downloader = MemberNodeObjectDownloader(
        base_url, DOWNLOAD_FOLDER
    )
    member_node_object_downloader.download_all()


# ==============================================================================


class MemberNodeObjectDownloader(object):
    def __init__(
        self,
        base_url,
        download_folder,
        object_id_filter_list=None,
        max_object_size=None,
    ):
        # self._mn_client = d1_client.mnclient_2_0.MemberNodeClient_2_0(base_url)
        self._mn_client = d1_client.mnclient.MemberNodeClient(base_url)
        self._base_url = base_url
        self._download_folder = download_folder
        self._object_id_filter_list = object_id_filter_list or []
        self._max_object_size = max_object_size

    def download_all(self):
        logging.info("Retrieving objects for Member Node: {}".format(self._base_url))
        current_start = 0
        while True:
            try:
                object_list = self._mn_client.listObjects(
                    start=current_start,
                    count=LIST_OBJECTS_PAGE_SIZE,
                    # formatId=LIST_OBJECTS_FORMAT_ID,
                    # replicaStatus=False
                )
            except d1_common.types.exceptions.DataONEException as e:
                logging.exception("listObjects() failed with exception:")
                raise
            else:
                logging.debug(
                    "Retrieved page: {}/{}".format(
                        current_start / LIST_OBJECTS_PAGE_SIZE + 1,
                        object_list.total / LIST_OBJECTS_PAGE_SIZE,
                    )
                )

            for d1_object in object_list.objectInfo:
                try:
                    self._download_object(d1_object)
                except (
                    DownloadError,
                    d1_common.types.exceptions.DataONEException,
                ) as e:
                    logging.error(e)

            current_start += object_list.count
            if current_start >= object_list.total:
                break

    def _download_object(self, d1_object):
        pid = d1_object.identifier.value()
        # Download System Metadata, raises DataONEException on error, which is
        # captured and logged by caller.
        sysmeta_pyxb = self._download_system_metadata(pid)
        # Filter on information in System Metadata
        if self._max_object_size and sysmeta_pyxb.size > self._max_object_size:
            raise DownloadError(
                "Ignoring large object. pid={}, size={}, max={}".format(
                    pid, sysmeta_pyxb.size, self._max_object_size
                )
            )
        self._write_system_metadata_to_file(sysmeta_pyxb, pid)
        self._download_object_bytes_to_file(pid)

    def _download_system_metadata(self, pid):
        try:
            return self._mn_client.getSystemMetadata(pid)
        except d1_common.types.exceptions.NotAuthorized:
            raise DownloadError("Ignoring non-public object. pid={}".format(pid))

    def _write_system_metadata_to_file(self, sysmeta_pyxb, pid):
        with open(
            os.path.join(
                self._download_folder,
                "{}.sysmeta.xml".format(self._pid_to_filename(pid)),
            ),
            "wb",
        ) as f:
            f.write(d1_common.xml.serialize_for_transport(sysmeta_pyxb))

    def _download_object_bytes_to_file(self, pid):
        try:
            object_stream = self._mn_client.get(pid)
        except d1_common.types.exceptions.DataONEException:
            logging.exception("get() failed with exception:")
            raise
        # The PID (DataONE Persistent Identifier) can contain characters that are
        # not valid for use as filenames (most commonly, slashes). A simple way to
        # make a PID safe for use as a filename is to "percent-encode" it.
        pid_filename = urllib.parse.quote(pid, safe="")
        with open(
            os.path.join(self._download_folder, "{}.bin".format(pid_filename)), "wb"
        ) as f:
            for chunk_str in object_stream.iter_content(chunk_size=4096):
                f.write(chunk_str)

    # The PID (DataONE Persistent Identifier) can contain characters that are
    # not valid for use as filenames (most commonly, slashes). A simple way to
    # make a PID safe for use as a filename is to "percent-encode" it.
    def _pid_to_filename(self, pid):
        return urllib.parse.quote(pid, safe="")


class DownloadError(Exception):
    pass


if __name__ == "__main__":
    sys.exit(main())
