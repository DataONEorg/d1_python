#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
:mod:`tweak_sysmeta`
=======================

:Synopsis:
  Adjust test set SysMeta XML files to make them more suitable for testing.

.. moduleauthor:: Roger Dahl
'''

# Stdlib.
import datetime
import glob
import os
import random
import re
import sys
import time
import urllib

# 3rd party.
# Lxml
try:
  from lxml import etree
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-lxml\n')
  raise

namespaces = {'D1': 'http://ns.dataone.org/service/types/0.6.2', }


def main():
  for sysmeta_path in sorted(
    glob.glob(
      os.path.join(
        './test_client_objects', '*.sysmeta'
      )
    )
  ):
    sysmeta_file = open(sysmeta_path, 'r')
    sysmeta_tree = etree.parse(sysmeta_file)
    sysmeta_file.close()

    # Variate dateSysMetadataModified.
    #el = sysmeta_tree.xpath('/D1:systemMetadata/dateSysMetadataModified', namespaces=namespaces)
    #el[0].text = datetime.datetime.fromtimestamp(random.randint(0, 60 * 60 * 24 * 365 * 30)).isoformat()

    # Fix pid (want it to be filename).
    #object_path = re.match(r'(.*)\.sysmeta', sysmeta_path).group(1)
    #pid = urllib.unquote(os.path.basename(object_path))
    #el = sysmeta_tree.xpath('/D1:systemMetadata/pid', namespaces=namespaces)
    #el[0].text = pid

    obj_format = sysmeta_tree.xpath(
      '/D1:systemMetadata/objectFormat',
      namespaces=namespaces
    )[0].text

    #root = sysmeta_tree.getroot()
    #root.remove(sysmeta_tree.xpath('/D1:systemMetadata/objectFormat', namespaces=namespaces)[0])
    #el1 = etree.Element('objectFormat')
    #el2 = etree.Element('fmtid')
    #el2.text = obj_format
    #el1.append(el2)
    #root.append(el1)
    #del sysmeta_tree.objectFormat

    el = sysmeta_tree.xpath('/D1:systemMetadata/objectFormat', namespaces=namespaces)[0]
    el.text = ''
    el2 = etree.Element('fmtid')
    el2.text = obj_format
    el.append(el2)
    el2 = etree.Element('formatName')
    el2.text = 'eml-2.0.0'
    el.append(el2)
    el2 = etree.Element('scienceMetadata')
    el2.text = 'false'
    el.append(el2)

    sysmeta_xml = etree.tostring(
      sysmeta_tree,
      pretty_print=True,
      encoding='UTF-8',
      xml_declaration=True
    )

    #print sysmeta_xml
    #break
    sysmeta_file = open(sysmeta_path, 'w')
    sysmeta_file.write(sysmeta_xml)
    sysmeta_file.close()


if __name__ == '__main__':
  main()
