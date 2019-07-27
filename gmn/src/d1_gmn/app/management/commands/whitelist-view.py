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
"""View the whitelist of DataONE subject that are allowed to access the DataONE APIs
for creating, updating and deleting Science Objects on this GMN.
"""

import d1_gmn.app
import d1_gmn.app.mgmt_base
import d1_gmn.app.models


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)

    def handle_serial(self):
        whitelist_list = self.get_whitelist_list()
        if not len(whitelist_list):
            self.log.info("The whitelist is empty")
            return
        self.log.info("Subjects in whitelist:")
        for subj_str in whitelist_list:
            self.log.info(f"  {subj_str}")
        self.log.info(f"Total: {len(whitelist_list)}")
