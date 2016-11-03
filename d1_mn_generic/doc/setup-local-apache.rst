Install and configure Apache
============================

Setting up Apache.

The :term:`mod_ssl` module handles TLS/SSL connections for GMN and validates
client side certificates. It is included in the apache2-common package,
installed in the next step.

The :term:`mod_wsgi` module enables Apache to communicate with :term:`Django`
and GMN.

  Install Apache2 and required modules::

    $ sudo apt-get --yes install apache2 libapache2-mod-wsgi

  Enable modules::

    $ sudo a2enmod wsgi ssl rewrite

  Install the GMN virtual host file and custom apache2.conf file::

    $ cd /var/local/dataone/gmn/lib/python2.7/site-packages/deployment
    $ sudo cp gmn-ssl.conf /etc/apache2/sites-available/
    $ sudo cp forward_http_to_https.conf /etc/apache2/conf-available

  Enable the HTTP forwarding configuration::

    $ sudo a2enconf forward_http_to_https

  Enable the GMN Virtual Host::

    $ sudo a2ensite gmn-ssl

