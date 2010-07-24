'''This script exercises a node by retrieving the list of all objects and
for each attempts to retrieve the associated metadata and the object.

Use with caution and care since it iterates over every object on the node.
'''
import sys
import logging
import d1pythonitk.client
import d1pythonitk.objectlist


def read_chunk(fobj, chunk_size=1024):
  while True:
    data = fobj.read(chunk_size)
    if not data:
      break
    yield data


def readAll(f):
  data = ''
  for chunk in read_chunk(f):
    data += chunk
  return data


def walkNode(target, start=0):
  '''Given a DataOne node, retrieve each object and it's associated system 
  metadata.
  '''
  client = d1pythonitk.client.DataOneClient(target=target)
  objects = d1pythonitk.objectlist.ObjectListIterator(client, start=start)
  logging.info("%d objects on target" % len(objects))
  counter = 0
  for obj in objects:
    counter += 1
    logging.info("ID (%d/%d) = %s" % (counter + start, len(objects), obj.identifier))
    try:
      meta = readAll(client.getSystemMetadataResponse(obj.identifier))
      logging.info("Meta size = %d" % len(meta))
    except Exception, e:
      logging.exception(e)
      logging.error("Trying to load: %s" % client.getMetaUrl(id=obj.identifier))
    try:
      data = readAll(client.get(obj.identifier))
      logging.info("Object size (%d) = %d" % (obj.size, len(data)))
      if len(data) != obj.size:
        logging.error("Size mismatch for %s" % client.getObjectUrl(id=obj.identifier))
    except Exception, e:
      logging.exception(e)
      logging.error("Trying to load: %s" % client.getObjectUrl(id=obj.identifier))
  logging.info('Done.')


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  #target = "http://dev-dryad-mn.dataone.org/mn"
  target = "http://129.24.0.15/mn"
  #target = "http://knb-mn.ecoinformatics.org/knb"
  #target = "http://cn-unm-1.dataone.org/knb"
  #target = "http://cn-ucsb-1.dataone.org/knb"
  walkNode(target, start=0)
