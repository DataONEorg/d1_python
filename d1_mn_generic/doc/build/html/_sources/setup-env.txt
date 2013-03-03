Select a DataONE environment
============================

In addition to the default production environment, DataONE maintains several
separate environments for use when developing and testing DataONE components.
There are no connections between the environments. For instance, certificates,
DataONE identities and science objects are exclusive to the environment in which
they were created.

The environments are:

=========== =================================== ======================================================================================================
Environment URL                                 Description
=========== =================================== ======================================================================================================
Production  https://cn.dataone.org              Stable production environment for use by the public.
Staging     https://cn-stage.test.dataone.org   Testing of release candiates.
Sandbox     https://cn-sandbox.test.dataone.org Like Production, but open to test instances of MNs. May contain both test and real science objects.
Development https://cn-dev.test.dataone.org     Unstable components under active development.
=========== =================================== ======================================================================================================

You may chose to register your MN in the Production environment. However, if
your MN is more experimental in nature, for instance, if the purpose is
to learn more about the DataONE infrastructure or if this MN will be populated
with objects that may not be of production quality, then one of the other
environments should be selected.

It may be easier to obtain a certificate for the development, staging or sandbox
environment than for the production environment.

Depending on which environment you select, substitute **<environment-url>**
and **<environment-name>** in the following pages of instructions with values
from the table.
