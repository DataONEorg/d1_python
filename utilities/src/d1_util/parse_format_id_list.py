#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2018 DataONE
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
"""Parse ObjectFormatList XML doc with XPath.

This is an example on how to use the DataONE Client and Common libraries for
Python. It shows how to:

- Download an ObjectFormatList from a CN
- Perform XPath queries against the downloaded object

"""
import logging
import sys

import d1_scimeta.util

import d1_common.const
import d1_common.env
import d1_common.utils.filesystem
import d1_common.utils.ulog
import d1_common.xml

import d1_client.cnclient_2_0
import d1_client.command_line

log = logging.getLogger(__name__)


def main():
    parser = d1_client.command_line.D1ClientArgParser(__doc__)
    args = parser.parse_args()
    d1_client.command_line.log_setup(args.debug)
    client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
        parser.get_method_args(args)
    )
    object_format_list_pyxb = client.listFormats()
    pretty_xml_str = d1_common.xml.serialize_to_xml_str(object_format_list_pyxb)
    log.debug(pretty_xml_str)
    xml_etree = d1_scimeta.util.parse_xml_bytes(pretty_xml_str.encode("utf-8"))
    # Find all objectFormat elements having a formatType child with the text 'METADATA'
    el_list = xml_etree.xpath(
        '//*[formatType="METADATA"]', namespaces=d1_scimeta.util.NS_MAP
    )
    _log("METADATA formatId list:")
    for el in el_list:
        _log(el.find("formatId").text, extra_indent=True)


def _log(msg, indent=0, log_=log.info, extra_indent=False, extra_line=False):
    if extra_line:
        log_("")
    log_("{}{}".format("  " * (indent + (1 if extra_indent else 0)), msg))


if __name__ == "__main__":
    sys.exit(main())
