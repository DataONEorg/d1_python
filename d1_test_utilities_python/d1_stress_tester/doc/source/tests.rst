Tests
=====

Multi-Mechanize Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each test has a configuration file that specifies the Multi-Mechanize
parameters, such as how long to run the test and how many threads to use. The
file is called `config.cfg` and is in the root folder for each test. For
instance, the test for `MNStorage.create()` has this file in
`projects/create/config.cfg`. See the `Multi-Mechanize home page
<http://multimechanize.com>`_ for information on how to use this file. In the
descriptions of the individual tests below, it is assumed that the settings in
`config.cfg` have already been configured.


Shared test configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

To avoid duplication of settings that are likely to be the same for each
test, the tests each read some of their configuration from the file stored in
`/projects/_shared/settings.py`. The main setting in this file is the Base URL
for the Member Node which is being tested.


Certificate configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

The tests rely on a set of certifcates. See :doc:`certificates` for details.


MNStorage.create()
~~~~~~~~~~~~~~~~~~

Stress testing of the `MNStorage.create()` API.

This test concurrently creates many small, randomized science objects on the
Member Node. Each science object has System Metadata with a number of randomly
selected parameters.

To facility stress testing of the `MNRead.listObjects()` API, the science
objects are created with access permissions for a subset of the subjects.

To run the test::

  $ multimech-run projects/create/


MNRead.listObjects()
~~~~~~~~~~~~~~~~~~~~

Stress testing of the `MNRead.listObjects()` API.

This test concurrently calls listObjects for many different subjects on the
Member Node.

To run the test::

  $ multimech-run projects/list_objects/



