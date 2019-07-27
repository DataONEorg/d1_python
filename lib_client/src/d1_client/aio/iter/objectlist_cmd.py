#!/usr/bin/env python

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
"""Utilities for command line tools that instantiate `DataONEClient()`,
`CoordinatingNodeClient()`, or `MemberNodeClient()` objects.

The intention is to both reduce the amount of boilerplate code in command line tools
that interact with the DataONE infrastructure and to standardize the behavior of the
scripts.

"""
import d1_common.utils.arg_parse
import d1_common.utils.ulog

import d1_client.aio.async_client
import d1_client.aio.iter.objectlist_async


class AsyncArgParser(d1_common.utils.arg_parse.ArgParserBase):
    def __init__(self, *args, **kwargs):
        self.parser_name = "Async ObjectList Iterator"
        self.parser_dict = {
            "object_list_ignore_errors": (
                "--object-list-ignore-errors",
                dict(
                    action="store_true",
                    help="Ignore errors that may cause incomplete results",
                ),
            ),
            "object_list_page_size": (
                "--object-list-page-size",
                dict(
                    type=int,
                    default=d1_client.aio.async_client.DEFAULT_PAGE_SIZE,
                    metavar="N",
                    action="store",
                    help="Number of items to retrieve in each page for DataONE APIs "
                    "that support paging",
                ),
            ),
            "list_objects_arg_dict": (
                "--list-objects-args",
                dict(
                    type=dict,
                    default={},
                    metavar="dict",
                    action="store",
                    help="Dictionary of arguments to pass to the listObjects API call",
                ),
            ),
        }
        super().__init__(*args, **kwargs)
