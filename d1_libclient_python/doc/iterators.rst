Iterators
=========

The iterators provide a convenient way to iterate over two of the most common
result sets retrieved from Nodes; Object Lists and Log Records.


ObjectListIterator
~~~~~~~~~~~~~~~~~~

See :ref:`d1_client_objectlistiterator` for details on how to create a
ObjectListOperator.

The ObjectListIterator takes a CoordinatingNodeClient or MemberNodeClient
together with filters to select a set of objects. It returns an iterator object
which enables using a Python ``for`` loop for iterating over the matching
objects. Using the ObjectListIterator is appropriate in circumstances where a
large percentage of the total number of objecs is expected to be returned or
when one of the limited number of filters can be used for selecting the desired
set of objects.

If more fine grained filtering is required, DataONE's Solr index should be used.
It can be accessed using the :ref:`Solr Client <solr_client>`.

Object information is retrieved from the Node only when required. This avoids
storing a large object list in memory.

The ObjectListIterator repeatedly calls the Node's ``listObjects()`` API method.
The CN implementation of this method yields only public objects and objects for
which the caller has access. This is also how ``listObjects()`` is implemented
in the :term:`Metacat` and :term:`GMN` Member Nodes. However, other MNs are free
to chose how or if to implement access control for this method.

To authenticate to the target Node, provide a valid CILogon signed certificate
when creating the CoordinatingNodeClient or MemberNodeClient.


Example
-------

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

Output::

  ---
  total: 5
  ---
  -
    item     : 1
    pid      : knb-lter-lno.9.1
    modified : 2011-01-13 18:42:32.469000
    format   : eml://ecoinformatics.org/eml-2.0.1
    size     : 6751
    checksum : 9039F0388DC76B1A13B0F139520A8D90
    algorithm: MD5
  -
    item     : 2
    pid      : LB30XX_030MTV2021R00_20080516.50.1
    modified : 2011-01-12 22:51:00.774000
    format   : eml://ecoinformatics.org/eml-2.0.1
    size     : 14435
    checksum : B2200FB7FAE18A3517AA9E2EA680EE09
    algorithm: MD5
  -
    ...


LogRecordIterator
~~~~~~~~~~~~~~~~~

See :ref:`d1_client_logrecorditerator` for details on how to create a
LogRecordIterator.

The LogRecordIterator takes a CoordinatingNodeClient or MemberNodeClient
together with filters to select a set of log records. It returns an iterator
object which enables using a Python ``for`` loop for iterating over the matching
log records.

Log records are retrieved from the Node only when required. This avoids storing
a large list of records in memory.

The LogRecordIterator repeatedly calls the Node's ``getLogRecords()`` API
method. The CN implementation of this method yields log records for objects for
which the caller has access. Log records are not provided for public objects.
This is also
how ``getLogRecords()`` is implemented in the :term:`Metacat` Member Node. In
:term:`GMN`, the requirements for authentication for this method are
configurable. Other MNs are free to chose how or if to implement access control
for this method.

To authenticate to the target Node, provide a valid CILogon signed certificate
when creating the CoordinatingNodeClient or MemberNodeClient.

See the `CNCore.getLogRecords()
<http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.getLogRecords>`_
and `MNCore.getLogRecords()
<http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNCore.getLogRecords>`_
specifications in the `DataONE Architecture Documentation
<http://mule1.dataone.org/ArchitectureDocs-current/index.html>`_ for more
information.

Example
-------

::

  #!/usr/bin/env python

  import d1_client.client
  import sys

  logging.basicConfig(level=logging.INFO)
  target = "https://mn-unm-1.dataone.org/mn"
  client = d1_client.client.MemberNodeClient(target=target)
  log_record_iterator = LogRecordIterator(client)
  for event in log_record_iterator:
    print "Event    = %s" % event.event
    print "Timestamp  = %s" % event.dateLogged.isoformat()
    print "IP Addres  = %s" % event.ipAddress
    print "Identifier = %s" % event.identifier
    print "User agent = %s" % event.userAgent
    print "Subject  = %s" % event.subject
    print '-' * 79
