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
"""Validate Science Metadata.

Usage:

    import d1_scimeta.validate

    try:
      d1_scimeta.validate.assert_valid(format_id, xml)
    except d1_scimeta.util.SciMetaError as e:
        log.error(e)

"""
import logging

import lxml.etree

import d1_scimeta.util

log = logging.getLogger(__name__)


def assert_valid(format_id, xml):
    """Validate an Science Metadata XML file.

    Args:
        format_id: str
            DataONE formatId. Must be one of the keys from the
            `format_id_to_schema.json` document. E.g.,
            `http://www.isotc211.org/2005/gmd`.

        xml: str, bytes or tree
            str: Path to XML file to validate.
            bytes: UTF-8 encoded bytes of XML doc to validate
            tree: lxml.etree of XML doc to validate

    Raises:
        On validation error: d1_scimeta.util.SciMetaError

    Returns:
        On successful validation: None

    """
    if isinstance(xml, lxml.etree._Element) or isinstance(xml, lxml.etree._ElementTree):
        validate_tree(format_id, xml)
    elif isinstance(xml, bytes):
        validate_bytes(format_id, xml)
    elif isinstance(xml, str):
        validate_path(format_id, xml)
    else:
        raise d1_scimeta.util.SciMetaError(
            "xml must be a path, bytes or an lxml.etree."
        )


def validate_tree(format_id, xml_tree):
    log.debug("Validating XML lxml.etree")
    _assert_valid(format_id, xml_tree)


def validate_bytes(format_id, xml_bytes):
    log.debug("Validating XML bytes")
    _assert_valid(format_id, d1_scimeta.util.parse_xml_bytes(xml_bytes))


def validate_path(format_id, xml_path):
    log.debug("Validating XML file: {}".format(xml_path))
    _assert_valid(format_id, d1_scimeta.util.load_xml_file_to_tree(xml_path))


def _assert_valid(format_id, xml_tree):
    root_xsd_path = d1_scimeta.util.get_abs_root_xsd_path(format_id)
    xsd_tree = d1_scimeta.util.load_xml_file_to_tree(root_xsd_path)
    stripped_xml_tree = d1_scimeta.util.strip_whitespace(xml_tree)
    _assert_valid_tree(xsd_tree, stripped_xml_tree)


def _assert_valid_tree(xsd_tree, xml_tree):
    validator = create_validator(xsd_tree)
    try:
        validator.assertValid(xml_tree)
    except lxml.etree.DocumentInvalid as e:
        raise d1_scimeta.util.SciMetaError(
            "XML document does not validate. {}".format(
                d1_scimeta.util.get_error_log_as_str(e)
            )
        )


def create_validator(xsd_tree):
    """Create a schema validator."""
    try:
        return lxml.etree.XMLSchema(xsd_tree)
    except lxml.etree.XMLSchemaParseError as e:
        raise d1_scimeta.util.SciMetaError(
            "Validation not performed: Unable to create schema required for validation. {}".format(
                d1_scimeta.util.get_error_log_as_str(e)
            )
        )
