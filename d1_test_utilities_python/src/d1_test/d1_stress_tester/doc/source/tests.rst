Tests
=====

Multi-Mechanize Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each test has a configuration file that specifies the Multi-Mechanize
parameters, such as how long the test should run and how many threads to use.
The file is called `config.cfg` and is in the root folder for each test. For
instance, the test for `MNStorage.create()` has this file in
`projects/create/config.cfg`. See the `Multi-Mechanize home page
<http://multimechanize.com>`_ for information on how to use this file. In the
descriptions of the individual tests below, it is assumed that the settings in
`config.cfg` have already been configured.


Shared test configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

To avoid duplication of settings that are likely to be the same for each
test, the tests each read some of their configuration from the file stored in
`./shared/settings.py`. The main setting in this file is the Base URL
for the Member Node which is being tested.


Certificate configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

The tests rely on a set of certifcates. See :doc:`certificates` for details.


Checking for valid responses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To keep the load on the computer running the stress tests to a minimum, the
tests do not attempt to deserialize the documents returned by the APIs being
tested. Instead, they perform a simple check for the "200 OK" HTTP status code
that the APIs are expected to return together with a valid DataONE data type
upon successful completion.


MNStorage.create()
~~~~~~~~~~~~~~~~~~

Stress testing of the `MNStorage.create()` API.

This test concurrently creates many small, randomized science objects on the
Member Node. Each science object has System Metadata with a number of randomly
selected parameters.

In addition to stress testing the `MNStorage.create()` API, this test sets
the server up for the other stress tests by creating test objects with a varied
set of permissions for the subjects for which certificates have been generated.

This stress tester always connects with the `subject_with_create_permissions`
certificate. This means that the MN must have been set up to allow the DataONE
subject,
`DC=com,DC=d1-stress-tester,C=US,O=d1-stress-tester,CN=subject_with_create_permissions`
to create objects.

To run the test::

  $ multimech-run projects/create/

After running the test, run the `generate_subject_object_list.py` script. It
creates a list of the objects that exist on the MN and their permissions, for
use by the subsequent tests.


MNRead.listObjects()
~~~~~~~~~~~~~~~~~~~~

Stress testing of the `MNRead.listObjects()` API.

This test concurrently calls listObjects, requesting random sized result sets
from the full range objects.

This stress tester always connects with the `subject_with_cn_permissions`
certificate. This means that the MN must be set up to allow the DataONE subject,
`DC=com,DC=d1-stress-tester,C=US,O=d1-stress-tester,CN=subject_with_cn_permissions`
to act as a Coordinating Node. The `MNRead.listObjects()` API is intended
primarily for CNs.

To run the test::

  $ multimech-run projects/list_objects/


