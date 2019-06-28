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

"""Generate a base namespace_to_xsd.json file which holds mappings from namespace to
root XSD paths.

The mappins are used for selecting the root XSDs for a given format_id and namespace.
The root XSDs are referenced directly in the top level XSD that is dynamically generated
for validating a given XML doc.

NOTE: The generated JSON file must be further hand edited to select root XSDs for
namespaces which could not be selected automatically.

"""

import logging
import os

import d1_scimeta.xml_schema

import d1_common.util
import d1_common.utils.filesystem

import d1_client.command_line

log = logging.getLogger(__name__)


def main():
    d1_client.command_line.log_setup(is_debug=False)

    format_id_list = d1_scimeta.xml_schema.get_supported_format_id_list()
    format_id_dict = gen_format_id_dict(format_id_list)
    dump_format_id_dict(format_id_dict)
    undetermined_root_path_count = select_root_xsd_path(format_id_dict)

    if undetermined_root_path_count:
        save_json(format_id_dict, "BASE_namespace_to_xsd.json")
        _log(
            "Undetermined root XSD paths: {}".format(undetermined_root_path_count),
            log_=log.warning,
        )
        _log(
            'Edit the "< COPY THE NAMESPACE ROOT XSD PATH HERE >" entries in the JSON file',
            log_=log.warning,
        )
        _log("Then replace the old .json file with the new version", log_=log.warning)

    else:
        save_json(format_id_dict, "namespace_to_xsd.json")
        _log("No Undetermined root XSD paths")


def save_json(format_id_dict, rel_json_path):
    abs_json_path = d1_common.utils.filesystem.abs_path(
        os.path.join("./ext", rel_json_path)
    )
    d1_common.util.save_json(format_id_dict, abs_json_path)
    _log("Wrote JSON file: {}".format(abs_json_path), log_=log.warning, extra_line=True)


def gen_format_id_dict(format_id_list):
    format_id_dict = {}
    for format_id in format_id_list:
        branch_path = d1_scimeta.xml_schema.get_schema_branch_path(format_id)
        xsd_path_list = d1_scimeta.xml_schema.gen_xsd_path_list(branch_path)
        ns_dict = gen_ns_dict(branch_path, xsd_path_list)

        format_id_dict.setdefault(format_id, {}).update(ns_dict)
    return format_id_dict


def select_root_xsd_path(format_id_dict):
    """Convert the xsd_path_list to a dict, move the existing path list to key "all",
    select a single root xsd_path for the namespace and store it under key, "root"."""
    undetermined_root_path_count = 0

    for format_id, ns_dict in format_id_dict.items():
        for ns, xsd_path_list in ns_dict.items():
            xsd_path_list.sort()
            ns_dict[ns] = {}
            if len(xsd_path_list) == 1:
                ns_dict[ns]["root"] = xsd_path_list[0]
            else:
                ns_dict[ns]["all"] = xsd_path_list
                root_xsd = select_root_xsd(ns, xsd_path_list)
                if root_xsd:
                    ns_dict[ns]["root"] = root_xsd
                else:
                    ns_dict[ns]["root"] = "< COPY THE NAMESPACE ROOT XSD PATH HERE >"
                    undetermined_root_path_count += 1

    return undetermined_root_path_count


def select_root_xsd(ns, xsd_path_list):
    """Select the root XSD for cases where we can make a good guess."""
    # If there is an xsd file that is named the same as the last segment in the
    # namespace, select it.
    ns_seg_list = ns.split(os.path.sep)
    if len(ns_seg_list) >= 2:
        for xsd_path in xsd_path_list:
            if xsd_path.endswith(ns_seg_list[-1] + ".xsd"):
                return xsd_path


def dump_format_id_dict(format_id_dict):
    for format_id, format_id_dict in sorted(format_id_dict.items(), key=lambda x: x[0]):
        _log(format_id, extra_line=True)
        for ns, xsd_path_list in sorted(format_id_dict.items()):
            _log(ns, indent=1)
            for xsd_path in xsd_path_list:
                _log(xsd_path, indent=2)


def gen_ns_dict(branch_path, xsd_path_list):
    ns_dict = {}

    for xsd_path in xsd_path_list:
        try:
            xsd_tree = d1_scimeta.xml_schema.parse_xml_file(xsd_path)
        except d1_scimeta.xml_schema.SciMetaValidationError as e:
            _log("Invalid XSD: {}: {}".format(xsd_path, str(e)), log_=log.error)
            continue
        target_ns = d1_scimeta.xml_schema.get_target_ns(xsd_tree)
        ns_dict.setdefault(target_ns, []).append(
            d1_scimeta.xml_schema.gen_rel_xsd_path(branch_path, xsd_path)
        )

    return ns_dict


def _log(msg, indent=0, log_=log.info, extra_indent=False, extra_line=False):
    if extra_line:
        log_("")
    log_("{}{}".format("  " * (indent + (1 if extra_indent else 0)), msg))


if __name__ == "__main__":
    main()
