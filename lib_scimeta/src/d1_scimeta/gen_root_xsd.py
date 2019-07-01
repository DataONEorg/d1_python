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

"""Generate preliminary root XSD docs for each formatId that is supported for
validation.

The XSD docs much be further edited by hand to correctly import all namespaces required
for validation of each given formatId.

"""
import lxml.etree

import logging
import os
import d1_scimeta.util

import d1_client.command_line

log = logging.getLogger(__name__)


def main():
    d1_client.command_line.log_setup(is_debug=True)

    for format_id in d1_scimeta.util.get_supported_format_id_list():
        orig_base, orig_ext = os.path.splitext(
            d1_scimeta.util.get_abs_root_xsd_path(format_id)
        )
        root_xsd_path = orig_base + ".base" + orig_ext
        branch_path = d1_scimeta.util.get_abs_schema_branch_path(format_id)
        ns_xsd_path_tup = sorted(
            gen_target_ns_to_rel_xsd_path_tup(branch_path, root_xsd_path)
        )
        xsd_tree = gen_xsd_tree(ns_xsd_path_tup)
        d1_scimeta.util.save_tree_to_file(xsd_tree, root_xsd_path)


def gen_target_ns_to_rel_xsd_path_tup(branch_path, root_xsd_path):
    return tuple(
        (
            d1_scimeta.util.get_target_ns(
                d1_scimeta.util.load_xml_file_to_tree(xsd_path)
            ),
            d1_scimeta.util.get_rel_path(root_xsd_path, xsd_path),
        )
        for xsd_path in d1_scimeta.util.gen_abs_xsd_path_list(branch_path)
    )


def gen_xsd_tree(ns_xsd_path_tup):
    root_el = lxml.etree.Element("{{{}}}schema".format(d1_scimeta.util.NS_MAP["xs"]))
    for ns, xsd_path in ns_xsd_path_tup:
        import_el = lxml.etree.Element(
            "{{{}}}import".format(d1_scimeta.util.NS_MAP["xs"]),
            namespace=ns,
            schemaLocation=xsd_path,
        )
        root_el.append(import_el)
    return root_el


if __name__ == "__main__":
    main()
