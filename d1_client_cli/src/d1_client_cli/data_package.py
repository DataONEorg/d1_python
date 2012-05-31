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
:mod:`data_package`
===================

:Synopsis: Wrapper around a data package
:Created: 2012-03-29
:Author: DataONE (Pippin)
'''

# Stdlib.
import os
import sys
import StringIO
from xml.dom.minidom import parse, parseString #@UnusedImport

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
  from d1_common.types.exceptions import DataONEException
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Please install d1_common.\n')
  raise

# cli
import cli_client
import cli_exceptions
import cli_util
from const import * #@UnusedWildImport
import system_metadata
from print_level import * #@UnusedWildImport

ALLOWABLE_PACKAGE_SERIALIZATIONS = (
  'xml', 'pretty-xml', 'n3', 'rdfa', 'json', 'pretty-json', 'turtle', 'nt', 'trix'
)
RDFXML_FORMATID = 'http://www.openarchives.org/ore/terms'

RDF_NS = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
CITO_NS = 'http://purl.org/spar/cito/'

#** DataPackage ***************************************************************


class DataPackage(object):
  def __init__(self, pid=None):
    ''' Create a package
    '''
    self.pid = pid
    #
    # Objects in here a dicts with keywords pid, dirty, obj, meta; which are
    # string, boolean, blob, and pyxb objects respectively.
    self.original_pid = None
    self.sysmeta = None
    self.scimeta = None
    self.scidata_dict = {}
    self.resmap = None

  #== Informational =========================================================

  def is_dirty(self):
    ''' Check to see if anything needs to be saved.
    '''
    if self.pid != self.original_pid:
      return True
    if self.scimeta is not None:
      if (self.scimeta.dirty) and self.scimeta.dirty:
        return True
    if self.scidata_dict is not None:
      for item in self.scidata_dict.values():
        if (item.dirty is not None) and item.dirty:
          return True
    return False

  #== Manipulation ==========================================================

  def name(self, pid):
    ''' Rename the package
    '''
    if pid is None:
      if cli_util.confirm('Do you really want to clear the name of the package?'):
        self.pid = None
      else:
        raise cli_exceptions.InvalidArguments('Missing the new pid')
    else:
      if self.pid is not None:
        print_info('Package name is cleared.')
      self.pid = pid

  def load(self, session):
    ''' Get the object referred to by pid and make sure it is a
        package.
    '''
    if self.pid is None:
      raise cli_exceptions.InvalidArguments('Missing pid')
    if session is None:
      raise cli_exceptions.InvalidArguments('Missing session')
    sysmeta = cli_client.get_sysmeta_by_pid(session, self.pid)
    if not sysmeta:
      print_error('Couldn\'t find "%s" in DataONE.' % self.pid)
      return None
    if sysmeta.formatId != RDFXML_FORMATID:
      print_error('Package must be in RDF/XML format (not "%s").' % sysmeta.formatId)
      return None

    rdf_xml_file = cli_client.get_object_by_pid(session, self.pid)
    if not self._parse_rdf_xml(rdf_xml_file):
      print_error('Unable to load package "%s".' % self.pid)
      return None

    self.original_pid = self.pid
    self.sysmeta = sysmeta
    if session.is_pretty():
      print_error("Loaded %s" % self.pid)
    return self

  def _parse_rdf_xml(self, xml_file):
    doc = parse(xml_file)
    #    print 'doc:\n', doc.toxml()
    self.scimeta = None
    self.scidata_dict = {}
    for desc in doc.getElementsByTagNameNS(RDF_NS, 'Description'):
      if desc.getElementsByTagNameNS(CITO_NS, 'documents'):
        if self.scimeta:
          msg = 'Already have Science Metadata Object: "%s"' % self.scimeta.url
          print_error(msg)
          self.scimeta = None
          self.scidata_dict = {}
          return False
        else:
          self.scimeta = DataObject()
          self.scimeta.from_url(desc.getAttributeNS(RDF_NS, 'about'))
          if not self.scimeta.pid:
            print_warn('Couldn\'t find pid in %s' % self.scimeta.url)
      else:
        documentedBy = desc.getElementsByTagNameNS(CITO_NS, 'isDocumentedBy')
        if documentedBy:
          scidata = DataObject()
          about_url = desc.getAttributeNS(RDF_NS, 'about')
          scidata.from_url(about_url)
          if not scidata.pid:
            msg = 'Couldn\'t find pid in "%s"' % about_url
            print_error(msg)
            self.scimeta = None
            self.scidata_dict = {}
            return False
          else:
            if len(documentedBy) > 1:
              print_warn('There are several science metadata objects - using the first')
            e = documentedBy[0]
            scidata.documented_by = e.getAttributeNS(RDF_NS, 'resource')
            self.scidata_dict[scidata.pid] = scidata
    return True

  def save(self, session):
    ''' Save this object referred to by this pid.
    '''
    if self.pid is None:
      raise cli_exceptions.InvalidArguments('Missing pid')

    pkg_xml = self._serialize(session, 'xml')

    algorithm = session.get(CHECKSUM_sect, CHECKSUM_name)
    hash_fcn = util.get_checksum_calculator_by_dataone_designator(algorithm)
    hash_fcn.update(pkg_xml)
    checksum = hash_fcn.hexdigest()

    access_policy = session.access_control.to_pyxb()
    replication_policy = session.replication_policy.to_pyxb()
    sysmeta_creator = system_metadata.system_metadata()
    sysmeta = sysmeta_creator.create_pyxb_object(
      session,
      self.pid,
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

    # Save all the objects.
    if self.scimeta and self.scimeta.dirty:
      self._create_or_update(self.scimeta)
    for scidata_pid in self.scidata_dict.keys():
      scidata = self.scidata.get(scidata_pid)
      if scidata and scidata.dirty:
        self._create_or_update(scidata)

    response = client.create(pid=self.pid, obj=flo, sysmeta=sysmeta)
    if response is None:
      return None
    else:
      self.original_pid = self.pid
      if self.scimeta:
        self.scimeta.dirty = False
      if self.scidata_dict:
        for scidata in self.scidata_dict.values():
          scidata.dirty = False
      if session.is_pretty():
        print_info('Saved "%s"' % self.pid)
      return response.value()

  def _create_or_update(self, client, data_object):
    ''' Either update the specified pid if it already exists or create a new one.
    '''
    if not data_object:
      raise cli_exceptions.InvalidArguments('data object cannot be null')
    if not data_object.pid:
      raise cli_exceptions.InvalidArguments('data object must have a pid')
    if not data_object.fname:
      raise cli_exceptions.InvalidArguments('data object must have a file to write')
    if not data_object.meta:
      raise cli_exceptions.InvalidArguments('data object must have system metadata')
    curr_sysmeta = client.getSystemMetadata(data_object.pid)
    # Create
    if not curr_sysmeta:
      with open(cli_util.expand_path(data_object.fname), 'r') as f:
        try:
          return client.create(data_object.pid, f, data_object.meta)
        except DataONEException as e:
          print_error(
            'Unable to create Science Object on Member Node\n{0}'
            .format(e.friendly_format())
          )
    # Update
    else:
      data_object.meta.serialVersion = (curr_sysmeta.serialVersion + 1)
      with open(cli_util.expand_path(data_object.fname), 'r') as f:
        try:
          return client.update(data_object.pid, f, data_object.pid, data_object.meta)
        except DataONEException as e:
          print_error(
            'Unable to update Science Object on Member Node\n{0}'
            .format(e.friendly_format())
          )
    # Nothing good happened.
    return None

  def scimeta_add(self, session, pid, file_name=None):
    ''' Add a scimeta object.
    '''
    if not session:
      raise cli_exceptions.InvalidArguments('Missing the session')
    if not pid:
      raise cli_exceptions.InvalidArguments('Missing the pid')
    if (self.scimeta and not
       cli_util.confirm('Do you wish to delete the existing science metadata object?')):
      return
    else:
      self.scimeta = None

    if session.is_pretty():
      sys.stdout.write('  Adding science metadata object "%s"...' % pid)

    if not file_name:
      new_meta = cli_client.get_sysmeta_by_pid(session, pid, True)
      if not new_meta:
        if session.is_pretty():
          sys.stdout.write('. [error]\n')
        print_error('Couldn\'t find scimeta in DataONE, and there was no file specified.')
        return
      if not self._is_metadata_format(new_meta.formatId):
        if session.is_pretty():
          sys.stdout.write('. [error]\n')
        print_error('"%s" is not an allowable science metadata type.' % new_meta.formatId)
        return
      new_pid = new_meta.identifier.value()
      if new_pid != pid:
        pid = new_pid

      self.scimeta = self._get_by_pid(session, pid, new_meta)
      authMN = new_meta.authoritativeMemberNode
      if authMN:
        baseURL = cli_client.get_baseUrl(session, authMN.value())
        if baseURL:
          self.scimeta.url = cli_client.create_get_url_for_pid(baseURL, pid)
      if session.is_pretty():
        print '. [retrieved]'

    else:
      complex_path = cli_util.create_complex_path(file_name)
      if not os.path.exists(complex_path.path):
        print_error('%s: file not found' % complex_path.path)
        return
      format_id = complex_path.formatId
      if not format_id:
        format_id = session.get(FORMAT_sect, FORMAT_name)
      if not format_id:
        if session.is_pretty():
          sys.stdout.write('. [error]\n')
        print_error('The object format could not be determined and was not defined.')
        return
      if not self._is_metadata_format(format_id):
        if session.is_pretty():
          sys.stdout.write('. [error]\n')
        print_error('"%s" is not an allowable science metadata type.' % new_meta.formatId)
        return
      #
      sysmeta = cli_util.create_sysmeta(
        session, pid, complex_path.path,
        formatId=format_id
      )
      self.scimeta = DataObject(pid, True, complex_path.path, None, sysmeta, format_id)
      if session.is_pretty():
        print '. [created]\n'
    scidata_list = self._find_scidata(self.scimeta)
    if scidata_list:
      for scidata in scidata_list:
        self.scidata_add(session, scidata.pid, scidata.fname)

  def scimeta_del(self):
    ''' Remove the science metadata object.
    '''
    if cli_util.confirm('Are you sure you want to remove the science meta object?'):
      self.scimeta = None

  def scidata_add(self, session, pid, file_name=None):
    ''' Add a science data object to the list.
    '''
    if not session:
      print_error('Missing the session')
      return
    if not pid:
      print_error('Missing the pid')
      return

    if file_name:
      if session.is_pretty():
        sys.stdout.write('  Adding science data object "%s"...' % pid)
      if cli_client.get_sysmeta_by_pid(session, pid):
        if not cli_util.confirm(
          'That pid (%s) already exists in DataONE.  Continue?' % pid
        ):
          return

      complex_path = cli_util.create_complex_path(file_name)
      format_id = complex_path.formatId
      if not format_id:
        format_id = session.get(FORMAT_sect, FORMAT_name)
      if not format_id:
        if session.is_pretty():
          print '. [error]'
        print_error('The object format could not be determined and was not defined.')
        return
      else:
        meta = cli_util.create_sysmeta(
          session, pid, complex_path.path,
          formatId=format_id
        )
        self.scidata_dict[pid] = DataObject(
          pid, True, complex_path.path, None, meta, format_id
        )
        if session.is_pretty():
          print '. [created]'

    else:
      sysmeta = cli_client.get_sysmeta_by_pid(session, pid, True)
      if not sysmeta:
        print_error('That pid (%s) was not found in DataONE.' % pid)
        return
      else:
        if session.is_pretty():
          sys.stdout.write('  Adding science data object "%s"...' % pid)
        pid = sysmeta.identifier.value()
        if pid in self.scidata_dict:
          if not cli_util.confirm(
            'That science data object (%s) is already in the package.  Replace?' % pid
          ):
            return
        # Get the scidata object.
        scidata = self._get_by_pid(session, pid, sysmeta)
        authMN = sysmeta.authoritativeMemberNode
        if authMN:
          baseURL = cli_client.get_baseUrl(session, authMN.value())
          if baseURL:
            scidata.url = cli_client.create_get_url_for_pid(baseURL, pid)
        self.scidata_dict[pid] = scidata
        if session.is_pretty():
          print '. [retrieved]'

  def scidata_get(self, pid):
    ''' Get the specified scidata object.
    '''
    if pid and pid in self.scidata_dict:
      return self.scidata_dict
    else:
      return None

  def scidata_del(self, pid):
    ''' Remove a science data object.
    '''
    if pid is None:
      raise cli_exceptions.InvalidArguments('Missing the pid')
    if pid in self.scidata_dict:
      if cli_util.confirm(
        'Are you sure you want to remove the science data object "%s"?' % pid
      ):
        del self.scidata_dict[pid]

  def scidata_clear(self):
    ''' Remove all science data objects
    '''
    if self.scidata_dict is None:
      self.scidata_dict = {}
    elif ((len(self.scidata_dict) > 0)
        and cli_util.confirm('Are you sure you want to remove all the science data objects?')):
      self.scidata_dict.clear()

    #== Helpers ===============================================================

  def _get_by_pid(self, session, pid, sysmeta=None):
    ''' Return (pid, dirty, fname, sysmeta)
    '''
    if session is None:
      raise cli_exceptions.InvalidArguments('Missing session')
    if pid is None:
      raise cli_exceptions.InvalidArguments('Missing pid')

    fname = cli_client.get_object_by_pid(session, pid, resolve=True)
    if fname is not None:
      meta = sysmeta
      if not meta:
        meta = cli_client.get_sysmeta_by_pid(session, pid)
      url = cli_client.create_get_url_for_pid(None, pid, session)
      return DataObject(pid, False, fname, url, meta, meta.formatId, None)
    else:
      return None

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

  def _generate_resmap(self, mn_client_base_url):
    ''' Create a package.
    '''
    # Create the aggregation
    foresite.utils.namespaces['cito'] = Namespace("http://purl.org/spar/cito/")
    aggr = foresite.Aggregation(self.pid)
    aggr._dcterms.title = 'Simple aggregation of science metadata and data.'

    # Create a reference to the science metadata
    uri_scimeta = URIRef(self.scimeta.url)
    res_scimeta = foresite.AggregatedResource(uri_scimeta)
    res_scimeta._dcterms.identifier = self.scimeta.pid
    res_scimeta._dcterms.description = 'Science metadata object.'

    # Create references to the science data
    resource_list = []
    for scidata in self.scidata_dict.values():
      uri_scidata = URIRef(scidata.url)
      res_scidata = foresite.AggregatedResource(uri_scidata)
      res_scidata._dcterms.identifier = scidata.pid
      res_scidata._dcterms.description = 'Science data object'
      res_scidata._cito.isDocumentedBy = uri_scimeta
      res_scimeta._cito.documents = uri_scidata
      resource_list.append(res_scidata)

      # Add all the resources.
    aggr.add_resource(res_scimeta)
    for resource in resource_list:
      aggr.add_resource(resource)

      # Create the resource map
    resmap_url = cli_client.create_get_url_for_pid(mn_client_base_url, format(self.pid))
    self.resmap = foresite.ResourceMap(resmap_url)
    self.resmap._dcterms.identifier = self.pid
    self.resmap.set_aggregation(aggr)
    return self.resmap

  def _serialize(self, session, fmt='xml'):
    assert (fmt in ALLOWABLE_PACKAGE_SERIALIZATIONS)
    if not self._prepare_urls(session):
      return
    mn_client = cli_client.CLIMNClient(session)
    self._generate_resmap(mn_client.base_url)
    if self.resmap.serializer is not None:
      self.resmap.serializer = None
    serializer = foresite.RdfLibSerializer(fmt)
    self.resmap.register_serialization(serializer)
    doc = self.resmap.get_serialization()
    return doc.data

  def _prepare_urls(self, session):
    ''' Walk through the objects make sure that everything can be
        serialized.
    '''
    if self.scimeta and not self.scimeta.url:
      if not self._check_item(self.scimeta):
        return False
      elif not self.scimeta.url:
        self.scimeta.url = cli_client.create_get_url_for_pid(
          None, self.scimeta.pid, session
        )
    if self.scidata_dict:
      for scidata in self.scidata_dict.values():
        if not self._check_item(scidata):
          return False
        elif not scidata.url:
          scidata.url = cli_client.create_get_url_for_pid(None, scidata.pid, session)
    return True

  def _check_item(self, item):
    errors = []
    if not self.scimeta.pid:
      errors.add('missing pid')
    if not self.scimeta.fname:
      errors.add('missing fname')
    if not self.scimeta.format_id:
      errors.add('missing format-id')
    if len(errors) == 0:
      return True
    else:
      msg = 'Cannot serialize the science object: '
      msg += ', '.join(errors)
      print_error(msg)
      return False

  def _create_object(self, session, item):
    ''' Create an object in DataONE. '''
    path = cli_util.expand_path(item.fname)
    cli_util.assert_file_exists(path)
    sysmeta = cli_util.create_sysmeta(session, item.pid, path, item.format_id)
    mn_client = cli_client.CLIMNClient(session)
    with open(path, 'r') as f:
      try:
        result = mn_client.create(item.pid, f, sysmeta)
        print_info('Created object "%s"' % item.pid)
        return result
      except DataONEException as e:
        print_error(
          'Unable to create Science Object on Member Node\n{0}'
          .format(e.friendly_format())
        )
        return None

  def _find_scidata(self, scimeta):
    '''  Search through an eml://ecoinformatics.org/eml-2.x.x document '''
    '''  looking for science data objects.                             '''
    '''                                                                '''
    '''               THIS IS GOING TO BE DIFFICULT!                   '''
    return ()


