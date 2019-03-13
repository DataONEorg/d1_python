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

import asyncio
import logging
import logging.config

import d1_gmn.app.auth
import d1_gmn.app.delete
import d1_gmn.app.did
import d1_gmn.app.event_log

# noinspection PyProtectedMember
import d1_gmn.app.management.commands.util.standard_args as args
import d1_gmn.app.management.commands.util.util as util
import d1_gmn.app.management.commands.async_client
import d1_gmn.app.management.commands.objectlist_async
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

import d1_common.checksum
import d1_common.const
import d1_common.date_time
import d1_common.revision
import d1_common.system_metadata
import d1_common.type_conversions
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.url
import d1_common.util
import d1_common.utils.progress_logger
import d1_common.xml

import django.conf
import django.core.management.base
import django.db

DEFAULT_TIMEOUT_SEC = 0
DEFAULT_PAGE_SIZE = 1000
DEFAULT_API_MAJOR = 2
DEFAULT_MAX_CONCURRENT_TASK_COUNT = 20

# noinspection PyClassHasNoInit,PyAttributeOutsideInit
class Command(django.core.management.base.BaseCommand):
    def _init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        args.add_arguments(parser, __doc__)

    def handle(self, *args, **options):
        self.options = options
        util.log_setup(self.options["debug"])
        self._logger = logging.getLogger(__name__.split(".")[-1])
        self.progress_logger = d1_common.utils.progress_logger.ProgressLogger(
            logger=self._logger
        )
        self._logger.info("Running management command: {}".format(__name__))
        util.exit_if_other_instance_is_running(__name__)

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
