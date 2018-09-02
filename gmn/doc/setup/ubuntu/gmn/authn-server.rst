.. _snake_oil_cert:

Install non-trusted server side certificate
===========================================

:doc:`Authentication and authorization </gmn/use-authn-and-authz>` in DataONE is based on :term:`X.509` (SSL) certificates.

GMN authenticates to incoming connections from :term:`DataONE` :term:`client`\ s and other parts of the DataONE infrastructure, such as :term:`CN`\ s by providing a :term:`server side certificate` during the SSL/TLS handshake.

By default, a stand-alone instance of GMN uses a non-trusted, self-signed,
"snakeoil" server side certificate. This defers the purchase of a publicly trusted certificate from a 3rd party :term:`CA` such as VeriSign or Thawte until the stand-alone instance is registered with DataONE.

A stand-alone instance that is not going to be registered with DataONE can use the non-trusted certificate indefinitely. Such a certificate is as secure as a publicly trusted certificate when used locally.

If you already have a publicly trusted certificate that you intend to use, you can still install the snakeoil certificate here and just follow the instructions to upgrade it later.

The snakeoil server side certificate is automatically generated when the
``ssl-cert`` package is installed.

Run the commands below to:

* Ensure that the ``ssl-cert`` package is installed
* Copy the certificate and key to the GMN standard locations

.. _clip2:

::

  sudo -H bash -c '
    apt install --yes ssl-cert
    mkdir -p /var/local/dataone/certs/server
    cp /etc/ssl/certs/ssl-cert-snakeoil.pem /var/local/dataone/certs/server/server_cert.pem
    cp /etc/ssl/private/ssl-cert-snakeoil.key /var/local/dataone/certs/server/server_key_nopassword.pem
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip2">Copy</button>
..


Updating the certificate if the IP address changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The DN of the snakeoil certificate matches the IP address of the server. If
the IP adddress of the server is changed some time in the future, the snakeoil
certificate can be regenerated with:

.. _clip3:

::

  # Only run if the server name or IP address changes.
  sudo -H bash -c '
    make-ssl-cert generate-default-snakeoil --force-overwrite;
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip3">Copy</button>
..

Then, copy the new versions to the GMN standard locations as described above.
