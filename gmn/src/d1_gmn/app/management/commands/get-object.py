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

import d1_gmn.app.management.commands.async_client
import d1_gmn.app.management.commands.objectlist_async
# noinspection PyProtectedMember
import d1_gmn.app.management.commands.util.standard_args
import d1_gmn.app.management.commands.util.util

import d1_common.utils.progress_logger

import django.core.management.base

DEFAULT_TIMEOUT_SEC = 0
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
            self._logger.exception("Import failed with exception")
            raise django.core.management.base.CommandError(str(e))
        finally:
            loop.close()
            self.progress_logger.completed()

    async def _handle(self):
        aclient = d1_gmn.app.management.commands.async_client.AsyncDataONEClient(
            base_url=self.options["baseurl"],
            timeout_sec=self.options["timeout"],
            cert_pub_path=self.options["cert_pem_path"],
            cert_key_path=self.options["cert_key_path"],
            disable_server_cert_validation=self.options[
                "disable_server_cert_validation"
            ],
            retry_count=self.options["retries"],
        )

        event_log_iterator = d1_gmn.app.management.commands.objectlist_async.ObjectListIteratorAsync(
            aclient,
            page_size=self.options["page_size"],
            list_objects_args_dict={
                # 'idFilter': django.conf.settings.NODE_IDENTIFIER,
            },
            max_concurrent_d1_rest_calls=self.options["max_concurrent"],
        )

        i = 0
        async for object_info_pyxb in event_log_iterator.itr():
            i += 1
            self._logger.info(i)
            self._logger.info(object_info_pyxb.toxml())

        await aclient.close()
