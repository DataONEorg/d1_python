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

"""Check GMN to CN Science Object synchronization and issues synchronization requests as
required.

This command queries the CN for basic information about each object that currently
exists locally. If the CN indicates that the object is unknown by responding with an
error, such as a 404 Not Found, the PID and basic information about the issue is
displayed. At program exit, a list of encountered issues with a count of occurrences for
each is displayed.

Unless disabled with the --no-sync switch, a request for sync is also sent to the CN via
the CNRead.synchronize() API for any objects found not to have synced.

CN connections are made using the DataONE provided client side certificate, which should
give access on the CN to all objects for which this GMN is registered as authoritative,
meaning that this GMN is the primary location from which the object should be available.

Unless the CN is working through large numbers of objects recently added to Member
Nodes, objects should synchronize to the CN in less than 24 hours. If, after that time,
objects are reported as unknown by the CN, the cause should be investigated.

Background
~~~~~~~~~~

The CN keeps its database of science objects that are available in the federation up to
date by regularly connecting to each MN and polling for new objects. The design of this
synchronization mechanism was kept simple in order to keep MN implementation complexity
as low as possible. The main disadvantage to the approach is that it's possible for
objects to slip through the regular sync and remain undiscovered by the CN. This may
happen due to bugs in the CN or MN stacks, but can also happen even when the system is
working as intended. For instance, if new objects are created on the MN or the system
clock on either the MN or CN is adjusted while synchronization is in progress.

In addition to the regular sync process, in which the CN polls MNs for new objects, the
CN provides the CNRead.synchronize() REST API, by which MNs can directly notify the CN
of the existence of a specific object that was not discovered during regular sync, and
request that the CN synchronizes it. The CN responds by adding a task to sync the
specified object to its task queue. When the CN later processes the task, the object is
synced using the same procedure by which objects that are discovered by the regular poll
are synced.

"""

import d1_gmn.app.mgmt_base
import d1_gmn.app.models


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)
        self.audit_tracker = None

    def add_components(self, parser):
        self.using_single_instance(parser)
        self.using_pid_file(parser)
        self.using_async_d1_client(parser)

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-sync",
            action="store_true",
            help="Do not issue sync requests for objects missing on the CN",
        )

    async def handle_async(self):
        self.log.info("Starting MN SciObj audit")
        total_count = await self.query_sciobj_count()
        self.log.info("Number of MN SciObj to audit: {}".format(total_count))
        self.audit_tracker = self.tracker.tracker(
            "Auditing CN availability of local SciObj", total_count
        )
        for sciobj_model in self.query_sciobj_with_pid_filter():
            await self.add_task(self.check_and_sync(sciobj_model.pid.did))

    async def check_and_sync(self, pid):
        self.audit_tracker.step()
        if not await self.is_object_synced_to_cn(pid):
            if not self.opt_dict["no_sync"]:
                await self.send_synchronization_request(pid)

    async def is_object_synced_to_cn(self, pid):
        """Check if object with {pid} has successfully synced to the CN.

        CNRead.describe() is used as it's a light-weight HTTP HEAD request.

        This assumes that the call is being made over a connection that has been
        authenticated and has read or better access on the given object if it exists. By
        default, connections are authenticated using a client side certificate, which
        should provide the required access.
        """
        status = await self.async_d1_client.describe(pid)
        if status == 200:
            self.audit_tracker.event(
                "Audit OK: SciObj already synced on CN", f'pid="{pid}"'
            )
            return True
        elif status == 404:
            self.audit_tracker.event(
                "Audit failed: SciObj has not synced to CN",
                f'pid="{pid}"',
                is_error=True,
            )
            return False
        self.audit_tracker.event(
            "CNRead.describe() returned unexpected status code. ",
            f'pid="{pid}" status="{status}"',
        )
        return True

    async def send_synchronization_request(self, pid):
        """Issue a notification and request for sync for object with {pid} to the CN."""
        # Skip CN call for debugging
        # status = 200
        status = await self.async_d1_client.synchronize(pid)
        if status == 200:
            self.audit_tracker.event("Issued sync request, CN accepted", f'pid="{pid}"')
        else:
            self.audit_tracker.event(
                "CNRead.synchronize() returned unexpected status code. ",
                f'pid="{pid}" status="{status}"',
                is_error=True,
            )
