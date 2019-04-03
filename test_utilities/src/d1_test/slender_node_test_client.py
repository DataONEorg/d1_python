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
import atexit
import io
import json
import os
import urllib.parse

import d1_common
import d1_common.types
import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.xml

DEFAULT_SCIOBJ_STORE_PATH = "./sciobj_store"
SCIOBJ_EXT_STR = ".sciobj.bin"
SYSMETA_EXT_STR = ".sysmeta.xml"
SID_MAP_FILENAME = "sid.json"


# noinspection PyUnusedLocal
class SlenderNodeTestClient:
    """A simple drop-in replacement for a MN client, for use when developing and testing
    SlenderNode scripts.

    - MN is simulated to the bare minimum required by SN scripts
    - Objects are stored in local files instead of on an MN
    - SID to PID dict is held in memory and dumped to file
    - Most args are simply ignored

    """

    def __init__(
        self,
        sciobj_store_path=DEFAULT_SCIOBJ_STORE_PATH,
        keep_existing=False,
        *args,
        **kwargs
    ):
        """Create the test client.

        - Store the sciobj and sysmeta in ``sciobj_store_path``
        - ``sciobj_store_path`` is created if it does not exist
        - If ``delete_existing`` is True, delete any existing files in
          ``sciobj_store_path``

        """
        self.sciobj_store_path = os.path.abspath(sciobj_store_path)
        os.makedirs(sciobj_store_path, exist_ok=True)
        if not keep_existing:
            self._delete_existing()
        self.did_json_path = os.path.join(self.sciobj_store_path, SID_MAP_FILENAME)
        self.did_dict = self._read_did_dict()
        atexit.register(self._cleanup)
        self.pyxb_binding = d1_common.types.dataoneTypes_v2_0

    def create(self, pid, sciobj_file, sysmeta_pyxb, *args, **kwargs):
        assert sysmeta_pyxb.obsoletedBy is None
        assert sysmeta_pyxb.obsoletes is None
        self._add_sid_map(sysmeta_pyxb)
        self._write_sysmeta_file(pid, sysmeta_pyxb)
        self._write_sciobj_file(pid, sciobj_file)

    def update(self, old_pid, sciobj_file, new_pid, new_sysmeta_pyxb, *args, **kwargs):
        old_sysmeta_pyxb = self._read_sysmeta_file(old_pid)
        assert old_sysmeta_pyxb.obsoletedBy is None
        assert new_sysmeta_pyxb.obsoletes is None
        old_sid = d1_common.xml.get_opt_val(old_sysmeta_pyxb, 'seriesId')
        new_sid = d1_common.xml.get_opt_val(new_sysmeta_pyxb, 'seriesId')
        if old_sid is not None:
            assert (
                new_sid is None or new_sid == old_sid
            ), 'Attempted to create chain with conflicting SIDs'
        old_sysmeta_pyxb.seriesId = new_sid
        old_sysmeta_pyxb.obsoletedBy = new_pid
        new_sysmeta_pyxb.obsoletes = old_pid
        self._write_sysmeta_file(old_pid, old_sysmeta_pyxb, overwrite=True)
        self._write_sysmeta_file(new_pid, new_sysmeta_pyxb)
        self._write_sciobj_file(new_pid, sciobj_file)

    def get(self, did, *args, **kwargs):
        """Return a file-like object with the sciobj bytes."""
        return io.BytesIO(self._read_sciobj_file(did))

    def getSystemMetadata(self, did, *args, **kwargs):
        """Return sysmeta_pyxb."""
        return self._read_sysmeta_file(did)

    #
    # Private
    #

    def _delete_existing(self):
        # If the sciobj store is set to an existing directory with unrelated files by
        # mistake, this could delete those files. To help prevent that, this is not
        # recursive and deletes only files with the extensions we use.
        for dir_entry in list(os.scandir(self.sciobj_store_path)):
            if dir_entry.is_file():
                ext_str = os.path.splitext(dir_entry.name)
                if dir_entry.name == SID_MAP_FILENAME or ext_str in (
                    SCIOBJ_EXT_STR,
                    SYSMETA_EXT_STR,
                ):
                    os.unlink(dir_entry.path)

    def _cleanup(self):
        self._write_did_dict()

    def _read_sciobj_file(self, did):
        """Raise NotFound if ``did`` does not exist as SID or PID."""
        return self._read_file(self._get_sciobj_path(did))

    def _write_sciobj_file(self, did, sciobj_file):
        """Raise IdentifierNotUnique if ``did`` already exists."""
        self._write_file(self._get_sciobj_path(did), sciobj_file.read())

    def _read_sysmeta_file(self, did):
        """Return sysmeta_pyxb.

        - Raise NotFound if ``did`` does not exist as SID or PID

        """
        return d1_common.types.dataoneTypes.CreateFromDocument(
            self._read_file(self._get_sysmeta_path(did))
        )

    def _write_sysmeta_file(self, did, sysmeta_pyxb, overwrite=False):
        """Write sysmeta_pyxb.

        - Raise IdentifierNotUnique if ``did`` already exists

        """
        self._write_file(
            self._get_sysmeta_path(did),
            d1_common.xml.serialize_for_transport(sysmeta_pyxb, pretty=True),
            overwrite=overwrite,
        )

    def _sid_lookup(self, did):
        """If ``did`` is a SID, return head PID, else return ``did``"""
        return self.did_dict.get(did, did)

    def _add_sid_map(self, sysmeta_pyxb):
        sid = d1_common.xml.get_opt_val(sysmeta_pyxb, 'seriesId')
        if sid is not None:
            self.did_dict[sid] = d1_common.xml.get_req_val(sysmeta_pyxb.identifier)

    def _get_sciobj_path(self, did):
        return self._get_safe_path(self._sid_lookup(did), SCIOBJ_EXT_STR)

    def _get_sysmeta_path(self, did):
        return self._get_safe_path(self._sid_lookup(did), SYSMETA_EXT_STR)

    def _get_safe_path(self, pid, ext_str):
        return os.path.join(
            self.sciobj_store_path,
            urllib.parse.quote(pid.encode("utf-8"), safe=" @$,~*&") + ext_str,
        )

    def _read_did_dict(self):
        if os.path.exists(self.did_json_path):
            with open(self.did_json_path, "rb") as f:
                return json.load(f)
        else:
            return {}

    def _write_did_dict(self):
        if os.path.exists(self.sciobj_store_path):
            with open(self.did_json_path, "wb") as f:
                json.dump(self.did_dict, f)

    def _read_file(self, path):
        if os.path.exists(path):
            with open(path, "rb") as f:
                return f.read()
        else:
            raise d1_common.types.exceptions.NotFound(
                0, 'Does not exist. path="{}"'.format(path)
            )

    def _write_file(self, path, b, overwrite=False):
        if not overwrite and os.path.exists(path):
            raise d1_common.types.exceptions.IdentifierNotUnique(
                0, 'Already exists. path="{}"'.format(path)
            )
        with open(path, "wb") as f:
            f.write(b)
