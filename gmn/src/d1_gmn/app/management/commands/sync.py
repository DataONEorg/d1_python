# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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

import argparse
import asyncio
import logging
import logging.config
import time

import d1_gmn.app.auth
import d1_gmn.app.delete
import d1_gmn.app.did
import d1_gmn.app.event_log

# noinspection PyProtectedMember
import d1_gmn.app.management.commands._util as util
import d1_gmn.app.management.commands.async_client
import d1_gmn.app.model_util
import d1_gmn.app.models
import d1_gmn.app.node
import d1_gmn.app.revision
import d1_gmn.app.sciobj_store
import d1_gmn.app.sysmeta
import d1_gmn.app.util
import d1_gmn.app.views.assert_db
import d1_gmn.app.views.create
import d1_gmn.app.views.util

import d1_common.const
import d1_common.revision
import d1_common.system_metadata
import d1_common.type_conversions
import d1_common.types.exceptions
import d1_common.url
import d1_common.util
import d1_common.xml
import d1_common.utils.progress_logger

import django.conf
import django.core.management.base
import django.db

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
        parser.description = __doc__
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument("--debug", action="store_true", help="Debug level logging")
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
            "--public",
            action="store_true",
            help="Do not use certificate even if available",
        )
        parser.add_argument(
            "--disable-server-cert-validation",
            action="store_true",
            help="Do not validate the TLS/SSL server side certificate of the source "
            "node (insecure)",
        )
        parser.add_argument(
            "--timeout",
            type=float,
            action="store",
            default=DEFAULT_TIMEOUT_SEC,
            help="Timeout for DataONE API calls to the source MN",
        )
        parser.add_argument(
            "--concurrent",
            type=int,
            action="store",
            default=DEFAULT_MAX_CONCURRENT_TASK_COUNT,
            help="Max number of concurrent API calls to the CN",
        )
        parser.add_argument("baseurl", help="Source MN or CN BaseURL")

    def handle(self, *args, **options):
        self.progress_logger = d1_common.utils.progress_logger.ProgressLogger()

        util.log_setup(options["debug"])
        logging.info("Running management command: {}".format(__name__))
        util.exit_if_other_instance_is_running(__name__)

        # Python 3.7
        # asyncio.run(self._handle(options))
        # Python 3.6
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self._handle(options))
        except Exception as e:
            logging.exception("Sync raised exception")
            logging.info("-" * 79)
            raise django.core.management.base.CommandError(str(e))
        finally:
            loop.close()

        self.progress_logger.completed()

    async def _handle(self, options):
        client = d1_gmn.app.management.commands.async_client.AsyncCoordinatingNodeClient_2_0(
            options["baseurl"],
            options["timeout"],
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
            if len(task_set) >= options["concurrent"]:
                result_set, task_set = await asyncio.wait(
                    task_set, return_when=asyncio.FIRST_COMPLETED
                )
            task_set.add(self.check_and_sync(client, pid))

            # Limit number of objects for debugging
            # if i == 234:
            #     break

        result_set, task_set = await asyncio.wait(task_set)
        assert not task_set, "There should be no remaining tasks at this point"

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
            self.progress_logger.event("SciObj has been successfully synced to CN")
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
        """Issue a notification and request for sync for object with {pid} to
        the CN.
        """
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
