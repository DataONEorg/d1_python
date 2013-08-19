.. _local_ca:

Setting up a local CA
=====================

These instructions describe how to:

* Set up a local CA
* Create a local CA root certificate

No background information is provided in these instructions, as such information
is readily available on the web. See for instance,
`SSL Certificates HOWTO <http://www.tldp.org/HOWTO/SSL-Certificates-HOWTO/x120.html>`_.

Prepare for setting up a local CA::

  $ cd /usr/lib/ssl/misc/
  $ sudo pico CA.pl

* Comment out the existing line starting with ``$SSLEAY_CONFIG`` by putting a
  hash mark ("#") in front of it. Then, add this line::

  $SSLEAY_CONFIG="-config /etc/ssl/local_ca/openssl.cnf";

* Change ``$CATOP`` to ``"/etc/ssl/local_ca";``
* Optionally, change ``$DAYS`` to ``3650`` (signed certs are valid for 10 years)
* Optionally, change ``$CADAYS`` to ``10950`` (the CA is valid for 30 years)


Set up work area for local CA::

  $ sudo mkdir /etc/ssl/local_ca
  $ cd /etc/ssl/local_ca

Set up a new openssl.cnf file for the local CA::

  $ sudo cp ../openssl.cnf .

Modify openssl.cnf to use the local_ca work area::

  $ sudo pico openssl.cnf

* Change ``dir`` (under ``CA_default``) to ``/etc/ssl/local_ca``.

Make the CA utilities more easily accessible::

  $ sudo ln -s /usr/lib/ssl/misc/* /usr/local/bin/

Create the local CA::

  $ sudo echo 01 | sudo tee serial > /dev/null
  $ sudo CA.pl -newca

* For the common Name (CN) use something like "Local CA root".

You now have a local CA root certificate:

| ``cacert.pem``: The local CA root cert
| ``private/cakey.pem``: The local CA root cert private key
