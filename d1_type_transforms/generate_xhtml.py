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

"""Generate sample XHTML documents.

The resulting objects can be opened directly in a browser.
"""
import logging
import pathlib
import shlex
import subprocess
import sys

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

XSLT_PARAM_DICT = {
    'base_url': './',
    'env_root_url': 'https://cn.dataone.org/cn/',
    'search_root_url': 'https://search.dataone.org/',
    'static_root_url': '../../',
}


def main():
    print(f'Applying XSLT transforms')
    for xml_path in pathlib.Path('./samples/xml').glob('*.xml'):
        xhtml_path = pathlib.Path('./samples/html', xml_path.name).with_suffix('.html')
        print(f'\n   {xml_path}\n-> {xhtml_path}')
        run_xsltproc(xml_path, xhtml_path)


def run_xsltproc(xml_path, xhtml_path):
    cmd_list = ['xsltproc', '--output', xhtml_path]
    for k, v in XSLT_PARAM_DICT.items():
        cmd_list.extend(['--stringparam', k, v])
    cmd_list.extend(['d1_xml_to_xhtml.xsl', xml_path])
    log.info(f'Running: {" ".join((shlex.quote(str(s)) for s in cmd_list))}')
    subprocess.run(cmd_list)


if __name__ == '__main__':
    sys.exit(main())
