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
"""Multiprocessed ObjectList Iterator.

Fast retrieval of ObjectList from a DataONE Node.

See additional notes in SysMeta iter docstring.

"""

import logging

import d1_client.iter.base_multi

logger = logging.getLogger(__name__)


# fmt: off
class ObjectListIteratorMulti(d1_client.iter.base_multi.MultiprocessedIteratorBase):
    def __init__(
        self,
        base_url,
        page_size=d1_client.iter.base_multi.PAGE_SIZE,
        max_workers=d1_client.iter.base_multi.MAX_WORKERS,
        max_result_queue_size=d1_client.iter.base_multi.MAX_RESULT_QUEUE_SIZE,
        max_task_queue_size=d1_client.iter.base_multi.MAX_TASK_QUEUE_SIZE,
        api_major=d1_client.iter.base_multi.API_MAJOR,
        client_arg_dict=None,
        list_objects_arg_dict=None,
    ):
        super(ObjectListIteratorMulti, self).__init__(
            base_url, page_size, max_workers, max_result_queue_size,
            max_task_queue_size, api_major, client_arg_dict, list_objects_arg_dict,
            None, _page_func, _iter_func, _item_proc_func
        )


def _page_func(client):
    return client.listObjects


def _iter_func(page_pyxb):
    return page_pyxb.objectInfo


# noinspection PyUnusedLocal
def _item_proc_func(client_, item_pyxb, item_proc_arg_dict_):
    return item_pyxb
