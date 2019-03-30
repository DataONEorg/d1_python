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

# TODO: This is the start of a command line wrapper for SubjectInfoRenderer

"""Render SubjectInfo XML doc to UI or image file."""
import sys

import d1_common
import d1_common.cert.subject_info_renderer
import d1_common.types
import d1_common.types.exceptions
import d1_common.xml

SUBJ_INFO_SAMPLE_PATH = "/home/dahl/dev/d1_python/test_utilities/src/d1_test/test_docs/xml/subject_info_production_sample.xml"
AUTH_SUBJ = "CN=Matt Jones A729,O=Google,C=US,DC=cilogon,DC=org"


# noinspection PyMissingOrEmptyDocstring
def main():
    subject_info_pyxb = deserialize_subject_info(SUBJ_INFO_SAMPLE_PATH)
    subject_info_renderer = d1_common.cert.subject_info_renderer.SubjectInfoRenderer(
        subject_info_pyxb
    )
    # subject_info_renderer.view(AUTH_SUBJ)
    subject_info_renderer.render_to_image_file(AUTH_SUBJ, "test_tree.png")
    return 0


def deserialize_subject_info(subject_info_xml_path):
    """Deserialize a SubjectInfo XML file to a PyXB object."""
    try:
        with open(subject_info_xml_path) as f:
            return d1_common.xml.deserialize(f.read())
    except ValueError as e:
        raise d1_common.types.exceptions.InvalidToken(
            0,
            'Could not deserialize SubjectInfo. subject_info="{}", error="{}"'.format(
                subject_info_xml_path, str(e)
            ),
        )


if __name__ == "__main__":
    sys.exit(main())
