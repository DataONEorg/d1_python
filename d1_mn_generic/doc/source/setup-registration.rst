Register the new Member Node with DataONE
=========================================

A Member Node (MN) integrates itself into DataONE through a process called Node
Registration. Registering the MN allows the Coordinating Nodes (CNs) to
synchronize content, index the metadata and resource maps, and replicate its
content to other MNs. Typically, a test instance of a new MN is registered into
one of the testing environments and tested before registering the
production-ready MN into the production DataONE environment.

Registering the MN involves the following steps:

#. Creating a DataONE identity in the environment that was selected in the
   :doc:`setup-env` step.

#. Submitting a Node document. The Node document describes the MN and
   the level at which it will participate in the DataONE infrastructure.

#. DataONE evaluates the submission. Upon approval, the registration is
   complete, and the Node is part of the DataONE infrastructure.

Perform the steps in order, as each step depends on earlier steps.


Create a DataONE identity
~~~~~~~~~~~~~~~~~~~~~~~~~

This step must be performed by the person who will be the contact for the new
MN. The contact person is often also the administrator for the MN.

Each DataONE environment has a web-based Identity Manager where DataONE
identities are created and maintained. To create a DataONE identity, you will
use the Identity Manager to authenticate with a :term:`CILogon`-recognized
identity, and then attach your name and contact email. At this point, DataONE
will validate this information manually.

To register the administrative contact's DataONE identity in the target
environment, perform the following steps:

#. Navigate to the Identity Manager of the target environment:

   =========== ==========================================
   Environment Identity Manager URL
   =========== ==========================================
   Production  https://cn.dataone.org/portal
   Staging     https://cn-stage.test.dataone.org/portal
   Sandbox     https://cn-sandbox.test.dataone.org/portal
   Development https://cn-dev.test.dataone.org/portal
   =========== ==========================================

#. Follow the prompts to authenticate against your :term:`Identity Provider`. If
   your institution is not listed, you can use a Google or ProtectNetwork account.

#. Once authenticated and back at the DataONE portal, supply your name and email,
   and then press **Register**

#. Record (copy to clipboard) the identity string shown in the 'Logged in as' field.
   This value is taken from the CILogon certificate issued when you authenticated
   against your chosen :term:`Identity Provider`, and is also a DataONE subject.

#. Paste this value into the contactSubject field of the Node document you plan to
   submit in the next step.

#. DataONE requires that DataONE subjects that are to be used as contacts for
   MNs be verified. To verify the account, send an email to support@dataone.org.
   In the email, include the identity string obtained in the step above and request
   that the account be verified.  You do not need to wait for a reply to continue
   to the next step.


Configure the Member Node information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most of the values that are set up in this section are described in the `Node
document section in the architecture documentation`_.

The Node document is a set of values that describe a MN or CN, its internet
location, and the services it supports.


.. _Node document section in the architecture documentation: http://mule1.dataone.org/ArchitectureDocs-current/apis/Types.html#Types.Node

GMN generates the Node document automatically based on the settings in
``settings_site.py``.

  Create a copy of the GMN settings template and edit the settings::

    $ cd /var/local/dataone/gmn/lib/python2.6/site-packages/service
    $ sudo cp settings_site_template.py settings_site.py

