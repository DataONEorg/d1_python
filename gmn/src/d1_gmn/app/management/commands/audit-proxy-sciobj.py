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

"""Check that proxy Science Objects are available and undamaged at their storage
locations on 3rd party servers.

Most clients provide object bytes when creating objects on GMN, causing GMN to store a
local copy of the object in a designated directory hierarchy on the local filesystem.
However, GMN also provides a vendor specific extension that allows a client to provide a
URL referencing the object bytes on a 3rd party server instead of providing the actual
bytes when creating the object. This allows making an object available in the DataONE
federation without having to create a duplicate of an object that is already available
online. Such objects are referred to as proxy objects in GMN.

Whenever the bytes are requested for a proxy object via DataONE APIs, GMN streams the
bytes through from the 3rd party server to the client. As any objects that are not
available will cause errors to be returned to users, it is important that they remain
available and unchanged on the 3rd party servers.

This command verifies proxy objects by fully downloading the object bytes, recalculating
the checksum and comparing it with the checksum that was originally supplied by the
client that created the object.

By default, all proxy objects are checked. Checks can be restricted to a smaller set of
objects by providing a path to a file holding a list of PIDs of objects to check.
Warnings are logged for any PIDs in the list that are not proxy objects.


Fixing broken URLs
~~~~~~~~~~~~~~~~~~

- If the object has moved to another known location on a 3rd party server:

  - Update the local URL with `diag-proxy-set-url`_ or have the server return a 3xx
    Redirect header pointing to the current location of the object. GMN will follow
    redirects until arriving at a page that returns a non-redirect status code. If
    the status code is 200 OK, the object is streamed from there to the client. If
    it's any other status code, a DataONE Exception XML type and status code is
    returned to the client.

- If the object is no longer available on the 3rd party server:

  - If there is a replica of the object on another MN, an option is to convert the
    proxy object to a regular object with the `diag-restore-sciobj`_ command. See the
    documentation for that command for more information.

  - If no replica of the object is available,

If provided, the file must be UTF-8 encoded if it contains any PIDs with non-ASCII
characters.

"""

import d1_gmn.app.did
import d1_gmn.app.mgmt_base
import d1_gmn.app.model_util
import d1_gmn.app.models
import d1_gmn.app.proxy


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)
        self.audit_tracker = None

    def add_components(self, parser):
        self.using_single_instance(parser)
        self.using_pid_file(parser)
        self.using_async_d1_client(parser, fixed_base_url="http://invalid")

    async def handle_async(self):
        if self.pid_set:
            await self.audit_proxy_by_pid_list()
        else:
            await self.audit_proxy_all()
        await self.await_all()
        self.audit_tracker.completed()

    async def audit_proxy_all(self):
        """Audit all proxy SciObj on this MN."""
        self.log.info("Starting proxy SciObj audit")
        total_count = d1_gmn.app.model_util.count_all_sysmeta_backed_sciobj()
        self.log.info(
            "Number of SciObj found (including non-proxy): {}".format(total_count)
        )
        self.audit_tracker = self.tracker.tracker("Auditing proxy SciObj", total_count)
        for sciobj_model in d1_gmn.app.model_util.query_all_sysmeta_backed_sciobj():
            await self.add_task(self.audit_proxy_pid(sciobj_model.pid.did))

    async def audit_proxy_by_pid_list(self):
        """Audit proxy SciObj on this MN by PID list file."""
        self.log.info("Starting proxy SciObj audit")
        total_count = len(self.pid_set)
        self.log.info(
            "Number of SciObj found (including non-proxy): {}".format(total_count)
        )
        self.audit_tracker = self.tracker.tracker("Auditing proxy SciObj", total_count)
        for pid in self.pid_set:
            await self.add_task(self.audit_proxy_pid(pid))

    async def audit_proxy_pid(self, pid):
        self.audit_tracker.step()
        try:
            sciobj_model = d1_gmn.app.model_util.get_sci_model(pid)
        except d1_gmn.app.models.ScienceObject.DoesNotExist:
            self.audit_tracker.event(
                "Received unknown PID", f'pid="{pid}"', is_error=True
            )
            return

        sciobj_url = sciobj_model.url
        if not d1_gmn.app.proxy.is_proxy_url(sciobj_url):
            self.audit_tracker.event(
                "Skipped locally stored (non-proxy) SciObj", f'pid="{pid}"'
            )
            return

        async with await self.async_d1_client.session.head(sciobj_url) as response:
            if response.status == 200:
                self.tracker.event(f"Proxy responded with 200 OK")
            else:
                self.tracker.event(
                    f"Proxy responded with unexpected status code",
                    'sciobj_url="{}" status={}'.format(sciobj_url, response.status),
                    is_error=True,
                )
