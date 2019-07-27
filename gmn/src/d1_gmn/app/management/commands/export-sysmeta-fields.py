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

"""Export specified System Metadata fields as CSV or JSON.

By default, the fields are exported for all SciObj in the database. To limit the export
to specific SciObj, specify a PID file.

If a file path is provided, the CSV or JSON is written to the file. Else it is written
to stdout.

The output format can be selected directly with the --format switch. If not selected,
CSV is used if only a single field is selected, and JSON is used if multiple fields are
selected.

UTF-8 encoding is used for both CSV and JSON.
"""
import os

import d1_gmn.app.mgmt_base
import d1_gmn.app.sysmeta_extract


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)

    def add_components(self, parser):
        self.using_pid_file(parser)

    def add_arguments(self, parser):
        parser.add_argument(
            "--format", choices=["json", "csv"], help="Select JSON or CSV output format"
        )
        parser.add_argument(
            "--output-path",
            action="store",
            help="Path to file in which to store the JSON or CSV document",
        )
        parser.add_argument(
            "field_list",
            nargs="+",
            choices=d1_gmn.app.sysmeta_extract.get_valid_field_name_list(),
            help="One or more System Metadata fields to export",
        )

    def handle_serial(self):
        format_str = self.opt_dict["format"] or (
            "json" if len(self.opt_dict["field_list"]) > 1 else "csv"
        )

        if not self.opt_dict["output_path"]:
            return self.write_stream(
                self.opt_dict["field_list"], self.stdout, format_str
            )

        output_path = self.opt_dict["output_path"]
        if os.path.splitext(output_path)[1].lower() != f".{format_str}":
            output_path += f".{format_str}"

        with open(output_path, "w", encoding="utf-8") as f:
            self.write_stream(self.opt_dict["field_list"], f, format_str)

    def write_stream(self, field_list, out_stream, out_format_str):
        d1_gmn.app.sysmeta_extract.extract_values(
            field_list=field_list,
            filter_arg_dict={"pid__did__in": self.pid_set} if self.pid_set else None,
            out_stream=out_stream,
            out_format=out_format_str,
        )
