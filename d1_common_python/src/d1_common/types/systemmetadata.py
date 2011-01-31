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
Module d1_common.types.systemmetadata
=====================================

Extends the PyXB generated class to enable serialization to and from CSV and 
JSON.

Note that the approach for handling serializers here is quite different from
the other types wrapped here.  In this case, the additional serialization 
methods are added dynamically to the class instantiated by the generated code.  
Hence the created object behaves exactly the same as the pyxb generated object, 
except with the additional serialization methods.

Example de-serialization::

  doc = getSystemMetdataDocument()
  sysm = CreateFromDocument(doc)
  print sysm.identifier


Example serialization::

  sysm = systemMetadata()
  #set sysm properties
  # ...
  doc = sysm.toxml() 

'''

import new
import d1_common.types.exceptions
import d1_common.types.generated.dataoneTypes

#===============================================================================


def toCSV(self, dialect='excel'):
  raise d1_common.types.exceptions.NotImplemented(
    '0.SystemMetaData.toCSV', 'Serializing SystemMetadata to CSV is not implemented.'
  )


def fromCSV(self, data, dialect='excel'):
  raise d1_common.types.exceptions.NotImplemented(
    '0.SystemMetaData.fromCSV',
    'De-serializing SystemMetadata from CSV is not implemented.'
  )


def toJSON(self):
  raise d1_common.types.exceptions.NotImplemented(
    '0.SystemMetaData.toJSON', 'Serializing SystemMetadata to JSON is not implemented.'
  )


def fromJSON(self, data):
  raise d1_common.types.exceptions.NotImplemented(
    '0.SystemMetaData.fromJSON',
    'De-serializing SystemMetadata from JSON is not implemented.'
  )


def toText(self):
  '''Provides a human readable rending of the content.  Returns a string.
  '''
  txt = []
  txt.append(u'Identifier: %s' % self.identifier)
  txt.append(u'Object Format: %s' % self.objectFormat)
  txt.append(u'Size: %s' % str(self.size))
  txt.append(u'Last Modified:' % str(self.dateSyMetadataModified))
  return u"\n".join(txt)


def systemMetadata():
  '''Returns a new, blank instance of SystemMetadata that can be modified and 
  subsequently serialized to one of the supported formats.
  
  :returns: Instance of SystemMetadata, blank
  :rtype: SystemMetadata
  '''
  sysm = d1_common.types.generated.dataoneTypes.systemMetadata()
  sysm.toCSV = new.instancemethod(toCSV, sysm, sysm.__class__)
  sysm.fromCSV = new.instancemethod(fromCSV, sysm, sysm.__class__)
  sysm.toJSON = new.instancemethod(toJSON, sysm, sysm.__class__)
  sysm.fromJSON = new.instancemethod(fromJSON, sysm, sysm.__class__)
  sysm.toText = new.instancemethod(toText, sysm, sysm.__class__)


def CreateFromDocument(data, format='text/xml'):
  '''Returns an instance of SystemMetadata with elements and attributes set from
  the values in the provided document.
  
  :param string data: The document to be deserialized
  :param string format: The mime-type of the data.
  :returns: The deserialized document as a SystemMetadata object
  :rtype: SystemMetadata
  '''
  format = format.strip().lower()
  if format == d1_common.MIMETYPES['xml']:
    sysm = d1_common.types.generated.dataoneTypes.CreateFromDocument(data)
    sysm.toCSV = new.instancemethod(toCSV, sysm, sysm.__class__)
    sysm.fromCSV = new.instancemethod(fromCSV, sysm, sysm.__class__)
    sysm.toJSON = new.instancemethod(toJSON, sysm, sysm.__class__)
    sysm.fromJSON = new.instancemethod(fromJSON, sysm, sysm.__class__)
    sysm.toText = new.instancemethod(toText, sysm, sysm.__class__)
    return sysm

  if format == d1_common.MIMETYPES['json']:
    res = systemMetadata()
    return res.fromJSON(data)

  if format == d1_common.MIMETYPES['csv']:
    res = systemMetadata()
    return res.fromCSV(data)

  raise ValueError('Unknown ObjectList serialization format: %s' % format)
