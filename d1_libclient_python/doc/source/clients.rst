Clients
=======

The client classes wrap all the DataONE API methods, hiding the many details
related to interacting with the DataONE API, such as creating MIME multipart
messages, encoding parameters into URLs and handling Unicode.

The clients allow the developer to communicate with nodes by calling native
Python methods which take and return native Python objects.

The clients also convert any errors received from the nodes into native
exceptions, enabling clients to use Python’s concise exception handling system
to handle errors.

The clients are arranged into the following class hierarchy:

.. graphviz::

  digraph G {
    dpi = 60;
    ratio = "compress";

    "REST Client\n(In D1 Common)" -> DataONEBaseClient

    DataONEBaseClient -> DataONEBaseClient_1_1 [weight=1000];
    DataONEBaseClient -> MemberNodeClient;
    DataONEBaseClient -> CoordinatingNodeClient;

    DataONEBaseClient_1_1 -> MemberNodeClient_1_1;
    DataONEBaseClient_1_1 -> CoordinatingNodeClient_1_1;

    MemberNodeClient -> MemberNodeClient_1_1;
    CoordinatingNodeClient -> CoordinatingNodeClient_1_1;

    MemberNodeClient -> DataONEClient;
    CoordinatingNodeClient -> DataONEClient;

    DataONEBaseClient_1_1 -> DataONEClient [style=invis, weight=1000]
  }


The classes without a version designator implement functionality defined in
v1.0 of the DataONE service specifications. The classes with the v1.1 designator
extend the v1.0 classes with extra functionality defined in the v1.1 service
specifications.

Because the v1.1 classes are derived from the v1.0 classes, the v1.1 classes
support both v1.0 and v1.1 APIs.


:DataONEBaseClient:
  Implemented in :ref:`d1_client_d1baseclient`. Contains methods that allow
  access to the v1.0 level APIs that are common to CN and MN clients.

:DataONEBaseClient_1_1:
  Implemented in :ref:`d1_client_d1baseclient_1_1`. Adds support for the v1.1
  level APIs that are common to CN and MN clients.

:MemberNodeClient:
  Implemented in :ref:`d1_client_mnclient`. Contains methods that allow access
  to the v1.0 level APIs that are specific to MNs.

:MemberNodeClient_1_1:
  Implemented in :ref:`d1_client_mnclient_1_1`. Adds support for the v1.1 level
  APIs that are specific to MNs.

:CoordinatingNodeClient:
  Implemented in :ref:`d1_client_cnclient`. Contains methods that allow access
  to the v1.0 level APIs that are specific to CNs.

:CoordinatingNodeClient_1_1:
  Implemented in :ref:`d1_client_cnclient_1_1`. Adds support for the v1.1 level
  APIs that are specific to CNs.

:DataONEClient:
  Implemented in :ref:`d1_client_d1client`. Uses CN- and MN clients to perform
  high level operations against the DataONE infrastructure.

:DataONEObject:
  Implemented in :ref:`d1_client_d1client`. Wraps a single DataONE Science
  Object and adds functionality such as resolve and get.

:SolrConnection:
  Implemented in :ref:`d1_client_solr_client`. Provides functionality for
  working with DataONE's Solr index, which powers the ONEMercury science data
  search engine.
