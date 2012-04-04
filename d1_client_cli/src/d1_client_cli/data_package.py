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
import sys
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
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Please install d1_common.\n')
  raise

# cli
from print_level import * #@UnusedWildImport
import cli_client
import cli_exceptions
import system_metadata

RDFXML_FORMATID = 'http://www.w3.org/TR/rdf-syntax-grammar'


class DataPackage(object):
  def __init__(self, pid):
    ''' Create a package
    '''
    self.pid = pid
    #
    self.scimeta_pid = None
    self.scidata_pid_list = ()

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

  def save(self, session):
    if session is None:
      raise cli_exceptions.InvalidArguments('Must specify a session to save')

    pkg_xml = self.serialize('xml')

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
    response = client.create(pid=self.pid, obj=flo, sysmeta=sysmeta)
    if response is not None:
      return response.value()
    else:
      return None

  def add_data(self, session, scimetapid, scidatapid_list):
    ''' Add a scimeta object and a sequence of scidata objects.
    '''
    # Safety dance.
    if session is None:
      raise cli_exceptions.InvalidArguments('session cannot be None')

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

#-- Static methods -------------------------------------------------------------


def find(pid):
  '''  Find a package by it's pid.
  '''
  raise cli_exceptions.CLIError(' data_package.find(): Method not implemented')
