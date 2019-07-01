#!/usr/bin/env python

import logging
import os
import sys

import d1_scimeta.util
import d1_scimeta.validate


import d1_common.utils.filesystem


import d1_client.command_line


import d1_common.utils.progress_logger

log = logging.getLogger(__name__)

"""Validate a large number of SciObj downloaded from the CN.

These should all validate.
"""


def main():
    d1_client.command_line.log_setup(is_debug=True)

    progress_logger = d1_common.utils.progress_logger.ProgressLogger(logger=log)

    for format_id in d1_scimeta.util.get_supported_format_id_list():
        validate_format_id(format_id, progress_logger)

    # "datacite-3.0": "datacite-3.0",
    # "datacite-3.1": "datacite-3.1",
    # "http://datacite.org/schema/kernel-3.0": "dc",
    # "http://datacite.org/schema/kernel-3.1": "dc",
    # "http://datadryad.org/profile/v3.1": "dryad",
    # "http://purl.org/dryad/terms/": "dryad",
    # "http://rs.tdwg.org/dwc/xsd/simpledarwincore/": "dwc",
    # "eml://ecoinformatics.org/eml-2.0.0": "eml-2.0.0",
    # "eml://ecoinformatics.org/eml-2.0.1": "eml-2.0.1",
    # "eml://ecoinformatics.org/eml-2.1.0": "eml-2.1.0",
    # "eml://ecoinformatics.org/eml-2.1.1": "eml-2.1.1",
    # "FGDC-STD-001-1998": "fgdc-bdp",
    # "FGDC-STD-001.1-1999": "fgdc-std-001-1998",
    # "http://www.isotc211.org/2005/gmd": "isotc211",
    # "http://www.isotc211.org/2005/gmd-noaa": "isotc211-noaa",
    # "http://www.isotc211.org/2005/gmd-pangaea": "isotc211-pangaea",
    # "http://www.openarchives.org/OAI/2.0/oai_dc/": "oai_dc",
    # "http://ns.dataone.org/metadata/schema/onedcx/v1.0": "onedcx",
    # "http://purl.org/ornl/schema/mercury/terms/v1.0": "ornl"

    # validate_format_id("http://www.isotc211.org/2005/gmd-noaa", progress_logger)
    # validate_format_id("http://www.isotc211.org/2005/gmd-pangaea", progress_logger)

    # validate_format_id("FGDC-STD-001-1998", progress_logger)

    progress_logger.completed()


def validate_format_id(format_id, progress_logger):
    schema_name = d1_scimeta.util.get_schema_name(format_id)
    out_dir_path = d1_common.utils.filesystem.abs_path(
        os.path.join("./test_xml", schema_name)
    )
    test_path_list = get_test_xml_path_list(out_dir_path)

    task_name = "Validate SciObj with formatId: {}".format(format_id)

    progress_logger.start_task_type(task_name, len(test_path_list))

    for test_xml_path in test_path_list:
        validate_xml(format_id, test_xml_path, progress_logger)

    progress_logger.end_task_type(task_name)


def validate_xml(format_id, test_xml_path, progress_logger):
    log.info("-" * 100)
    log.info(format_id)
    log.info(test_xml_path)

    event_logged = False
    while True:
        try:
            d1_scimeta.validate.assert_valid(format_id, test_xml_path)

        except d1_scimeta.util.SciMetaError as e:
            if not event_logged:
                progress_logger.event(
                    "Validation failed: formatId: {}".format(format_id)
                )
                event_logged = True

            log.info(">" * 100)
            log.info("FAILED")
            log.info(str(e))
            log.info("<" * 100)

            # log.info('>'*100)
            # log.info('xmllint:')
            # subprocess.call(['xmllint', '--schema', root_xsd_path, test_xml_path])
            # log.info('<'*100)

            # answer_str = input('Open/Skip/Retry [o/s/Enter]: ')
            #
            # root_xsd_path = d1_scimeta.util.get_abs_root_xsd_path(format_id)
            #
            # if answer_str == 'o':
            #     d1_test.pycharm.open_and_set_cursor(test_xml_path)
            #     d1_test.pycharm.open_and_set_cursor(root_xsd_path)
            # elif answer_str == 's':
            #     break
            break

        else:
            log.info("")
            log.info("SUCCESS")

            progress_logger.event(
                "Validation successful: formatId: {}".format(format_id)
            )

            break


def get_test_xml_path_list(out_dir_path):
    return tuple(os.path.join(out_dir_path, f) for f in os.listdir(out_dir_path))


if __name__ == "__main__":
    sys.exit(main())
