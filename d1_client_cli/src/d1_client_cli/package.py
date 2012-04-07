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
:mod:`package`
==============

:Synopsis: Create a data package
:Created: 2012-03-13
:Author: DataONE (Pippin)
'''

# Stdlib.
import cmd
import sys
import shlex
import string
import urlparse
import StringIO

# 3rd party
from rdflib import Namespace, URIRef
try:
  import foresite
  import foresite.utils
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    '  available at: https://foresite-toolkit.googlecode.com/svn/foresite-python/trunk\n'
  )
  raise

# DataONE
# common
try:
  import d1_common.util as util
  import d1_common.types.exceptions
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Please install d1_common.\n')
  raise

# cli
from print_level import * #@UnusedWildImport
import cli_client
import cli_exceptions
import cli_util
from const import VERBOSE_sect, VERBOSE_name #@UnusedImport
import data_package
import system_metadata

## -- Constants.

GET_ENDPOINT = 'object'
META_ENDPOINT = 'meta'
RDFXML_FORMATID = 'http://www.w3.org/TR/rdf-syntax-grammar'

#-- Package CLI ----------------------------------------------------------------


class PackageCLI(cmd.Cmd):
  ''' Inner cli.
  '''

  def __init__(self, session):
    cmd.Cmd.__init__(self)
    self.session = session
    self.package = None
    self.doc_header = 'Documented "package" commands (type package help <topic>):'
    self.nohelp = '*** No "package" help on %s'

  # From dataone.py:CLI
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

  ## Override methods in Cmd object ##
  def preloop(self):
    '''Initialization before prompting user for commands.
       Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
    '''
    # Set up command completion.
    cmd.Cmd.preloop(self)

  def postloop(self):
    '''Take care of any unfinished business.
       Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
    '''
    cmd.Cmd.postloop(self) ## Clean up command completion
#    print_info('Exiting...')

  def precmd(self, line):
    ''' This method is called after the line has been input but before
      it has been interpreted. If you want to modify the input line
      before execution (for example, variable substitution) do it here.
    '''
    return line

  def postcmd(self, stop, line):
    '''If you want to stop the console, return something that evaluates to true.
       If you want to do some post command processing, do it here.
    '''
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
      if lowerCase.find('desc') == 0:
        self.do_describe(' '.join(filter(None, queryArgs[1:])))
      elif lowerCase.find('meta') == 0:
        self.do_scimeta(' '.join(filter(None, queryArgs[1:])))
      elif lowerCase.find('data') == 0:
        self.do_scidata(' '.join(filter(None, queryArgs[1:])))
      elif lowerCase.find('add') == 0:
        self._add(queryArgs[1:])
      else:
        print_error('Unknown "package" command: "%s"' % queryArgs[0])

  def _add(self, args):
    ''' Transpose the scimeta and scidata command "add".
    
    args: (sub_cmd, pid, file_name)
    '''
    if self.package is None:
      raise cli_exceptions.InvalidArguments('There is no package.')

    args_len = len(args)
    pid = ''
    path = ''
    if args_len > 1:
      pid = ' ' + args[1]
    if args_len > 2:
      path = ' ' + args[2]

    if args_len == 0:
      print_error("Add to what?")
    elif ((cmd == 'scimeta') or (cmd == 'meta')):
      self.do_scimeta('add ' + pid + path)
    elif ((cmd == 'scidata') or (cmd == 'data')):
      self.do_scidata('add ' + pid + path)
    else:
      print_error('Use "scimeta add" or "scidata add".')

  def do_help(self, line):
    '''Get help on commands
    'help' or '?' with no arguments displays a list_objects of commands for which help is available
    'help <command>' or '? <command>' gives help on <command>
    '''
    # The only reason to define this method is for the help text in the doc
    # string
    cmd.Cmd.do_help(self, line)

  ##== Commands =============================================================

  def do_create(self, line):
    ''' create <pid> [scimeta [scidata [...]]]
        Create a package.
    '''
    # Check to see if we already have a package and it needs saving.
    if self.package is not None:
      if not self.package.is_dirty():
        self.package = None
      elif cli_util.confirm('Package needs to be saved.  Continue?'):
        self.package = None
      else:
        return

    # Get the pid from the arguments.
    values = cli_util.clear_None_from_list(self._split_args(line, 0, 9))
    pid = None
    if len(values) > 0:
      pid = values[0]

      # See if such an object already exists, if so see if the user wants to continue.
      mn_client = cli_client.CLICNClient(self.session)
      object_location_list = None
      try:
        object_location_list = mn_client.resolve(pid)
      except d1_common.types.exceptions.DataONEException as e:
        if e.errorCode != 404:
          raise cli_exceptions.CLIError(
            'Unable to get resolve: {0}\n{1}'.format(pid, e.friendly_format())
          )
      except:
        exc_type, exc_msgs = sys.exc_info()[:2] # ignore the traceback. @UnusedVariable
        if exc_type.__name__ != 'NotFound': # The dang thing throws an exeption on a 404.
          cli_util._handle_unexpected_exception()
      # Now see if there was something.
      if ((object_location_list is not None)
          and (len(object_location_list.objectLocation) > 0)):
        if not cli_util.confirm(
          'An object already exists under "%s".  Are you sure you want to create one?' %
          pid
        ):
          return

      # Create the package object (finally!).
    if self.session.is_pretty() and len(values) > 0:
      print('Creating package "%s"' % pid)
    self.package = data_package.DataPackage(pid)

    # Add an existing scimeta item.
    if len(values) > 1:
      self.package.scimeta_add(self.session, values[1], None)

    # Add exiting scidata items.
    if len(values) > 2:
      for scidata_pid in cli_util.clear_None_from_list(values[2:]):
        self.package.scidata_add(self.session, scidata_pid, None)

  def do_delete(self, line):
    ''' Delete the package.
    '''
    if ((self.package is not None)
        and self.package.is_dirty()
        and cli_util.confirm('Do you really want to delete the package?')):
      self.package = None

  def do_name(self, line):
    ''' name <pid>
        Name the package (assign a (possibly new) pid).
    '''
    if self.package is None:
      raise cli_exceptions.InvalidArguments('There is no package to rename.')

    pid = self._split_args(line, 0, 1)
    self.package.name(pid)

  def do_show(self, line):
    ''' show [scimeta] [scidata [pid]]
        Display the contents of the package, the science metadata object or
        a science data object in the package
    '''
    sub_cmd, pid = self._split_args(line, 0, 2)
    pretty = self.session.is_pretty()
    verbose = self.session.is_verbose()
    if not sub_cmd:
      if self.package is None:
        print_info('There is no package to show.')
      else:
        self.package.show(pretty, verbose)
    elif sub_cmd == 'scimeta' or sub_cmd == 'meta':
      self.package.scimeta_showobj(pretty, verbose)
    elif sub_cmd == 'scidata' or sub_cmd == 'data':
      self.package.scidata_showobj(pid, pretty, verbose)
    else:
      print_error('Don\'t know how to show a "%s".' % sub_cmd)

  def do_describe(self, line):
    ''' desc [scimeta] [scidata [pid]]
    
        Describe the contents of the package, the science metadata object or
        a science data object in the package
    '''
    sub_cmd, pid = self._split_args(line, 0, 2)
    pretty = self.session.is_pretty()
    verbose = self.session.is_verbose()
    if not sub_cmd:
      if self.package is None:
        print_info('There is no package to describe.')
      else:
        self.package.describe(pretty, verbose)
    elif sub_cmd == 'scimeta' or sub_cmd == 'meta':
      self.package.scimeta_describe(pretty, verbose)
    elif sub_cmd == 'scidata' or sub_cmd == 'data':
      self.package.scidata_describe(pid, pretty, verbose)
    else:
      print_error('Don\'t know how to describe a "%s".' % sub_cmd)

  def do_load(self, line):
    ''' load [pid]
        Load a package.  If no pid is given, use the current pid.
    '''
    pid = self._split_args(line, 0, 1)
    if pid is not None:
      load_pid = pid
    elif ((self.package is not None) and (self.package.pid is not None)):
      load_pid = self.package.pid
    else:
      raise cli_exceptions.InvalidArguments('No package specified to load.')
    #
    # Create the package object
    new_package = data_package.DataPackage(load_pid)
    if new_package is not None:
      self.package = new_package
      self.package.load()

  def do_save(self, line):
    ''' save
        Save the package.  If a pid is given, rename the current
          package to the given pid, and save the pacakge as the
          new pid.
    '''
    if self.package is None:
      raise cli_exceptions.InvalidArguments('There is no package to save.')
    elif self.package.pid is None:
      raise cli_exceptions.InvalidArguments('The current package has no pid.')
    self.package.save(self.session)

  def do_scimeta(self, line):
    ''' scimeta [add | del | show | meta ] [options]
          add    pid [file]  Assign the science meta object
          del    Remove the science meta object from the package.
          show   Display the current science meta object.
          meta   Display the system meta data for the science meta object.
          desc   Describe the current science meta object.
    '''
    if self.package is None:
      raise cli_exceptions.InvalidArguments('There is no package.')
    sub_cmd, pid, file_name = self._split_args(line, 1, 2)
    if sub_cmd is None:
      msg = 'What do you wish to do to the science metadata object?.\n  (add, del, show, meta)'
      raise cli_exceptions.InvalidArguments(msg)
    #
    if string.find('add', sub_cmd) == 0:
      self.package.scimeta_add(self.session, pid, file_name)
    elif string.find('del', sub_cmd) == 0:
      self.package.scimeta_del()
    elif string.find('show', sub_cmd) == 0:
      self.package.scimeta_showobj(self.session)
    elif string.find('meta', sub_cmd) == 0:
      self.package.scimeta_showmeta(self.session)
    else:
      raise cli_exceptions.InvalidArguments('Unknown scimeta sub-command: %s' % sub_cmd)

  def do_scidata(self, line):
    ''' scidata [add | del | show | meta ] <pid>
          add    <pid>  [file]  Add the science object to the package.
          del    <pid>  Remove the given science object from the package.
          clear  Remove all science data objects from the package.
          show   <pid>  Display the given science object.
          meta   <pid>  Display the system meta data for the given science object.
          desc   <pid>  Describe the given science object.
    '''
    if self.package is None:
      raise cli_exceptions.InvalidArguments('There is no package.')
    sub_cmd, pid, opt = self._split_args(line, 2, 1)
    if sub_cmd is None:
      msg = 'What do you wish to do to the science data object?.\n  (add, del, clear, show, meta)'
      raise cli_exceptions.InvalidArguments(msg)
    #
    if string.find('add', sub_cmd, ) == 0:
      self.package.scidata_add(self.session, pid, opt)
    elif string.find('del', sub_cmd) == 0:
      self.package.scidata_del(pid)
    elif string.find('clear', sub_cmd) == 0:
      self.package.scidata_clear()
    elif string.find('desc', sub_cmd) == 0:
      self.package.scidata_desc(self.session, pid)
    elif string.find('show', sub_cmd) == 0:
      self.package.scidata_showobj(self.session, pid)
    elif string.find('meta', sub_cmd) == 0:
      self.package.scidata_showmeta(self.session, pid)
    else:
      raise cli_exceptions.InvalidArguments('Unknown scidata sub-command: %s' % sub_cmd)

# Shouldn't be called - handled in do_package.

  def do_quit(self, line):
    ''' Exit package mode.
    '''
    return

# Shouldn't be called - handled in do_package.

  def do_exit(self, line):
    ''' Exit package mode.
    '''
    return

#-----------------------------------------------------------------------------
# Command processing.
#-----------------------------------------------------------------------------

#-- Public (static) interface --------------------------------------------------


def action(dataONECLI, queryArgs):
  '''
  '''
  #  Create a new package.
  if queryArgs[0] == 'create':
    print 'burp'

  # Load either a new package, or reload the same package.
  elif queryArgs[0] == 'load':
    if len(queryArgs) == 1:
      if dataONECLI.package.pid is None:
        raise cli_exceptions.InvalidArguments('Load which pid?')
      else:
        new_pkg = data_package.find(dataONECLI.package.pid)
        if new_pkg is not None:
          dataONECLI.package = new_pkg
    else:
      new_pkg = data_package.find(queryArgs[1])
      if new_pkg is not None:
        dataONECLI.package = new_pkg
      else:
        print_warn('%s: no such package' % queryArgs[1])

  # Save the package out to DataONE.
  elif queryArgs[0] == 'save':
    if len(queryArgs) == 1:
      if dataONECLI.package.pid is None:
        raise cli_exceptions.InvalidArguments('Save as what pid?')
      else:
        dataONECLI.package.save()
    else:
      dataONECLI.package.pid = queryArgs[1]
      dataONECLI.package.save()

    # Add, remove, or show the science metadata object.
  elif queryArgs[0] == 'scimeta':
    if len(queryArgs) == 1:
      msg = 'What action with the scimeta?  (add, del, show, meta)'
      raise cli_exceptions.InvalidArguments('What action with the scimeta?')
    elif queryArgs[1] == 'add':
      if len(queryArgs) == 2:
        raise cli_exceptions.InvalidArguments('Add what object as scimeta?')
      else:
        dataONECLI.package.add_scimeta(dataONECLI.session, queryArgs[2])
    elif queryArgs[1] == 'del':
      dataONECLI.package.del_scimeta()
    elif queryArgs[1] == 'show':
      dataONECLI.object_print(dataONECLI.package.scimeta)
    elif queryArgs[1] == 'meta':
      dataONECLI.system_metadata_print(dataONECLI.package.scimeta_sysmeta)
    else:
      dataONECLI.package.add_scimeta(queryArgs[1])

    # Add, remove, or show the science data object.
  elif queryArgs[0] == 'scidata':
    if len(queryArgs) == 1:
      msg = 'What action with the scidata?  (add, del, show, meta)'
      raise cli_exceptions.InvalidArguments(msg)
    elif queryArgs[1] == 'add':
      if len(queryArgs) <= 2:
        raise cli_exceptions.InvalidArguments('Add what object(s) as scidata?')
      else:
        dataONECLI.package.add_data(queryArgs[2:])
    elif queryArgs[1] == 'del':
      dataONECLI.package.del_meta(queryArgs[2:])
    elif queryArgs[1] == 'show':
      if len(queryArgs) <= 2:
        raise cli_exceptions.InvalidArguments('Show which scidata object?')
      elif queryArgs[2] not in dataONECLI.package.scidata:
        raise cli_exceptions.InvalidArguments(': unknown scidata object')
      else:
        dataONECLI.object_print(dataONECLI.package.scidata[queryArgs[2]])
    elif queryArgs[1] == 'meta':
      if len(queryArgs) <= 2:
        raise cli_exceptions.InvalidArguments('Show sysmeta from which scidata object?')
      elif queryArgs[2] not in dataONECLI.package.scidata_sysmeta:
        raise cli_exceptions.InvalidArguments(': unknown scidata object')
      else:
        dataONECLI.system_metadata_print(dataONECLI.package.scidata_sysmeta[queryArgs[2]])

  else:
    msg = '%s: unknown sub-command' % queryArgs[0]
    raise cli_exceptions.InvalidArguments(msg)


def create(session, name, pids):
  ''' Do the heavy lifting of creating a package.
  '''
  # Create the resource map.
  submit = session.get('sysmeta', 'submitter')
  rights = session.get('sysmeta', 'rights-holder')
  orig_mn = session.get('sysmeta', 'origin-mn')
  auth_mn = session.get('sysmeta', 'authoritative-mn')
  pkg = Package(name, submit, rights, orig_mn, auth_mn)

  # Find all of the scimeta objects
  package_objects = []
  for pid in pids:
    get_scimeta_url = _resolve_scimeta_url(session, pid)
    if get_scimeta_url is None:
      print_error('Couldn\'t find any object with pid "%s"' % pid)
      return None
    else:
      scimeta_url = get_scimeta_url.replace(
        '/' + GET_ENDPOINT + '/', '/' + META_ENDPOINT + '/'
      )
      scimeta_obj = _get_scimeta_obj(session, get_scimeta_url)
      package_objects.append(
        {
          'scimeta_obj': scimeta_obj,
          'scimeta_url': scimeta_url,
          'scidata_pid': pid,
          'scidata_url': get_scimeta_url
        }
      )

  pkg.finalize(package_objects)
  return pkg


def save(session, pkg):
  ''' Save the package in DataONE.
  '''
  pkg_xml = pkg.serialize('xml')

  algorithm = session.get('sysmeta', 'algorithm')
  hash_fcn = util.get_checksum_calculator_by_dataone_designator(algorithm)
  hash_fcn.update(pkg_xml)
  checksum = hash_fcn.hexdigest()

  access_policy = session.access_control.to_pyxb()
  replication_policy = session.replication_policy.to_pyxb()
  sysmeta_creator = system_metadata.system_metadata()
  sysmeta = sysmeta_creator.create_pyxb_object(
    session,
    pkg.pid,
    len(
      pkg_xml
    ),
    checksum,
    access_policy,
    replication_policy,
    formatId=RDFXML_FORMATID
  )

  client = cli_client.CLIMNClient(session)
  flo = StringIO.StringIO(pkg_xml)
  response = client.create(pid=pkg.pid, obj=flo, sysmeta=sysmeta)
  if response is not None:
    return response.value()
  else:
    return None


def get_host(url):
  '''Get the host component without the port number.
  '''
  url_dict = urlparse.urlparse(url)
  if url_dict.netloc is not None:
    host = url_dict.netloc
    ndx = host.find(":")
    if ndx > 0:
      host = host[:ndx]
    return host

#-- Public class ---------------------------------------------------------------


class Package(object):
  def __init__(
    self,
    pid,
    submitter=None,
    rights_holder=None,
    orig_mn=None,
    auth_mn=None,
    scimeta_pid=None
  ):
    ''' Create a package
    '''
    self.resmap = None
    #
    self.pid = pid
    self.submitter = submitter
    self.rights_holder = rights_holder
    self.orig_mn = orig_mn
    self.auth_mn = auth_mn
    if scimeta_pid is not None:
      self.add(scimeta_pid)

  def serialize(self, fmt='xml'):
    assert (
      fmt in (
        'xml', 'pretty-xml', 'n3', 'rdfa', 'json', 'pretty-json', 'turtle', 'nt', 'trix'
      )
    )
    if self.resmap.serializer is not None:
      self.resmap.serializer = None
    serializer = foresite.RdfLibSerializer(fmt)
    self.resmap.register_serialization(serializer)
    doc = self.resmap.get_serialization()
    return doc.data

  def finalize(self, package_objects):
    ''' Create the resource map.
    '''
    for package_object in package_objects:
      sysmeta_obj = package_object['scimeta_obj']
      if self._is_metadata_format(sysmeta_obj.formatId):
        self._add_inner_package_objects(package_objects, sysmeta_obj)

    return self._generate_resmap(package_objects)

  def _add_inner_package_objects(self, package_objects, sysmeta_obj):
    ''' The given sysmeta object actually defines a data package.  Process the
        package and add all of the thingsd specified to the package_object_list.
    '''
    print_info('+ Using metadata to add to an existing package')
    print_error('package._add_inner_package_objects() is not implemented!!!')

  def _generate_resmap(self, package_object_list):
    ''' The scimeta is part of a package.  Create a package.
    
        An example package_object item looks like:
                {
                  'scimeta_obj': <d1_common.types.generated.dataoneTypes.SystemMetadata>,
                  'scimeta_url': 'https://demo1.test.dataone.org:443/knb/d1/mn/v1/meta/test-object'
                  'scidata_pid':pid,
                  'scidata_url':get_scimeta_url
                }
    '''
    # Create the aggregation
    foresite.utils.namespaces['cito'] = Namespace("http://purl.org/spar/cito/")
    aggr = foresite.Aggregation(self.pid)
    aggr._dcterms.title = 'Simple aggregation of science metadata and data.'

    # Create references to the science data
    for item in package_object_list:
      # Create a reference to the science metadata
      scimeta_obj = item['scimeta_obj']
      scimeta_pid = scimeta_obj.identifier.value()
      uri_scimeta = URIRef(item['scimeta_url'])
      res_scimeta = foresite.AggregatedResource(uri_scimeta)
      res_scimeta._dcterms.identifier = scimeta_pid
      res_scimeta._dcterms.description = 'A reference to a science metadata object using a DataONE identifier'

      uri_scidata = URIRef(item['scidata_url'])
      res_scidata = foresite.AggregatedResource(uri_scidata)
      res_scidata._dcterms.identifier = item['scidata_pid']
      res_scidata._dcterms.description = 'A reference to a science data object using a DataONE identifier'
      res_scidata._cito.isDocumentedBy = uri_scimeta
      res_scimeta._cito.documents = uri_scidata

      aggr.add_resource(res_scimeta)
      aggr.add_resource(res_scidata)

    # Create the resource map
    resmap_id = "resmap_%s" % self.pid
    self.resmap = foresite.ResourceMap("https://cn.dataone.org/object/%s" % resmap_id)
    self.resmap._dcterms.identifier = resmap_id
    self.resmap.set_aggregation(aggr)
    return self.resmap

  def _is_metadata_format(self, formatId):
    ''' Check to see if this formatId specifies a resource map.
    '''
    if formatId is None:
      return False
    elif ((len(formatId) >= 4) and (formatId[:4] == "eml:")):
      return True
    elif ((len(formatId) >= 9) and (formatId[:9] == "FGDC-STD-")):
      return True
    else:
      return False

#-- Private methods ------------------------------------------------------------


def _verbose(session):
  ''' Are we verbose?
  '''
  verbosity = session.get('cli', 'verbose')
  if verbosity is not None:
    return verbosity
  else:
    return False


def _resolve_scimeta_url(session, pid):
  ''' Get a URL on a member node of the pid.
  '''
  cnclient = cli_client.CLICNClient(session)
  try:
    locations = cnclient.resolve(pid)
    if locations is not None:
      for location in locations.objectLocation:
        return location.url # Just get one.
  except:
    exc_class = sys.exc_info()[:1]
    if exc_class.__name__ == 'NotFound':
      print_warn(' no such pid: %s' % pid)
    cli_util._handle_unexpected_exception()
    return None


def _get_scimeta_obj(session, obj_url):
  ''' Get the actual science metadata object of the url.
  '''
  mn = session.get('node', 'mn-url')
  mn_dict = urlparse.urlparse(mn)
  obj_dict = urlparse.urlparse(obj_url)
  #
  try:
    base = mn_dict.scheme + '://' + obj_dict.netloc + mn_dict.path
    ndx = obj_dict.path.find(GET_ENDPOINT)
    pid = obj_dict.path[(ndx + len(GET_ENDPOINT) + 1):]
    client = cli_client.CLIMNClient(session, base)
    return client.getSystemMetadata(pid)
  except:
    cli_util._handle_unexpected_exception()
    return None
