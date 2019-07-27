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
"""Update the System Metadata for objects on this GMN by copying specified elements from
external SystemMetadata XML documents.

The source SystemMetadata is either an XML file or root directory referenced by --root
or an object on a remote node, referenced by --baseurl.

When --root is a root directory or when using --baseurl, a bulk operation is performed
where all discovered objects are matched up with local objects by PID. The specified
elements are then copied from the discovered object to the matching local object.

Any discovered objects that do not have a local matching PID are ignored. A regular
expression can also be specified to ignore discovered objects even when there are
matching local objects.

Only elements that are children of root are supported. See SYSMETA_ROOT_CHILD_LIST.

If a discovered object does not have an element that has been specified for copy, the
element is removed from the local object.

"""

import re

import d1_common.iter.path
import d1_common.system_metadata
import d1_common.type_conversions
import d1_common.types.exceptions
import d1_common.util
import d1_common.utils.ulog
import d1_common.xml

import d1_client.iter.sysmeta_multi

import d1_gmn.app.delete
import d1_gmn.app.did
import d1_gmn.app.mgmt_base
import d1_gmn.app.sysmeta
import d1_gmn.app.sysmeta_extract


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)
        self.audit_tracker = None

    def add_components(self, parser):
        self.using_single_instance(parser)
        self.using_force_for_production(parser)
        self.using_pid_file(parser)

    def add_arguments(self, parser):
        parser.add_argument(
            "--root", help="Path to source SystemMetadata XML file or root of dir tree"
        )
        parser.add_argument(
            "--baseurl", help="Base url to node holding source documents"
        )
        parser.add_argument(
            "--pidrx", default=False, help="Regex pattern for PIDs to process"
        )
        parser.add_argument(
            "element",
            nargs="+",
            choices=d1_gmn.app.sysmeta_extract.get_valid_field_name_list(),
            help="One or more elements to update",
        )

    def handle_serial(self):
        if self.opt_dict["root"] and self.opt_dict["baseurl"]:
            raise self.CommandError("--root and --baseurl are mutually exclusive")
        if not (self.opt_dict["root"] or self.opt_dict["baseurl"]):
            raise self.CommandError("Must specify --root or --baseurl")
        if not (self.opt_dict["element"]):
            raise self.CommandError("Must specify at least one element to copy")
        try:
            self.update_sysmeta(
                self.opt_dict["root"],
                self.opt_dict["baseurl"],
                self.opt_dict["pidrx"],
                self.opt_dict["element"],
                self.opt_dict["cert_pem_path"],
                self.opt_dict["cert_key_path"],
            )
        except self.CommandError as e:
            self.log.error(str(e))
        self.events.dump_to_log()

    def update_sysmeta(
        self, sysmeta_path, base_url, pid_rx, element_list, cert_pem_path, cert_key_path
    ):
        for i, discovered_sysmeta_pyxb in enumerate(
            self.discovered_sysmeta_iter(
                sysmeta_path, base_url, cert_pem_path, cert_key_path
            )
        ):
            self.events.count("SystemMetadata objects discovered")
            pid = d1_common.xml.get_req_val(discovered_sysmeta_pyxb.identifier)
            if pid_rx and not re.search(pid_rx, pid):
                skip_msg = "Skipped: --pidrx mismatch"
                self.events.count(skip_msg)
                self.log.info("{}: {}".format(skip_msg, pid))
                continue

            if not d1_gmn.app.did.is_existing_object(pid):
                skip_msg = "Skipped: Unknown on local node"
                self.events.count(skip_msg)
                self.log.info("{}: {}".format(skip_msg, pid))
                continue

            before_sysmeta_pyxb = d1_gmn.app.sysmeta.model_to_pyxb(pid)
            sysmeta_pyxb = d1_gmn.app.sysmeta.model_to_pyxb(pid)
            self.log.info("Updating: {}".format(pid))
            d1_common.system_metadata.update_elements(
                sysmeta_pyxb, discovered_sysmeta_pyxb, element_list
            )
            d1_gmn.app.sysmeta.create_or_update(sysmeta_pyxb)

            #
            import d1_test.sample

            self.log.debug(
                d1_test.sample.get_sxs_diff(before_sysmeta_pyxb, sysmeta_pyxb)
            )
            self.events.count("Updated")

    def discovered_sysmeta_iter(
        self, sysmeta_path, base_url, cert_pem_path, cert_key_path
    ):
        if sysmeta_path:
            return self.discovered_sysmeta_file_iter(sysmeta_path)
        else:
            return d1_client.iter.sysmeta_multi.SystemMetadataIteratorMulti(
                base_url,
                # client_dict={
                #     "cert_pem_path": cert_pem_path,
                #     "cert_key_path": cert_key_path,
                # },
                # list_objects_dict={},
            )

    def discovered_sysmeta_file_iter(self, sysmeta_path):
        for xml_path in d1_common.iter.path.path_generator(
            path_list=[sysmeta_path], include_glob_list=["*.xml"]
        ):
            try:
                with open(xml_path, "rb") as f:
                    obj_pyxb = d1_common.xml.deserialize(f.read())
            except (EnvironmentError, ValueError):
                # self.log.debug('Unable to read or parse. path="{}" err="{}"'.format(xml_path,str(e)))
                continue
            pyxb_type_str = d1_common.type_conversions.pyxb_get_type_name(obj_pyxb)
            if pyxb_type_str != "SystemMetadata":
                continue
            yield obj_pyxb