Django requires a unique, secret key to be set up for each application.

  Set a random secret key in ``settings_site.py``::

    $ sudo sed -i 's/^SECRET_KEY.*/SECRET_KEY = '\'`openssl rand -hex 32`\''/' settings_site.py

  Edit ``settings_site.py``::

    $ sudo pico /var/local/dataone/gmn/lib/python2.6/site-packages/service/settings_site.py

  Modify the following settings:

  * NODE_IDENTIFIER: A unique identifier for the node of the form
    \urn:node:NODEID where NODEID is the node specific identifier. This value
    MUST NOT change for future implementations of the same node, whereas the
    baseURL may change in the future.

    NODEID is typically a short name or acronym. As the identifier must be
    unique, coordinate with your DataONE developer contact to establish your
    test and production identifiers. The conventions for these are
    ``urn:node:mnTestNODEID`` for the development, sandbox and staging
    environments and ``urn:node:NODEID`` for the production environment. For
    reference, see the `list of current DataONE Nodes
    <http://mule1.dataone.org/OperationDocs/membernodes.html>`_.

    E.g.: \urn:node:USGSCSAS (for production) and \urn:node:TestUSGSCSAS (for
    testing).

  * NODE_NAME: A human readable name of the Node. This name can be used as a label
    in many systems to represent the node, and thus should be short, but
    understandable.

    E.g.: USGS Core Sciences Clearinghouse

  * NODE_DESCRIPTION: Description of a Node, explaining the community it serves
    and other relevant information about the node, such as what content is
    maintained by this node and any other free style notes.

    E.g.: US Geological Survey Core Science Metadata Clearinghouse archives
    metadata records describing datasets largely focused on wildlife biology,
    ecology, environmental science, temperature, geospatial data layers
    documenting land cover and stewardship (ownership and management), and more.


  * NODE_BASEURL: The base URL of the node, indicating the protocol, fully
    qualified domain name, and path to the implementing service, excluding the
    version of the API.

    E.g.: \https://server.example.edu/app/d1/mn


  * NODE_SUBJECT: Specify the subject for this Node (retrieved from the client
    certificate provided by DataONE)

  * NODE_CONTACT_SUBJECT: The appropriate person or group to contact regarding
    the disposition, management, and status of this Member Node. The
    contactSubject is an X.509 Distinguished Name for a person or group that can
    be used to look up current contact details (e.g., name, email address) for
    the contact in the DataONE Identity service. DataONE uses the contactSubject
    to provide notices of interest to DataONE nodes, including information such
    as policy changes, maintenance updates, node outage notifications, among
    other information useful for administering a node. Each node that is
    registered with DataONE must provide at least one contactSubject that has
    been verified with DataONE.

    The contactSubject must be the subject of the DataONE identity that was
    created in the :ref:`previous step <create_dataone_identity>`.

    E.g.: CN=My Name,O=Google,C=US,DC=cilogon,DC=org


  * NODE_REPLICATE: Set to true if the node is willing to be a
    :term:`replication target`, otherwise false.


  * DATAONE_ROOT: Select the environment that matches the one that was
    selected in :doc:`setup-env`.

    E.g.: https://cn-stage.dataone.org/cn


  * PASSWORD: Set the password that was selected for the gmn user in
    :doc:`setup-postgresql`.


Submit Member Node information to DataONE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Member Node information is submitted to DataONE in a Node document. GMN
automatically generates the Node document based on the settings configured in
the previous step.

  After editing ``settings_site.py``, check if the Node document is successfully
  generated::

    $ su gmn
    $ python /var/local/dataone/gmn/lib/python2.6/site-packages/service/manage.py register_node_with_dataone --view

  If the Node document is successfully generated, an XML document will be
  displayed. For more information about this document, refer to
  http://mule1.dataone.org/ArchitectureDocs-current/apis/Types.html#Types.Node

  When the Node document is successfully generated and displayed, register the
  MN by submitting the Node document to DataONE. The Node document is
  automatically submitted to DataONE over a TLS/SSL connection that has been
  authenticated with the certificate obtained in :doc:`setup-authn-client`.

  ::

    $ python lib/python2.6/site-packages/service/manage.py register_node_with_dataone

  * Check for a message saying that the registration was successful.

After running the script or running an automated registration, the Member Node
should email support@dataone.org to notify of the registration request.


DataONE evaluates the submission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DataONE evaluates the submitted Node document and contacts the person listed as
*contactSubject* in the Node document by email with the outcome of the approval
process. After the node has been approved, the MN is part of the infrastructure
environment in which it has been registered, and the CNs in that environment will
start processing the information on the node.
