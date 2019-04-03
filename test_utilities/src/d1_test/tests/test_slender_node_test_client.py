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
import io
import os
import tempfile

import pytest

import d1_common.xml

import d1_test.d1_test_case
import d1_test.instance_generator.identifier
import d1_test.instance_generator.sciobj
import d1_test.slender_node_test_client


@pytest.fixture(scope="function")
def sn_client():
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        yield d1_test.slender_node_test_client.SlenderNodeTestClient(
            sciobj_store_path=tmp_dir_path
        )


class TestSlenderNodeTestClient(d1_test.d1_test_case.D1TestCase):
    def _generate_sciobj_with_defaults(self, client, pid=True, sid=None):
        sid = (
            d1_test.instance_generator.identifier.generate_sid() if sid is True else sid
        )
        option_dict = {
            k: v for (k, v) in (('identifier', pid), ('seriesId', sid)) if v is not True
        }
        pid, sid, sciobj_bytes, sysmeta_pyxb = d1_test.instance_generator.sciobj.generate_reproducible_sciobj_with_sysmeta(
            client, None if pid is True else pid, option_dict
        )
        return pid, sid, sciobj_bytes, sysmeta_pyxb

    def test_1000(self, sn_client):
        """Instantiate."""
        assert os.path.exists(sn_client.sciobj_store_path)
        assert sn_client.did_dict == {}

    def test_1010(self, sn_client):
        """create() and get() by PID."""
        pid, sid, sciobj_bytes, sysmeta_pyxb = self._generate_sciobj_with_defaults(
            sn_client
        )
        sn_client.create(pid, io.BytesIO(sciobj_bytes), sysmeta_pyxb)
        read_sciobj_bytes = sn_client.get(pid).read()
        assert read_sciobj_bytes == sciobj_bytes

    def test_1020(self, sn_client):
        """create() and get() by SID."""
        pid, sid, sciobj_bytes, sysmeta_pyxb = self._generate_sciobj_with_defaults(
            sn_client, sid='test_sid'
        )
        sn_client.create(pid, io.BytesIO(sciobj_bytes), sysmeta_pyxb)
        read_sciobj_bytes = sn_client.get('test_sid').read()
        assert read_sciobj_bytes == sciobj_bytes

    def test_1030(self, sn_client):
        """create() and getSystemMetadata()"""
        pid, sid, sciobj_bytes, sysmeta_pyxb = self._generate_sciobj_with_defaults(
            sn_client  # , sid='test_sid',
        )
        sn_client.create(pid, io.BytesIO(sciobj_bytes), sysmeta_pyxb)
        read_sysmeta_pyxb = sn_client.getSystemMetadata(pid)
        assert d1_common.xml.get_req_val(
            sysmeta_pyxb.identifier
        ) == d1_common.xml.get_req_val(read_sysmeta_pyxb.identifier)
        assert d1_common.xml.get_opt_val(
            sysmeta_pyxb, 'seriesId'
        ) == d1_common.xml.get_opt_val(read_sysmeta_pyxb, 'seriesId')

    def test_1040(self, sn_client):
        """create() and update(): Valid chain."""
        # create()
        old_pid, old_sid, old_sciobj_bytes, old_sysmeta_pyxb = self._generate_sciobj_with_defaults(
            sn_client, sid='test_sid'
        )
        sn_client.create(old_pid, io.BytesIO(old_sciobj_bytes), old_sysmeta_pyxb)
        # update()
        new_pid, new_sid, new_sciobj_bytes, new_sysmeta_pyxb = self._generate_sciobj_with_defaults(
            sn_client, sid='test_sid'
        )
        sn_client.update(
            old_pid, io.BytesIO(new_sciobj_bytes), new_pid, new_sysmeta_pyxb
        )
        #
        read_old_scimeta_bytes = sn_client.get(old_pid).read()
        read_old_sysmeta_pyxb = sn_client.getSystemMetadata(old_pid)
        read_new_scimeta_bytes = sn_client.get(new_pid).read()
        read_new_sysmeta_pyxb = sn_client.getSystemMetadata(new_pid)

        assert old_sciobj_bytes == read_old_scimeta_bytes
        assert d1_common.xml.get_req_val(read_old_sysmeta_pyxb.identifier) == old_pid
        assert d1_common.xml.get_opt_val(read_old_sysmeta_pyxb, 'seriesId') == old_sid
        assert d1_common.xml.get_opt_val(read_old_sysmeta_pyxb, 'obsoletes') is None
        assert (
            d1_common.xml.get_opt_val(read_old_sysmeta_pyxb, 'obsoletedBy') == new_pid
        )

        assert new_sciobj_bytes == read_new_scimeta_bytes
        assert d1_common.xml.get_req_val(read_new_sysmeta_pyxb.identifier) == new_pid
        assert d1_common.xml.get_opt_val(read_new_sysmeta_pyxb, 'seriesId') == new_sid
        assert d1_common.xml.get_opt_val(read_new_sysmeta_pyxb, 'obsoletes') == old_pid
        assert d1_common.xml.get_opt_val(read_new_sysmeta_pyxb, 'obsoletedBy') is None

    def test_1050(self, sn_client):
        """create() and update(): Conflicting SIDs."""
        # create()
        old_pid, old_sid, old_sciobj_bytes, old_sysmeta_pyxb = self._generate_sciobj_with_defaults(
            sn_client, sid='test_1'
        )
        sn_client.create(old_pid, io.BytesIO(old_sciobj_bytes), old_sysmeta_pyxb)
        # update()
        new_pid, new_sid, new_sciobj_bytes, new_sysmeta_pyxb = self._generate_sciobj_with_defaults(
            sn_client, sid='test_2'
        )
        with pytest.raises(
            AssertionError, match='Attempted to create chain with conflicting SIDs'
        ):
            sn_client.update(
                old_pid, io.BytesIO(new_sciobj_bytes), new_pid, new_sysmeta_pyxb
            )
