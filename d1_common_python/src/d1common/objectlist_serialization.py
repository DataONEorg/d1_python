'''
Implements serializaton and de-serialization for the ObjectList.
'''

import d1common

from d1common.types import objectlist

#===============================================================================


class ObjectListSerialization(object):
  def __init__(self):
    pass

  def serialize(self, data, destfile, format="text/xml"):
    '''
    :param data: An iterator that supports next()
    :param destfile: File open for writing the serialized output
    :param format: Mime type of the output format
    '''
    format = format.strip().lower()
    if format == d1common.MIMETYPES['xml']:
      return self.serializeXml(data, destfile)
    if format == d1common.MIMETYPES['json']:
      return self.serializeJson(data, destfile)
    if format == d1common.MIMETYPES['csv']:
      return self.serializeCsv(data, destfile)
    raise ValueError('Unknown ObjectList serialization format: %s' % format)

  def serializeXml(self, data, destfile):
    '''
    Given a pyxb instance, write the xml doc to destfile.
    '''
    destfile.write(data.toxml())

  def serializeJson(self, data, destfile):
    pass

  def serializeCsv(self, data, destfile):
    pass

  def deserialize(self, document, format="text/xml"):
    format = format.strip().lower()
    if format == d1common.MIMETYPES['xml']:
      return self.deserializeXml(document)
    if format == d1common.MIMETYPES['json']:
      return self.deserializeJson(document)
    if format == d1common.MIMETYPES['csv']:
      return self.deserializeCsv(document)
    raise ValueError('Unknown de-serialization format: %s' % format)

  def deserializeXml(self, document):
    # This is kind of inefficient, loading the entire document to a model as
    # defined by the pyxb parser
    res = objectlist.CreateFromDocument(document)
    return res

  def deserializeJson(self, document):
    pass

  def deserializeCsv(self, document):
    pass
