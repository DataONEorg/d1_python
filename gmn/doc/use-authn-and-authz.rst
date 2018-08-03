Authentication and authorization
================================

DataONE specifies a security model for Member Nodes. The model covers most aspects of how clients authenticate and which content they are authorized for. Some aspects are left open for Member Nodes to implement as best fits their requirements.

This section outlines the main aspects of how authentication and authorization is implemented in GMN and how to configure GMN and clients. In-depth coverage of these topics is provided in the `DataONE architecture documentation
<https://releases.dataone.org/online/api-documentation-v2.0.1/index.html>`_.


Authentication
~~~~~~~~~~~~~~

In DataONE, authentication is the process of confirming the identity claimed by a person or system that connects to a node in order to call the node's DataONE REST API methods.

A person or system can connect to a node without claiming an identity. This is done by connecting via HTTPS (or HTTP for Tier 1 nodes) without providing a
:term:`X.509` (SSL) :term:`client side certificate`. In this case, the connection is granted access only to publicly available APIs and objects.

To claim an identity, the person or system connects with a client side certificate. The certificate must be issued by a :term:`CA` that is trusted by the node. A DataONE compliant serialization of the certificate :term:`DN`
becomes the primary DataONE subject. The certificate can also contain an X.509 v3 extension that hold additional DataONE subjects in the form of equivalent identities and group memberships.

When a node first receives an incoming connection with a client side certificate, it does basic validation of the certificate itself. This includes checking that the certificate was issued by a trusted CA, that it has not expired, has not been revoked and has not been tampered with. After the certificate has passed these tests, the node extracts the primary subject and any other subjects from the certificate. These become the authenticated subjects for the connection and authentication is complete.

GMN uses Apache for performing the basic validation of the certificate. If a certificate is provided but is invalid, Apache will return an error to the client, indicating why the certificate failed validation and will then terminate the connection.


Authorization
~~~~~~~~~~~~~~

In DataONE, authorization is the process of confirming that an authenticated subject has access to a DataONE REST API method or object. Authorization happens each time a REST API call is made. When the call is made, the node will look at the list of authenticated subjects that is associated with the connection through which the call was made. If the list of authenticated subjects does not include a subject to which access to the REST API method has been granted, authorization is denied and GMN returns a 401 NotAuthorized exception to the client.

.. _crud_perm:

Permissions for create, update and delete
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DataONE does not specify how Member Nodes should control access to the APIs that allow users to create, update and delete contents on the node. GMN controls the access to these APIs with a whitelist. If a subject that is not in the whitelist attempts to call, for instance, ``MNStorage.create()``, GMN will return a DataONE exception such as this (formatted for readability)::

  Exception: NotAuthorized
  errorCode: 401
  detailCode: 0
  description:
    Access allowed only for subjects with Create/Update/Delete permission.
    Active subjects:
      authenticatedUser (equivalent),
      public (equivalent),
      CN=First Last,O=Google,C=US,DC=cilogon,DC=org (primary)

This means that the connection was made with a certificate in which the subject was ``CN=First Last,O=Google,C=US,DC=cilogon,DC=org`` and that this subject was not in GMNs whitelist for create, update and delete.

To create a whitelist with this subject, first create a file, for instance,
``whitelist.txt``. The most convenient location for this file is in the
``gmn`` folder::

  $ [ `whoami` != gmn ] && sudo -Hsu gmn
  $ cd /var/local/dataone/gmn_venv/lib/python2.7/site-packages/gmn
  $ nano whitelist.txt

In this file, add a line with an exact copy of the subject string marked as
``primary`` in the NotAuthorized exception (``CN=First Last,O=Google,C=US,DC=cilogon,DC=org`` in this case).

Blank lines and lines starting with "#" are ignored in the whitelist file, allowing comments. The remaining lines must each contain a separate subject.

Then, add the entries in the whitelist text file to GMN's database with the following command::

  $ python manage.py set_whitelist whitelist.txt

Any existing subjects in the database are cleared before adding the subjects from the whitelist file. So subjects can be added or removed from the whitelist by adding or removing them in the file and then synchronizing with the database by running the command above.


Creating authenticated connections to your Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create an authenticated connection to your Node, you must connect over HTTPS and provide a client side certificate. For a stand-alone node, only the local CA is trusted by default. So only certificates issued by this CA can be used. If the GMN instance is joined to DataONE, it is set up to also trust certificates issued by CILogon and DataONE.

In addition, the certificate must be for a subject that has the rights required for performing the operation(s) the client intends to perform after connecting. For instance, GMN requires that the subject used in connections that create content on the Node validate against an internal :ref:`whitelist <crud_perm>`.

For automated tasks, certificates issued by the local CA are preferred. DataONE does not issue certificates for clients, so cannot be used for this purpose and certificates issued by CILogon are secured by having a time limit of 18 hours, making them unsuitable for automated tasks.

When running as a regular user, the local CA must be used for a stand-alone instance. The local CA can also be used for a public instance but CILogon is a more secure choice due to the 18 hour expiration time.


Authenticating without a certificate
------------------------------------

In a stand-alone testing environment, where network access to the GMN instance is strictly limited, it is possible to simply add ``public`` to the
:ref:`whitelist for create, update and delete <crud_perm>`. Because the public subject is assigned to all connections, this allows access to create, update and delete objects on the node without any authentication.

Thus, this mode allows modifying node contents when connecting entirely without a certificate. It also lets GMN be set up for access over regular HTTP.


Authenticating with any trusted certificate
-------------------------------------------

Connections that are made with any certificate that is trusted by GMN are assigned the ``authenticatedUser`` subject. So, adding this subject to the
:ref:`whitelist for create, update and delete <crud_perm>` enables anyone that connects with a trusted certificate to alter content on the Node. This is highly insecure if the Node is set up to trust CILogon, as anyone can obtain a CILogon certificate through OpenID. However, it may be useful if the node exposes only public objects and so, does not need to trust CILogon.
