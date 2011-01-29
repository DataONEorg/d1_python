'''
Created on Jan 26, 2011

@author: vieglais
'''

import logging
import urlparse
from d1_common import const
from d1_common import exceptions
import cnclient
import mnclient


class DataONEObject(object):
  def __init__(self, pid):
    self.pid = pid
    self._locations = []
    self._systemmetadata = None
    self._content = None
    self.__client = None

  def getCredentials(self):
    '''Override this method to retrieve credentials that can be used to
    authenticate and retrieve a token for further operations.
    '''
    return {}

  def _getClient(self, forcenew=False):
    '''Internal method used to retrieve an instance of a DataONE client that
    can be used for interacting with the DataONE services.
    '''
    if self.__client is None or forcenew:
      self.__client = DataONEClient(credentials=self.getCredentials())
    return self.__client

  def getLocations(self, forcenew=False):
    '''Retrieve a list of node base urls known to hold a copy of this object.
    '''
    if len(self._locations) < 1 or forcenew:
      cli = self._getClient()
      self._locations = cli.resolve(self.pid)
    return self._locations

  def getSystemMetadata(self, forcenew=False):
    if self._systemmetadata is None or forcenew:
      cli = self._getClient()
      self._systemmetadata = cli.getSystemMetadata(self.pid)
    return self._systemmetadata

  def getRelatedObjects(self):
    cli = self._getClient()
    return cli.getRelatedObjects(self.pid)

  def load(self, outstr):
    '''Persist a copy of the bytes of this object to outstr, which is a 
    file like object open for writing.
    '''
    cli = self._getClient()
    instr = cli.get(self.pid)
    while True:
      data = instr.read(4096)
      if not data:
        return
      outstr.write(data)

  def save(self, filename):
    '''Save the object to a local file
    '''
    outstr = file(filename, "wb")
    self.realize(outstr)
    outstr.close()

#===============================================================================


class DataONEClient(object):
  def __init__(self, cnBaseUrl=const.URL_DATAONE_ROOT, credentials={}):
    self.cnBaseUrl = cnBaseUrl
    self.cn = None
    self.mn = None
    self.credentials = credentials
    self.authToken = None
    self._sysmetacache = {}

  def _getCN(self, forcenew=False):
    if self.cn is None or forcenew:
      self.cn = cnclient.CoordinatingNodeClient(baseurl=self.cnBaseUrl)
    return self.cn

  def _getMN(self, baseurl, forcenew=False):
    if self.mn is None or forcenew:
      self.mn = mnclient.MemberNodeClient(baseurl=baseurl)
    elif self.mn.baseurl != baseurl:
      self.mn = mnclient.MemberNodeClient(baseurl=baseurl)
    return self.mn

  def getAuthToken(self, forcenew=False):
    '''Returns an authentication token using the credentials provided when
    this client was instantiated.
    
    :return type: AuthToken
    '''
    if self.authToken is None or forcenew:
      self.authToken = None
    return self.authToken

  def resolve(self, pid):
    '''
    :return type: list of baseurl
    '''
    cn = self._getCN()
    token = self.getAuthToken()
    result = cn.resolve(token, pid)
    #result.objectLocation.sort(key='priority')
    res = []
    for location in result.objectLocation:
      res.append(location.baseURL)
    return res

  def get(self, pid):
    '''Returns a stream open for reading that returns the bytes of the object
    identified by PID. 
    :return type: HTTPResponse
    '''
    locations = self.resolve(pid)
    token = self.getAuthToken()
    for location in locations:
      print location
      mn = self._getMN(location)
      try:
        return mn.get(token, pid)
      except Exception, e:
        logging.exception(e)
    raise Exception('Object could not be retrieved from any resolved targets')
    return None

  def create(self, targetNodeId=None, ):
    '''
    '''
    pass

  def getSystemMetadata(self, pid):
    '''
    '''
    if self._sysmetacache.has_key(pid):
      return self._sysmetacache[pid]
    cn = self._getCN()
    token = self.getAuthToken()
    self._sysmetacache[pid] = cn.getSystemMetadata(token, pid)
    return self._sysmetacache[pid]

  def getRelatedObjects(self, pid):
    '''
    :return type: list of DataONEObject
    '''
    relations = {
      'obsoletes': [],
      'obsoletedBy': [],
      'derivedFrom': [],
      'describedBy': [],
      'describes': [],
    }
    sysmeta = self.getSystemMetadata(pid)
    for pid in sysmeta.obsoletes:
      relations['obsoletes'].append(pid.value())
    for pid in sysmeta.obsoletedBy:
      relations['obsoletedBy'].append(pid.value())
    for pid in sysmeta.derivedFrom:
      relations['derivedFrom'].append(pid.value())
    for pid in sysmeta.describedBy:
      relations['describedBy'].append(pid.value())
    for pid in sysmeta.describes:
      relations['describes'].append(pid.value())
    return relations

  def isData(self, pid):
    '''Returns True is pid refers to a data object.
    
    Determine this by looking at the describes property of the system metadata.
    '''
    sysmeta = self.getSystemMetadata(pid)
    return len(sysmeta.describes) == 0

  def isScienceMetadata(self, pid):
    '''return True if pid refers to a science metadata object
    '''
    sysmeta = self.getSystemMetadata(pid)
    return len(sysmeta.describes) > 0

  def getScienceMetadata(self, pid):
    '''Retrieve the pid for science metadata object for the specified PID. If 
    PID refers to a science metadata object, then that object is returned. 
    '''
    if self.isScienceMetadata(pid):
      return [pid, ]
    res = []
    sysmeta = self.getSystemMetadata(pid)
    for id in sysmeta.describedBy:
      res.append(id.value())
    return res

  def getData(self, pid):
    if self.isData(pid):
      return [pid, ]
    res = []
    sysmeta = self.getSystemMetadata(pid)
    for id in sysmeta.describes:
      res.append(id.value())
    return res

  def getObjects(self, pids):
    '''
    '''
    pass
