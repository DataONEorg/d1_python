Register the MN
===============

Registering the MN is a two step process. First, a client side certificate is
obtained for the MN. The MN will use the client side certificate to identify
itself in all calls to DataONE nodes.

Second, an XML document, called a Node document is submitted to a DataONE
CN. The document contains the information required by the DataONE infrastructure
to interact with the MN.


Selecting a DataONE environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition the the default production environment, DataONE maintains several
separate environments for use when developing and testing DataONE components.
There are no connections between the environments. For instance, certificates,
DataONE identities and science objects are exclusive to the environment in
which they were created.

The environments are:

* **Development**: Unstable components under active development.
* **Staging**: Testing of release candiates.
* **Sandbox**: Like Production, but open to test instances of MNs. May contain
  both test and real science objects.
* **Production**: Stable production environment for use by the public.

You may chose to register this MN deployment in the Production environment.
However, if this deployment is more experimental in nature, for instance, if the
purpose is to learn more about the DataONE infrastructure or if this MN will
be populated with objects that may not be of production quality, then one of
the other environments should be selected.

Depending on which environment you select, substitute **<env>** in the
instructions below with one of::

  https://cn-dev.dataone.org
  https://cn-stage.dataone.org
  https://cn-sandbox.dataone.org
  https://cn.dataone.org


Create a DataONE identify
~~~~~~~~~~~~~~~~~~~~~~~~~

Use the DataONE Identity Manager to create a DataONE identity for the
administrator / contact for the new MN.

Visit **<env>**/portal/ and follow the instructions.


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
  Province Name*, *Locality Name*, *Organization Name* and *Common Name*. Leave
  the remaining fields blank. For fields with a default, type a period (".").
  For fields without a default, press Enter.

Note: Anyone who has the private key can impersonate your Node in the DataONE
infrastructure. Keep the private key safe. If your private key becomes
compromised, please inform DataONE so that the certificate can be revoked.

  Email the my_member_node.csr file to DataONE at cert-requests@dataone.org. In
  the email, include for which environment you would like the certificate to be
  signed. The certificate will only be trusted in that environment.


Registering the MN with DataONE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This step can only be performed after the signed client side certificate has
been received from DataONE. See `Obtaining a client side certificate`_

Each DataONE Node has an XML document associated with it that describes the
various aspects of the Node, such as its URL, the services it supports and who
maintains and runs the Node. For now, it is necessary to manually edit this
file with information specific to this MN. A template is provided to simplify
this process.

  Customize the Node document.

  Copy the Node XML template::

    $ cd /var/local/dataone/mn_generic/service/stores/static/
    $ cp nodeRegistry_template.xml nodeRegistry.xml

  Edit the document:

    Edit
    ``/var/local/dataone/mn_generic/service/stores/static/nodeRegistry.xml``.

    Replace the upper case texts with information specific to your MN. The parts
    of the document that do not contain upper case text should remain unchanged.

    - **identifier**: A unique identifier for the node. This may initially be
      the same as the baseURL, however this value should not change for future
      implementations of the same node, whereas the baseURL may change in the
      future.

    - **name**: A human readable name of the Node.

    - **description**: Description of content maintained by this node and any
      other free style notes.

    - **baseURL**: The URL at which the Node is available.

    - **contactSubject**: The subject field exactly as it is displayed in the
      DataONE Identity Manager. See `Create a DataONE identify`_

    For more information about the Node document, refer to
    http://mule1.dataone.org/ArchitectureDocs-current/apis/Types.html#Types.Node


To register the new MN with DataONE, the Node XML document is submitted to
DataONE via a CN REST API. The connection to DataONE is made over TLS/SSL,
with the client side certificate that DataONE issued.

A command line tool is provided for submitting the registration.

  Register the MN with DataONE::

    $ cd /var/local/dataone/mn_generic/tools
    $ python register.py \
      --cert-path <path to the DataONE issued MN client side certificate> \
      --cert-key <path to the DataONE issued MN client side certificate key> \
      --dataone-url <dev>/cn
      ../service/stores/static/nodeRegistry.xml

A new MN must be approved by DataONE. The person that is registered as
*contactSubject* in the Node document, will be contacted by email with the
outcome of the approval process. After the Node has been approved, CNs will
start processing the information on the node.


Revisit the GMN configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the :doc:`setup-d1-gmn` step, setting the NODE_IDENTIFIER value was deferred
because it must be set up to match the value configured in this step.

  Edit: ``/var/local/dataone/mn_generic/service/settings_site.py``

  * Set NODE_IDENTIFIER to match the value specified in the identifier field
    in the Node XML document.


:doc:`setup-async`
