''' 
Module d1objectlist
===================
 
:Created: 20100122
:Author: vieglais


.. autoclass:: D1ObjectList
   :members:
'''


class ObjectList(object):
  '''Implements an immutable list that represents all objects in DataONE.  Data 
  is retrieved from the target only when required.
  '''

  def __init__(self, client):
    pass

  def __len__(self):
    pass

  def __getitem__(self, key):
    '''Implements list[key] and list[a:b]
    
    :param key: integer or slice
    '''
    print "Key = %s" % str(key)
    if isinstance(key, int):
      print "Key is integer"
      return None
    print "Key is slice"
    print "Start = %s, stop=%s, step = %s" % (key.start, key.stop, key.step)
    return None

  def __iter__(self):
    pass
