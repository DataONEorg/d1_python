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
"""Reprocess all OAI-ORE Resource Maps (data packages).

Reprocess each existing Resource Map Science Object with the algorithm currently used
for new Resource Maps.

Resource Maps are initially processed when they are created by a client create().
Unsuccessful processing causes the create() call to be rejected. The results of
successfully processed Resource Maps are stored in the database. If GMN upgrades cause
the internal representations of Resource Maps to change, this command will redo the
processing and update the database to match the result of current create() calls for
Resource Maps.

Any issues with the previous processing may be resolved by this command as well.
"""

import d1_common.const
import d1_common.util
import d1_common.utils.ulog

import d1_gmn.app.did
import d1_gmn.app.mgmt_base
import d1_gmn.app.model_util
import d1_gmn.app.models
import d1_gmn.app.resource_map
import d1_gmn.app.sciobj_store


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)
        self.res_tracker = None

    def add_components(self, parser):
        self.using_single_instance(parser)

    def add_arguments(self, parser):
        pass

    def handle_serial(self):
        self.reprocess_all()
        self.res_tracker.completed()

    def reprocess_all(self):
        total_count = d1_gmn.app.model_util.count_all_sysmeta_backed_sciobj()
        self.res_tracker = self.tracker.tracker(
            "Reprocessing Resource Maps", total_count
        )
        for sciobj_model in d1_gmn.app.model_util.query_all_sysmeta_backed_sciobj():
            self.res_tracker.step()
            pid = sciobj_model.pid.did
            if not self.is_resource_map(sciobj_model):
                self.res_tracker.event("Not a Resource Map", f"pid={pid}")
            elif not d1_gmn.app.did.is_resource_map_db(pid):
                with d1_gmn.app.sciobj_store.open_sciobj_file_by_pid_ctx(
                    pid
                ) as sciobj_file:
                    resource_map_xml = sciobj_file.read()
                resource_map = d1_gmn.app.resource_map.parse_resource_map_from_str(
                    resource_map_xml
                )
                d1_gmn.app.resource_map.create_or_update(pid, resource_map)
                self.res_tracker.event(
                    "Triggered processing for unprocessed Resource Map", f"pid={pid}"
                )

            else:
                self.res_tracker.event(
                    "Resource Map is already processed", f'pid="{pid}"'
                )

    def is_resource_map(self, sciobj_model):
        return sciobj_model.format.format == d1_common.const.ORE_FORMAT_ID
