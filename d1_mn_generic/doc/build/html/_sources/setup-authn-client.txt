Step 6: Client Side Authentication
==================================

The :term:`DataONE` infrastructure uses :term:`X.509` :term:`certificate`\ s for
authenticating :term:`client`\ s.


CILogon CA certificates
-----------------------

:term:`CILogon` provides three :term:`LOA`\ s. These instructions set GMN up to
accept all three. Ubuntu comes with a complete set of commonly trusted
:term:`CA` :term:`certificates`. However, we do not want GMN to accept
certificates signed by these, so we establish a separate CA store for the
CILogon CAs.

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

Set Apache up to accept optional :term:`SSL` :term:`Client Side Authentication`.
Any certificate provided by the client must be signed by the :term:`CILogon`
:term:`CA`.

Also see: :doc:`setup-example-default-ssl`.


Enable Client Side Authentication:

Edit ``/etc/apache2/sites-available/default-ssl``.

Add / modify::

	SSLVerifyClient optional
	SSLVerifyDepth  10


Forward Client Side Authentication information to GMN:

* To get information from the certificate used in the client side authentication
  available to GMN, we turn on “SSLOptions +StdEnvVars” for .wsgi files (the GMN
  wsgi handler is called gmn.wsgi).

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



:doc:`setup-python-deps`
