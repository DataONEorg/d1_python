#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PyCharm can't resolve the relative paths written by pytest's coverage plugin.
This converts them to absolute, which PyCharm handles.
"""

import logging
import os
import xml.etree.ElementTree

import d1_dev.util

import d1_common.type_conversions
import d1_common.util
import d1_common.xml


def main():
  d1_common.util.log_setup()

  repo_root_path = d1_dev.util.find_repo_root()

  logging.info('Repository: {}'.format(repo_root_path))

  cov_xml_path = os.path.join(repo_root_path, 'coverage.xml')
  fixed_cov_xml_path = os.path.join(repo_root_path, 'fixed_coverage.xml')

  with open(cov_xml_path, 'rb') as f:
    cov_tree = d1_common.type_conversions.str_to_etree(f.read())

  filename_el_list = cov_tree.findall('.//*[@filename]')
  for filename_el in filename_el_list:
    filename_el.attrib['filename'] = os.path.join(
      repo_root_path, filename_el.attrib['filename']
    )

  fixed_cov_xml = xml.etree.ElementTree.tostring(cov_tree, 'utf-8')

  with open(fixed_cov_xml_path, 'wb') as f:
    f.write(d1_common.xml.pretty_xml(fixed_cov_xml))


if __name__ == '__main__':
  main()
