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

"""Subjects and permissions.
"""
import contextlib
import io
import logging

import d1_common.const
import d1_common.utils.ulog

import d1_gmn.app.auth

log = logging.getLogger(__name__)


def create_subject_report(
    title_str, primary_str: str, equivalent_set: iter, stream_writer=None
):
    """Create a an overview of what this GMN knows about a set of subjects. Formatted
    for human readability.

    Args:
        title_str:
        primary_str (str):
        equivalent_set (iter):
        stream_writer (stream): ulog.ULogger or ulog.StreamWriter
    """
    equivalent_set -= {
        # d1_common.const.SUBJECT_PUBLIC,
        # d1_common.const.SUBJECT_VERIFIED,
        # d1_common.const.SUBJECT_AUTHENTICATED,
        primary_str,
    }

    whitelisted_set = d1_gmn.app.auth.get_whitelisted_subject_set()
    trusted_set = d1_gmn.app.auth.get_trusted_subjects()
    client_cert_subj_str = d1_gmn.app.auth.get_client_side_certificate_subject()

    string_io = None
    if not stream_writer:
        string_io, stream_writer = d1_common.utils.ulog.string_io_writer()

    @contextlib.contextmanager
    def section(header_str_, ind=4):
        with stream_writer.section(header_str_, col_space=4, header_indent=ind, list_indent=4, count=True, sort=True) as w:
            yield w

    def yesno(cond):
        return "yes" if cond else "no"

    def log_subject_sciobj_perm_count(subj_str_):
        with section(
            "Number of science objects with access for subject",
        ) as w:
            perm_tup = d1_gmn.app.auth.get_permission_count(subj_str_)
            for level, count in enumerate(perm_tup if any(perm_tup) else ()):
                w(f"{d1_gmn.app.auth.level_to_action(level)}:| {count}")

    def log_subject_gmn_permissions(subj_str_):
        with section(
            "Administrative permissions on this GMN",
        ) as w:
            w(
                f"Whitelisted for create, update and delete of science objects:| "
                    f"{yesno(subj_str_ in whitelisted_set)}"
            ),
            w(
                    f"Recognized as CN or other fully trusted infrastructure component:|"
                    f"{yesno(subj_str_ in trusted_set)}"
                ),
            w(
                f"Is GMN client side certificate subject:|"
                    f"{yesno(subj_str_ == client_cert_subj_str)}"
                ),

    stream_writer.header(title_str)

    with section("Primary subject") as w:
        w(primary_str)

    with section("Equivalent subjects") as w:
        w(equivalent_set)

    subj_set = equivalent_set | {primary_str}
    known_subj_set, unknown_subj_set = d1_gmn.app.auth.split_known_and_unknown_subj(
        subj_set
    )
    is_single_known = len(known_subj_set) == 1

    if not unknown_subj_set:
        log.info(
            (
                f'{"The subject provides" if is_single_known else "All of the subjects provide"} '
                f"permissions on this GMN"
            )
        )
    elif not known_subj_set:
        log.info(
            (
                f'{"The subject does not" if is_single_known else "None of the subjects"} '
                f"provide permissions on this GMN"
            )
        )
        return
    else:
        with section("Subjects known by this GMN", ind=0) as w:
            w(known_subj_set)

        with section("Subjects not known by this GMN", ind=0) as w:
            w(unknown_subj_set)

    subj_set = known_subj_set

    stream_writer.header("Subject details")

    for subj_str in sorted(subj_set):
        stream_writer.header(f"Subject: {subj_str}", indent=2)
        log_subject_sciobj_perm_count(subj_str)
        log_subject_gmn_permissions(subj_str)

    if string_io:
        return string_io.getvalue()
