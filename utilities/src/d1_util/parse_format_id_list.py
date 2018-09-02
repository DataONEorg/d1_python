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
"""Parse ObjectFormatList XML doc with XPath

This is an example on how to use the DataONE Client and Common libraries for
Python. It shows how to:

- Extract formatIds from a DataONE ObjectFormatList using XPath
"""
import argparse
import sys

import lxml.etree

NS_MAP = {
  # None : XHTML_NAMESPACE
  'xs': 'http://www.w3.org/2001/XMLSchema',
  'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
}


def main():
  print(get_scimeta_format_id_list('./formats.xml'))


def get_scimeta_format_id_list(xsd_path):
  format_id_list = []
  parser = lxml.etree.XMLParser(no_network=True)
  etree_obj = lxml.etree.parse(xsd_path, parser=parser)
  el_list = etree_obj.xpath('//*[formatType="METADATA"]')
  for el in el_list:
    format_id_list.append(el.find('formatId').text)
  return format_id_list


if __name__ == '__main__':
  sys.exit(main())
