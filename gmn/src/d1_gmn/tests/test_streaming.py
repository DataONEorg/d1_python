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
"""Test that SciObjs are streamed directly to and from disk and network without being
buffered in memory."""
import logging

import pytest
import requests_toolbelt

import d1_common.xml

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_wsgi

import d1_test.d1_test_case
import d1_test.instance_generator.identifier
import d1_test.instance_generator.system_metadata

logger = logging.getLogger(__name__)

# Size in GiB of the SciObj that will be submitted to GMN.
SPARSE_FILE_SIZE_GIB = 30
# SPARSE_FILE_SIZE_GIB = 1

# Object buffering is detected by monitoring the memory usage while the SciObj is
# created and submitted to GMN. An increase over this causes the test to fail.
MEMORY_INCREASE_LIMIT_BYTES = 2 * 1024 ** 3

# Override the default OBJECT_STORE_PATH.
TMP_OBJECT_STORE_PATH = "/mnt/hdd"
# "/home/dahl/dev/d1_python"


@d1_test.d1_test_case.reproducible_random_decorator("TestSciObjStreaming")
@pytest.mark.skip("Slow, creates large test file")
class TestSciObjStreaming(d1_gmn.tests.gmn_test_case.GMNTestCase):
    def _create_sysmeta(self, gmn_client_v2, large_sparse_stream, pid):
        logging.debug("Generating SysMeta for sparse file...")
        sysmeta_pyxb = d1_test.instance_generator.system_metadata.generate_from_file(
            gmn_client_v2, large_sparse_stream, option_dict={"identifier": pid}
        )
        large_sparse_stream.seek(0)
        return sysmeta_pyxb

    def _create_mmp_stream(self, large_sparse_stream, pid, sysmeta_pyxb):
        mmp_stream = requests_toolbelt.MultipartEncoder(
            fields={
                "pid": pid.encode("utf-8"),
                "object": ("content.bin", large_sparse_stream),
                "sysmeta": (
                    "sysmeta.xml",
                    d1_common.xml.serialize_to_xml_str(sysmeta_pyxb),
                ),
            }
        )
        return mmp_stream

    def _call_mnread_create(self, mmp_stream):
        logging.debug("Calling create() on sparse file...")

        wsgi_client = d1_gmn.tests.gmn_wsgi.WSGIClient()

        with wsgi_client.send_request(
            {
                "REQUEST_METHOD": "POST",
                "PATH_INFO": "/v2/object",
                "CONTENT_TYPE": mmp_stream.content_type,
                "CONTENT_LENGTH": mmp_stream.len,
                "REMOTE_ADDR": "127.0.0.1",
                "wsgi.input": mmp_stream,
            }
        ) as response:
            assert response.status_code == 200
            logger.debug(response.content)

    def test_1000(self, gmn_client_v2):
        pid = d1_test.instance_generator.identifier.generate_pid(
            "{}_GiB_PID".format(SPARSE_FILE_SIZE_GIB)
        )

        logging.debug(
            "Creating temporary {} GiB sparse file...".format(SPARSE_FILE_SIZE_GIB)
        )

        with d1_test.d1_test_case.temp_sparse_file(
            gib=SPARSE_FILE_SIZE_GIB
        ) as large_sparse_stream:
            sysmeta_pyxb = self._create_sysmeta(gmn_client_v2, large_sparse_stream, pid)

            with d1_gmn.tests.gmn_mock.disable_sciobj_store_write():
                with d1_gmn.tests.gmn_mock.disable_auth():
                    with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
                        with d1_test.d1_test_case.memory_limit(
                            MEMORY_INCREASE_LIMIT_BYTES
                        ):
                            with d1_gmn.tests.gmn_test_case.unique_sciobj_store(
                                TMP_OBJECT_STORE_PATH
                            ):
                                mmp_stream = self._create_mmp_stream(
                                    large_sparse_stream, pid, sysmeta_pyxb
                                )
                                self._call_mnread_create(mmp_stream)
