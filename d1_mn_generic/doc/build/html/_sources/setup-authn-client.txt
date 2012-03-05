Client side authentication
==========================

In the :term:`DataONE` infrastructure, :term:`MN`\ s and :term:`CN`\ s use
:term:`X.509` client side :term:`certificate`\ s for authenticating
:term:`client`\ s and other DataONE nodes.

During :term:`client side authentication`, the client provides a certificate,
proving its identity to the server. A DataONE client or Node may connecty to
another Node without providing a client side certificate, but then gains only
public access on the Node.

For a client side certificate to be considered valid by the server, the server
must trust the :term:`CA` that signed the client side certificate. This step
sets up the CAs to be trusted.


CILogon CA certificates
-----------------------

:term:`CILogon` provides three :term:`LOA`\ s. These instructions set GMN up to
accept all three. Ubuntu comes with a complete set of commonly trusted
:term:`CA` certificates. However, DataONE Nodes should not accept certificates
signed by these, so we establish a separate CA store for the CILogon CAs.

  Download and install the CA certificates from CILogon::

    $ sudo -s
    # mkdir -p /var/local/dataone/ca
    # cd /var/local/dataone/ca
    # wget https://cilogon.org/cilogon-ca-certificates.tar.gz
    # tar xzf cilogon-ca-certificates.tar.gz
    # mv cilogon-ca/certificates/* .
    # rm -r cilogon-ca cilogon-ca-certificates.tar.gz
    # c_rehash .
    # <ctrl-d>


Apache SSL setup
----------------

Set Apache up to accept optional :term:`SSL` Client side authentication.

Setting the client side certificate to be optional allows a client to connect to
the Node without a certificate for anonymous access to public science data. If
the client does supply a certificate, the certificate must be valid, not
expired, and must be signed by the :term:`CILogon` :term:`CA`.

Also see: :doc:`setup-example-default-ssl`.

  Enable Client side authentication:

  Edit ``/etc/apache2/sites-available/default-ssl``.

  Add / modify::

    SSLVerifyClient optional
    SSLVerifyDepth  10

GMN needs to have access to the submitted client side certificate. Configure
mod_ssl to forward the certificate to the GMN WSGI handler in an environment
variable.

  Edit ``/etc/apache2/sites-available/default-ssl``.

  Add “wsgi” in the FilesMatch expression.

  Change::

    <FilesMatch "\.(cgi|shtml|phtml|php)$">
      SSLOptions +StdEnvVars
    </FilesMatch>

  to::

    <FilesMatch "\.(wsgi|cgi|shtml|phtml|php)$">
      SSLOptions +StdEnvVars
    </FilesMatch>


Use the CILogon CA certificates instead of the default ones.

  Add / modify ``SSLCACertificatePath``::

    SSLCACertificatePath /var/local/dataone/ca

  Restart Apache::

    $ apache2ctl restart

    Check for any error messages from Apache.


:doc:`setup-python-deps`
