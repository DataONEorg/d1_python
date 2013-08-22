API
===

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


:d1baseclient:
  Implements DataONEBaseClient, which contains methods that allow access to the
  v1.0 level APIs that are common to CN and MN clients.

:d1baseclient_1_1:
  Implements DataONEBaseClient_1_1, which adds support for the v1.1 level
  APIs that are common to CN and MN clients.

:mnclient:
  Implements MemberNodeClient, which contains methods that allow access to the
  v1.0 level APIs that are specific to MNs.

:mnclient_1_1:
  Implements MemberNodeClient_1_1, which adds support for the v1.1 level APIs
  that are specific to MNs.

:cnclient:
  Implements CoordinatingNodeClient, which contains methods that allow access
  to the v1.0 level APIs that are specific to CNs.

:cnclient_1_1:
  Implements CoordinatingNodeClient_1_1, which adds support for the v1.1 level
  APIs that are specific to CNs.

:d1client:
  Implements:
  - DataONEClient, which uses cn- and mn clients to perform high level
    operations against the DataONE infrastructure.
  - DataONEObject, which wraps a single object and adds functionality such as
    resolve and get.

:solrclient:
  Functionality for working with the Solr index behind Mercury. Will probably be
  moved into d1common. Ignore for now.

:logrecorditerator:
  Implements an iterator that iterates over the entire set of LogRecords
  for a DataONE node. Data is retrieved from the target only when required.


.. toctree::
  :numbered:
  :maxdepth: 2

  overview
  generated
