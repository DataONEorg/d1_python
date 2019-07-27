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
"""Add a list of DataONE subjects to the whitelist of subjects that are allowed to access the
DataONE APIs for creating, updating and deleting Science Objects on this GMN.

This command takes a path to a file containing a list of subjects to add. For adding
individual subjects, see related whitelist- commands.

Lines starting with "#" and blank lines in the file are ignored.

This will only add subjects to the whitelist. Subjects that are already whitelisted are
ignored. See ``whitelist-sync-file`` to both add and delete subjects.
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
        file_subj_set = self.load_set_from_file(self.opt_dict["whitelist-sync-file"])
        whitelist_subj_set = self.get_whitelist_list()
        for add_subj_str in sorted(file_subj_set - whitelist_subj_set):
            self.add_subj_to_whitelist(add_subj_str)
        if add_count:
            self.log.info("Added subjects: {}".format(add_count))
        else:
            self.log.info("Nothing to do: All subjects in file already whitelisted")
