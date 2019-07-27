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

import logging


class NodeListIterator(object):
    """Iterate over the nodes that are registered in a DataONE environment.

    This is a serial implementation. See :ref:`d1_client/ref/iterators:DataONE
    Iterators` for an overview of the available iterator types and implementations.
    """

    def __init__(self, cn_client):
        self._cn_client = cn_client
        self._log = logging.getLogger(__name__)

    def __iter__(self):
        # The NodeList type does not support slicing.
        node_list_pyxb = self._cn_client.listNodes()
        self._log.debug("Retrieved {} Node documents".format(len(node_list_pyxb.node)))
        for node_pyxb in sorted(
            node_list_pyxb.node, key=lambda x: x.identifier.value()
        ):
            yield node_pyxb
