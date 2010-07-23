'''
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
import d1common
import d1common.exceptions
import d1common.types.generated.systemmetadata

#===============================================================================


def toCSV(self, dialect='excel'):
  raise d1common.exceptions.NotImplemented(
    '0.SystemMetaData.toCSV', 'Serializing SystemMetadata to CSV is not implemented.'
  )


def fromCSV(self, data, dialect='excel'):
  raise d1common.exceptions.NotImplemented(
    '0.SystemMetaData.fromCSV',
    'De-serializing SystemMetadata from CSV is not implemented.'
  )


def toJSON(self):
  raise d1common.exceptions.NotImplemented(
    '0.SystemMetaData.toJSON', 'Serializing SystemMetadata to JSON is not implemented.'
  )


def fromJSON(self, data):
  raise d1common.exceptions.NotImplemented(
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
  sysm = d1common.types.generated.systemmetadata.systemMetadata()
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
  if format == d1common.MIMETYPES['xml']:
    sysm = d1common.types.generated.systemmetadata.CreateFromDocument(data)
    sysm.toCSV = new.instancemethod(toCSV, sysm, sysm.__class__)
    sysm.fromCSV = new.instancemethod(fromCSV, sysm, sysm.__class__)
    sysm.toJSON = new.instancemethod(toJSON, sysm, sysm.__class__)
    sysm.fromJSON = new.instancemethod(fromJSON, sysm, sysm.__class__)
    sysm.toText = new.instancemethod(toText, sysm, sysm.__class__)
    return sysm

  if format == d1common.MIMETYPES['json']:
    res = systemMetadata()
    return res.fromJSON(data)

  if format == d1common.MIMETYPES['csv']:
    res = systemMetadata()
    return res.fromCSV(data)

  raise ValueError('Unknown ObjectList serialization format: %s' % format)
