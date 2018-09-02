#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
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
"""PyCharm can't resolve the relative paths written by pytest's coverage plugin.
This converts them to absolute, which PyCharm handles.
"""

import os
import sys
import xml.etree.ElementTree

import d1_dev.util

import d1_common.type_conversions
import d1_common.util
import d1_common.xml


def main():
  d1_common.util.log_setup()

  repo_root_path = d1_dev.util.find_repo_root()

  cov_xml_path = os.path.join(repo_root_path, 'coverage.xml')
  fixed_cov_xml_path = os.path.join(repo_root_path, 'coverage_pycharm.xml')

  with open(cov_xml_path, 'rb') as f:
    cov_tree = d1_common.type_conversions.str_to_etree(f.read())

  filename_el_list = cov_tree.findall('.//*[@filename]')
  for filename_el in filename_el_list:
    filename_el.attrib['filename'] = os.path.join(
      repo_root_path, filename_el.attrib['filename']
    )

  fixed_cov_xml = xml.etree.ElementTree.tostring(cov_tree, 'utf-8')

  with open(fixed_cov_xml_path, 'wb') as f:
    f.write(d1_common.xml.serialize_to_transport(fixed_cov_xml))


if __name__ == '__main__':
  sys.exit(main())
