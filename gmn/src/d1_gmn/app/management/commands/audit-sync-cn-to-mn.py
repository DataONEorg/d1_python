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

"""Check local availability of SciObj for which the CN has this GMN registered as
authoritative.

The CN is queried for a complete list of objects for which this GMN is registered as the
authoritative Member Node, meaning that it is the primary location from which the object
should be available.

The identifiers (PIDs) are displayed along with a summary for any objects that do not
exist locally.

"""

# TODO: Add check for objects for which this GMN is registered as holding a replica.
# Requires a Solr query.

import django.conf
import django.core.management.base

import d1_gmn.app.did
import d1_gmn.app.mgmt_base
import d1_gmn.app.models


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)
        self.audit_tracker = None

    def add_components(self, parser):
        self.using_single_instance(parser)
        self.using_pid_file(parser)
        self.using_async_object_list_iter(
            parser,
            fixed_list_objects_arg_dict={
                "nodeId": django.conf.settings.NODE_IDENTIFIER
            },
        )

    async def handle_async(self, *args):
        if self.pid_set:
            await self.audit_cn_to_mn_by_pid_set()
        else:
            await self.audit_cn_to_mn()
        await self.await_all()
        self.audit_tracker.completed()

    async def audit_cn_to_mn(self):
        self.log.info("Starting CN SciObj audit")
        total_count = await self.async_object_list_iter.total
        self.log.info("Number of CN SciObj to audit: {}".format(total_count))
        self.audit_tracker = self.tracker.tracker(
            "Auditing local availability of CN SciObj", total_count
        )
        async for object_info_pyxb in self.async_object_list_iter:
            pid = object_info_pyxb.identifier.value()
            await self.add_task(self.audit_cn_to_mn_pid(pid))

    async def audit_cn_to_mn_by_pid_set(self):
        self.log.info("Starting CN SciObj audit from PID file")
        pid_set = self.load_set_from_file(self.opt_dict["pid_path"])
        total_count = len(pid_set)
        self.log.info("Number of CN SciObj to audit: {}".format(total_count))
        if not total_count:
            self.log.error("Aborted: Loaded empty list from file")
            return
        self.audit_tracker = self.tracker.tracker(
            "Auditing local availability of CN SciObj by PID file", total_count
        )
        for pid in pid_set:
            await self.add_task(self.audit_cn_to_mn_pid(pid))

    async def audit_cn_to_mn_pid(self, pid):
        self.audit_tracker.step()

        if d1_gmn.app.did.is_existing_object(pid):
            self.audit_tracker.event(
                "Audit OK: Object for which this GMN is registered as authoritative exists locally",
                f'pid="{pid}"',
            )
        else:
            self.audit_tracker.event(
                "Audit failed: Object for which this GMN is registered as authoritative is {}".format(
                    d1_gmn.app.did.classify_identifier(pid)
                ),
                f'pid="{pid}"',
                is_error=True,
            )
