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
"""Strip whitespace that might interfere with XSD schema validation.

Overall formatting is maintained. Note that pretty printing the doc is likely to add
the stripped whitespace back in.

This is an example on how to use the DataONE Science Metadata library for Python. It
shows how to:

- Deserialize, process and serialize XML docs.
- Apply an XSLT stransform which strips potentially problematic whitespace.
- Display or save the resulting XML doc.

"""
import argparse
import logging

import d1_scimeta.util

import d1_client.command_line

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("xml_path", help="Path to XML file to process")
    parser.add_argument("--debug", action="store_true", help="Debug level logging")
    parser.add_argument("--update", action="store_true", help="Update the XML file")

    args = parser.parse_args()

    d1_client.command_line.log_setup(is_debug=args.debug)

    xml_tree = d1_scimeta.util.load_xml_file_to_tree(args.xml_path)

    stripped_xml_tree = d1_scimeta.util.strip_whitespace(xml_tree)
    d1_scimeta.util.dump_pretty_tree(
        stripped_xml_tree, "Result of XSLT processing", log.info
    )
    if args.update:
        d1_scimeta.util.save_tree_to_file(stripped_xml_tree, args.xml_path)


def _log(msg, indent=0, log_=log.info, extra_indent=False, extra_line=False):
    if extra_line:
        log_("")
    log_("{}{}".format("  " * (indent + (1 if extra_indent else 0)), msg))


class ResolveError(Exception):
    pass


if __name__ == "__main__":
    main()