class DataObject(object):
  def __init__(
    self,
    pid=None,
    dirty=None,
    fname=None,
    url=None,
    meta=None,
    format_id=None,
    documented_by=None
  ):
    ''' Create a data object
    '''
    self.pid = pid
    self.dirty = dirty
    self.fname = fname
    self.url = url
    self.meta = meta
    self.format_id = format_id
    self.documented_by = documented_by

  def is_dirty(self):
    return (self.dirty is not None) and self.dirty

  def str(self): #@ReservedAssignment
    m = 'None'
    if self.meta is not None:
      m = '<...>'
    return 'DataObject[pid=%s,dirty=%s,fname=%s,meta=%s]' % (
      self.pid, str(
        self.dirty
      ), self.fname, m
    )

  def from_url(self, url):
    self.url = url
    ndx = url.find('/resolve/') + 8
    if ndx > 8:
      self.pid = url[ndx:]

  def summary(self, prefix, pretty, verbose):
    p = prefix
    if not prefix:
      p = '  '

    if (verbose is not None) and verbose:
      pass
    else:
      flags = ''
      pre = ' ('
      post = ''

      if (self.dirty is not None) and self.dirty:
        flags += pre + 'needs saving'
        pre = ', '
        post = ')'
      if self.fname is not None:
        flags += pre + 'has an object file'
        if verbose:
          flags += ' (%s)' % self.fname
        pre = ', '
        post = ')'
      if self.meta is not None:
        flags += pre + 'has sysmeta'
        pre = ', '
        post = ')'

      flags = flags + post
      print_info('%s%s%s' % (p, self.pid, flags))

    #== Static methods =======================================================================


def find(pid):
  ''' Find the pid.
  '''
  raise cli_exceptions.CLIError('data_pacakge.find(): not implemented')


def _newline(session):
  if session:
    if session.get(PRETTY_sect, PRETTY_name):
      print
