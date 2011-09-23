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
:mod:`dataone`
=======================

:Synopsis:
  DataONE Command Line Client

.. moduleauthor:: Roger Dahl
'''

# Stdlib.
import csv
import datetime
import dateutil
import glob
import hashlib
import httplib
import json
import logging
import optparse
import os
import random
import re
import shutil
import stat
import StringIO
import sys
import time
import unittest
import urllib
import urlparse
import uuid
import xml.dom.minidom

# 3rd party.
import pyxb

# If this was checked out as part of the MN service, the libraries can be found here.
sys.path.append(
  os.path.abspath(
    os.path.join(
      os.path.dirname(
        __file__
      ), '../../mn_prototype/'
    )
  )
)

# MN API.
try:
  import d1_common.mime_multipart
  import d1_common.types.exceptions
  import d1_common.types.generated.dataoneTypes as dataoneTypes
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/api-common-python/src/d1_common\n'
  )
  raise
try:
  import d1_client
  import d1_client.mnclient
  import d1_client.cnclient
  import d1_client.systemmetadata
  import d1_client.objectlistiterator
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/itk/d1-python/src/d1_client\n'
  )
  raise

# 3rd party.
try:
  from lxml import etree, objectify
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-lxml\n')
  raise
try:
  import iso8601
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-setuptools\n')
  sys.stderr.write(
    '     sudo easy_install http://pypi.python.org/packages/2.5/i/iso8601/iso8601-0.1.4-py2.5.egg\n'
  )
  raise


def log_setup():
  # Set up logging.
  # We output everything to both file and stdout.
  logging.getLogger('').setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(levelname)-8s %(message)s')
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


class MNException(Exception):
  pass

#===============================================================================


class DataONECLI():
  def __init__(self, opts, args):
    self.opts = opts
    self.args = args

    # Command map.
    self.command_map = {
      'create': self.create,
      'get': self.get,
      'meta': self.meta,
      'related': self.related,
      'list': self.list,
      'search': self.search,
      'log': self.log,
      'objectformats': self.objectformats,
      'resolve': self.resolve,
    }

  def _gen_sysmeta(self, pid, size, md5):
    sysmeta = dataoneTypes.systemMetadata()
    sysmeta.identifier = pid
    sysmeta.fmtid = self.opts['sysmeta_object_format']
    sysmeta.size = size
    sysmeta.submitter = self.opts['sysmeta_submitter']
    sysmeta.rightsHolder = self.opts['sysmeta_rightsholder']
    sysmeta.checksum = dataoneTypes.checksum(md5)
    sysmeta.checksum.algorithm = 'MD5'
    sysmeta.dateUploaded = datetime.datetime.now()
    sysmeta.dateSysMetadataModified = datetime.datetime.now()
    sysmeta.originMemberNode = self.opts['sysmeta_origin_member_node']
    sysmeta.authoritativeMemberNode = self.opts['sysmeta_authoritative_member_node']
    return sysmeta

  def output(self, flo):
    # If no output file is specified, dump to stdout.
    if self.opts['output'] is not None:
      try:
        file = open(self.opts['output'], 'wb')
        shutil.copyfileobj(flo, file)
        file.close()
      except EnvironmentError as (errno, strerror):
        err_msg = 'Could not write Science Object to file: {0}\n'.format(
          self.opts['output']
        )
        err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
        logging.error(err_msg)
    else:
      shutil.copyfileobj(flo, sys.stdout)

  def create(self):
    '''Use Case 04 - Create New Object.
    '''

    if len(self.args) != 2:
      logging.error('Invalid arguments')
      logging.error('Usage: create <pid> <science data path>')
      return

    # create <pid> <system metadata path> <science metadata path> <science data path>
    pid = self.args[0]
    scidata_path = self.args[1]

    try:
      scidata_file = open(scidata_path, 'r')
    except EnvironmentError as (errno, strerror):
      err_msg = 'Could not open Science Data file: {0}\n'.format(scidata_path)
      err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
      logging.error('Create failed: {0}'.format(err_msg))
      return

    md5 = hashlib.md5(scidata_file.read()).hexdigest()
    size = scidata_file.tell()
    scidata_file.seek(0)

    sysmeta = self._gen_sysmeta(pid, size, md5)

    client = d1_client.mnclient.MemberNodeClient(self.opts['mn_url'])

    try:
      client.create(pid, scidata_file, sysmeta)
    except:
      logging.error('Create failed')
      raise

  def get(self):
    '''Use Case 01 - Get Object Identified by GUID.
    '''

    if len(self.args) != 1:
      logging.error('Invalid arguments')
      logging.error('Usage: get <pid>')
      return

    pid = self.args[0]

    # Get
    client = d1_client.mnclient.MemberNodeClient(self.opts['dataone_url'])

    sci_obj = client.get(pid)

    self.output(sci_obj)

  def meta(self):
    '''Use Case 37 - Get System Metadata for Object.
    '''

    if len(self.args) != 1:
      logging.error('Invalid arguments')
      logging.error('Usage: get <pid>')
      return

    pid = self.args[0]

    # Get SysMeta.
    client = d1_client.mnclient.MemberNodeClient(self.opts['dataone_url'])
    sci_meta = client.getSystemMetadata(pid)
    sci_meta_xml = sci_meta.toxml()

    if self.opts['pretty']:
      dom = xml.dom.minidom.parseString(sci_meta_xml)
      sci_meta_xml = dom.toprettyxml()

    self.output(StringIO.StringIO(sci_meta_xml))

  def related(self):
    '''
    '''

    if len(self.args) != 1:
      logging.error('Invalid arguments')
      logging.error('Usage: related <pid>')
      return

    pid = self.args[0]

    # Get
    client = d1_client.mnclient.MemberNodeClient(
      self.opts['dataone_url'],
      certfile=opts_dict['cert_path'],
      keyfile=opts_dict['key_path']
    )
    sci_meta = client.getSystemMetadata(pid)

    print 'Describes:'
    if len(sci_meta.describes) > 0:
      for describes in sci_meta.describes:
        print '  {0}'.format(describes)
    else:
      print '  <none>'

    print 'Described By:'
    if len(sci_meta.describedBy) > 0:
      for describedBy in sci_meta.describedBy:
        print '  {0}'.format(describedBy)
    else:
      print '  <none>'

  def resolve(self):
    '''Get Object Locations for Object.
    '''

    if len(self.args) != 1:
      logging.error('Invalid arguments')
      logging.error('Usage: resolve <pid>')
      return

    pid = self.args[0]

    # Get
    client = d1_client.cnclient.CoordinatingNodeClient(baseurl=self.opts['dataone_url'])

    object_location_list = client.resolve(pid)

    for object_location in object_location_list.objectLocation:
      print object_location.url

  def list(self):
    '''MN listObjects.
    '''
    if len(self.args) != 0:
      logging.error('Invalid arguments')
      logging.error(
        'Usage: list --mn_url [--start-time] [--end-time] '
        '[--object-format] [--slice-start] [--slice-count] '
      )
      return

    client = d1_client.mnclient.MemberNodeClient(self.opts['mn_url'])

    object_list = client.listObjects(
      startTime=self.opts['start_time'],
      endTime=self.opts['end_time'],
      objectFormat=self.opts['object_format'],
      start=self.opts['slice_start'],
      count=self.opts['slice_count']
    )

    object_list_xml = object_list.toxml()

    if self.opts['pretty']:
      dom = xml.dom.minidom.parseString(object_list_xml)
      object_list_xml = dom.toprettyxml()

    self.output(StringIO.StringIO(object_list_xml))

  def search(self):
    '''CN search.
    '''
    print 'Not implemented'

  def log(self):
    '''MN log.
    '''
    if len(self.args) != 0:
      logging.error('Invalid arguments')
      logging.error(
        'Usage: log --mn_url [--start-time] [--end-time] '
        '[--slice-start] [--slice-count] '
      )
      return

    client = d1_client.mnclient.MemberNodeClient(self.opts['mn_url'])

    object_list = client.getLogRecords(
      fromDate=self.opts['start_time'],
      toDate=self.opts['end_time'],
      #start=self.opts['slice_start'],
      #count=self.opts['slice_count']
    )

    object_list_xml = object_list.toxml()

    if self.opts['pretty']:
      dom = xml.dom.minidom.parseString(object_list_xml)
      object_list_xml = dom.toprettyxml()

    self.output(StringIO.StringIO(object_list_xml))

  def objectformats(self):
    '''Get a list of object formats available on the target.
    :return: (object format, count) object formats.

    TODO: May need to be completely
    removed (since clients should use CNs for object discovery).
    '''

    if len(self.args) != 0:
      logging.error('Invalid arguments')
      logging.error('Usage: objectformats')
      return

    client = d1_client.mnclient.MemberNodeClient(self.opts['mn_url'])

    object_list = d1_client.objectlistiterator.ObjectListIterator(client)

    unique_objects = {}
    for info in object_list:
      logging.debug("ID:%s | FMT: %s" % (info.identifier, info.objectFormat))
      try:
        unique_objects[info.objectFormat] += 1
      except KeyError:
        unique_objects[info.objectFormat] = 1

    self.output(StringIO.StringIO('\n'.join(unique_objects) + '\n'))


def main():
  log_setup()

  # Command line options.
  parser = optparse.OptionParser('usage: %prog <command> [options] [arguments]')
  # General
  parser.add_option(
    '--dataone-url',
    dest='dataone_url',
    action='store',
    type='string',
    default=d1_common.const.URL_DATAONE_ROOT,
    help='URL to DataONE Root'
  )
  parser.add_option(
    '--mn-url',
    dest='mn_url',
    action='store',
    type='string',
    default='http://localhost:8000/',
    help='URL to Member Node'
  )
  parser.add_option(
    '--cn-url',
    dest='cn_url',
    action='store',
    type='string',
    default='http://localhost:8000/cn/',
    help='URL to Coordinating Node'
  )
  parser.add_option(
    '--xsd-path',
    dest='xsd_url',
    action='store',
    type='string',
    default='http://localhost/schemas/systemmetadata.xsd',
    help='Location of System Metadata schema'
  )
  parser.add_option(
    '--output',
    dest='output',
    action='store',
    type='string',
    help='store data to file instead of writing it to StdOut'
  )
  parser.add_option(
    '--pretty',
    dest='pretty',
    action='store_true',
    default=False,
    help='render Pretty Printed XML'
  )
  parser.add_option(
    '--verbose',
    dest='verbose',
    action='store_true',
    default=False,
    help='display more information'
  )
  parser.add_option(
    '--slice-start',
    dest='slice_start',
    action='store',
    type='int',
    default=0,
    help='Start position for sliced resultset'
  )
  parser.add_option(
    '--slice-count',
    dest='slice_count',
    action='store',
    type='int',
    default=d1_common.const.MAX_LISTOBJECTS,
    help='Max number of elements in sliced resultset'
  )
  parser.add_option(
    '--request-format',
    dest='request_format',
    action='store',
    type='string',
    default='text/xml',
    help='Request serialization format for response from server'
  )
  # Auth
  parser.add_option(
    '--cert-path',
    dest='cert_path',
    action='store',
    type='string',
    default=''
  )
  parser.add_option(
    '--key-path', dest='key_path',
    action='store',
    type='string',
    default=''
  )
  # SysMeta.
  parser.add_option(
    '--sysmeta-object-format',
    dest='sysmeta_object_format',
    action='store',
    type='string',
    default=''
  )
  parser.add_option(
    '--sysmeta-submitter',
    dest='sysmeta_submitter',
    action='store',
    type='string',
    default=''
  )
  parser.add_option(
    '--sysmeta-rightsholder',
    dest='sysmeta_rightsholder',
    action='store',
    type='string',
    default=''
  )
  parser.add_option(
    '--sysmeta-origin-member-node',
    dest='sysmeta_origin_member_node',
    action='store',
    type='string',
    default=''
  )
  parser.add_option(
    '--sysmeta-authoritative-member-node',
    dest='sysmeta_authoritative_member_node',
    action='store',
    type='string',
    default=''
  )
  # Search filters
  parser.add_option(
    '--start-time',
    dest='start_time',
    action='store',
    type='string',
    default=None
  )
  parser.add_option(
    '--end-time',
    dest='end_time',
    action='store',
    type='string',
    default=None
  )
  parser.add_option(
    '--object-format',
    dest='object_format',
    action='store',
    type='string',
    default=None
  )
  # Log
  parser.add_option(
    '--event-type',
    dest='event_type',
    action='store',
    type='string',
    default=None
  )
  (opts, args) = parser.parse_args()

  opts_dict = vars(opts)

  # Examples:
  #
  # create:
  # ./dataone.py --verbose --dataone-url http://localhost:8000/cn create 1234 test_objects/sysmeta/knb-lter-gce10911 test_objects/scimeta/knb-lter-gce10911 test_objects/harvested/knb-lter-gce10911_MERGED.xml
  #
  # resolve:
  # ./dataone.py --verbose --dataone-url http://localhost:8000/cn resolve 'hdl:10255/dryad.669/mets.xml'
  #
  # get:
  # ./dataone.py --verbose --dataone-url http://localhost:8000/cn get 'hdl:10255/dryad.669/mets.xml'
  #
  # meta:
  # ./dataone.py --verbose --pretty --dataone-url http://localhost:8000/cn meta 'hdl:10255/dryad.669/mets.xml'
  #
  # related:
  # ./dataone.py --dataone-url http://localhost:8000/cn related 'hdl:10255/dryad.669/mets.xml'
  #
  # list:
  # ./dataone.py list --pretty --mn_url=http://dataone.org/mn
  #
  # search:
  # ./dataone.py search --pretty --start-time=2020-01-01T05:00:00
  # ./dataone.py search --pretty --objectFormat=abc
  #
  # log:
  # ./dataone.py log --verbose --pretty --mn-url=http://localhost:8000/
  #
  # objectformats:
  # ./dataone.py objectformats --verbose --mn_url=http://dataone.org/mn

  if not opts.verbose:
    logging.getLogger('').setLevel(logging.ERROR)

  # If certificate path was not provided, set it to the path CILogon downloads
  # certificates to by default.
  if opts_dict['cert_path'] == '':
    opts_dict['cert_path'] = '/tmp/x509up_u{0}'.format(os.getuid())
  if opts_dict['key_path'] == '':
    key_path = None

    # args[1] is not guaranteed to exist but the slice args[1:] would still be
    # valid and evaluate to an empty list.
  dataONECLI = DataONECLI(opts_dict, args[1:])

  # Sanity.
  if len(args) == 0 or args[0] not in dataONECLI.command_map.keys():
    parser.error(
      '<command> is required and must be one of: {0}'
      .format(', '.join(dataONECLI.command_map.keys()))
    )

  if opts.slice_count > d1_common.const.MAX_LISTOBJECTS:
    parser.error(
      '--slice-count must be {0} or less'.format(
        parser.error(
          '<command> is required and must be one of: {0}'
          .format(', '.join(dataONECLI.command_map.keys()))
        )
      )
    )

  # Check dates and convert them from ISO 8601 to datetime.
  date_opts = ['start_time', 'end_time']
  error = False
  for date_opt in date_opts:
    if opts_dict[date_opt] != None:
      try:
        opts.__dict__[date_opt] = iso8601.parse_date(opts_dict[date_opt])
      except (TypeError, iso8601.iso8601.ParseError):
        logging.error(
          'Invalid date option {0}: {1}'.format(
            date_opt, opts_dict[date_opt]
          )
        )
        error = True

  if error == True:
    return

  # Call out to specific command.
  dataONECLI.command_map[args[0]]()


if __name__ == '__main__':
  main()
