#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
:mod:`mk_test_log_csv`
======================

:Synopsis: Prepare a CSV file that contains fake log entries for testing.
:Author: DataONE (Dahl)
'''

# Stdlib.
import csv
import datetime
import glob
import logging
import optparse
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

namespaces = {'D1': 'http://ns.dataone.org/service/types/SystemMetadata/0.1', }

events = [
  'create', # "create" must be first entry.
  'read',
  'update',
  'delete',
  'replicate',
]

ip_addresses = [
  '1.2.3.4',
  '5.6.7.8',
  '9.10.11.12',
  '13.14.15.16',
  '17.18.19.20',
  '21.22.23.24',
  '25.26.27.28',
]

user_agents = [
  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6',
  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
  'Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 5.1; .NET CLR 1.1.4322)',
  'Opera/9.20 (Windows NT 6.0; U; en)',
  'Opera/9.00 (Windows NT 5.1; U; en)',
  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.50',
  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0',
  'Mozilla/4.0 (compatible; MSIE 6.0; MSIE 5.5; Windows NT 5.1) Opera 7.02 [en]',
  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20060127 Netscape/8.1',
  'Googlebot/2.1 ( http://www.googlebot.com/bot.html)',
  'Googlebot-Image/1.0 ( http://www.googlebot.com/bot.html)',
  'Mozilla/2.0 (compatible; Ask Jeeves)',
  'msnbot-Products/1.0 (+http://search.msn.com/msnbot.htm)',
]

subjects = [
  '1.2.3.4',
  '5.6.7.8',
  '9.10.11.12',
  '13.14.15.16',
  '17.18.19.20',
  '21.22.23.24',
  '25.26.27.28',
]

member_nodes = ['MN1', 'MN2', 'MN3', 'MN4', ]


def pick_random(l):
  return l[random.randint(0, len(l) - 1)]


def log_setup():
  # Set up logging.
  # We output everything to both file and stdout.
  logging.getLogger('').setLevel(logging.DEBUG)
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  file_logger = logging.FileHandler(os.path.splitext(__file__)[0] + '.log', 'a')
  file_logging.setFormatter(formatter)
  logging.getLogger('').addHandler(file_logger)
  console_logger = logging.StreamHandler(sys.stdout)
  console_logging.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  log_setup()

  # Command line options.
  parser = optparse.OptionParser()
  parser.add_option(
    '-c',
    '--csv-path',
    dest='csv_path',
    action='store',
    type='string',
    default='test_log.csv'
  )
  parser.add_option(
    '-p',
    '--obj-path',
    dest='obj_path',
    action='store',
    type='string',
    default='./test_objects'
  )
  parser.add_option('-v', '--verbose', action='store_true', default=False, dest='verbose')

  (options, args) = parser.parse_args()

  if not options.verbose:
    logging.getLogger('').setLevel(logging.ERROR)

  # Create csv file.
  csv_file = open(options.csv_path, 'wb')
  csv_writer = csv.writer(csv_file)

  for sysmeta_path in sorted(glob.glob(os.path.join(options.obj_path, 'sysmeta', '*'))):
    sysmeta_file = open(sysmeta_path, 'rb')
    sysmeta_tree = etree.parse(sysmeta_file)
    sysmeta_file.close()

    pid = d1_common.url.decodePathElement(os.path.basename(sysmeta_path))

    logging.info(pid)

    # All objects must have a "create" log. We reserve the first week after the
    # epoch for them since they must occur before all other events.
    csv_writer.writerow(
      [
        pid,
        events[0], # "create" only.
        pick_random(ip_addresses),
        pick_random(user_agents),
        pick_random(subjects),
        datetime.datetime.fromtimestamp(random.randint(0, 60 * 60 * 24 * 7)).isoformat(),
        pick_random(member_nodes),
      ]
    )

    # Determine how many log entries we will create for this object. We want
    # some objects that have only a "create" log.
    event_cnt = random.randint(0, 10) - 2
    if event_cnt < 0:
      event_cnt = 0

    for event_idx in range(event_cnt):
      csv_writer.writerow(
        [
          pid,
          events[random.randint(1, len(events) - 1)], # excludes "create".
          pick_random(ip_addresses),
          pick_random(user_agents),
          pick_random(subjects),
          datetime.datetime.fromtimestamp(
            random.randint(60 * 60 * 24 * 7, 60 * 60 * 24 * 365 * 30)
          ).isoformat(),
          pick_random(member_nodes),
        ]
      )


if __name__ == '__main__':
  main()
