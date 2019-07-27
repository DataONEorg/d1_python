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
"""Register this GMN as a new Member Node in a DataONE environment.

The Node document contains basic information about a Member Node, such as it's NodeID
and BaseURL.

Before registration, view the Node document that will be submitted with the node-view
command and update values as needed in the settings.py file.

After registration, there is a manual approval process performed by DataONE. After being
approved, the MN becomes active in the environment and will start receiving DataONE API
calls from the Coordinating Node and end users.

Use node-update to submit an updated Node document if settings in settings.py are
changed after initial registration.

"""

import d1_common.xml

import d1_gmn.app.mgmt_base
import d1_gmn.app.node


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)

    def add_components(self, parser):
        self.using_d1_client(parser)

    def handle_serial(self):
        node_pyxb = d1_gmn.app.node.get_pyxb()
        self.log.info(d1_common.xml.serialize_to_xml_str(node_pyxb, pretty=True))
