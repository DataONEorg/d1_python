Testing the replication processing
==================================

The DataONE Test Utilities for Python includes the Replication Tester (RepTest), a Python app that performs basic testing of the replication functionality of a Tier 4 MN. This describes how to set GMN up for testing with RepTest.

RepTest takes on the roles of the CN and another MN. So, for the test to be successful, GMN must be set up to accept RepTest both as a CN and another MN during the transfer of the object being replicated. GMN must also be set up to call back to RepTest during replication instead of to the root CN.


Without certificates
~~~~~~~~~~~~~~~~~~~~

The simplest way to test the replication functionality is to turn off access control for objects and the replication API methods in GMN. Of course, this means that the access control is not tested.

<TODO: Describe how to set this up>


Changing root CN
----------------

RepTest needs to be set up as the root CN for the GMN instance being tested. This is done by modifying ``DATAONE_ROOT`` in ``settings.py`` to point to RepTest. E.g., if RepTest is running on the same machine as GMN::

  DATAONE_ROOT = 'http://localhost:8181'

The port and network interface on which RepTest listens is configurable.


Background
``````````

The first time that GMN handles a request after startup, it will call
``CNCore.listNodes()`` on the root CN in the environment in which it is set up to find information about the other nodes in the environment. GMN will perform this call at even intervals to refresh its cache of the information.

When RepTest is set to be the root CN, RepTest receives this initial call. RepTest responds with a customized list of nodes holding only a CN and a MN. These nodes both point back to RepTest, thus setting the GMN instance up to accept calls from RepTest as if they originate from a CN. In addition, the replication related calls that GMN makes to the CN and MN replication counterpart become directed to RepTest, which uses them for orchestrating the replication process and checking that the MN is performing the replication correctly.

If GMN is not set up to use RepTest as a root CN, RepTest will abort testing with a authentication related exception. For instance, if RepTest calls
``MNRead.getReplica()``, the exception may look like the following:

::

  d1_common.types.exceptions.NotAuthorized: name: NotAuthorized
  errorCode: 401
  detailCode: 0
  description:
    A CN has not authorized the target MN, "public" to create a replica of "anterior1.jpg".
    Exception received from the CN:
    name: NotAuthorized
    errorCode: 401
    detailCode: 4871
    description: There is no Member Node registered with a node subject matching public
  nodeId: urn:node:mnDevGMN

This somewhat confusing error message is a NotAuthorized exception from GMN with a description field that contains the exception that was received from the CN which, in this case, is also a NotAuthorized exception.

The exception is raised because GMN called a real CN to get authorization for a call to ``MNRead.getReplica()``. Since the replication was initiated by RepTest and not the real CN, the real CN rejects the request.
