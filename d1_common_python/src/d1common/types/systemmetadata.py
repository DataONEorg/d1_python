'''
Extends the PyXB generated class to enable serialization to and from CSV and 
JSON.
'''
import d1common
import d1common.exceptions
import d1common.types.generated.systemmetadata

#===============================================================================


def CreateFromDocument(data, format='text/xml'):
  format = format.strip().lower()
  if format == d1common.MIMETYPES['xml']:
    return d1common.types.generated.systemmetadata.CreateFromDocument(data)

  if format == d1common.MIMETYPES['json']:
    res = SystemMetadata()
    return res.fromJSON(data)

  if format == d1common.MIMETYPES['csv']:
    res = SystemMetadata()
    return res.fromCSV(data)

  raise ValueError('Unknown ObjectList serialization format: %s' % format)

#===============================================================================


class SystemMetadata(d1common.types.generated.systemmetadata.SystemMetadata):
  '''Actually nothing to do here since SystemMetadata is expressed as XML.
  
  These methods may be overridden later if necessary to support the
  respective mechanisms
  '''

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
