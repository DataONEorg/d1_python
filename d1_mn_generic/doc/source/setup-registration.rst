Register the MN
===============

Before a Member Node can participate in the DataONE infrastructure, it must be
registered. Registering the MN involves the following steps:

#. Selecting a DataONE environment for the MN.

#. Creating a DataONE identity that is valid in the selected environment.

#. Obtaining a client side certificate from DataONE. The certificate enables the
   MN to authenticate itself in the selected environment.

#. Creating a Node document. The Node document describes the MN and
   the level at which it will participate in the DataONE infrastructure

#. The Node document is submitted to DataONE over a TLS/SSL connection that has
   been authenticated with the certificate obtained above.

#. DataONE evaluates the submission. Upon approval, the registration is
   complete.

Perform the steps in order, as each step depends on earlier steps.


Selecting a DataONE environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default production environment, DataONE maintains several
separate environments for use when developing and testing DataONE components.
There are no connections between the environments. For instance, certificates,
DataONE identities and science objects are exclusive to the environment in
which they were created.

The environments are:

=========== ============================== ===================================================================================================
Environment URL                            Description
=========== ============================== ===================================================================================================
Development https://cn-dev.dataone.org     Unstable components under active development.
Staging     https://cn-stage.dataone.org   Testing of release candiates.
Sandbox     https://cn-sandbox.dataone.org Like Production, but open to test instances of MNs. May contain both test and real science objects.
Production  https://cn.dataone.org         Stable production environment for use by the public.
=========== ============================== ===================================================================================================

You may chose to register your MN in the Production environment. However, if
your MN is more experimental in nature, for instance, if the purpose is
to learn more about the DataONE infrastructure or if this MN will be populated
with objects that may not be of production quality, then one of the other
environments should be selected.

It may be easier to obtain a certificate for the development, staging or sandbox
environment than for the production environment.

Depending on which environment you select, substitute **<environment-url>** in
the instructions below with one of the URLs in the table.


Create a DataONE identity
~~~~~~~~~~~~~~~~~~~~~~~~~

Use the DataONE Identity Manager to create a DataONE identity for the
administrator / contact for the new MN.

  Visit **<environment-url>**/portal/ and follow the instructions.


Obtaining a client side certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To obtain a client side certificate, generate a certificate request and email
it to DataONE. DataONE will return a signed certificate by email.

  Create the private key for the certificate::

    $ openssl genrsa -des3 -out my_member_node.key 4096

  Create the certificate request::

    $ openssl req -new -key my_member_node.key -out my_member_node.csr

  You will be prompted for information that, combined, will become the
  Distinguished Name (DN) for this MN. Please supply *Country Name*, *State or
  Province Name*, *Locality Name*, *Organization Name* and *Common Name*. The
  remaining fields may be left blank. To remove the default value from a field,
  type a period ("."). To leave a field blank, press Enter.

Note: Anyone who has the private key can act as your Node in the DataONE
infrastructure. Keep the private key safe. If your private key becomes
compromised, please inform DataONE so that the certificate can be revoked.

  Email the my_member_node.csr file to DataONE at cert-requests@dataone.org. In
  the email, include for which environment you would like the certificate to be
  signed. The certificate will only be trusted in that environment.


Installing the client side certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  When the signed client side certificate has been received from DataONE,
  move it and its private key to the
  ``/var/local/dataone/mn_generic/service/certificates`` folder.

  Edit the GMN settings file::

  ``/var/local/dataone/mn_generic/service/settings_site.py``.

  Set the paths to the certificate files in CLIENT_CERT_PATH and
  CLIENT_CERT_PRIV_KEY_PATH.


Registering the MN with DataONE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GMN generates the Node document automatically based on the settings in
``settings_site.py``.

  Edit the GMN settings file::

  ``/var/local/dataone/mn_generic/service/settings_site.py``.

  Each setting is described in the file.

  After editing ``settings_site.py``, check if the Node document is successfully
  generated::

    ./manage.py register_node_with_dataone --view

  For more information about the Node document, refer to
  http://mule1.dataone.org/ArchitectureDocs-current/apis/Types.html#Types.Node

  If the Node document is successfully generated and displayed, register the
  MN by submitting the Node document to DataONE::

    ./manage.py register_node_with_dataone


A new MN must be approved by DataONE. The person that is registered as
*contactSubject* in the Node document, will be contacted by email with the
outcome of the approval process. After the Node has been approved, CNs will
start processing the information on the node.
