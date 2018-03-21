#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Validate Science Metadata

Usage:

import d1_scimeta.xml_schema
try:
  d1_scimeta.xml_schema.validate(format_id, xml_str)
except d1_scimeta.xml_schema.SciMetaValidationError as e:
  ...
"""
import inspect
import io
import json
import logging
import os
import pprint
import re

import lxml
import lxml.etree

import d1_common.types.exceptions
import d1_common.util

NS_MAP = {
  # None : 'http://www.w3.org/2001/XMLSchema',
  'xs': 'http://www.w3.org/2001/XMLSchema',
  'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
}

SCHEMA_ROOT_PATH = './schema'
FORMAT_ID_JSON_PATH = './schema/format_id_to_schema_root.json'


class Validate(object):
  def __init__(self):
    self._format_id_to_schema_root_dict = None

  def __call__(self, format_id, xml_str):
    if self._format_id_to_schema_root_dict is None:
      self._format_id_to_schema_root_dict = (
        self.load_format_id_to_schema_root_dict(FORMAT_ID_JSON_PATH)
      )
      # self.dump(
      #   'format_id_to_schema_root_dict', self._format_id_to_schema_root_dict
      # )
    # self.validate(format_id, self.strip_xml_encoding_declaration(xml_str))
    self.validate(format_id, xml_str)

  def validate(self, format_id, xml_str):
    try:
      xml_tree = self.parse_xml_bytes(xml_str)
    except lxml.etree.XMLSyntaxError as e:
      self.raise_validation_error(e, format_id)
    xml_schema = self.gen_xml_schema(format_id, xml_tree)
    try:
      xml_schema.assertValid(xml_tree)
    except (lxml.etree.DocumentInvalid, lxml.etree.XMLSyntaxError) as e:
      self.raise_validation_error(
        '{}\n{}'.format(str(e), '\n'.join(map(str, xml_schema.error_log))),
        format_id
      )

  def raise_validation_error(self, e, format_id):
    raise SciMetaValidationError(
      'XML Schema (XSD) validation failed. format_id="{}" error="{}"'.
      format(format_id, str(e))
    )

  def gen_xml_schema(self, format_id, xml_tree):
    schema_root_path = self.get_schema_root_path(SCHEMA_ROOT_PATH, format_id)
    # self.dump('schema_root_path', schema_root_path)
    xsd_path_list = self.find_xsd_files(schema_root_path)
    xsd_path_to_info_dict = self.gen_xsd_path_to_info_dict(xsd_path_list)
    # self.dump('xsd_path_to_info_dict', xsd_path_to_info_dict)
    self.rel_to_abs_import_list(xsd_path_to_info_dict)
    # self.dump('xsd_path_to_info_dict', xsd_path_to_info_dict)
    self.remove_imported(xsd_path_to_info_dict)
    # self.dump('xsd_path_to_info_dict', xsd_path_to_info_dict)
    ns_to_xsd_dict = self.gen_ns_to_xsd_dict(xsd_path_to_info_dict)
    # self.dump('final list to import', ns_to_xsd_dict)
    prefix_uri_list = self.gen_prefix_uri_list(xml_tree)
    # self.dump('prefix_uri_list', prefix_uri_list)
    xsd_tree = self.gen_combined_xsd_tree(ns_to_xsd_dict, prefix_uri_list)
    # self.dump_tree(xsd_tree)
    # self.dump_tree_to_file(xsd_tree, 'dump.xsd')
    xml_schema = lxml.etree.XMLSchema(xsd_tree)
    return xml_schema

  def is_installed_scimeta_format_id(self, format_id):
    """Return True if:
    - {format_id} is formatId of a Science Metadata format that is recognized
    and parsed by CNs (in the objectFormatList, the objectFormat has a
    formatType of METADATA)
    - And the XML Schema (XSD) files required for validating the object is
    installed in this validator's local schema store.
    """
    try:
      self.get_schema_root_path('/', format_id)
    except SciMetaValidationError:
      return False
    return True

  def get_schema_root_path(self, schema_store_root_path, format_id):
    if self._format_id_to_schema_root_dict is None:
      self._format_id_to_schema_root_dict = (
        self.load_format_id_to_schema_root_dict(FORMAT_ID_JSON_PATH)
      )
    try:
      schema_root_path = self._format_id_to_schema_root_dict[format_id]
    except LookupError:
      raise SciMetaValidationError(
        'Invalid Science Metadata formatId. format_id="{}"'.format(format_id)
      )
    else:
      if schema_root_path is None:
        raise SciMetaValidationError(
          'Schema not installed for Science Metadata formatId. format_id="{}"'.
          format(format_id)
        )
    return self.normalize_path(schema_store_root_path, schema_root_path)

  def load_format_id_to_schema_root_dict(self, format_id_json_path):
    abs_format_id_json_path = d1_common.util.abs_path(format_id_json_path)
    with open(abs_format_id_json_path, 'r') as f:
      return json.load(f)

  def remove_imported(self, xsd_path_to_info_dict):
    indirect_import_set = {
      v[1]
      for info_dict in list(xsd_path_to_info_dict.values())
      for v in info_dict['import_list']
    }
    # self.dump('indirect_import_set', indirect_import_set)
    direct_import_set = set()
    for xsd_path, xsd_info in list(xsd_path_to_info_dict.items()):
      if xsd_path not in indirect_import_set:
        direct_import_set.add(xsd_path)
        # self.dump('add', xsd_path)
      else:
        # self.dump('del', xsd_path)
        del xsd_path_to_info_dict[xsd_path]

  def gen_xsd_path_to_info_dict(self, xsd_path_list):
    return {p: self.gen_xsd_info_dict(p) for p in xsd_path_list}

  def gen_xsd_info_dict(self, xsd_path):
    xsd_tree = self.parse_xml_file(xsd_path)
    return {
      'target_ns': self.get_target_ns(xsd_tree),
      'import_list': self.get_import_uri_path_list(xsd_tree),
    }

  def gen_ns_to_xsd_dict(self, xsd_path_to_info_dict):
    ns_to_xsd_dict = {}
    for xsd_path, xsd_info in list(xsd_path_to_info_dict.items()):
      ns_to_xsd_dict.setdefault(xsd_info['target_ns'], []).append(xsd_path)
    return ns_to_xsd_dict

  def parse_xml_file(self, xml_path):
    with open(xml_path, 'rb') as f:
      return self.parse_xml_bytes(f.read())

  def parse_xml_bytes(self, xml_bytes):
    xml_parser = lxml.etree.XMLParser(no_network=True)
    xml_tree = lxml.etree.parse(io.BytesIO(xml_bytes), parser=xml_parser)
    return xml_tree

  def find_xsd_files(self, schema_root_dir):
    xsd_path_list = []
    for root_path, dir_list, file_list in os.walk(schema_root_dir):
      for file_name in file_list:
        if not os.path.splitext(file_name)[1] == '.xsd':
          continue
        xsd_path = os.path.join(root_path, file_name)
        xsd_path_list.append(xsd_path)
    return xsd_path_list

  def get_target_ns(self, xml_tree):
    ns_list = xml_tree.xpath('//*[@targetNamespace]')
    assert len(ns_list) in (0, 1)
    if len(ns_list):
      return ns_list[0].attrib['targetNamespace']

  def get_import_uri_path_list(self, xsd_tree):
    flat_list = xsd_tree.xpath(
      '//xs:import/@namespace|xs:import/@schemaLocation', namespaces=NS_MAP
    )
    return list(zip(flat_list[::2], flat_list[1::2]))

  def rel_to_abs_import_list(self, xsd_path_to_info_dict):
    for xsd_path, info_dict in list(xsd_path_to_info_dict.items()):
      info_dict['import_list'] = [
        (import_uri, self.normalize_path(xsd_path, import_path))
        for import_uri, import_path in info_dict['import_list']
      ]

  def normalize_path(self, base_path, rel_path=None):
    if os.path.isfile(base_path):
      base_path = os.path.split(base_path)[0]
    res = os.path.realpath(
      d1_common.util.abs_path_from_base(base_path, rel_path)
    )
    if os.path.exists(res):
      return res

  def gen_combined_xsd_tree(self, ns_to_xsd_dict, prefix_uri_list):
    ns_uri_list = [v[1] for v in prefix_uri_list]
    root_el = lxml.etree.Element(
      "{{{}}}schema".format(NS_MAP['xs']), nsmap=NS_MAP
    )
    for ns_uri in ns_uri_list:
      if ns_uri in ns_to_xsd_dict:
        for xsd_path in ns_to_xsd_dict[ns_uri]:
          xsd_file_url = 'file://{}'.format(xsd_path)
          import_el = lxml.etree.Element(
            '{{{}}}import'.format(NS_MAP['xs']), namespace=ns_uri,
            schemaLocation=xsd_file_url
          )
          root_el.append(import_el)

    return root_el

  def gen_prefix_uri_list(self, xml_tree):
    """Return list of tuples of prefix and namespace URI
    E.g.:
    [
      ('xml', 'http://www.w3.org/XML/1998/namespace'),
      ('xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
      ('srv', 'http://www.isotc211.org/2005/srv'),
      ...
    ]
    """
    ns_list = xml_tree.xpath("/*/namespace::*")
    return ns_list

  def strip_xml_encoding_declaration(self, xml_str):
    # It's safe to do this with a regex since it operates only on the first
    # line, containing the XML declaration, not on the XML doc itself.
    return re.sub(r'\s*encoding\s*=\s*"UTF-8"\s*', '', xml_str, re.IGNORECASE)

  def dump_tree(self, xml_tree):
    self.dump(self.pretty_format_tree(xml_tree))

  def dump_tree_to_file(self, xml_tree, xml_path):
    with open(xml_path, 'wb') as f:
      f.write(self.pretty_format_tree(xml_tree))

  def dump_ns_to_xsd_dict(self, ns_to_xsd_dict):
    for target_ns, xsd_list in sorted(ns_to_xsd_dict.items()):
      logging.debug('{}:'.format(target_ns))
      list(map(logging.debug, ['  {}'.format(p) for p in xsd_list]))

  def dump(self, msg_str, o):
    line_int = inspect.currentframe().f_back.f_lineno
    list(
      map(
        logging.debug, (
          '{} LINE {} {}'.format('#' * 40, line_int, '#' * 40),
          '{}:'.format(msg_str)
        )
      )
    )
    list(map(logging.debug, [s for s in pprint.pformat(o).splitlines()]))

  def pretty_format_tree(self, xml_tree):
    return lxml.etree.tostring(
      xml_tree, pretty_print=True, xml_declaration=True, encoding='utf-8'
    )


class SciMetaValidationError(Exception):
  pass


validate = Validate()


def is_installed_scimeta_format_id(format_id):
  return validate.is_installed_scimeta_format_id(format_id)
