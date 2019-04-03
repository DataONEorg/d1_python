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

import asyncio
import logging

import d1_gmn.app.did
import d1_gmn.app.management.commands.async_client
import d1_gmn.app.management.commands.objectlist_async
# noinspection PyProtectedMember
import d1_gmn.app.management.commands.util.standard_args
import d1_gmn.app.management.commands.util.util
import d1_gmn.app.models

import d1_common.types.exceptions
import d1_common.utils.progress_logger
import d1_common.xml

import django.conf
import django.core.management.base


# noinspection PyClassHasNoInit,PyAttributeOutsideInit
class Command(django.core.management.base.BaseCommand):
    def _init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        d1_gmn.app.management.commands.util.standard_args.add_arguments(
            parser, __doc__, add_base_url=False
        )

    def handle(self, *args, **options):
        self.options = options
        d1_gmn.app.management.commands.util.util.log_setup(self.options["debug"])
        self._logger = logging.getLogger(__name__.split(".")[-1])
        self.progress_logger = d1_common.utils.progress_logger.ProgressLogger(
            logger=self._logger
        )
        self._logger.info("Running management command: {}".format(__name__))
        d1_gmn.app.management.commands.util.util.exit_if_other_instance_is_running(
            __name__
        )

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self._handle())
        except Exception as e:
            self._logger.exception("Audit failed with exception")
            raise django.core.management.base.CommandError(str(e))
        finally:
            loop.close()
            self.progress_logger.completed()

    async def _handle(self):
        client = d1_gmn.app.management.commands.async_client.AsyncDataONEClient(
            base_url=self.options["baseurl"],
            timeout_sec=self.options["timeout"],
            cert_pub_path=self.options["cert_pem_path"],
            cert_key_path=self.options["cert_key_path"],
            disable_server_cert_validation=self.options[
                "disable_server_cert_validation"
            ],
        )

        # await self.audit_mn_cn_sync(client)
        await self.audit_cn_mn_sync(client)

        await client.close()

    # MN -> CN

    async def audit_mn_cn_sync(self, client):
        task_name = "Auditing MN -> CN sync"

        self.progress_logger.start_task_type(
            task_name, d1_gmn.app.models.ScienceObject.objects.count()
        )

        task_set = set()

        for i, sciobj_model in enumerate(
            d1_gmn.app.models.ScienceObject.objects.order_by("pid__did")
        ):
            self.progress_logger.start_task(task_name)

            pid = sciobj_model.pid.did
            if len(task_set) >= self.options["max_concurrent"]:
                result_set, task_set = await asyncio.wait(
                    task_set, return_when=asyncio.FIRST_COMPLETED
                )
            task_set.add(self.check_object_synced_to_cn(client, pid))

            # Limit number of objects for debugging
            # if i == 234:
            #     break

        result_set, task_set = await asyncio.wait(task_set)
        assert not task_set, "There should be no remaining tasks at this point"

        self.progress_logger.end_task_type(task_name)

    async def check_object_synced_to_cn(self, client, pid):
        if self.is_object_synced_to_cn(client, pid):
            self.progress_logger.event("SciObj has not synced to CN")
            self._logger.error("SciObj has not synced to CN: {}".format(pid))
        else:
            self.progress_logger.event("SciObj already synced on CN")

    async def is_object_synced_to_cn(self, client, pid):
        """Check if object with {pid} has successfully synced to the CN.

        CNRead.describe() is used as it's a light-weight HTTP HEAD request.

        This assumes that the call is being made over a connection that has been
        authenticated and has read or better access on the given object if it exists.

        """
        try:
            await client.describe(pid)
        except d1_common.types.exceptions.DataONEException:
            return False
        return True

    # CN -> MN

    async def audit_cn_mn_sync(self, client):
        task_name = "Auditing CN -> MN sync"

        self.progress_logger.start_task_type(
            task_name, d1_gmn.app.models.ScienceObject.objects.count()
        )

        object_list_iterator = d1_gmn.app.management.commands.objectlist_async.ObjectListIteratorAsync(
            client,
            retry_count=self.options["retries"],
            list_objects_args_dict={'nodeId': django.conf.settings.NODE_IDENTIFIER},
        )
        async for object_info_pyxb in object_list_iterator.itr():
            self.progress_logger.start_task(task_name)

            pid = d1_common.xml.get_req_val(object_info_pyxb.identifier)
            if self.is_object_still_on_mn(pid):
                self.progress_logger.event("SciObj on CN is still on MN")
            else:
                self.progress_logger.event("SciObj on CN is missing on MN")
                self._logger.error("SciObj on CN is missing on MN: {}".format(pid))

        self.progress_logger.end_task_type(task_name)

    def is_object_still_on_mn(self, pid):
        """Check if object with {pid} that the CN reports to be on this GMN instance is
        actually here."""
        return d1_gmn.app.did.is_existing_object(pid)
