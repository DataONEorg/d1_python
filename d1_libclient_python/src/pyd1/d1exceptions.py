'''
Module pyd1.d1exceptions
========================

:Created: 20100111

:Author: vieglais

Defines exceptions unique to PyD1.
'''


class D1Exception(Exception):
  '''Base class for exceptions raised by PyD1.
  '''
  pass


class IntrospectionDataNotAvailableException(D1Exception):
  '''Raised when DataONE introspection information can not be retrieved either
  because the specified node does not provide it or a well known root node (i.e.
  one of the coordinating nodes) cannot be contacted.
  '''
  pass


class TargetNotAvailableException(D1Exception):
  '''General error that is raised when accessing a URL.  The message contains
  additional information. The response attribute of the exception contains the
  HTTP response. 
  '''

  def __init__(self, response, *args, **kwargs):
    '''
    :param response: The response from the httplib2.request().
    '''
    D1Exception.__init__(self, *args, **kwargs)
    self.response = response
