objectlistiterator example
==========================

::

  #!/usr/bin/env python
  from d1_client import d1baseclient
  from d1_client.objectlistiterator import ObjectListIterator

  # The Base URL for a DataONE Coordinating Node or Member Node.
  base_url = 'https://cn.dataone.org/cn'
  # Start retrieving objects from this position.
  start = 0
  # Maximum number of entries to retrieve.
  max = 500
  # Maximum number of entries to retrieve per call.
  pagesize = 100

  client = d1baseclient.DataONEBaseClient(base_url)
  ol = ObjectListIterator(client, start=start, pagesize=pagesize, max=max)
  counter = start
  print "---"
  print "total: %d" % len(ol)
  print "---"
  for o in ol:
    print "-"
    print "  item     : %d" % counter
    print "  pid      : %s" % o.identifier.value()
    print "  modified : %s" % o.dateSysMetadataModified
    print "  format   : %s" % o.formatId
    print "  size     : %s" % o.size
    print "  checksum : %s" % o.checksum.value()
    print "  algorithm: %s" % o.checksum.algorithm
    counter += 1
