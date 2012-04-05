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
import string
import StringIO
import tempfile
import xml.dom.minidom

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

RDFXML_FORMATID = 'http://www.w3.org/TR/rdf-syntax-grammar'

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
    self.scimeta = None
    self.scidata_dict = {}

  #== Informational =========================================================

  def is_dirty(self):
    ''' Check to see if anything needs to be saved.
    '''
    if self.scimeta is not None:
      if (self.scimeta.dirty) and self.scimeta.dirty:
        return True
    if self.scidata_dict is not None:
      for item in self.scidata_dict.values():
        if (item.dirty is not None) and item.dirty:
          return True
    return False

  #== Manipulation ==========================================================

  def show(self, pretty=False, verbose=False):
    ''' Display the package, optionally in a "pretty" and/or "verbose" manner.
    '''
    if (pretty is not None) and pretty:
      msg = self.pid
      if self.pid is None:
        msg = '(none)'
      print_info('Id:              %s' % msg)

      if self.scimeta is None:
        print_info('SciMeta Object:  (none)')
      else:
        print_info('SciMeta Object:')
        self._print_dataitem(self.scimeta, pretty, verbose)

      if ((self.scidata_dict is None) or (len(self.scidata_dict) == 0)):
        print_info('Data Objects:    (none)')
      else:
        print_info('Data Objects:')
        for item in self.scidata_dict.values():
          self._print_dataitem(item, pretty, verbose)

      if self.is_dirty():
        print_info("* package needs saving.")
    else:
      print_warn("  **  data_package.show(): Need to implement non-pretty.")

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
    ''' Get the object referred to by this pid and make sure it is a
        package.
    '''
    if self.pid is None:
      raise cli_exceptions.InvalidArguments('Missing pid')

    print_debug('_get_by_pid.pid: %s' % self.pid)
    data_object = self._get_by_pid(session, self.pid)
    print_debug('_get_by_pid.data_object: %s' % str(data_object))

    print_error("  **  data_package.load(): not implemented.")

    return data_object

  def save(self):
    ''' Save this object referred to by this pid.
    '''
    if self.pid is None:
      raise cli_exceptions.InvalidArguments('Missing pid')
    print_error("  **  data_package.save() is not implemented.")
    return

  def scimeta_add(self, session, pid, file_name=None):
    ''' Add a scimeta object.
    '''
    if session is None:
      raise cli_exceptions.InvalidArguments('Missing the session')
    if pid is None:
      raise cli_exceptions.InvalidArguments('Missing the pid (and possibly the object)')
    if ((self.scimeta is not None)
         and not cli_util.confirm('Do you wish to delete the existing science metadata object?')):
      return
    else:
      self.scimeta = None

    new_scimeta = self._get_by_pid(session, pid)
    if new_scimeta is not None: # Could we find it?
      self.scimeta = self._validate_scimeta_obj(new_scimeta) # throws exception
    else:
      if file_name is None:
        print_error(
          'Couldn\'t find scimeta by pid %s, and there was no file specified.' % pid
        )
        return
      # Check the file
      format_id = self._determine_format_id(file_name)
      if format_id is None:
        format_id = session.get(FORMAT_sect, FORMAT_name)
        if format_id is None:
          print_error('The object format could not be determined and was not defined.')
          return
      self.scimeta = DataObject(pid, True, file_name, None, format_id)

  def scimeta_del(self):
    ''' Remove the science metadata object.
    '''
    if cli_util.confirm('Are you sure you want to remove the science meta object?'):
      self.scimeta = None

  def scimeta_showobj(self, session):
    ''' Show the science metadata object.
    '''
    if session is None:
      raise cli_exceptions.InvalidArguments('Missing the session')
    if self.scimeta is None:
      raise cli_exceptions.InvalidArguments('There is no science metadata object defined')
    elif self.scimeta.fname is not None:
      self._print_dataitem(self.scimeta.str(), session._is_pretty())

  def scimeta_showmeta(self, session):
    ''' Show the system metadata of the science metadata object.
    '''
    if session is None:
      raise cli_exceptions.InvalidArguments('Missing the session')
    if self.scimeta is None:
      raise cli_exceptions.InvalidArguments('There is no science metadata object defined')
    elif self.scimeta.meta is not None:
      self._print_sysmeta(self.scimeta.meta, session._is_pretty(), session._is_verbose())

  def scidata_add(self, session, pid, file_name):
    ''' Add a science data object to the list.
    '''
    if session is None:
      raise cli_exceptions.InvalidArguments('Missing the session')
    if pid is None:
      raise cli_exceptions.InvalidArguments('Missing the pid')
    if pid in self.scidata_dict:
      raise cli_exceptions.InvalidArguments(
        'That pid (%s) is already in the package.' % pid
      )
    self.scidata_dict[pid] = self._create_object(session, pid, file_name)

  def scidata_del(self, pid):
    ''' Remove a science data object.
    '''
    if pid is None:
      raise cli_exceptions.InvalidArguments('Missing the pid')
    if pid not in self.scidata_dict:
      print_warn('There isn\'t a science data object with pid %s' % pid)
    elif cli_util.confirm(
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

  def scidata_showobj(self, session, pid):
    ''' Show the specified science data object.
    '''
    if session is None:
      raise cli_exceptions.InvalidArguments('Missing the session')
    if pid is None:
      raise cli_exceptions.InvalidArguments('Missing the pid')
    if self.scidata_dict is None:
      self.scidata_dict = []
    if pid not in self.scidata_dict:
      raise cli_exceptions.InvalidArguments('%s: no such science data object defined')
    self._print_dataitem(
      self.scidata_dict[pid], session.is_pretty(), session.is_verbose(
      )
    )

  def scidata_showmeta(self, session, pid):
    ''' Show the system metadata for the specified science data object.
    '''
    if session is None:
      raise cli_exceptions.InvalidArguments('Missing the session')
    if pid is None:
      raise cli_exceptions.InvalidArguments('Missing the pid')
    if self.scidata_dict is None:
      self.scidata_dict = []
    if pid not in self.scidata_dict:
      raise cli_exceptions.InvalidArguments('%s: no such science data object defined')
    self._print_sysmeta(self.scidata_dict[pid], session.is_pretty(), session.is_verbose())

    #== Helpers ===============================================================

  def _get_by_pid(self, session, pid):
    ''' Return (pid, dirty, fname, sysmeta)
    '''
    if session is None:
      raise cli_exceptions.InvalidArguments('Missing session')
    if pid is None:
      raise cli_exceptions.InvalidArguments('Missing pid')

    fname = cli_client.get_object_by_pid(session, pid, resolve=True)
    if fname is not None:
      return DataObject(pid, False, fname, None)
    else:
      return None

  def _create_object(self, session, pid, file_name):
    ''' Create a data object.
        Return (object, dirty, object, system metadata)
    '''
    if session is None:
      raise cli_exceptions.InvalidArguments('Missing session')
    if pid is None:
      raise cli_exceptions.InvalidArguments('Missing pid')
    if file_name is None:
      raise cli_exceptions.InvalidArguments('Missing file_name')
    if not os.path.isfile(os.path.expanduser(file_name)):
      msg = 'Invalid file: {0}'.format(file_name)
      raise cli_exceptions.InvalidArguments(msg)
    format_id = session.get(FORMAT_sect, FORMAT_name)
    if format_id is None:
      raise cli_exceptions.InvalidArguments('Missing object format id')
    #
    return DataObject(pid, True, file_name, None, format_id)

  def _create_sysmeta(self, obj):
    ''' Create a system meta data object.
    '''
    print_warn('data_package._create_sysmeta(): not implemented')

  def _validate_scimeta_obj(self, scimeta_obj):
    ''' Verify that the object is really a science metadata object.
    '''
    if scimeta_obj is None:
      raise cli_exceptions.InvalidArguments('Missing scimeta_obj')
    if scimeta_obj.fname is None:
      raise cli_exceptions.InvalidArguments('Missing the actual science metadata object')
    #
    print_warn('This object has not been checked for validity!')

    #    objectId = self._is_metadata_format(scimeta_obj.get(KEY_Obj).objectId)
    #    if not self._is_metadata_format(objectId):
    #      msg = 'The science metadata object is not the right type (%s)'
    #      raise cli_exceptions.InvalidArguments(msg % objectId)
    return scimeta_obj

  def _print_dataitem(self, item, pretty=False, verbose=False):
    if (pretty is not None) and pretty:
      flags = ''
      pre = ' ('
      post = ''

      if (item.dirty is not None) and item.dirty:
        flags += pre + 'needs saving'
        pre = ', '
        post = ')'
      if item.fname is not None:
        flags += pre + 'has an object file'
        if verbose:
          flags += ' (%s)' % item.fname
        pre = ', '
        post = ')'
      if item.meta is not None:
        flags += pre + 'has sysmeta'
        pre = ', '
        post = ')'

      flags = flags + post
      print_info('  %s%s' % (item.pid, flags))

  def _print_sysmeta(self, item, pretty=False, verbose=False):
    if (item is not None) and (item.meta is not None):
      sci_meta_xml = item.meta.toxml()

      if pretty():
        dom = xml.dom.minidom.parseString(sci_meta_xml)
        sci_meta_xml = dom.toprettyxml(indent='  ')
      cli_util.output(StringIO.StringIO(self._pretty(sci_meta_xml)), None)

  def _determine_format_id(self, filename):
    ''' Try and get the object format from this document.
    '''
    print_warn('data_package._determine_format_id() has not been implemented.')
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

    #
    #  def serialize(self, fmt='xml'):
    #    assert(fmt in ('xml', 'pretty-xml', 'n3', 'rdfa', 'json', 'pretty-json', 'turtle', 'nt', 'trix'))
    #    if self.resmap.serializer is not None:
    #      self.resmap.serializer = None
    #    serializer = foresite.RdfLibSerializer(fmt)
    #    self.resmap.register_serialization(serializer)
    #    doc = self.resmap.get_serialization()
    #    return doc.data
    #
    #
    #  def finalize(self, package_objects):
    #    ''' Create the resource map.
    #    '''
    #    for package_object in package_objects:
    #      sysmeta_obj = package_object['scimeta_obj']
    #      if self._is_metadata_format(sysmeta_obj.formatId):
    #        self._add_inner_package_objects(package_objects, sysmeta_obj)
    #        
    #    return self._generate_resmap(package_objects)
    #
    #
    #
    #  def save(self, session):
    #    if session is None:
    #      raise cli_exceptions.InvalidArguments('Must specify a session to save')
    #  
    #    pkg_xml = self.serialize('xml')
    #  
    #    algorithm = session.get(session.CHECKSUM[0], session.CHECKSUM[1])
    #    hash_fcn = util.get_checksum_calculator_by_dataone_designator(algorithm)
    #    hash_fcn.update(pkg_xml)
    #    checksum = hash_fcn.hexdigest()
    #  
    #    access_policy = session.access_control.to_pyxb()
    #    replication_policy = session.replication_policy.to_pyxb()
    #    sysmeta_creator = system_metadata.system_metadata()
    #    sysmeta = sysmeta_creator.create_pyxb_object(session, self.pid, len(pkg_xml),
    #                                                 checksum, access_policy,
    #                                                 replication_policy,
    #                                                 formatId=RDFXML_FORMATID)
    #  
    #    client = cli_client.CLIMNClient(session)
    #    flo = StringIO.StringIO(pkg_xml)
    #    response = client.create(pid=self.pid, obj=flo, sysmeta=sysmeta)
    #    if response is not None:
    #      return response.value()
    #    else:
    #      return None
    #
    #
    #  def add_data(self, session, scimetapid, scidatapid_list):
    #    ''' Add a scimeta object and a sequence of scidata objects.
    #    '''
    #    # Safety dance.
    #    if session is None:
    #      raise cli_exceptions.InvalidArguments('session cannot be None')
    #
    #
    #  def _add_inner_package_objects(self, package_objects, sysmeta_obj):
    #    ''' The given sysmeta object actually defines a data package.  Process the
    #        package and add all of the thingsd specified to the package_object_list.
    #    '''
    #    print_info('+ Using metadata to add to an existing package')
    #    print_error('package._add_inner_package_objects() is not implemented!!!')
    #    
    #
    #  def _generate_resmap(self, package_object_list):
    #    ''' The scimeta is part of a package.  Create a package.
    #    
    #        An example package_object item looks like:
    #                {
    #                  'scimeta_obj': <d1_common.types.generated.dataoneTypes.SystemMetadata>,
    #                  'scimeta_url': 'https://demo1.test.dataone.org:443/knb/d1/mn/v1/meta/test-object'
    #                  'scidata_pid':pid,
    #                  'scidata_url':get_scimeta_url
    #                }
    #    '''
    #    # Create the aggregation
    #    foresite.utils.namespaces['cito'] = Namespace("http://purl.org/spar/cito/")
    #    aggr = foresite.Aggregation(self.pid)
    #    aggr._dcterms.title = 'Simple aggregation of science metadata and data.'
    #
    #
    #    # Create references to the science data
    #    for item in package_object_list:
    #      # Create a reference to the science metadata
    #      scimeta_obj = item['scimeta_obj']
    #      scimeta_pid = scimeta_obj.identifier.value()
    #      uri_scimeta = URIRef(item['scimeta_url'])
    #      res_scimeta = foresite.AggregatedResource(uri_scimeta)
    #      res_scimeta._dcterms.identifier = scimeta_pid
    #      res_scimeta._dcterms.description = 'A reference to a science metadata object using a DataONE identifier'
    #
    #      uri_scidata = URIRef(item['scidata_url'])
    #      res_scidata = foresite.AggregatedResource(uri_scidata)
    #      res_scidata._dcterms.identifier = item['scidata_pid']
    #      res_scidata._dcterms.description = 'A reference to a science data object using a DataONE identifier'
    #      res_scidata._cito.isDocumentedBy = uri_scimeta
    #      res_scimeta._cito.documents = uri_scidata
    #
    #      aggr.add_resource(res_scimeta)
    #      aggr.add_resource(res_scidata)
    #
    #    # Create the resource map
    #    resmap_id = "resmap_%s" % self.pid
    #    self.resmap = foresite.ResourceMap("https://cn.dataone.org/object/%s" % resmap_id)
    #    self.resmap._dcterms.identifier = resmap_id
    #    self.resmap.set_aggregation(aggr)
    #    return self.resmap

    #== Static methods ========================================================


def find(pid):
  ''' Find the pid.
  '''
  raise cli_exceptions.CLIError('data_pacakge.find(): not implemented')

#** DataObject *****************************************************************


class DataObject(object):
  def __init__(self, pid=None, dirty=None, fname=None, meta=None, object_id=None):
    ''' Create a data object
    '''
    self.pid = pid
    self.dirty = dirty
    self.fname = fname
    self.meta = meta
    self.object_id = object_id

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
