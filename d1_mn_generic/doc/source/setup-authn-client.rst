Install the DataONE client side certificate
===========================================

In addition to its regular server role, GMN also acts as a client, initiating
connections to other Nodes.

During :term:`client side authentication`, the client provides a certificate,
proving its identity to the server. A DataONE client or Node may connecty to
another Node without providing a client side certificate, but then gains only
public access on the Node.


Obtaining a client side certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To obtain a client side certificate, generate a certificate request and email
it to DataONE. DataONE will return a signed certificate by email.

  Create the private key for the certificate request::

    $ sudo mkdir -p /var/local/dataone/certs/client
    $ cd /var/local/dataone/certs/client
    $ sudo openssl genrsa -des3 -out my_member_node.key 4096

  Create the certificate request::

    $ openssl req -new -key my_member_node.key -out my_member_node.csr

  * You will be prompted for information that, combined, will become the
    Distinguished Name (DN) for this MN. Please supply *Country Name*, *State or
    Province Name*, *Locality Name*, *Organization Name* and *Common Name*. The
    remaining fields may be left blank. To remove the default value from a
    field, type a period ("."). To leave a field blank, press Enter.

Note: Anyone who has the private key can act as your Node in the DataONE
infrastructure. Keep the private key safe. If your private key becomes
compromised, please inform DataONE so that the certificate can be revoked.

  * Email the my_member_node.csr file to DataONE at cert-requests@dataone.org.
    In the email, include for which environment you would like the certificate
    to be signed. The certificate will only be trusted in that environment.


Installing the client side certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  When the signed client side certificate has been received from DataONE, move
  it and its private key to the ``/var/local/dataone/certs/client`` folder.

  * Rename the files to client.crt and client.key.

  Other names may be used. If so, update the GMN ``settings_site.py`` file to
  match the new names.
