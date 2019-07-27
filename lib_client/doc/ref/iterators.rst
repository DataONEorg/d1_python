DataONE Iterators
-----------------

DataONE provides generators / iterators that offer convenient ways to iterate over content on nodes.

The types of content that can be downloaded with iterators is:

- **ObjectInfo**: Basic information about Science Objects
- **SystemMetadata**: System level information about Science Objects
- **LogRecord**: Information about downloads and other events that have occurred on Science Objects

The iterators are also offered in different implementations, each with different trade-offs.

The iterators are named by the object type they return and the implementation. The serial iterators have names ending with ``Iterator``, e.g., ``ObjectListIterator``. Asynchronous iterator names end with ``Async``, and multiprocessed iterators end with ``Multi``.

The iterators all use a DataONE Client in the background to retrieve information from the remote node. The type of client and how it is provided to the iterator differs between iterators. Async iterators need the async DataONE Client. Serial and async iterators take the client directly as an argument, as they need only a single client. Multiprocessed iterators take client creation parameters instead, as they need to create an arbitrary number of clients that will be used in parallel.

For instances when more fine grained filtering is required, DataONE provides a Solr index. The index can be queried via the :ref:`d1_client/api/d1_client:d1\\_client.solr\\_client module`.

Serial iterators
~~~~~~~~~~~~~~~~

Provides the lowest effort in using from client software, but offers low performance, as it creates only a single connection to the target node, and has to wait for a responses to to requests.

Asynchronous iterators
~~~~~~~~~~~~~~~~~~~~~~

Offers good trade-off between ease of use and performance. Based on ``asyncio`` and ``aiohttp`` and typically offers very high performance.

Multiprocessed iterators
~~~~~~~~~~~~~~~~~~~~~~~~

Potentially very high performance, but also resource hungry and with more potential for unexpected behavior.

Unhandled exceptions raised in client code while iterating over results from this iterator, or in the iterator itself, will not be shown and may cause the client code to hang. This is a limitation of the multiprocessing module.

If there is an error when retrieving a System Metadata, such as NotAuthorized, an object that is derived from d1_common.types.exceptions.DataONEException is returned instead.

Will create the same number of DataONE clients and HTTP or HTTPS connections as the number of workers. A single connection is reused, first for retrieving a page of results, then all System Metadata objects in the result.

``MAX_QUEUE_SIZE`` setting:

- Queues that become too large can cause deadlocks:

  https://stackoverflow.com/questions/21641887/python-multiprocessing-process-hangs-on-join-for-large-queue

- Each item in the queue is a potentially large SysMeta PyXB object, so we set a low max queue size.


ObjectList iterators
--------------------

ObjectList iterators are based on the ``MNRead.listObjects()`` and ``CNRead.listObjects()`` API methods, which are available on both CNs and MNs, so the iterators can be used with both. The API method provides basic filtering that can be applied in order to control which objects are returned, and this is made available by the iterator as well. The filters available from MNs are: ``fromDate``, ``toDate``, ``formatId`` and ``identifier``. CNs additionally support filtering on ``nodeId``.

As with other DataONE APIs, ``listObjects()`` checks any access policies that may have been set on the objects by the rights holder and will only include objects that have public access or for which the client has read access or better. In order to authenticate to the node, provide an X509 certificate or JWT web token when creating the iterator.

``ObjectListIterator`` takes a ``CoordinatingNodeClient`` or ``MemberNodeClient`` together with filters to select a set of objects. It returns an iterator object which enables using a Python ``for`` loop for iterating over the matching objects.


SystemMetadata iterators
------------------------

Similar to ObjectList iterators but includes downloading and deserializing of SystemMetadata XML objects. The SystemMetadata is provided as PyXB objects, ready to process in the client software.



Event Log iterators
-------------------

The LogRecordIterator repeatedly calls the Node's ``getLogRecords()`` API method. The CN implementation of this method yields log records for objects for which the caller has access. Log records are not provided for public objects. This is also how ``getLogRecords()`` is implemented in the :term:`Metacat` Member Node. In :term:`GMN`, the requirements for authentication for this method are configurable. Other MNs are free to chose how or if to implement access control for this method.

To authenticate to the target Node, provide a valid CILogon signed certificate when creating the CoordinatingNodeClient or MemberNodeClient.

See also:

  Architecture documentation:

    - `CNCore.getLogRecords() <https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.getLogRecords>`_

    - `MNCore.getLogRecords() <https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNCore.getLogRecords>`_

    - `DataONE Architecture Documentation <https://releases.dataone.org/online/api-documentation-v2.0.1/index.html>`_


Node iterators
--------------

For each Node in the environment, returns a PyXB representation of a DataONE Node document.

https://releases.dataone.org/online/api-documentation-v2.0/apis/Types.html#Types.Node


