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
"""Synchronize the whitelist of DataONE subject that are allowed to access the DataONE
APIs for creating, updating and deleting Science Objects on this GMN.

This command synchronizes the whitelist with a a list of subjects provided in a file,
adding and deleting subjects from the whitelist as required in order to create a
whitelist that exactly matches the file.

The file must contain a single DataONE subject string per line.

"""

import d1_gmn.app
import d1_gmn.app.mgmt_base
import d1_gmn.app.models


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            "whitelist-file",
            help="Path to an ASCII or UTF-8 file containing a list of DataONE subjects",
        )

    def handle_serial(self):
        add_count = 0
        del_count = 0
        file_subj_set = self.load_set_from_file(self.opt_dict["whitelist-file"])
        whitelist_subj_set = set(self.get_whitelist_list())
        for add_subj_str in sorted(file_subj_set - whitelist_subj_set):
            self.add_subj_to_whitelist(add_subj_str)
            add_count += 1

        for del_subj_str in sorted(whitelist_subj_set - file_subj_set):
            self.log_and_remove_subj_from_whitelist(del_subj_str)
            del_count += 1

        if add_count or del_count:
            self.log.info("Added subjects: {}".format(add_count))
            self.log.info("Removed subjects: {}".format(del_count))
        else:
            self.log.info("Nothing to do: Whitelist already synchronized with file")
