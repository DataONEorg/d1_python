#!/usr/bin/env python

import logging
import os
import sys

import d1_scimeta.util
import d1_scimeta.validate

import d1_common.utils.filesystem
import d1_common.utils.tracker
import d1_common.utils.ulog

import d1_client.command_line

log = logging.getLogger(__name__)

"""Validate a large number of SciObj downloaded from the CN.

These should all validate.
"""


def main():
    d1_client.command_line.log_setup(is_debug=True)

    with d1_common.utils.tracker.ProgressTracker(logger=log) as tracker:

        for format_id in d1_scimeta.util.get_supported_format_id_list():
            if format_id in ("FGDC-STD-001-1998", "FGDC-STD-001.1-1999"):
                continue
            validate_format_id(format_id, tracker)


def validate_format_id(format_id, tracker):
    schema_name = d1_scimeta.util.get_schema_name(format_id)
    out_dir_path = d1_common.utils.filesystem.abs_path(
        os.path.join("./test_xml", schema_name)
    )
    test_path_list = get_test_xml_path_list(out_dir_path)

    task_name = "Validate SciObj with formatId: {}".format(format_id)

    tracker.start_task_type(task_name, len(test_path_list))

    for test_xml_path in test_path_list:
        validate_xml(format_id, test_xml_path, tracker)

    tracker.end_task_type(task_name)


def validate_xml(format_id, test_xml_path, tracker):
    log.info("-" * 100)
    log.info(format_id)
    log.info(test_xml_path)

    event_logged = False
    while True:
        try:
            d1_scimeta.validate.assert_valid(format_id, test_xml_path)

        except d1_scimeta.util.SciMetaError as e:
            if not event_logged:
                tracker.event("Validation failed: formatId: {}".format(format_id))
                event_logged = True

            log.info(">" * 100)
            log.info("FAILED")
            log.info(str(e))
            log.info("<" * 100)
            exit()
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

            tracker.event("Validation successful: formatId: {}".format(format_id))

            break


def get_test_xml_path_list(out_dir_path):
    return tuple(os.path.join(out_dir_path, f) for f in os.listdir(out_dir_path))


if __name__ == "__main__":
    sys.exit(main())
