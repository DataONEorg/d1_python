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

"""Export Science Metadata System Metadata values to a JSON file."""

import logging

import d1_gmn.app.management.commands.util.standard_args
import d1_gmn.app.management.commands.util.util
import d1_gmn.app.models
import d1_gmn.app.sysmeta
import d1_gmn.app.sysmeta_extract

import d1_common.util
import d1_common.utils.progress_logger

import django.core.management.base
import django.db.models

# 0 = Timeout disabled
DEFAULT_TIMEOUT_SEC = 0
DEFAULT_WORKER_COUNT = 16
DEFAULT_LIST_COUNT = 1
DEFAULT_PAGE_SIZE = 1000
DEFAULT_API_MAJOR = 2

DEFAULT_MAX_CONCURRENT_TASK_COUNT = 20


# TODO: Add to documentation


# noinspection PyClassHasNoInit,PyAttributeOutsideInit
class Command(django.core.management.base.BaseCommand):
    def _init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        d1_gmn.app.management.commands.util.standard_args.add_arguments(
            parser, __doc__, add_base_url=False
        )
        # Due to limitations in the argparser or Django, could not use `choice` with
        # `nargs='*'`, so handling the list of fields manually as a comma separated
        # list.
        parser.add_argument(
            "--fields",
            default=None,
            help="Comma separated list of fields to include. If not specified, all fields are included. Valid fields: {}".format(
                ",".join(d1_gmn.app.sysmeta_extract.get_valid_field_name_list())
            ),
        )
        parser.add_argument(
            "json_path",
            action="store",
            help="Path to file in which to store the JSON document",
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

        if self.options["fields"] is not None:
            field_list = [v.strip() for v in self.options["fields"].split(",")]
        else:
            field_list = None

        json_path = self.options["json_path"]
        if not json_path.lower().endswith(".json"):
            json_path += ".json"

        self._list(field_list, json_path)

    def _list(self, field_list, json_path):
        with open(json_path, "w", encoding="utf-8") as f:
            d1_gmn.app.sysmeta_extract.extract_values(
                # filter_arg_dict={
                #     'pid__chainmember_pid__chain__sid__did__contains': 'bc'},
                field_list=field_list,
                out_stream=f,
            )
