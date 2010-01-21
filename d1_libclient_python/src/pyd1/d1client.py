'''
Module pyd1.d1client
====================

:Created: 20100111
:Author: vieglais

:Dependencies:

  - httplib2 is used for HTTP interactions.  This library offers many features
    that extend the capabilities of the standard Python urllib2, especially
    a well thought out, simple caching mechanism and a slew of common 
    authentication mechanisms.  httplib2 can be found at:
    
      http://code.google.com/p/httplib2/ 


.. autoclass:: D1Client
   :members:
'''

import logging
import urllib
import urlparse

try:
  import cjson as json
except:
  import json

import httplib2
from pyd1 import d1const
from pyd1 import d1exceptions
from pyd1 import d1sysmeta


class D1Client(httplib2.Http):
  '''Implements a basic client for interaction with the DataONE system.
  
  Example:
  
    >>> from pyd1 import d1client
    >>> target = "http://localhost:8000/mn"
    >>> cli = d1client.D1Client()
    >>> objects = cli.listObjects(target=target, count=10)
    >>> objects.keys()
    [u'count', u'start', u'total', u'data']
    >>> objects['count']
    10
    >>> print objects['data'][0]
    {u'guid': u'02c3f67e-b2e1-4550-8fae-f6d90e9f15f6', 
     u'hash': u'2e01e17467891f7c933dbaa00e1459d23db3fe4f', 
     u'modified': u'2010-01-06T12:44:26', u'oclass': u'data', u'size': 2}
    >>> cli.get(objects['data'][0]['guid'], target=target)
    '49'
    >>> sysm = cli.getSystemMetadata(objects['data'][0]['guid'], target=target)
    >>> dir(sysm)
    ['AccessRule', 'AuthoritativeMemberNode', 'Checksum', 'ChecksumAlgorthm', 
     'Created', 'DerivedFrome', 'DescribedBy', 'Describes', 'EmbargoExpires', 
     'Expires', 'Identifier', 'ObjectFormat', 'ObsoletedBy', 'Obsoletes', 
     'OriginMemberNode', 'Replica', 'RightsHolder', 'Size', 'Submitter', 
     'SysMetadataCreated', 'SysMetadataModified', '__class__', '__delattr__', 
     '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', 
     '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', 
     '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 
     '__weakref__', '_getValues', '_parse', 'etree', 'isValid', 'toXml', 'xmldoc']
    >>> sysm.Size
    2
    >>> sysm.created
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'D1SystemMetadata' object has no attribute 'created'
    >>> sysm.Created
    datetime.datetime(2010, 1, 6, 12, 44, 26)
  
  '''

  def __init__(
    self,
    introspection_target=d1const.URL_DATAONE_ROOT,
    cache=d1const.HTTP_RESPONSE_CACHE,
    timeout=d1const.RESPONSE_TIMEOUT,
    proxy_info=None
  ):
    '''
    :param introspection_target: Location of a service for discovering
      information about the DataONE system, such as the locations of resolvers, 
      coordinating nodes and member nodes.
    :param cache: Either the name of a directory to be used as a flat file 
      cache, or it must an object that implements httlib2.FileCache interface
    :param timeout: Socket level timeout (seconds)
    :param proxy_info: httplib2.ProxyInfo instance
    '''
    httplib2.Http.__init__(self, cache=cache, timeout=timeout, proxy_info=proxy_info)
    self.logger = logging.getLogger(self.__class__.__name__)
    self.d1root = introspection_target
    self.useragent = d1const.USER_AGENT
    self._last_response = None

  def _getHeaders(self):
    headers = {'User-Agent': self.useragent, 'Accept': '*/*'}
    return headers

  def _normalizeTarget(self, target):
    '''Internal method to ensure target url is in suitable form before 
    adding paths.
    '''
    if not target.endswith("/"):
      target += "/"
    return target

  def lastResponse(self):
    '''Returns the last response metadata returned from a Http request.

    :rtype: httplib2.Response
    '''
    return self._last_response

  def request(self, *args, **kwargs):
    '''An oversight in httplib2 Http.request() means that when connecting to a
    valid host that isn't connectable, the conn object within the Http class 
    is not tested for None before calling httplib.  This results in httplib
    raising an attribute error, which is a bit confusing.  Here the error
    is trapped and re-raised as a Httplib2.HttpLib2Error.
    
    The _last_response instance variable is updated.
    
    :rtype: Tuple of Response and data returned from the Http request  
    '''
    try:
      self._last_response, data = super(D1Client, self).request(*args, **kwargs)
      return self._last_response, data
    except AttributeError, e:
      message = u"No socket connection could be created for Http target.\n"
      raise httplib2.HttpLib2Error(message + str(e))
    return None

  def getObjectsURL(self, target, start=None, count=None, oclass=None):
    '''Returns the path of the objects collection for the specified target.
    
    :param target: The URL of the service from which the collection is being 
      retrieved.
    :param start: Zero based index of the first object to retrieve.
    :param count: Maximum number of objects to be retrieved.
    :param oclass: The type of object being requested.
    
    :rtype: URL for retrieving the specified content.
    '''
    target = self._normalizeTarget(target)
    url = urlparse.urljoin(target, d1const.URL_OBJECT_PATH)
    if not url.endswith("/"):
      url += "/"
    params = {}
    if not start is None:
      start = int(start)
      assert (start >= 0)
      params['start'] = str(start)
    if not count is None:
      count = int(count)
      if count >= d1const.MAX_LISTOBJECTS:
        raise ValueError('Too many objects being requested (%s)' % str(count))
      params['count'] = str(count)
    if not oclass is None:
      if not oclass in d1const.OBJECT_CLASSES:
        raise ValueError('%s is not a valid Object Class' % str(oclass))
      params['oclass'] = oclass
    if len(params.keys()) > 0:
      url = "%s?%s" % (url, urllib.urlencode(params))
    self.logger.debug("getObjectsURL=%s" % url)
    return url

  def getObjectURL(self, target, guid):
    '''
    Given a host and object identifier, return a URL that can be used to 
    retrieve the object.
    
    :param target: The host (e.g. http://mn1.dataone.org/base/)
    :param guid: The GUID for the object
    :rtype: URL to retrieve the object bytes
    '''
    target = self._normalizeTarget(target)
    url = urlparse.urljoin(
      target, '%s/%s' % (d1const.URL_OBJECT_PATH, urllib.quote(guid))
    )
    self.logger.debug("getObjectURL=%s" % url)
    return url

  def getObjectMetadataURL(self, target, guid):
    '''
    Given a host and object identifier, return a URL that can be used to 
    retrieve the system metadata about the object.
    
    :param target: The host to which the request is being sent.
    :param guid: The GUID for the object
    :rtype: URL for retrieving the system metadata about the object
    '''
    url = self.getObjectURL(target, guid)
    url = self._normalizeTarget(url)
    url = urlparse.urljoin(url, '%s' % d1const.URL_SYSMETA_PATH)
    self.logger.debug("getObjectMetadataURL=%s" % url)
    return url

  def listObjects(
    self,
    target=d1const.URL_DATAONE_ROOT,
    start=0,
    count=d1const.DEFAULT_LISTOBJECTS,
    oclass=None
  ):
    '''Retrieves a list of objects available on target.
    
    :param target: The host being queried.  If none provided then objects from
                   the DataONE root are listed, which should be a list of all
                   objects in the DataONE system.
    :param start: Zero based index for first item to retrieve
    :param count: Number of items to retrieve
    :param oclass: Optional restriction for type of object to retrieve
    :rtype: (dictionary) Containing a list of objects (guid, oclass, hash, 
            modified, size) 
    
    :raises: TargetNotAvailableException
    '''
    url = self.getObjectsURL(target, start=start, count=count, oclass=oclass)
    headers = self._getHeaders()
    response, data = self.request(url, method='GET', headers=headers)
    if response.status not in d1const.HTTP_STATUS_OK:
      message = u"Error listing objects from target %s." % target
      message += u"\nStatus = %s" % str(response.status)
      message += u"\nFull URL=%s" % url
      raise d1exceptions.TargetNotAvailableException(response, message)
    #Try and convert JSON to python
    self.logger.debug("data = %s" % data)
    objects = json.loads(data)
    return objects

  def resolve(self, guid):
    '''
    Given an identifier, returns a list of URLs from which the object may be 
    retrieved.  In general, the first list entry is the preferred retrieval 
    option.
    
    Not Implemented.
    
    :param guid: Globally unique identifier known to the DataONE system.
    :rtype: (list of string)  List of URLs for accessing <guid>
    '''
    raise NotImplementedError('Resolve method is not implemented.')
    pass

  def get(self, guid, target=None):
    '''Returns the bytes of an object retrieved from the DataONE system.  If a
    target is not provided, then the location of the object is resolved first,
    and the bytes are retrieved from the resolved target.
    
    Note that the resulting object may be quite large.  If this is a concern,
    then check the system metadata for the object first.

    :param guid: The globally unique identifier for the object
    :param target: Optional host from which to retrieve the object.
    :rtype: (Bytes) The bytes of the object.    
    '''
    #resolve object
    if target is None:
      target = self.resolve(guid)
    url = self.getObjectURL(target, guid)
    #retrieve
    headers = self._getHeaders()
    response, data = self.request(url, 'GET', headers=headers)
    return data

  def getSystemMetadata(self, guid, target=None):
    '''Retrieve the DataONE system metadata describing the specified object.

    :param guid: The globally unique identifier for the object
    :param target: Optional host from which to retrieve the object.
    :rtype: (D1SystemMetadata) instance representing the object's system 
            metadata    
    '''
    #resolve object
    if target is None:
      target = self.resolve(guid)
    url = self.getObjectMetadataURL(target, guid)
    headers = self._getHeaders()
    response, data = self.request(url, 'GET', headers=headers)
    if response.status not in d1const.HTTP_STATUS_OK:
      message = u"Error retrieving system metadata for %s." % guid
      message += u"\nStatus = %s" % str(response.status)
      message += u"\nFull URL=%s" % url
      raise d1exceptions.TargetNotAvailableException(response, message)
    self.logger.debug("getSystemMetadata data=%s" % data)
    return d1sysmeta.D1SystemMetadata(xmldoc=data)

  def getSystemMetadataSchema(self):
    '''Convenience function to retrieve the system metadata schema document.
    
    :rtype: (Unicode) The system metadata document schema.
    '''
    headers = self._getHeaders()
    url = d1const.SYSTEM_METADATA_SCHEMA_URL
    response, data = self.request(url, 'GET', headers=headers)
    assert (response.status in d1const.HTTP_STATUS_OK)
    return data
