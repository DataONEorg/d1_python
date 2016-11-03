Final configuration and startup
===============================

Filesystem permissions
~~~~~~~~~~~~~~~~~~~~~~

  Set all the files to be owned by the gmn account, and to be writable by www-data::

    $ sudo chown -R gmn:www-data /var/local/dataone/
    $ sudo chmod -R g+w /var/local/dataone/

Unlike the certificates, the contents of the private keys are sensitive. Set
them to be readable only by gmn and follow best practices for security to keep
root or gmn from being compromised.

  Set the private keys to be readable only by the gmn user::

    $ sudo chmod 400 `find /var/local/dataone/certs -name '*_key*'`


Initialize the database
~~~~~~~~~~~~~~~~~~~~~~~

  ::

    $ sudo su gmn
    $ python /var/local/dataone/gmn/lib/python2.7/site-packages/service/manage.py syncdb
    $ exit


Set server to UTC timezone (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GMN translates incoming date-times to UTC and provides outgoing date-times in
UTC. Because of this, it is convenient to run the server in UTC, so that server
related timestamps, such as the ones in logs, match up with timestamps stored in
the GMN database and provided in DataONE REST API responses.

  ::

    $ sudo dpkg-reconfigure tzdata

  Select ``None of the Above`` | ``UTC``.


Firewall
~~~~~~~~

  Open for HTTPS in the firewall::

    $ sudo ufw allow 443


Starting GMN
~~~~~~~~~~~~

GMN should now be ready to start. Simply restart Apache::

  $ sudo service apache2 restart

Check the Apache logs for error messages. In case of any issues, refer to
:doc:`troubleshooting`

Continue to the next section to test your new node.
