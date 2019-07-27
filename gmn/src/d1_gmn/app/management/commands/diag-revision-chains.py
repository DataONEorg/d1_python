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
"""Examine and repair revision / obsolescence chains.

obsoleted and obsoletedBy references should not break during regular use of GMN in
production, but it may happen during development or if the database is manipulated
directly during testing.

"""

import d1_gmn.app.did
import d1_gmn.app.mgmt_base
import d1_gmn.app.model_util
import d1_gmn.app.models
import d1_gmn.app.revision


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
            "Reprocessing Revision / Obsolescence chains", total_count
        )
        for sciobj_model in d1_gmn.app.model_util.query_all_sysmeta_backed_sciobj():
            self.res_tracker.step()

            self.res_tracker.event(
                "Writing revision chains",
                f'sciobj_model.pid.did="{sciobj_model.pid.did}"',
            )

            obsoletes_pid = d1_gmn.app.did.get_did_by_foreign_key(
                sciobj_model.obsoletes
            )
            obsoleted_by_pid = d1_gmn.app.did.get_did_by_foreign_key(
                sciobj_model.obsoleted_by
            )

            d1_gmn.app.revision.set_revision_links(
                sciobj_model, obsoletes_pid, obsoleted_by_pid
            )
            d1_gmn.app.revision.create_or_update_chain(
                sciobj_model.pid.did, None, obsoletes_pid, obsoleted_by_pid
            )
