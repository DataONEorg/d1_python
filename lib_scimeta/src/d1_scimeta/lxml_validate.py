#!/usr/bin/env python

import argparse
import logging
import sys

import d1_scimeta.util
import d1_scimeta.validate

import d1_client.command_line

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--formats", action="store_true", help="List valid formatIds")
    parser.add_argument("--debug", action="store_true", help="Debug level logging")
    parser.add_argument("xml_path", help="Path to XML file to validate")
    parser.add_argument(
        "format_id",
        nargs="?",
        default="http://www.isotc211.org/2005/gmd",
        help="FormatId or short name for the XML file (e.g., eml://ecoinformatics.org/eml-2.1.1",
    )

    args = parser.parse_args()

    d1_client.command_line.log_setup(is_debug=args.debug)

    if args.formats:
        d1_scimeta.util.get_supported_format_id_list()
        return 0

    try:
        d1_scimeta.validate.assert_valid(args.format_id, args.xml_path)
    except d1_scimeta.util.SciMetaError as e:
        for line in str(e).splitlines():
            log.error(line)
        return 1

    log.info("Validation OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
