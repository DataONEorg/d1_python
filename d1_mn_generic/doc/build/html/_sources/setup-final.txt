Final configuration and startup
===============================

Initialize the database
~~~~~~~~~~~~~~~~~~~~~~~

::

  $ su gmn
  $ python /var/local/dataone/gmn/lib/python2.6/site-packages/service/manage.py syncdb
  $ <ctrl-d>

Filesystem permissions
~~~~~~~~~~~~~~~~~~~~~~

Set all the files to be owned by the gmn account, and to be writable by www-data::

  $ cd /var/local/dataone/
  $ sudo chown -R gmn:www-data .
  $ sudo chmod -R g+w .

Unlike the certificates, the contents of the private keys are sensitive. Set
them to be readable only by root and follow best practices for security to keep
root from being compromised.

Protect the certificate key files. The gmn user must have access to the client
key because the asynchronous replication task runs under that user.

  Set the private keys to be readable only by the gmn user::

    $ cd /var/local/dataone/certs
    $ sudo chmod 400 `find . -name '*.key'`

Set server to the UTC timezone (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GMN translates incoming date-times to UTC and provides outgoing date-times in
UTC. Because of this, it may also convenient to run the server in UTC, so that
server related date-times, such as the ones in logs, match up with date-times
stored in the database and provided in REST responses.

  ::

    $ sudo dpkg-reconfigure tzdata

  * Select Etc | UTC.


Firewall
~~~~~~~~

Open for HTTPS in the firewall::

  $ sudo ufw allow 443


Stand-alone mode
~~~~~~~~~~~~~~~~

When setting up a :doc:`stand-alone node <setup-local>`, set ``STAND_ALONE`` to
``True`` in the ``settings_site.py`` file::

  # Only perform this step on a stand-alone instance of GMN.
  $ sudo pico /var/local/dataone/gmn/lib/python2.6/site-packages/service/settings_site.py

* Set ``STAND_ALONE`` to ``True``.


Starting GMN
~~~~~~~~~~~~

GMN should now be ready to start. Simply restart Apache::

  $ sudo service apache2 restart

Check the Apache logs for error messages. In case of any issues, refer to
:doc:`troubleshooting` and :doc:`setup-resources`.

See :doc:`use` for notes on how to use the Node.
