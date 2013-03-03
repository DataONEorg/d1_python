Setting up a stand-alone test instance
======================================

GMN can set up as a stand-alone test instance in which no interaction with any
of the DataONE infrastructure environments are established. Such a setup is
useful for various testing scenarios, such as when creating scripts for
populating GMN and running performance testing.

When setting up a stand-alone instance of GMN, the :doc:`setup-env`,
:doc:`setup-tier` and :doc:`setup-async` sections do NOT have to be performed.

A modified version of the :doc:`setup-authn-server` and
:doc:`setup-authn-client` sections must be performed. See :doc:`setup-local-ca`
for details.

In the :doc:`setup-registration` section, only the steps under *Submitting a
Node document* must be performed. It should be verified that the Node document
is rendered correctly, though submitting it will not work (as CNs will not
accept a submitted Node document without a matching DataONE issued certificate).

