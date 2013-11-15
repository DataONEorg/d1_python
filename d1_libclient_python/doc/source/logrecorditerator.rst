LogRecordIterator example
=========================

::

  #!/usr/bin/env python

  import d1_client.client
  import sys
  logging.basicConfig(level=logging.INFO)
  target = "https://mn-unm-1.dataone.org/mn"
  client = d1_client.client.DataOneClient(target=target)
  log_record_iterator = LogRecordIterator(client)
  for event in log_record_iterator:
    print "Event    = %s" % event.event
    print "Timestamp  = %s" % event.dateLogged.isoformat()
    print "IP Addres  = %s" % event.ipAddress
    print "Identifier = %s" % event.identifier
    print "User agent = %s" % event.userAgent
    print "Subject  = %s" % event.subject
    print '-' * 79
