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
'''Module d1_client.tests.node_test_common
==========================================

:Created: 2011-01-27
:Author: DataONE (vieglais)
:Dependencies:
  - python 2.6
'''

import sys
from optparse import OptionParser
import logging
'''TEST_INFO is a list of dictionaries, with each dictionary containing
entries for baseurl, existingpid, and boguspid.
'''
TEST_INFO = {
  'schema_version': 'http://ns.dataone.org/service/types/0.6.2',

  'MN': [
    {'baseurl': 'http://localhost:8000',
    'existingpid': 'hdl:10255/dryad.1073/mets.xml',
    'existingpid_ck': 'aac6cca196fb6330d1013a10cce6a4604ca180d3',
    'boguspid': 'some bogus id'
    },
    #    {'baseurl': 'http: //dev-dryad-mn.dataone.org/mn',
    #    'existingpid': 'hdl: 10255/dryad.105/mets.xml',
    #    'existingpid_ck': 'e494ca7b15404f41006356a5a87dbf44b9a415e7',
    #    'boguspid': 'some bogus id'
    #    },
    #     {'baseurl': 'http: //daacmn.dataone.utk.edu/mn',
    #      'existingpid': 'MD_ORNLDAAC_787_03032010095920',
    #      'existingpid_ck': '49fd46daad283f0cbd411e0297e0d68d56d001a4',
    #      'boguspid': 'some bogus id'},
    #    {'baseurl': 'http: //knb-mn.ecoinformatics.org/knb/d1',
    #     'existingpid': 'knb-lter-sev.4892.1',
    #     'existingpid_ck': '08B1F55E0C214E15621B5334D84A1D2B',
    #     'boguspid': 'some bogus id'
    #    },
    #    {'baseurl': 'http: //sandbox08.uwrl.usu.edu/gmn_cuahsi/mn.svc',
    #     'existingpid': '56e2c6c3-03ff-46a4-9f08-96a5beb66183',
    #     'existingpid_ck': '???',
    #     'boguspid': 'some bogus pid'
    #    }
  ],

  'CN': [
    #    {'baseurl': 'http: //cn.dataone.org/cn',
    #     'existingpid': 'knb-lter-arc.1248.1',
    #     'existingpid_ck': '',
    #     'boguspid': 'some bogus pid'
    #     }
  ]
}


def loadTestInfo(
  baseurl=None,
  pid=None,
  checksum=None,
  schemaversion=TEST_INFO['schema_version'],
  boguspid='some bogus pid'
):
  '''Populate TEST_INFO dynamically
  '''
  if baseurl is None:
    return TEST_INFO
  test = {'schema_version': schemaversion,
          'MN': [{'baseurl': baseurl,
                 'existingpid': pid,
                 'existingpid_ck': checksum,
                 'boguspid': boguspid}],
          'CN': []}
  return test


def initMain():
  parser = OptionParser()
  parser.add_option(
    '-b',
    '--baseurl',
    dest='baseurl',
    default=None,
    help='Use BASEURL instead of predefined targets for testing'
  )
  parser.add_option(
    '-p',
    '--pid',
    dest='pid',
    default=None,
    help='Use PID for testing existing object access'
  )
  parser.add_option(
    '-c',
    '--checksum',
    dest='checksum',
    default=None,
    help='CHECKSUM for specified PID.'
  )
  parser.add_option('-l', '--loglevel', dest='llevel', default=None,
                help='Reporting level: 10=debug, 20=Info, 30=Warning, ' +\
                     '40=Error, 50=Fatal')
  parser.add_option('-v', '--verbose', dest='verbose', action='store_true', \
                    default=False)
  parser.add_option('-q', '--quiet', dest='quiet', action='store_true', \
                    default=False)
  (options, args) = parser.parse_args()
  if options.llevel not in ['10', '20', '30', '40', '50']:
    options.llevel = 20
  logging.basicConfig(level=int(options.llevel))
  test_data = loadTestInfo(
    baseurl=options.baseurl,
    pid=options.pid, checksum=options.checksum
  )
  options_tpl = ('-b', '--baseurl', '-p', '--pid', '-c', '--checksum', '-l', '--loglevel')
  del_lst = []
  for i, option in enumerate(sys.argv):
    if option in options_tpl:
      del_lst.append(i)
      del_lst.append(i + 1)

  del_lst.reverse()
  for i in del_lst:
    del sys.argv[i]
  return test_data
