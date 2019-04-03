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

"""Compare the local GMN and CN SciObj lists and issue synchronization requests to the
CN for any SciObj that are only present locally, and so are unknown to the CN.

This management command iterates over all objects stored on the local GMN instance and,
for each object, checks if the object is known to the CN by querying the CN for basic
information about the object. If the CN indicates that the object is unknown by
responding with an error, such as a 404 Not Found, the command then issues a
notification and request for sync for the object to the CN via the CNRead.synchronize()
API.

Background:

The CN keeps its database of science objects that are available in the federation up to
date by regularly connecting to each MN and polling for new objects. The design of this
synchronization mechanism was kept simple in order to keep MN implementation complexity
as low as possible. The main disadvantage to the approach is that it's possible for
objects to slip through the regular sync and remain undiscovered on the MN. This may
happen due to bugs in the CN or MN stacks, but can also happen even when the system is
working as intended. For instance, if new objects are created on the MN or the system
clock on either the MN or CN is adjusted while synchronization is in progress.

So, in addition to the regular sync process, in which the CN polls MNs for new objects,
the CN provides the CNRead.synchronize() REST API, by which MNs can directly notify the
CN of the existence of a specific object that was not discovered during regular sync,
and request that the CN synchronizes it. The CN responds by adding a task to sync the
specified object to its task queue. When the CN later processes the task, the object is
synced just as if it was discovered by the regular poll based sync.

"""

import asyncio
import logging

import d1_gmn.app.management.commands.async_client
# noinspection PyProtectedMember
import d1_gmn.app.management.commands.util.standard_args
import d1_gmn.app.management.commands.util.util
import d1_gmn.app.models

import d1_common.utils.progress_logger

import django.conf
import django.core.management.base

# 0 = Timeout disabled

DEFAULT_TIMEOUT_SEC = 0
DEFAULT_WORKER_COUNT = 16
DEFAULT_LIST_COUNT = 1
DEFAULT_PAGE_SIZE = 1000
DEFAULT_API_MAJOR = 2

DEFAULT_MAX_CONCURRENT_TASK_COUNT = 20

# noinspection PyClassHasNoInit,PyAttributeOutsideInit
class Command(django.core.management.base.BaseCommand):
    def _init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        d1_gmn.app.management.commands.util.standard_args.add_arguments(parser, __doc__)

    def handle(self, *args, **options):
        self.options = options
        logging.basicConfig(level=logging.DEBUG)
        self._log = logging.getLogger(__name__.split(".")[-1])
        self.progress_logger = d1_common.utils.progress_logger.ProgressLogger(
            logger=self._log
        )
        # util.log_setup(self.options["debug"])
        self._log.info("Running management command: {}".format(__name__))
        d1_gmn.app.management.commands.util.util.exit_if_other_instance_is_running(
            __name__
        )

        # Python 3.7
        # asyncio.run(self._handle())
        # Python 3.6
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self._handle())
        except Exception as e:
            self._log.exception("Sync failed with exception")
            raise django.core.management.base.CommandError(str(e))
        finally:
            loop.close()
            self.progress_logger.completed()

    async def _handle(self):
        client = d1_gmn.app.management.commands.async_client.AsyncDataONEClient(
            self.options["baseurl"],
            self.options["timeout"],
            django.conf.settings.CLIENT_CERT_PATH,
            django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH,
        )

        task_set = set()

        self.progress_logger.start_task_type(
            "Sync MN -> CN", d1_gmn.app.models.ScienceObject.objects.count()
        )

        for i, sciobj_model in enumerate(
            d1_gmn.app.models.ScienceObject.objects.order_by("pid__did")
        ):
            self.progress_logger.start_task("Sync MN -> CN")

            pid = sciobj_model.pid.did
            if len(task_set) >= self.options["max_concurrent"]:
                result_set, task_set = await asyncio.wait(
                    task_set, return_when=asyncio.FIRST_COMPLETED
                )
            task_set.add(self.check_and_sync(client, pid))

            # Limit number of objects for debugging
            # if i == 234:
            #     break

        await asyncio.wait(task_set)

        self.progress_logger.end_task_type("Sync MN -> CN")

        await client.close()

    async def check_and_sync(self, client, pid):
        if not await self.is_object_synced_to_cn(client, pid):
            await self.send_synchronization_request(client, pid)

    async def is_object_synced_to_cn(self, client, pid):
        """Check if object with {pid} has successfully synced to the CN.

        CNRead.describe() is used as it's a light-weight HTTP HEAD request.

        This assumes that the call is being made over a connection that has
        been authenticated and has read or better access on the given object if
        it exists.

        """
        status = await client.describe(pid)
        if status == 200:
            self.progress_logger.event("SciObj already synced on CN")
            return True
        elif status == 404:
            self.progress_logger.event("SciObj has not synced to CN")
            return False
        self.progress_logger.event(
            "CNRead.describe() returned unexpected status code. "
            'pid="{}" status="{}"'.format(pid, status)
        )
        return True

    async def send_synchronization_request(self, client, pid):
        """Issue a notification and request for sync for object with {pid} to the CN."""
        # Skip CN call for debugging
        # status = 200
        status = await client.synchronize(pid)
        if status == 200:
            self.progress_logger.event("Issued sync request, CN accepted")
        else:
            self.progress_logger.event(
                "CNRead.synchronize() returned unexpected status code. "
                'pid="{}" status="{}"'.format(pid, status)
            )
