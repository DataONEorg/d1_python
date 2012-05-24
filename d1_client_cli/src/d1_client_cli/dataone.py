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
==============

:Synopsis: DataONE Command Line Interface
:Created: 2011-11-20
:Author: DataONE (Dahl)
'''

# Stdlib.
import cmd
import htmlentitydefs
import logging
import optparse
from optparse import make_option
import os
import re
import shlex
import StringIO
from string import join
import sys
import xml.dom.minidom

# D1
try:
  import d1_common.util
  import d1_common.const
  import d1_common.types.exceptions
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install DataONE_Common\n')
  raise

# App.
from print_level import * #@UnusedWildImport
import cli_client
import cli_exceptions
import cli_util
from const import * #@UnusedWildImport
import initialize #@UnusedImport
import package_cli
import session

known_object_formats = None
DEFAULT_PREFIX = ''
DEFAULT_PROMPT = '> '
SOLR_FORMAT_ID_NAME = 'formatId'


def log_setup():
  logging.getLogger('').setLevel(logging.INFO)
  formatter = logging.Formatter('%(levelname)-8s %(message)s')
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def expand_path(filename):
  if filename:
    return os.path.expanduser(filename)
  return None

#===============================================================================
#   Command-line options.
#
option_list = [
  make_option(
    "--" + CHECKSUM_name,
    action="store",
    dest="algorithm",
    help="Checksum algorithm used for a Science Data Object."
  ),
  make_option(
    "--" + ANONYMOUS_name,
    action="store_true",
    dest="anonymous",
    help="Ignore any installed certificates and connect anonymously"
  ),
  make_option(
    "--no-" + ANONYMOUS_name,
    action="store_false",
    dest="anonymous",
    help="Use the installed certificates and do not connect anonymously"
  ),
  make_option(
    "--" + AUTH_MN_name,
    action="store",
    dest="authoritative_mn",
    metavar="MN-URI",
    help="Authoritative Member Node for generating System Metadata."
  ),
  make_option(
    "--" + CERT_FILENAME_name,
    action="store",
    dest="cert_file",
    metavar="FILE",
    help="Path to client certificate"
  ),
  make_option(
    "--" + COUNT_name,
    action="store",
    dest="count",
    type="int",
    help="Maximum number of items to display"
  ),
  make_option(
    "--" + CN_URL_name,
    action="store",
    dest="dataone_url",
    metavar="URI",
    help="URI to use for the Coordinating Node"
  ),
  make_option(
    "--" + FROM_DATE_name,
    action="store",
    dest="from_date",
    metavar="DATE",
    help="Start time used by operations that accept a date range"
  ),
  make_option(
    "--" + KEY_FILENAME_name,
    action="store",
    dest="key_file",
    metavar="FILE",
    help="File of client private key (not required if key is in cert-file"
  ),
  make_option(
    "--" + MN_URL_name,
    action="store",
    dest="mn_url",
    metavar="URI",
    help="Member Node URL"
  ),
  make_option(
    "--" + FORMAT_name,
    action="store",
    dest="object_format",
    metavar="OBJECT-FORMAT",
    help="ID for the Object Format to use when generating System Metadata"
  ),
  make_option(
    "--" + ORIG_MN_name,
    action="store",
    dest="origin_mn",
    metavar="MN-URI",
    help="Originating Member Node to use when generating System Metadata"
  ),
  make_option(
    "--" + PRETTY_name,
    action="store_true",
    dest="pretty",
    help="Display XML with human friendly formatting"
  ),
  make_option(
    "--no-" + PRETTY_name,
    action="store_false",
    dest="pretty",
    help="Display XML with human friendly formatting"
  ),
  make_option(
    "--" + QUERY_STRING_name,
    action="store",
    dest="query_string",
    metavar="QUERY",
    help="Query string (SOLR or Lucene query syntax) for searches"
  ),
  make_option(
    "--" + OWNER_name,
    action="store",
    dest="rights_holder",
    metavar="SUBJECT",
    help="Subject of the rights holder to use when generating System Metadata"
  ),
  make_option(
    "--" + SEARCH_FORMAT_name,
    action="store",
    dest="search_object_format",
    metavar="OBJECT-FORMAT",
    help="Include only objects of this format when searching"
  ),
  make_option(
    "--" + START_name,
    action="store",
    dest="start",
    type="int",
    help="First item to display for operations that display a list_objects of items"
  ),
  make_option(
    "--" + SUBMITTER_name,
    action="store",
    dest="submitter",
    metavar="SUBJECT",
    help="Subject of the submitter to use when generating System Metadata"
  ),
  make_option(
    "--" + TO_DATE_name,
    action="store",
    dest="to_date",
    metavar="DATE",
    help="End time used by operations that accept a date range"
  ),
  make_option(
    "-v",
    "--" + VERBOSE_name,
    action="store_true",
    dest="verbose",
    help="Display more information"
  ),
  make_option(
    "--no-" + VERBOSE_name,
    action="store_false",
    dest="verbose",
    help="Display less information"
  ),
  make_option(
    "--allow-public",
    action="store_true",
    dest="action_allowPublic",
    help="Allow public read access."
  ),
  make_option(
    "--deny-public",
    action="store_false",
    dest="action_allowPublic",
    help="Deny public read access."
  ),
  make_option(
    "--allow-replication",
    action="store_true",
    dest="action_allowReplication",
    help="Allow objects to be replicated."
  ),
  make_option(
    "--disallow-replication",
    action="store_false",
    dest="action_allowReplication",
    help="Do not allow objects to be replicated."
  ),
  make_option(
    "--replicas",
    action="store",
    dest="action_numReplicas",
    metavar="#replicas",
    help="Set the preferred number of replicas."
  ),
  make_option(
    "--add_blocked",
    action="store",
    dest="action_blockNode",
    metavar="MN",
    help="Add blocked Member Node to access policy."
  ),
  make_option(
    "--add_preferred",
    action="store",
    dest="action_preferNode",
    metavar="MN",
    help="Add Member Node to list_objects of preferred replication targets."
  ),
  #  make_option("--configure", action="store_true", dest="action_configure",
  #              help="Perform initial configuration"),
  make_option(
    "--cn",
    action="store",
    dest="cn_host",
    metavar="HOST",
    help="Name of the host to use for the Coordinating Node"
  ),
  make_option(
    "--mn",
    action="store",
    dest="mn_host",
    metavar="HOST",
    help="Name of the host to use for the Member Node"
  ),
  make_option(
    "-i",
    "--interactive",
    action="store_true",
    dest="interactive",
    help="Allow interactive commands"
  ),
  make_option(
    "--no-interactive",
    action="store_false",
    dest="interactive",
    help="Don't allow interactive commands"
  ),
  make_option(
    "-q",
    "--quiet",
    action="store_false",
    dest="verbose",
    help="Display less information"
  ),
]


def handle_options(cli, options):
  try:
    if options.algorithm:
      cli.d1.session_set_parameter(CHECKSUM_name, options.algorithm)
    if options.anonymous:
      cli.d1.session_set_parameter(ANONYMOUS_name, options.anonymous)
    if options.authoritative_mn:
      cli.d1.session_set_parameter(AUTH_MN_name, options.authoritative_mn)
    if options.cert_file:
      cli.d1.session_set_parameter(CERT_FILENAME_name, options.cert_file)
    if options.count:
      cli.d1.session_set_parameter(COUNT_name, options.count)
    if options.dataone_url:
      cli.d1.session_set_parameter(CN_URL_name, options.dataone_url)
    if options.cn_host:
      url = ''.join(
        (
          d1_common.const.DEFAULT_CN_PROTOCOL, '://', options.cn_host,
          d1_common.const.DEFAULT_CN_PATH
        )
      )
      cli.d1.session_set_parameter(CN_URL_name, url)
    if options.from_date:
      cli.d1.session_set_parameter(FROM_DATE_name, options.from_date)
    if options.key_file:
      cli.d1.session_set_parameter(KEY_FILENAME_name, options.key_file)
    if options.mn_url:
      cli.d1.session_set_parameter(MN_URL_name, options.mn_url)
    if options.mn_host:
      url = ''.join(
        (
          d1_common.const.DEFAULT_MN_PROTOCOL, '://', options.mn_host,
          d1_common.const.DEFAULT_MN_PATH
        )
      )
      cli.d1.session_set_parameter(MN_URL_name, url)
    if options.object_format:
      cli.d1.session_set_parameter(FORMAT_name, options.object_format)
    if options.origin_mn:
      cli.d1.session_set_parameter(ORIG_MN_name, options.origin_mn)
    if options.pretty:
      cli.d1.session_set_parameter(PRETTY_name, options.pretty)
    if options.query_string:
      cli.d1.session_set_parameter(QUERY_STRING_name, options.query_string)
    if options.rights_holder:
      cli.d1.session_set_parameter(OWNER_name, options.rights_holder)
    if options.search_object_format:
      try:
        cli.d1.session_set_parameter(SEARCH_FORMAT_name, options.search_object_format)
      except ValueError as e:
        print_error(e.args[0])
    if options.start:
      cli.d1.session_set_parameter(START_name, options.start)
    if options.submitter:
      cli.d1.session_set_parameter(SUBMITTER_name, options.submitter)
    if options.to_date:
      cli.d1.session_set_parameter(TO_DATE_name, options.to_date)
    if options.verbose:
      cli.d1.session_set_parameter(VERBOSE_name, options.verbose)

    if options.action_allowPublic is not None:
      if options.action_allowPublic:
        cli.d1.access_control_allow_public(True)
      else:
        cli.d1.access_control_allow_public(False)
    if options.action_allowReplication is not None:
      if options.action_allowReplication:
        cli.d1.replication_policy_set_replication_allowed(True)
      else:
        cli.d1.replication_policy_set_replication_allowed(False)
    if options.action_numReplicas:
      cli.d1.replication_policy_set_number_of_replicas(options.action_numReplicas)
    if options.action_blockNode:
      cli.d1.replication_policy_add_blocked(options.action_blockNode)
    if options.action_preferNode:
      cli.d1.replication_policy_add_preferred(options.action_preferNode)

#    if (options.action_configure is not None) and options.action_configure:
#      initialize.configuration(cli.d1.session)

    cli._update_verbose()
  except cli_exceptions.InvalidArguments as e:
    print_error(e)
  except:
    cli_util._handle_unexpected_exception()

#===============================================================================


class DataONECLI():
  def __init__(self):
    self.session = session.session()
    self.session.load(suppress_error=True)
    self.known_object_formats = None

  def get_known_object_formats(self):
    if self.known_object_formats is None:
      formats = None
      try:
        client = cli_client.CLICNClient(self.session)
        formats = client.listFormats()
        num_formats = len(formats.objectFormat)
        #
        # Only process if there are enough (>10) items.
        if 10 < num_formats:
          self.known_object_formats = []
          for f in list(formats.objectFormat):
            self.known_object_formats.append(f.formatId)
      except (d1_common.types.exceptions.ServiceFailure) as e:
        print_error("Unable to get allowed types.")
    #
    # Return it if you found something.
    if self.known_object_formats is not None:
      return list(self.known_object_formats)
    else:
      return ()

  def _get_file_size(self, path):
    with open(expand_path(path), 'r') as f:
      f.seek(0, os.SEEK_END)
      size = f.tell()
    return size

  def _get_file_checksum(self, path, algorithm='SHA-1', block_size=1024 * 1024):
    h = d1_common.util.get_checksum_calculator_by_dataone_designator(algorithm)
    with open(expand_path(path), 'r') as f:
      while True:
        data = f.read(block_size)
        if not data:
          break
        h.update(data)
    return h.hexdigest()

  def _assert_file_exists(self, path):
    if not os.path.isfile(expand_path(path)):
      msg = 'Invalid file: {0}'.format(path)
      raise cli_exceptions.InvalidArguments(msg)

  def _set_invalid_checksum_to_default(self):
    algorithm = self.session.get(CHECKSUM_sect, CHECKSUM_name)
    try:
      d1_common.util.get_checksum_calculator_by_dataone_designator(algorithm)
    except (ValueError, LookupError, KeyError) as e:
      self.session.set(
        CHECKSUM_sect, CHECKSUM_name, d1_common.const.DEFAULT_CHECKSUM_ALGORITHM
      )
      print_error(
        'Invalid checksum algorithm, "{0}", set to default, "{1}"'
        .format(algorithm, d1_common.const.DEFAULT_CHECKSUM_ALGORITHM)
      )

  def _create_system_metadata(self, pid, path, formatId=None):
    checksum = self._get_file_checksum(
      expand_path(path), self.session.get(
        CHECKSUM_sect, CHECKSUM_name
      )
    )
    size = self._get_file_size(expand_path(path))
    sysmeta = self.session.create_system_metadata(pid, checksum, size, formatId)
    return sysmeta

  def _create_system_metadata_xml(self, pid, path):
    sysmeta = self._create_system_metadata(pid, expand_path(path))
    return sysmeta.toxml()

  def _is_verbose(self):
    verbosity = self.session.get(VERBOSE_sect, VERBOSE_name)
    if verbosity is not None:
      return verbosity
    else:
      return False

  def _is_pretty(self):
    pretty = self.session.get(PRETTY_sect, PRETTY_name)
    if pretty is not None:
      return pretty
    else:
      return False

  ##-- Create --------------------------------------------------------------

  def _post_file_and_system_metadat_to_member_node(self, client, pid, path, sysmeta):
    with open(expand_path(path), 'r') as f:
      try:
        return client.create(pid, f, sysmeta)
      except d1_common.types.exceptions.DataONEException as e:
        print_error(
          'Unable to create Science Object on Member Node\n{0}'
          .format(e.friendly_format())
        )

  def science_object_create(self, pid, path, formatId=None):
    '''Create a new Science Object on a Member Node
    '''
    path = expand_path(path)
    self._assert_file_exists(path)
    sysmeta = self._create_system_metadata(pid, path, formatId)
    client = cli_client.CLIMNClient(self.session)
    self._post_file_and_system_metadat_to_member_node(client, pid, path, sysmeta)

  ##-- Update --------------------------------------------------------------

  def _put_file_and_system_metadat_to_member_node(
    self, client, old_pid, path, new_pid, sysmeta
  ):
    with open(expand_path(path), 'r') as f:
      try:
        return client.update(old_pid, f, new_pid, sysmeta)
      except d1_common.types.exceptions.DataONEException as e:
        print_error(
          'Unable to update Science Object on Member Node\n{0}'
          .format(e.friendly_format())
        )

  def science_object_update(self, old_pid, path, new_pid):
    '''Obsolete a Science Object on a Member Node with a different one.
    '''
    path = expand_path(path)
    self._assert_file_exists(path)
    sysmeta = self._create_system_metadata(new_pid, path)
    self._add_obsoletes_to_sysmeta_if_missing(sysmeta, old_pid)
    client = cli_client.CLIMNClient(self.session)
    self._put_file_and_system_metadat_to_member_node(
      client, old_pid, path, new_pid, sysmeta
    )

  def _add_obsoletes_to_sysmeta_if_missing(self, sysmeta, old_pid):
    if sysmeta.obsoletes is None:
      sysmeta.obsoletes = old_pid

  ##-- Delete --------------------------------------------------------------

  def science_object_archive(self, pid):
    client = cli_client.CLIMNClient(self.session)
    self._archive_on_member_node(client, pid)

  def _archive_on_member_node(self, client, pid):
    try:
      return client.delete(pid)
    except d1_common.types.exceptions.DataONEException as e:
      print_error(
        'Unable to delete Science Object from Member Node\n{0}'
        .format(e.friendly_format())
      )

  def _copy_file_like_object_to_file(self, file_like_object, path):
    cli_util.copy_file_like_object_to_file(file_like_object, path)

  def output(self, file_like_object, path):
    '''Display or save file like object'''
    if not path:
      for line in file_like_object:
        if self._is_verbose():
          print_info(line.rstrip())
        else:
          print line.rstrip()
    else:
      self._copy_file_like_object_to_file(file_like_object, expand_path(path))

  def _get_science_object_from_member_node(self, client, pid):
    try:
      return client.get(pid)
    except d1_common.types.exceptions.DataONEException as e:
      raise cli_exceptions.CLIError(
        'Unable to get Science Object from Member Node\n{0}'\
          .format(e.friendly_format()))

  def science_object_get(self, pid, path):
    client = cli_client.CLIMNClient(self.session)
    response = self._get_science_object_from_member_node(client, pid)
    self.output(response, expand_path(path))

  def _get_system_metadata(self, client, pid):
    try:
      return client.getSystemMetadata(pid)
    except d1_common.types.exceptions.DataONEException as e:
      raise cli_exceptions.CLIError(
        'Unable to get System Metadata from Coordinating Node\n{0}'\
          .format(e.friendly_format()))

  def _pretty(self, xml_doc):
    if self._is_pretty():
      dom = xml.dom.minidom.parseString(xml_doc)
      return dom.toprettyxml(indent='  ')
    return xml_doc

  def system_metadata_get(self, pid, path):
    metadata = None
    foundOnCN = False
    try:
      client = cli_client.CLICNClient(self.session)
      metadata = client.getSystemMetadata(pid)
    except d1_common.types.exceptions.DataONEException as e:
      pass
    if metadata is not None:
      foundOnCN = True
    else:
      try:
        client = cli_client.CLIMNClient(self.session)
        metadata = client.getSystemMetadata(pid)
      except d1_common.types.exceptions.DataONEException as e:
        pass
    if metadata is None:
      print_info(e.friendly_format())
    else:
      self.system_metadata_print(metadata, path, foundOnCN)

  def system_metadata_print(self, metadata, path=None, foundOnCN=False):
    if self.session.is_pretty() and not foundOnCN:
      print("<!-- Found the metadata on the Member Node... -->")
    sci_meta_xml = metadata.toxml()
    self.output(StringIO.StringIO(self._pretty(sci_meta_xml)), expand_path(path))

  def resolve(self, pid):
    '''Get Object Locations for Object.
    '''
    client = cli_client.CLICNClient(self.session)
    try:
      object_location_list = client.resolve(pid)
    except d1_common.types.exceptions.DataONEException as e:
      raise cli_exceptions.CLIError(
        'Unable to get resolve: {0}\n{1}'.format(pid, e.friendly_format())
      )
    for location in object_location_list.objectLocation:
      if self._is_verbose():
        print_info(location.url)
      else:
        print location.url

  def list_objects(self, path):
    '''MN listObjects.
    '''
    client = cli_client.CLIMNClient(self.session)
    object_list = client.listObjects(
      fromDate=self.session.get(FROM_DATE_sect, FROM_DATE_name),
      toDate=self.session.get(TO_DATE_sect, TO_DATE_name),
      objectFormat=self.session.get(SEARCH_FORMAT_sect, SEARCH_FORMAT_name),
      start=self.session.get(START_sect, START_name),
      count=self.session.get(COUNT_sect, COUNT_name)
    )
    object_list_xml = object_list.toxml()
    self.output(StringIO.StringIO(self._pretty(object_list_xml)), expand_path(path))

  def log(self, path):
    '''MN log.
    '''
    client = cli_client.CLIMNClient(self.session)
    object_log = client.getLogRecords(
      fromDate=self.session.get(FROM_DATE_sect, FROM_DATE_name),
      toDate=self.session.get(TO_DATE_sect, TO_DATE_name),
      start=self.session.get(START_sect, START_name),
      count=self.session.get(COUNT_sect, COUNT_name)
    )
    object_log_xml = object_log.toxml()
    self.output(StringIO.StringIO(self._pretty(object_log_xml)), expand_path(path))

  def set_access_policy(self, pid):
    access_policy = self.session.access_control_get_pyxb()
    if access_policy is None:
      print_error('There is no access policy defined.')
      return None
    client = cli_client.CLICNClient(self.session)
    try:
      metadata = client.getSystemMetadata(pid)
      if ((metadata is None) or (metadata.serialVersion is None)):
        raise cli_exceptions.CLIError(
          'Unable to get current serial version of: {0}'.format(pid)
        )
      return client.setAccessPolicy(pid, access_policy, metadata.serialVersion)
    except d1_common.types.exceptions.DataONEException as e:
      raise cli_exceptions.CLIError(
        'Unable to set access policy on: {0}\nError:\n{1}'\
          .format(pid, e.friendly_format()))

  def set_replication_policy(self, pid):
    replication_policy = self.session.replication_control_get_pyxb()
    client = cli_client.CLICNClient(self.session)
    try:
      metadata = client.getSystemMetadata(pid)
      if ((metadata is None) or (metadata.serialVersion is None)):
        raise cli_exceptions.CLIError(
          'Unable to get current serial version of: {0}'.format(pid)
        )

      return client.setReplicationPolicy(
        pid, policy=replication_policy,
        serialVersion=metadata.serialVersion
      )
    except d1_common.types.exceptions.DataONEException as e:
      raise cli_exceptions.CLIError(
        'Unable to set replication policy on: {0}\nError:\n{1}'\
          .format(pid, e.friendly_format()))

  # ----------------------------------------------------------------------------
  # Ping
  # ----------------------------------------------------------------------------

  def ping(self, hosts):
    pretty = self.session.is_pretty()
    if len(hosts) == 0:
      url = self.session.get(CN_URL_sect, CN_URL_name)
      success = self._pingCN(url)
      self._print_ping_result(success, url, pretty)
      #
      url = self.session.get(MN_URL_sect, MN_URL_name)
      success = self._pingMN(url)
      self._print_ping_result(success, url, pretty)
    else:
      for target in hosts:
        self._ping(target, pretty)

  def _ping(self, target, pretty=True):
    msg = ''
    if target.find('http') == 0:
      msg = target
      success = self._pingCN(target)
      if not success:
        success = self._pingMN(target)
    else:
      msg = target
      url = str(
        d1_common.const.DEFAULT_CN_PROTOCOL + '://' + target +
        d1_common.const.DEFAULT_CN_PATH
      )
      success = self._pingCN(url)
      if success:
        msg = target + ' (a DataONE node)'
      else:
        url = str(
          d1_common.const.DEFAULT_MN_PROTOCOL + '://' + target +
          d1_common.const.DEFAULT_MN_PATH
        )
        success = self._pingMN(url)
        if success:
          msg = target + ' (a Member node)'
    # Show result.
    self._print_ping_result(success, msg, pretty)

  def _pingCN(self, cnURL):
    return cli_client.CLICNClient(self.session, cnURL).ping()

  def _pingMN(self, mnURL):
    return cli_client.CLIMNClient(self.session, mnURL).ping()

  def _print_ping_result(self, result, url, pretty):
    if pretty is not None and pretty:
      if result:
        print_info('%s is awake.' % url)
      else:
        print_warn('%s did not respond.' % url)
    else:
      if not result:
        print_warn('%s did not respond.' % url)

      # ----------------------------------------------------------------------------
      # Search
      # ----------------------------------------------------------------------------

  def search(self, line):
    '''CN search.
    '''
    if self.session.get(QUERY_ENGINE_sect, QUERY_ENGINE_name) == 'solr':
      return self.search_solr(line)
    return self.search_generic(line)

  def search_solr(self, line):
    '''Perform a SOLR search.
    '''
    try:
      query = (
        line + ' ' + self._object_format_to_solr_filter(line) + ' ' +
        self._time_span_to_solr_filter()
      )

      client = cli_client.CLICNClient(self.session)
      object_list = client.search(
        queryType=d1_common.const.DEFAULT_SEARCH_ENGINE,
        q=query,
        start=self.session.get(START_sect, START_name),
        rows=self.session.get(COUNT_sect, COUNT_name)
      )
      print self._pretty(object_list.toxml())
    #
    # SOLR returns HTML instead of XML when there's a problem.  See:
    #   https://issues.apache.org/jira/browse/SOLR-141
    except d1_common.types.exceptions.ServiceFailure as e:
      e = "%".join(str(e).splitlines()) # Flatten line
      regexp = re.compile(
        r"errorCode: (?P<error_code>\d+)%.*%Status code: (?P<status_code>\d+)"
      )
      result = regexp.search(e)
      if ((result is not None) and
          (result.group('error_code') == '500') and
          (result.group('status_code') == '400')):
        result = re.search(r"<b>description</b> <u>(?P<description>[^<]+)</u>", e)
        msg = re.sub(
          '&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]),
          result.group('description')
        )
        print_info('Warning: %s' % msg)
      else:
        if self._is_verbose():
          print_error('Unexpected error:\n%s' % str(e))
        else:
          print_error('Unexpected error')

  def search_generic(self, line):
    '''Perform a generic search.
    '''
    pass

  def _time_span_to_solr_filter(self):
    fromdate = self.session.get(FROM_DATE_sect, FROM_DATE_name)
    todate = self.session.get(TO_DATE_sect, TO_DATE_name)
    return 'dateModified:[{0} TO {1}]'.format(
      d1_common.date_time.to_http_datetime(fromdate) if fromdate else '*',
      d1_common.date_time.to_http_datetime(todate) if todate else '*'
    )

  def _object_format_to_solr_filter(self, line):
    search_format_id = self.session.get(SEARCH_FORMAT_sect, SEARCH_FORMAT_name)
    if (search_format_id != None) and (search_format_id != ''):
      if line.find(SOLR_FORMAT_ID_NAME) >= 0:
        print_warn('Using query format restriction instead "%s"' % search_format_id)
      else:
        return '%s:%s' % (SOLR_FORMAT_ID_NAME, search_format_id)
    return ''

  # ----------------------------------------------------------------------------
  # Session parameters
  # ----------------------------------------------------------------------------

  def reset(self):
    return self.session.reset()

  def session_load(self, suppress_error=False, pickle_file_path=None):
    return self.session.load(suppress_error, expand_path(pickle_file_path))

  def session_save(self, pickle_file_path=None):
    return self.session.save(expand_path(pickle_file_path))

  def session_print_parameter(self, name):
    return self.session.print_parameter(name)

  def session_set_parameter(self, name, value):
    self.session_validate_parameter(name, value)
    return self.session.set_with_conversion_implicit_section(name, value)

  def session_clear_parameter(self, name):
    return self.session.set_with_implicit_section(name, None)

  def session_validate_parameter(self, name, value):
    # Skip None.
    if value is None:
      return
    #
    # Validate the hash algorithm
    if name == CHECKSUM_name:
      try:
        d1_common.util.get_checksum_calculator_by_dataone_designator(value)
      except (KeyError, NameError) as e:
        raise ValueError('"%s": Invalid algorithm value' % value)
    #
    # Validate the object format.
    if name == FORMAT_name or name == SEARCH_FORMAT_name:
      formats = self.get_known_object_formats()
      if len(formats) > 0 and value not in formats:
        raise ValueError('"%s": Invalid format' % value)

  # ----------------------------------------------------------------------------
  # Access control
  # ----------------------------------------------------------------------------

  def access_control_add_allowed_subject(self, subject, permission):
    return self.session.access_control_add_allowed_subject(subject, permission)

  def access_control_remove_allowed_subject(self, subject):
    return self.session.access_control_remove_allowed_subject(subject)

  def access_control_allow_public(self, allow):
    self.session.access_control_allow_public(allow)

  def access_control_remove_all_allowed_subjects(self):
    self.session.access_control_remove_all_allowed_subjects()

  # ----------------------------------------------------------------------------
  # Replication policy
  # ----------------------------------------------------------------------------

  def replication_policy_clear(self):
    return self.session.replication_policy_clear()

  def replication_policy_add_preferred(self, mn):
    return self.session.replication_policy_add_preferred(mn)

  def replication_policy_add_blocked(self, mn):
    return self.session.replication_policy_add_blocked(mn)

  def replication_policy_remove(self, mn):
    return self.session.replication_policy_remove(mn)

  def replication_policy_set_replication_allowed(self, replication_allowed):
    return self.session.replication_policy_set_replication_allowed(replication_allowed)

  def replication_policy_set_number_of_replicas(self, number_of_replicas):
    return self.session.replication_policy_set_number_of_replicas(number_of_replicas)

  def replication_policy_print(self):
    return self.session.replication_policy_print()

#===============================================================================


class CLI(cmd.Cmd):
  def __init__(self):
    self.d1 = DataONECLI()
    cmd.Cmd.__init__(self)
    self._update_verbose()
    self.prefix = DEFAULT_PREFIX
    self.prompt = DEFAULT_PROMPT
    self.intro = 'DataONE Command Line Interface'

    self.packageCLI = None
    self.keep_looping = False
    self.interactive = False

  def _split_args(self, line, n_required, n_optional):
    args = shlex.split(line)
    if len(args) < n_required or len(args) > n_required + n_optional:
      msg = 'Need {0} required and {1} optional parameters'.format(
        n_required if n_required else 'no', n_optional if n_optional else 'no'
      )
      raise cli_exceptions.InvalidArguments(msg)
    # Pad the list_objects out with None for any optional parameters that were not
    # provided.
    args += [None] * (n_required + n_optional - len(args))
    if len(args) == 1:
      return args[0]
    return args

  def _update_verbose(self):
    verbosity = self.d1.session.get(VERBOSE_sect, VERBOSE_name)
    if verbosity is not None:
      if verbosity:
        logging.getLogger('').setLevel(logging.DEBUG)
      else:
        logging.getLogger('').setLevel(logging.INFO)

  def do_reset(self, line):
    '''reset
    Set all session parameters to their default values
    '''
    try:
      self._split_args(line, 0, 0)
      self.d1.reset()
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_load(self, line):
    '''load [file]
    Load session parameters from file
    '''
    try:
      load_file = self._split_args(line, 0, 1)
      self.d1.session_load(pickle_file_path=expand_path(load_file))
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_save(self, line):
    '''save [config_file]
    Save session parameters to a file
    '''
    try:
      config_file = self._split_args(line, 0, 1)
      self.d1.session_save(pickle_file_path=expand_path(config_file))
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_show(self, line):
    '''show [session parameter]
    Display the value of a session parameter. Display all parameters if
  [session parameter] is omitted.
  
    "show formats" will display all known object formats.
    "show package" will invoke "package show".
    '''
    try:
      params = cli_util.clear_None_from_list(self._split_args(line, 0, 9))
      if len(params) > 0:
        if not self._show_special_parameter(params):
          self.d1.session_print_parameter(params[0])
      else:
        self.d1.session_print_parameter(None)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_set(self, line):
    '''set <parameter> <value>  or  <parameter>=<value>
    Set the value of a session parameter
    '''
    if len(shlex.split(line)) == 0:
      self.do_show(line)
    else:
      try:
        session_parameter, value = self._split_args(line, 1, 1)
        if not value:
          name_value = session_parameter.split('=', 1)
          if len(name_value) < 1:
            print_error('Please specify value.')
            return
          else:
            session_parameter = name_value[0]
            value = name_value[1]
        self.d1.session_set_parameter(session_parameter, value)
      except cli_exceptions.InvalidArguments as e:
        print_error(e)
      except ValueError as e:
        print_error(e)
      except:
        cli_util._handle_unexpected_exception()

  def do_clear(self, line):
    '''clear <session parameter>
    Clear the value of a session parameter.
    '''
    try:
      session_parameter = self._split_args(line, 1, 0)
      self.d1.session_clear_parameter(session_parameter)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  #-----------------------------------------------------------------------------
  # Access control.
  #-----------------------------------------------------------------------------

  def do_allow(self, line):
    '''allow <subject> [access level]
    Allow access to subject.

    Access level is one of:
        'read', 'write', 'changePermission', 'execute', 'replicate'
    '''
    try:
      subject, permission = self._split_args(line, 1, 1)
      if subject == 'public':
        print_error('"public" is a reserved identity.  Please use "allowpublic".')
        return
      self.d1.access_control_add_allowed_subject(subject, permission)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_deny(self, line):
    '''deny <subject>
    Remove subject from access policy
    '''
    try:
      subject = self._split_args(line, 1, 0)
      if subject == 'public':
        print_error('"public" is a reserved identity.  Please use "denypublic".')
        return
      self.d1.access_control_remove_allowed_subject(subject)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_allowpublic(self, line):
    '''allowpublic
    Allow public read
    '''
    try:
      self._split_args(line, 0, 0)
      self.d1.access_control_allow_public(True)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_denypublic(self, line):
    '''denypublic
    Deny public read
    '''
    try:
      self._split_args(line, 0, 0)
      self.d1.access_control_allow_public(False)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_denyall(self, line):
    '''denyall
    Remove all subjects from access policy and deny public read
    '''
    try:
      self._split_args(line, 0, 0)
      self.d1.access_control_remove_all_allowed_subjects()
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  #-----------------------------------------------------------------------------
  # Replication policy.
  #-----------------------------------------------------------------------------

  def do_clearreplication(self, line):
    '''clearreplication
    Clear replication policy
    '''
    try:
      self._split_args(line, 0, 0)
      return self.d1.replication_policy_clear()
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_addpreferred(self, line):
    '''addpreferred <member node>
    Add Member Node to list_objects of preferred replication targets
    '''
    try:
      mn = self._split_args(line, 1, 0)
      return self.d1.replication_policy_add_preferred(mn)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_addblocked(self, line):
    '''addblocked <member node>
    Add blocked Member Node to access policy
    '''
    try:
      mn = self._split_args(line, 1, 0)
      return self.d1.replication_policy_add_blocked(mn)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_remove(self, line):
    '''remove <member node>
    Remove Member Node from access policy
    '''
    try:
      mn = self._split_args(line, 1, 0)
      return self.d1.replication_policy_remove(mn)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_allowreplication(self, line):
    '''allowreplication
    Allow object to be replicated
    '''
    try:
      self._split_args(line, 0, 0)
      return self.d1.replication_policy_set_replication_allowed(True)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_denyreplication(self, line):
    '''denyreplication
    Prevent object from being replicated
    '''
    try:
      self._split_args(line, 0, 0)
      return self.d1.replication_policy_set_replication_allowed(False)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_setreplicas(self, line):
    '''setreplicas <number of replicas>
    Set preferred number of replicas
    '''
    try:
      n_replicas = self._split_args(line, 1, 0)
      return self.d1.replication_policy_set_number_of_replicas(n_replicas)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  #-----------------------------------------------------------------------------
  # Search
  #-----------------------------------------------------------------------------

  def do_search(self, line):
    '''search [query]
    Comprehensive search for Science Data Objects across all available MNs.  See:
      http://mule1.dataone.org/ArchitectureDocs-current/design/SearchMetadata.html
    for the available search terms.
    '''
    try:
      queryArgs = self._split_args(line, 0, 30)
      query = ' '.join(filter(None, queryArgs))
      self.d1.search(query)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  #-----------------------------------------------------------------------------
  # Science Object Operations
  #-----------------------------------------------------------------------------

  def do_get(self, line):
    '''get <pid> <file>
    Get an object from a Member Node
    '''
    try:
      pid, output_file = self._split_args(line, 2, 0)
      self.d1.science_object_get(pid, output_file)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_meta(self, line):
    '''meta <pid> [file]
    Get System Metdata from a Coordinating Node
    '''
    try:
      pid, output_file = self._split_args(line, 1, 1)
      self.d1.system_metadata_get(pid, output_file)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(str(e))
    except:
      cli_util._handle_unexpected_exception()

  def do_create(self, line):
    '''create <pid> <file>
    Create a new Science Object on a Member Node
    '''
    try:
      pid, input_file = self._split_args(line, 2, 0)
      complex_path = cli_util.create_complex_path(input_file)
      self.d1.science_object_create(pid, complex_path.path, complex_path.formatId)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_update(self, line):
    '''update <current-pid> <new-pid> <file>
    Update an existing Science Object on a Member Node
    '''
    try:
      curr_pid, new_pid, input_file = self._split_args(line, 3, 0)
      self.d1.science_object_update(curr_pid, input_file, new_pid)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_archive(self, line):
    '''archive <pid>
    Mark an existing Science Object as archived.
    '''
    try:
      pid = self._split_args(line, 1, 0)
      self.d1.science_object_archive(pid)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_resolve(self, line):
    '''resolve <pid>
    Given the PID for a Science Object, find all locations from which the Science Object can be downloaded
    '''
    try:
      pid = self._split_args(line, 1, 0)
      self.d1.resolve(pid)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_list(self, line):
    '''list_objects
    Retrieve a list_objects of available Science Data Objects from a single MN with basic filtering
    '''
    try:
      path = self._split_args(line, 0, 1)
      self.d1.list_objects(path)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)
    except (KeyboardInterrupt, IOError) as e:
      return
    except:
      cli_util._handle_unexpected_exception()

  def do_log(self, line):
    '''log [path]
    Retrieve event log
    '''
    try:
      path = self._split_args(line, 0, 1)
      self.d1.log(path)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_setaccess(self, line):
    '''setaccess <pid>
    Update the Access Policy on an existing Science Data Object
    '''
    try:
      pid = self._split_args(line, 1, 0)
      self.d1.set_access_policy(pid)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_setreplication(self, line):
    '''setreplication <pid>
    Update the Replication Policy on an existing Science Data Object
    '''
    try:
      pid = self._split_args(line, 1, 0)
      self.d1.set_replication_policy(pid)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_ping(self, line):
    ''' _ping [host|url [host|url] ...]
    Check if the remote host or URL is up and functioning as a DataONE node.
    '''
    try:
      hosts = cli_util.clear_None_from_list(self._split_args(line, 0, 99))
      self.d1.ping(hosts)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_package(self, line):
    ''' package <subcommand> [args]
          See "package help" for available subcommands.
    '''
    try:
      # Get out of package mode?
      argv = self._split_args(line, 0, 99)
      query = ' '.join(filter(None, argv))
      if query == '':
        self.prefix = 'package '
        self.prompt = '[package] > '
        self.keep_looping = True
        return
      elif ((query == 'exit') or (query == 'quit') or (query == 'leave')):
        self.prefix = DEFAULT_PREFIX
        self.prompt = DEFAULT_PROMPT
        return
      elif query == 'EOF':
        print ''
        self.prefix = DEFAULT_PREFIX
        self.prompt = DEFAULT_PROMPT
        return

      if self.packageCLI is None:
        self.packageCLI = package_cli.PackageCLI(self.d1.session)

      self.packageCLI.onecmd(line)

    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  #-----------------------------------------------------------------------------
  # CLI
  #-----------------------------------------------------------------------------

  def do_history(self, line):
    '''history
    Display a list_objects of commands that have been entered
    '''
    try:
      self._split_args(line, 0, 0)
      for idx, item in enumerate(self._history):
        print_info('{0: 3d} {1}'.format(idx, item))
    except cli_exceptions.InvalidArguments as e:
      print_error(e)
    except:
      cli_util._handle_unexpected_exception()

  def do_exit(self, line):
    '''exit
    Exit from the CLI
    '''
    try:
      # Check if there is a package, and if so, whether it needs to be saved.
      save_package = False
      if self.packageCLI is not None:
        if self.packageCLI.package is not None:
          if self.packageCLI.package.is_dirty():
            save_package = True
      # Save the pacakge
      if save_package:
        if self.interactive:
          if cli_util.confirm('\nThe package needs to be saved.  Exit anyway?'):
            sys.exit()
          self.packageCLI.package.save(self.d1.session)

      # Say goodnight, Gracie.
      sys.exit()
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_quit(self, line):
    '''quit
    Exit from the CLI
    '''
    self.do_exit(line)

  def do_EOF(self, line):
    '''Exit on system EOF character'''
    print ''
    return self.do_exit(line)

  def do_help(self, line):
    '''Get help on commands
    'help' or '?' with no arguments displays a list_objects of commands for which help is available
    'help <command>' or '? <command>' gives help on <command>
    '''
    # The only reason to define this method is for the help text in the doc
    # string
    cmd.Cmd.do_help(self, line)

  def _show_special_parameter(self, param_list):
    ''' Check to see if this a "special" parameter.
    '''
    if ((param_list is None) or (len(param_list) == 0)):
      return False
    #
    elif param_list[0] == 'formats':
      print_info(
        'Known formats:\n  ' + '\n  '.join(sorted(self.d1.get_known_object_formats()))
      )
      return True
    #
    elif param_list[0] == 'package':
      pid = ''
      if len(param_list) > 1:
        pid = ' ' + param_list[1]
      self.do_package('show' + pid)
      return True
    #
    return False

  #-----------------------------------------------------------------------------
  # Command processing.
  #-----------------------------------------------------------------------------

  ## Override methods in Cmd object ##
  def preloop(self):
    '''Initialization before prompting user for commands.
       Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
    '''
    # Set up command completion.
    cmd.Cmd.preloop(self)
    self._history = []

  def postloop(self):
    '''Take care of any unfinished business.
       Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
    '''
    cmd.Cmd.postloop(self) ## Clean up command completion
    print_info('Exiting...')

  def precmd(self, line):
    ''' This method is called after the line has been input but before
      it has been interpreted. If you want to modify the input line
      before execution (for example, variable substitution) do it here.
    '''
    line = self.prefix + line
    self._history += [line.strip()]
    return line

  def postcmd(self, stop, line):
    '''If you want to stop the console, return something that evaluates to true.
       If you want to do some post command processing, do it here.
    '''
    self._update_verbose()
    self.d1._set_invalid_checksum_to_default()
    return stop

  def emptyline(self):
    '''Do nothing on empty input line'''
    pass

  def default(self, line):
    '''Called on an input line when the command prefix is not recognized.
    '''
    queryArgs = self._split_args(line, 0, 99)
    if len(queryArgs) > 0:
      lowerCase = queryArgs[0].lower()
      if lowerCase.find('sh') == 0:
        self.do_show(' '.join(filter(None, queryArgs[1:])))
      elif lowerCase.find('pkg') == 0:
        self.do_package(' '.join(filter(None, queryArgs[1:])))
      else:
        print_error('Unknown command: "%s"' % queryArgs[0])

  def run_command_line_arguments(self, commands):
    for command in commands:
      self.onecmd(command)
      self._update_verbose()
      self.d1._set_invalid_checksum_to_default()


def initial_configuration(session):
  ''' Perform initial configuration. '''


def main():
  log_setup()

  parser = optparse.OptionParser(
    usage='usage: %prog [command] ...',
    option_list=option_list
  )
  options, remainder = parser.parse_args()

  cli = CLI()
  cli._update_verbose()
  handle_options(cli, options)

  # Start the command line interpreter loop, or just do one command?
  if (((options.interactive is not None) and options.interactive)
      or (len(remainder) == 0)):
    cli.interactive = True
    try:
      if len(remainder) != 0:
        cli.onecmd(join(remainder))
        print ''
      cli.cmdloop()
    except KeyboardInterrupt as e:
      cli.do_exit('')

  else:
    cli.interactive = False
    cli.onecmd(join(remainder))
    #
    if cli.keep_looping:
      cli.keep_looping = False
      try:
        cli.cmdloop()
      except KeyboardInterrupt as e:
        print ''
        cli.do_exit('')


if __name__ == '__main__':
  main()
