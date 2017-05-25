Clients
=======

The client classes wrap all the DataONE API methods, hiding the many details related to interacting with the DataONE API, such as creating MIME multipart messages, encoding parameters into URLs and handling Unicode.

The clients allow the developer to communicate with nodes by calling native Python methods which take and return native Python objects.

The clients also convert any errors received from the nodes into native exceptions, enabling clients to use Python’s concise exception handling system to handle errors.

The clients are arranged into the following class hierarchy:

.. graphviz::

  digraph G {
    dpi = 72;
    edge [dir = back];

    "REST Client\n(In D1 Common)" -> DataONEBaseClient

    DataONEBaseClient -> DataONEBaseClient_1_1 [weight=1000];
    DataONEBaseClient -> MemberNodeClient;
    DataONEBaseClient -> CoordinatingNodeClient;

    DataONEBaseClient_1_1 -> MemberNodeClient_1_1;
    DataONEBaseClient_1_1 -> CoordinatingNodeClient_1_1;

    MemberNodeClient -> MemberNodeClient_1_1;
    CoordinatingNodeClient -> CoordinatingNodeClient_1_1;

    MemberNodeClient -> DataONEBaseClient_1_1 [style=invis];
    CoordinatingNodeClient -> DataONEBaseClient_1_1 [style=invis];

    DataONEBaseClient_1_1 -> DataONEBaseClient_2_0 [weight=1000];
    MemberNodeClient_1_1 -> DataONEBaseClient_2_0 [style=invis];
    CoordinatingNodeClient_1_1 -> DataONEBaseClient_2_0 [style=invis];

    DataONEBaseClient_2_0 -> MemberNodeClient_2_0;
    DataONEBaseClient_2_0 -> CoordinatingNodeClient_2_0;

    MemberNodeClient_1_1 -> MemberNodeClient_2_0;
    CoordinatingNodeClient_1_1 -> CoordinatingNodeClient_2_0;

    MemberNodeClient_2_0 -> DataONEClient;
    CoordinatingNodeClient_2_0 -> DataONEClient;
  }

The classes without version designators implement functionality defined in v1.0 of the DataONE service specifications. The classes with version designators implement support for the corresponding DataONE service specifications.

DataONEBaseClient

  The DataONEBaseClient classes contain methods that allow access to APIs
  that are common to Coordinating Nodes and Member Nodes.

  * d1_client.d1baseclient
  * d1_client.d1baseclient_1_1
  * d1_client.d1baseclient_2_0

MemberNodeClient

  The MemberNodeClient classes contain methods that allow access to APIs that
  are specific to Member Nodes.

  * d1_client.mnclient
  * d1_client.mnclient_1_1
  * d1_client.mnclient_2_0

CoordinatingNodeClient

  The CoordinatingNodeClient classes contain methods that allow access to APIs
  that are specific to Coordinating Nodes.

  * d1_client.cnclient
  * d1_client.cnclient_1_1
  * d1_client.cnclient_2_0

DataONEClient

  The DataONEClient uses CN- and MN clients to perform high level operations
  against the DataONE infrastructure.

  * d1_client.d1client

DataONEObject

  Wraps a single DataONE Science Object and adds functionality such as resolve
  and get.

  * d1_client.d1client

SolrConnection

  Provides functionality for working with DataONE's Solr index, which powers the
  ONEMercury science data search engine.

  * d1_client.solr_client
