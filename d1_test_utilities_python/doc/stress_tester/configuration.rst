Configuration
=============

Each test has a configuration file that specifies the Multi-Mechanize
parameters, such as how long the test should run and how many threads to use.
The file is called `config.cfg` and is in the root folder for each test. For
instance, the test for `MNStorage.create()` has this file in
`projects/create/config.cfg`. See the `Multi-Mechanize home page
<http://multimechanize.com>`_ for information on how to use this file. In the
descriptions on how to run the tests, it is assumed that the settings in
`config.cfg` have already been configured.


Shared settings
~~~~~~~~~~~~~~~

To avoid duplication of settings that are likely to be the same for each
test, the tests each read some of their configuration from the file stored in
`./shared/settings.py`. The main setting in this file is the Base URL
for the Member Node which is being tested.


Subjects
~~~~~~~~



Certificates
~~~~~~~~~~~~

The tests rely on a set of certificates. See :doc:`certificates` for details.



