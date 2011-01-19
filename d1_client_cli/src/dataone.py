#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
  import d1common.mime_multipart
  import d1common.exceptions
  import d1common.types.objectlist_serialization
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/api-common-python/src/d1common\n'
  )
  raise
try:
  import d1pythonitk
  import d1pythonitk.xmlvalidator
  import d1pythonitk.client
  import d1pythonitk.systemmetadata
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/itk/d1-python/src/d1pythonitk\n'
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

#------------------------------------------------------------------------------


class DataONECLI():
  def __init__(self, opts, args):
    self.opts = opts
    self.args = args

    # Command map.
    self.command_map = {
      'create': self.create,
      'get': self.get,
      'meta': self.meta,
      'search': self.search,
      'log': self.log,
    }

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
    logging.info(
      'create <identifier> <system metadata path> <science metadata path> <science data path>'
    )

    if len(self.args) != 4:
      logging.error('Invalid arguments')
      return

    identifier = self.args[0]
    sysmeta_path = self.args[1]
    scimeta_path = self.args[2]
    scidata_path = self.args[3]

    try:
      sysmeta_file = open(sysmeta_path, 'r')
    except EnvironmentError as (errno, strerror):
      err_msg = 'Could not open System Metadata file: {0}\n'.format(sysmeta_path)
      err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
      logging.error('Create failed: {0}'.format(err_msg))
      return

    try:
      scimeta_file = open(scimeta_path, 'r')
    except EnvironmentError as (errno, strerror):
      err_msg = 'Could not open Science Metadata file: {0}\n'.format(scimeta_path)
      err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
      logging.error('Create failed: {0}'.format(err_msg))
      return

    try:
      scidata_file = open(scidata_path, 'r')
    except EnvironmentError as (errno, strerror):
      err_msg = 'Could not open Science Data file: {0}\n'.format(scidata_path)
      err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
      logging.error('Create failed: {0}'.format(err_msg))
      return

    client = d1pythonitk.client.DataOneClient(self.opts.mn_url)

    try:
      client.create(identifier, scimeta_file, sysmeta_file)
    except:
      logging.error('Create failed')
      raise

    try:
      client.create(identifier, scidata_file, sysmeta_file)
    except:
      logging.error('Create failed')
      raise

  def get(self):
    '''Use Case 01 - Get Object Identified by GUID.
    No distinction is made between Member Node and Coordinating Node
    implementation as they are identical at this level of detail.
    '''
    logging.info('get <identifier>')

    identifier = self.args[0]

    # Get
    client = d1pythonitk.client.SimpleDataOneClient()

    sci_obj = client.get(identifier)

    self.output(sci_obj)

  def meta(self):
    '''Use Case 37 - Get System Metadata for Object.
    '''
    logging.info('meta <identifier>')

    identifier = self.args[0]

    # Get
    #client = d1pythonitk.client.SimpleDataOneClient()
    client = d1pythonitk.client.SimpleDataOneClient()

    sci_meta = client.getSysMeta(identifier)
    sci_meta_xml = sci_meta.toxml()

    if self.opts['pretty']:
      dom = xml.dom.minidom.parseString(sci_meta_xml)
      sci_meta_xml = dom.toprettyxml()

    self.output(StringIO.StringIO(sci_meta_xml))

  def search(self):
    logging.info('search')

    start = 0
    count = d1pythonitk.const.MAX_LISTOBJECTS
    requestFormat = "text/xml"
    headers = None

    client = d1pythonitk.client.SimpleDataOneClient()

    object_list = client.listObjects(
      startTime=self.opts['startTime'],
      endTime=self.opts['endTime'],
      objectFormat=self.opts['objectFormat'],
      start=start,
      count=count,
      requestFormat=requestFormat
    )

    object_list_xml = object_list.toxml()

    if self.opts['pretty']:
      dom = xml.dom.minidom.parseString(object_list_xml)
      object_list_xml = dom.toprettyxml()

    self.output(StringIO.StringIO(object_list_xml))

  def log(self):
    logging.info('log')

    start = 0
    count = d1pythonitk.const.MAX_LISTOBJECTS
    requestFormat = "text/xml"
    headers = None

    client = d1pythonitk.client.SimpleDataOneClient()

    object_list = client.getLogRecords(
      startTime=self.opts['startTime'],
      endTime=self.opts['endTime'],
      objectFormat=self.opts['objectFormat'],
      start=start,
      count=count
    )

    object_list_xml = object_list.toxml()

    if self.opts['pretty']:
      dom = xml.dom.minidom.parseString(object_list_xml)
      object_list_xml = dom.toprettyxml()

    self.output(StringIO.StringIO(object_list_xml))


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
    default=d1pythonitk.const.URL_DATAONE_ROOT,
    help='URL to DataONE Root'
  )
  parser.add_option(
    '--mn-url',
    dest='mn_url',
    action='store',
    type='string',
    default='http://127.0.0.1:8000/',
    help='URL to MN'
  )
  parser.add_option(
    '--cn-url',
    dest='cn_url',
    action='store',
    type='string',
    default='http://cn-dev.dataone.org/cn/',
    help='URL to CN'
  )
  parser.add_option(
    '--xsd-path',
    dest='xsd_url',
    action='store',
    type='string',
    default='http://129.24.0.11/systemmetadata.xsd',
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
  # Search filters
  parser.add_option(
    '--startTime',
    action='store',
    type='string',
    default=None,
    dest='startTime'
  )
  parser.add_option(
    '--endTime', action='store',
    type='string',
    default=None, dest='endTime'
  )
  parser.add_option(
    '--objectFormat',
    action='store',
    type='string',
    default=None,
    dest='objectFormat'
  )

  (opts, args) = parser.parse_args()

  opts_dict = vars(opts)

  # Examples:
  # ./dataone.py meta nceas9318
  # ./dataone.py search --pretty --startTime=2020-01-01T05:00:00
  # ./dataone.py search --pretty --objectFormat=abc

  #if not opts.verbose:
  #  logging.getLogger('').setLevel(logging.ERROR)

  # args[1] is not guaranteed to exist but the slice args[1:] would still be
  # valid and evaluate to an empty list.
  dataONECLI = DataONECLI(opts_dict, args[1:])

  # Sanity.
  if len(args) == 0 or args[0] not in dataONECLI.command_map.keys():
    parser.error(
      '<command> is required and must be one of: {0}'.format(
        ', '.join(
          dataONECLI.command_map.keys(
          )
        )
      )
    )

  # Check dates and convert them from ISO 8601 to datetime.
  date_opts = ['startTime', 'endTime']
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
