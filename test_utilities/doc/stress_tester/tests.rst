Tests
=====

Checking the test setup
~~~~~~~~~~~~~~~~~~~~~~~

Before the tests are run via ``multimech-run``, they can be checked by running them directly. When a test script is run directly, it will execute a single instance of the test and any issues are displayed directly as an exception trace. When tests are run via ``multimech-run``, exceptions are only counted, not displayed. For example, to execute a single instance of the
``MNStorage.create()`` test, normally started with ``multimech-run projects/create``, run
``./projects/create/test_scripts/tier_3_mn_storage_create.py``.


Checking for valid responses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To keep the load on the computer running the stress tests to a minimum, the tests do not attempt to deserialize the documents returned by the APIs being tested. Instead, they perform a simple check for the "200 OK" HTTP status code that the APIs are expected to return together with a valid DataONE data type upon successful completion.


.. _object_subject_list:

Creating and using test objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many of the tests require a set of test objects to be available on the MN being tested and a list of the objects that are available for tests. The
``MNStorage.create()`` stress test has the secondary purpose of creating the test objects.

The tests use either publicly accessible test objects or access controlled objects. Depending on the required type of object, a test reads a file containing a list of pubclicly accessible objects or a file containing a list of access controlled objects plus a list of subjects that have access to each object.

Each line in the file used for publicly accessible objects is an object identifier. The default location is ``./generated/public_objects.txt`` and can be modified in ``settings.py``. The file is UTF-8 encoded.

Each line in the file used for access controlled objects contains object identifier, a tab separator and a subject that has at least read access to the object. If the object is readable by more than one subject, the object identifier is repeated on multiple lines, each with a separate subject.

GMN includes a management command to generate these files. Typical usage is::

  $ ./manage.py generate_object_list --public public_objects.txt
  $ ./manage.py generate_object_list private_objects.txt

The location of the file can be configured in ``settings.py``. The default locations are::

  ./generated/public_objects.txt
  ./generated/private_objects.txt


General test procedure
~~~~~~~~~~~~~~~~~~~~~~

The tests all follow the same basic pattern:

- The tests work with two lists of objects, one for public and one for private
  objects. See :ref:`object_subject_list` for more information on how to set up
  these lists. Public objects can be read by any subject without authentication.
  Private objects are access controlled. They are accessible only to a specific
  list of one or more subjects.

- Read the public and private object lists from disk and store them as tables in
  memory.

- Create a number of threads, as specified in the ``threads`` section of the
  ``./projects/<test>/config.cfg``. The number of threads equals the number of
  concurrent connections that will be made to the MN.

- Each thread repeatedely selects random objects and subjects from the object
  tables and:

- Create a public or authenticated connection to the MN designated in the
  ``BASEURL`` setting in ``settings.py``. Public connections are made without a
  certificate and authenticated connections use one of the :ref:`generated
  certificates <certificates>`.

- Issue the API call to be stress tested to MN.

- Read and discard the entire returned stream.

- Check for a valid status code.

Some tests issue combinations of API calls concurrently.


MNStorage.create()
~~~~~~~~~~~~~~~~~~

Stress testing of the ``MNStorage.create()`` API.

This test concurrently creates many small, randomized science objects on the MN. Each science object has System Metadata with a number of randomly selected parameters.

In addition to stress testing the ``MNStorage.create()`` API, this test serves a second purpose, which is to populate the MN with test objects with a varied set of permissions for use by other stress tests. By default, the generates objects are small (1024 bytes) to prevent network bandwidth from becoming the limiting factor for performance.

The test generates permissions for randomly selected subjects in the
:ref:`object_subject_list`.

The test always connects with the ``subject_with_create_permissions``
certificate. This means that the MN must have been set up to allow the DataONE subject,
``CN=subject_with_create_permissions,O=d1-stress-tester,C=US,DC=d1-stress-tester,DC=com``
to create objects.

To run the test::

  $ multimech-run projects/create/


MNRead.get()
~~~~~~~~~~~~

Stress testing of the ``MNRead.get()`` API with public objects.

This test creates concurrent unauthenticated connections to the MN. For each connection, a random public object is selected and retrieved. The retrieved stream is discarded and the status code is checked.

See the ``MNRead.get_auth()`` test for testing with authenticated connections.

To run the test::

  $ multimech-run projects/get


MNRead.get_auth()
~~~~~~~~~~~~~~~~~~

Stress testing of the ``MNRead.get()`` API with authenticated connections and access controlled objects.

This test creates concurrent authenticated connections to the MN. For each connection, a random private object and subject with read access to the object is selected. A connection is made to the MN using the subject's certificate and the private object is retrieved. The retrieved stream id discarded and the status code is checked.

To run the test::

  $ multimech-run projects/get_auth/


MNRead.listObjects(), called by Coordinating Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stress testing of the ``MNRead.listObjects()`` API.

This test concurrently retrieves object lists with with random offset and page size, selected from the full range of objects. All connections are made with the
``subject_with_cn_permissions`` certificate. This means that the MN must be set up to allow the DataONE subject,
``CN=subject_with_cn_permissions,O=d1-stress-tester,C=US,DC=d1-stress-tester,DC=com``
to act as a Coordinating Node.

To run the test::

  $ multimech-run projects/list_objects/


MNRead.getLogRecords() called by client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stress testing of the ``MNRead.getLogRecords()`` API as used for getting the log records for a single private object by a client with regular permissions.

When called by a regular authenticted client, individual access control is applied to each object.

The test selects a random private object. It then creates an authenticated connection using the certificate for one of the subjects which have read access to the object.

To run the test::

  $ multimech-run projects/get_log_records_client/


MNRead.getLogRecords() called by Coordinating Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stress testing of the ``MNRead.getLogRecords()`` API as used by Coordinating Nodes to retrieve a large number of log records created within a given time period.

When a client successfully authenticates as a Coordinating Node, individual access control is not applied to objects.

The test selects a random private object. It then creates a connection and authenticates as a CN. It then retrieves all log records created within a given, random, date range.

To run the test::

  $ multimech-run projects/get_log_records_client/


.. _combination_1:

Combination 1
~~~~~~~~~~~~~

Stress testing using a of a combination of the MNRead.get(), MNRead.listObjects() and MNStorage.create() tests described above.

Before running this test, the MN must be populated with test objects, for instance by running the test for MNStorage.create(). The objects that are created during this test do not themselves become available for testing until the list of public and private objects is updated as described in
:ref:`object_subject_list`.

The individual stress tests use configuration values from the ``config.cfg``
file in the combination project directory, not the values in the ``config.cfg``
files in their own project directories.


.. _combination_2:

Combination 2
~~~~~~~~~~~~~

Stress testing using a combination of MNRead.get() and MNRead.getLogRecords().

Otherwise, like :ref:`combination_1`.

